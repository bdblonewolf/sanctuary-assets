"""Bake animation clips into a raw NPC GLB (system python: numpy/scipy).
usage: python3 anim.py NAME RAW_GLB OUT_GLB
Clips are retargeted with pose.Retarget (rest-corrected, bone-direction aligned -- NOT a naive name copy),
then converted back to local TRS per target joint. Fingers get a relaxed baked curl (or a grip for tool clips)."""
import sys,json,struct,os,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pose import G,Retarget,rot,rotdiff
from scipy.spatial.transform import Rotation as R, Slerp
SRC=os.path.dirname(os.path.abspath(__file__))
KNIGHT='/workspace/sanctuary-assets/models/knight_anim_v10b.glb'
FPS=30
NAME,RAW,OUT=sys.argv[1:4]
T=G(RAW)
J=T.j['skins'][0]['joints']
nm=lambda i:T.n[i].get('name','')
idx=lambda short:T.byname['mixamorig:'+short]
PROPS=[i for i,n in enumerate(T.n) if '_prop_' in n.get('name','')]
TW=T.world()
def fix_props():
    """prop meshes were exported with model-space vertices under a hand-bone parent (double transform);
       bake inverse(rest world of the prop node) into their vertices so they sit in the fist."""
    buf=bytearray(T.bin); done=set()
    for p in [i for i,n in enumerate(T.n) if ('_prop_' in n.get('name','') or n.get('name','').endswith('_keepsake')) and 'mesh' in n]:
        Minv=np.linalg.inv(TW[p]); Rinv=Minv[:3,:3]
        for pr in T.j['meshes'][T.n[p]['mesh']]['primitives']:
            for att,isp in (('POSITION',1),('NORMAL',0),('TANGENT',0)):
                if att not in pr['attributes']: continue
                ai=pr['attributes'][att]
                if ai in done: continue
                done.add(ai); a=T.j['accessors'][ai]; bv=T.j['bufferViews'][a['bufferView']]
                nc=3 if att!='TANGENT' else 4; st=bv.get('byteStride',4*nc); off=bv.get('byteOffset',0)+a.get('byteOffset',0)
                for k in range(a['count']):
                    o=off+k*st; v=np.frombuffer(bytes(buf[o:o+12]),np.float32).astype(float)
                    v=(Minv@np.r_[v,1])[:3] if isp else Rinv@v
                    buf[o:o+12]=v.astype(np.float32).tobytes()
                if isp:
                    arr=np.array([np.frombuffer(bytes(buf[off+k*st:off+k*st+12]),np.float32) for k in range(a['count'])])
                    a['min']=arr.min(0).tolist(); a['max']=arr.max(0).tolist()
    T.bin=bytes(buf)
fix_props()
P3=lambda W,i:W[i][:3,3].copy()
# ---------------------------------------------------------------- pose helper on the target
class Pose:
    def __init__(s,ov=None): s.ov=dict(ov or {})
    def world(s): return T.world(s.ov)
    def local_rot(s,i): return R.from_quat(s.ov.get(('r',i),T.n[i].get('rotation',[0,0,0,1])))
    def rotate_world(s,i,Rw,W=None):
        W=W if W is not None else s.world()
        pr=rot(W[T.par[i]]) if i in T.par else R.identity()
        s.ov[('r',i)]=(pr.inv()*(Rw*rot(W[i]))).as_quat()
    def aim(s,i,child,target_dir):
        W=s.world(); s.rotate_world(i,rotdiff(P3(W,child)-P3(W,i),np.asarray(target_dir,float)),W)
def from_world(W):
    """world matrices (dict) -> local overrides for all joints (+ hips translation)"""
    ov={}
    for i in J:
        pw=W[T.par[i]] if i in T.par else np.eye(4)
        Lm=np.linalg.inv(pw)@W[i]
        ov[('r',i)]=rot(Lm).as_quat()
        if i==idx('Hips'): ov[('t',i)]=Lm[:3,3].copy()
    return ov
# ---------------------------------------------------------------- fingers
FING=['Index','Middle','Ring','Pinky','Thumb']
def palm_dir(side):
    h,i1,m1,p1,t2=[P3(TW,idx(side+k)) for k in ('Hand','HandIndex1','HandMiddle1','HandPinky1','HandThumb2')]
    n=np.cross(m1-h,i1-p1); n/=np.linalg.norm(n)
    c=(i1+p1)/2
    if np.dot(t2-c,n)<0: n=-n
    return n
CURL={}
for side in ('Left','Right'):
    p=palm_dir(side)
    for f in FING:
        for k in (1,2,3):
            i=idx(f'{side}Hand{f}{k}')
            ch=T.byname.get(f'mixamorig:{side}Hand{f}{k+1}')
            d=(P3(TW,ch)-P3(TW,i)) if ch is not None else (P3(TW,i)-P3(TW,idx(f'{side}Hand{f}{k-1}')))
            ax=np.cross(d,p); ax/=np.linalg.norm(ax)
            CURL[i]=(rot(TW[i]).inv().apply(ax),R.from_quat(T.n[i].get('rotation',[0,0,0,1])))
RELAX={1:15,2:25,3:20,'T':10}
FIST={1:72,2:85,3:55,'T':30}
def set_fingers(ov,side,amt,thumb=None,per=None):
    for f in FING:
        for k in (1,2,3):
            i=idx(f'{side}Hand{f}{k}'); ax,L0=CURL[i]
            a=(thumb if thumb is not None else amt['T']) if f=='Thumb' else amt[k]
            if per and f in per: a=per[f][k-1]
            ov[('r',i)]=(L0*R.from_rotvec(ax*np.radians(a))).as_quat()
# ---------------------------------------------------------------- sources
_cache={}
def src(path):
    if path not in _cache:
        g=G(path); _cache[path]=(g,Retarget(g,T))
    return _cache[path]
def retarget_world(path,clip,t,inplace=True):
    g,rt=src(path); d=g.dur(clip); return rt.pose(clip,t%d if d>0 else 0,inplace)
def dur(path,clip): return src(path)[0].dur(clip)
UPPER=['Neck','Head','LeftShoulder','LeftArm','LeftForeArm','LeftHand','RightShoulder','RightArm','RightForeArm','RightHand']
def composite(Wbase,Wup,ref='Spine2',bones=UPPER):
    """upper-body bones from Wup re-expressed relative to ref bone of Wbase"""
    W=dict(Wbase); r=idx(ref)
    D=Wbase[r]@np.linalg.inv(Wup[r])
    order=[idx(b) for b in bones]
    # recompute bones top-down keeping their *local* rotations from Wup but parent chain from W
    for i in order:
        pw=Wup[T.par[i]]; Lm=np.linalg.inv(pw)@Wup[i]
        W[i]=W[T.par[i]]@Lm
    # children (fingers etc) follow with rest/animated locals from Wup
    def fix(i):
        for c in T.n[i].get('children',[]):
            if c in J:
                Lm=np.linalg.inv(Wup[i])@Wup[c]; W[c]=W[i]@Lm; fix(c)
    for b in ('LeftHand','RightHand','Head'): fix(idx(b))
    return W
def damp(ovs,k):
    """keep fraction k of the motion around each joint's mean rotation"""
    keys=[key for key in ovs[0] if key[0]=='r']
    out=[dict(o) for o in ovs]
    for key in keys:
        q=np.array([o[key] for o in ovs]); mean=R.from_quat(q).mean()
        for o,qq in zip(out,q):
            rr=R.from_quat(qq); d=(mean.inv()*rr).as_rotvec()*k; o[key]=(mean*R.from_rotvec(d)).as_quat()
    tk=[key for key in ovs[0] if key[0]=='t']
    for key in tk:
        m=np.mean([o[key] for o in ovs],axis=0)
        for o,src_ in zip(out,ovs): o[key]=m+(src_[key]-m)*k
    return out
def loop_fade(ovs,secs=0.6):
    n=len(ovs); m=min(int(secs*FPS),n//3); out=[dict(o) for o in ovs]
    for j in range(m):
        f=n-m+j; w=(j+1)/m; w=w*w*(3-2*w)
        for key,v in ovs[f].items():
            a=np.asarray(v); b=np.asarray(ovs[0][key])
            if key[0]=='r':
                if np.dot(a,b)<0: b=-b
                out[f][key]=Slerp([0,1],R.from_quat([a,b]))([w]).as_quat()[0]
            else: out[f][key]=a*(1-w)+b*w
    return out
def ease(x): x=np.clip(x,0,1); return x*x*(3-2*x)
def nlerp(a,b,w):
    v=np.asarray(a)*(1-w)+np.asarray(b)*w; return v/np.linalg.norm(v)
# ---------------------------------------------------------------- IK
def ik_arm(ps,side,target,pole,lat_dir=None,palm_hint=None):
    W=ps.world(); a,f,h=idx(side+'Arm'),idx(side+'ForeArm'),idx(side+'Hand')
    S=P3(W,a); l1=np.linalg.norm(P3(W,f)-S); l2=np.linalg.norm(P3(W,h)-P3(W,f))
    Tg=np.asarray(target,float); v=Tg-S; d=np.linalg.norm(v)
    d2=np.clip(d,abs(l1-l2)+0.02,0.985*(l1+l2)); u=v/d; Tg=S+u*d2
    aa=(l1*l1-l2*l2+d2*d2)/(2*d2); hh=np.sqrt(max(l1*l1-aa*aa,1e-8))
    w=np.asarray(pole,float)-S; w=w-u*np.dot(w,u); w/=np.linalg.norm(w)
    E=S+u*aa+w*hh
    ps.aim(a,f,E-S); ps.aim(f,h,Tg-E)
    if lat_dir is not None:
        W=ps.world(); lat=P3(W,idx(side+'HandIndex1'))-P3(W,idx(side+'HandPinky1'))
        ps.rotate_world(h,rotdiff(lat,np.asarray(lat_dir,float)),W)
        if palm_hint is not None:   # roll about the lateral axis so the palm faces palm_hint
            W=ps.world(); hw=P3(W,h); m1=P3(W,idx(side+'HandMiddle1')); fwd=m1-hw
            ld=np.asarray(lat_dir,float)/np.linalg.norm(lat_dir)
            fp=fwd-ld*np.dot(fwd,ld); hp=np.asarray(palm_hint,float); hp=hp-ld*np.dot(hp,ld)
            if np.linalg.norm(fp)>1e-6 and np.linalg.norm(hp)>1e-6:
                ps.rotate_world(h,rotdiff(fp,hp),W)
    return E
def bend(ps,bone,axis,deg):
    ps.rotate_world(idx(bone),R.from_rotvec(np.asarray(axis,float)/np.linalg.norm(axis)*np.radians(deg)))
X=np.array([1.,0,0]); Y=np.array([0,1.,0]); Z=np.array([0,0,1.])
# ---------------------------------------------------------------- clip builders
def clip_retarget(path,clip,secs=None,inplace=True,fingers=True,grab=None):
    d=dur(path,clip); secs=secs or d; n=int(round(secs*FPS))+1; out=[]
    for k in range(n):
        ov=from_world(retarget_world(path,clip,k/FPS,inplace))
        if fingers:
            for s_ in ('Left','Right'): set_fingers(ov,s_,RELAX)
        out.append(ov)
    return out
def clip_talk(secs=None):
    tp=SRC+'/anim_src/talking.glb'; d=dur(tp,'talking'); secs=secs or 2*d; n=int(round(secs*FPS))+1; out=[]
    for k in range(n):
        t=k/FPS
        Wb=retarget_world(KNIGHT,'town_idle',t); Wu=retarget_world(tp,'talking',t)
        ov=from_world(composite(Wb,Wu))
        for s_ in ('Left','Right'): set_fingers(ov,s_,RELAX)
        out.append(ov)
    return out
def with_props(ovs,visible):
    for o in ovs:
        for p in PROPS: o[('s',p)]=np.ones(3) if (p in visible) else np.zeros(3)
    return ovs
def clip_hammer():
    """3 strikes (0.8 s each) then 1.2 s turning the work with the tongs = 3.6 s.
       anvil face ~0.88 m, strike point (-0.02,0.90,0.52) in glTF/model space."""
    base=clip_retarget(KNIGHT,'town_idle',3.6)
    STRIKE=np.array([-0.02,0.90,0.52]); IMP=np.array([-0.13,1.02,0.28]); RAISE=np.array([-0.30,1.50,0.36])
    D_IMP=STRIKE-IMP; D_IMP/=np.linalg.norm(D_IMP); D_RAISE=np.array([0.05,0.80,-0.55]); D_RAISE/=np.linalg.norm(D_RAISE)
    REST_R=np.array([-0.20,1.10,0.24]); D_REST=np.array([0.25,-0.55,0.55]); D_REST/=np.linalg.norm(D_REST)
    TONG=np.array([0.12,1.00,0.30]); D_TONG=STRIKE+np.array([0.0,0.035,0.0])-TONG; D_TONG/=np.linalg.norm(D_TONG)
    out=[]
    for k,ov in enumerate(base):
        t=k/FPS; ps=Pose(ov)
        if t<2.4:
            c=(t%0.8)/0.8
            if c<0.5: w=ease(c/0.5); pos=IMP+(RAISE-IMP)*w+np.array([0,0.06,0])*np.sin(np.pi*w); dirv=nlerp(D_IMP,D_RAISE,w); lean=8*(1-w)+2*w
            elif c<0.68: w=((c-0.5)/0.18)**1.6; pos=RAISE+(IMP-RAISE)*w+np.array([0,0.08,0.05])*np.sin(np.pi*w); dirv=nlerp(D_RAISE,D_IMP,w); lean=2+6*w
            else: w=(c-0.68)/0.32; pos=IMP+np.array([0,0.012,0])*np.sin(np.pi*w); dirv=D_IMP; lean=8
            if t<0.4: # blend in from the rest grip at the loop seam
                pass
            tw=0.0
        else:
            u=(t-2.4)/1.2
            w=ease(min(u/0.25,1))*(1-ease(max((u-0.75)/0.25,0)))
            pos=IMP+(REST_R-IMP)*w; dirv=nlerp(D_IMP,D_REST,w); lean=8-3*w
            tw=np.sin(np.pi*ease(min(max((u-0.15)/0.7,0),1)))   # tongs turn the bar
        bend(ps,'Spine1',X,lean*0.5); bend(ps,'Spine2',X,lean*0.5)
        bend(ps,'Neck',X,10); bend(ps,'Head',X,15)
        ik_arm(ps,'Right',pos,pos+np.array([-0.45,0.05,-0.35]),dirv,palm_hint=np.array([0.3,-0.2,0.9]))
        tp=TONG+np.array([0.01,0.02*tw,-0.01*tw]); td=R.from_rotvec(D_TONG*np.radians(55*tw)).apply(D_TONG)
        ik_arm(ps,'Left',tp,tp+np.array([0.45,-0.05,-0.35]),td,palm_hint=np.array([-0.5,0.2,0.8]))
        if tw: bend(ps,'LeftHand',D_TONG,40*tw)
        set_fingers(ps.ov,'Right',FIST); set_fingers(ps.ov,'Left',FIST)
        out.append(ps.ov)
    return with_props(out,{T.byname.get(NAME+'_prop_hammer'),T.byname.get(NAME+'_prop_tongs')})
def clip_sleep(sit):
    out=damp(sit,0.08); res=[]
    n=len(out)
    for k,ov in enumerate(out):
        t=k/FPS; ps=Pose(ov); br=np.sin(2*np.pi*t/4.0)
        bend(ps,'Spine',X,6); bend(ps,'Spine1',X,6+1.2*br); bend(ps,'Spine2',X,4+1.0*br)
        bend(ps,'Neck',X,22); bend(ps,'Head',X,18+1.5*br); bend(ps,'Head',Z,8)
        res.append(ps.ov)
    return res
def clip_write(secs=8.0):
    """standing at a slanted lectern (page centre ~(0.02,1.06,0.36) glTF): writes lines, dips ink at t~3.2-4.0,
       furtive glance over the right shoulder at t~5.5-6.8. Left hand pins the page."""
    base=damp(clip_retarget(KNIGHT,'town_idle',secs),0.35)
    PAGE=np.array([0.02,1.06,0.36]); INK=np.array([-0.20,1.08,0.42])
    LAT=np.array([-0.10,0.80,-0.45]); LAT/=np.linalg.norm(LAT)       # pinky->index axis; the prop's nib sits on the pinky side (-LAT)
    FH=np.array([0.75,-0.35,0.40])                                      # finger direction hint
    out=[]
    for k,ov in enumerate(base):
        t=k/FPS; ps=Pose(ov)
        dip=ease(min(max((t-3.2)/0.25,0),1))*(1-ease(min(max((t-3.75)/0.25,0),1)))
        g=ease(min(max((t-5.5)/0.3,0),1))*(1-ease(min(max((t-6.5)/0.3,0),1)))
        line=(t*0.9)%1.0                                                # one line per ~1.1 s
        row=int(t*0.9)%4
        nib=PAGE+np.array([0.07-0.14*line,-0.012*row+0.02,0.006*row])+np.array([0,0.004,0])*np.sin(t*37)*(1-dip)
        nib=nib+np.array([0,0.025,0])*max(0,(line-0.9)/0.1)          # lift at end of line
        nib=nib*(1-dip)+(INK+np.array([0,0.02*np.sin(np.pi*dip),0]))*dip
        nib=nib+np.array([0,0.04,-0.02])*g                                # pen lifts while he glances
        lean=12*(1-0.6*g)
        bend(ps,'Spine1',X,lean*0.5); bend(ps,'Spine2',X,lean*0.5)
        bend(ps,'Neck',X,10*(1-g)); bend(ps,'Head',X,(14+2*np.sin(t*1.3))*(1-g)-4*g)
        if g: bend(ps,'Neck',Y,-30*g); bend(ps,'Head',Y,-28*g); bend(ps,'Spine2',Y,-8*g)
        W=ps.world()
        wr=nib+LAT*0.060-FH/np.linalg.norm(FH)*0.075
        ik_arm(ps,'Right',wr,wr+np.array([-0.45,-0.25,-0.25]),LAT,palm_hint=FH)
        lp=np.array([0.17,1.095,0.27])+np.array([0,0.005,0])*np.sin(t*0.7)
        ik_arm(ps,'Left',lp,lp+np.array([0.45,-0.2,-0.3]),np.array([-1.0,0.0,0.1]),palm_hint=np.array([-0.2,-0.12,1.0]))
        set_fingers(ps.ov,'Right',{1:40,2:50,3:35,'T':25},per={'Index':(30,35,25),'Thumb':(20,25,20)}); set_fingers(ps.ov,'Left',{1:10,2:12,3:8,'T':8})
        out.append(ps.ov)
    return with_props(out,{T.byname.get(NAME+'_prop_quill')})
EXTRA_LIFT={'wolcen':0.0,'quill':0.0}
if os.environ.get('EXTRA_LIFT'): EXTRA_LIFT={k:float(os.environ['EXTRA_LIFT']) for k in EXTRA_LIFT}
def foot_fix(C):
    """the retargeted foot pitch points the toes ~6 cm into the ground; measure the pitch error on the
       idle clip (feet planted) and post-multiply a constant local correction on both feet in every clip."""
    W0=T.world(); ref=C['idle'][0]; Wi=T.world(ref)
    for side in ('Left','Right'):
        f,tb=idx(side+'Foot'),idx(side+'ToeBase')
        d0=P3(W0,tb)-P3(W0,f); d=P3(Wi,tb)-P3(Wi,f)
        h=np.array([d[0],0,d[2]]); hl=np.linalg.norm(h); s0=d0[1]/np.linalg.norm([d0[0],d0[2]])
        tgt=h/hl*np.linalg.norm(d)/np.sqrt(1+s0*s0); tgt[1]=s0*np.linalg.norm(tgt)
        Rw=rotdiff(d,tgt); Rf=rot(Wi[f]); corr=Rf.inv()*Rw*Rf
        for ovs in C.values():
            for o in ovs:
                q=o.get(('r',f),T.n[f].get('rotation',[0,0,0,1])); o[('r',f)]=(R.from_quat(q)*corr).as_quat()
        print('FOOTFIX',side,round(float(np.degrees(Rw.magnitude())),1),'deg')
    # standing clips: the retargeted hips sit ~1 cm low -> lift so the planted feet match the rest height
    hp=idx('Hips'); Wi=T.world(C['idle'][0]); dy=float(np.mean([P3(W0,idx(s_+'Foot'))[1]-P3(Wi,idx(s_+'Foot'))[1] for s_ in ('Left','Right')]))
    dy+=EXTRA_LIFT.get(NAME,0.0)   # measured: lowest skinned vertex per standing clip (heels) -> >= 0
    Pinv=np.linalg.inv(W0[T.par[hp]]) if hp in T.par else np.eye(4); dl=Pinv[:3,:3]@np.array([0,dy,0])
    for k,ovs in C.items():
        if k.startswith('sit') or k=='sleep': continue
        for o in ovs:
            if ('t',hp) in o: o[('t',hp)]=np.asarray(o[('t',hp)])+dl
    print('HIPLIFT',round(dy,4))
# ---------------------------------------------------------------- GLB writer
def write(ovs_by_clip,out):
    j=T.j; binb=bytearray(T.bin)
    def pad():
        while len(binb)%4: binb.append(0)
    def add_acc(arr,typ,minmax=False):
        pad(); arr=np.ascontiguousarray(arr,np.float32); off=len(binb); binb.extend(arr.tobytes())
        j['bufferViews'].append(dict(buffer=0,byteOffset=off,byteLength=arr.nbytes))
        a=dict(bufferView=len(j['bufferViews'])-1,componentType=5126,count=len(arr),type=typ)
        if minmax: a['min']=[float(arr.min())]; a['max']=[float(arr.max())]
        j['accessors'].append(a); return len(j['accessors'])-1
    j['animations']=[]
    for cname,ovs in ovs_by_clip.items():
        n=len(ovs); ti=add_acc(np.arange(n,dtype=np.float32)/FPS,'SCALAR',True)
        ch=[];sa=[]
        keys=sorted({k for o in ovs for k in o},key=lambda k:(k[1],k[0]))
        for key in keys:
            path={'r':'rotation','t':'translation','s':'scale'}[key[0]]
            vals=np.array([o.get(key,ovs[0][key]) for o in ovs],float)
            if key[0]=='r':
                for q in range(1,n):
                    if np.dot(vals[q],vals[q-1])<0: vals[q]=-vals[q]
                vals/=np.linalg.norm(vals,axis=1,keepdims=True)
            oi=add_acc(vals,'VEC4' if key[0]=='r' else 'VEC3')
            sa.append(dict(input=ti,output=oi,interpolation='LINEAR')); ch.append(dict(sampler=len(sa)-1,target=dict(node=key[1],path=path)))
        j['animations'].append(dict(name=cname,channels=ch,samplers=sa))
    for p in PROPS: j['nodes'][p]['scale']=[0.0,0.0,0.0]   # tools hidden unless a work clip shows them
    for m in j['materials']:
        if m.get('alphaMode')=='BLEND': m['alphaMode']='MASK'; m['alphaCutoff']=0.5
    pad(); j['buffers'][0]['byteLength']=len(binb)
    js=json.dumps(j,separators=(',',':')).encode()
    while len(js)%4: js+=b' '
    with open(out,'wb') as f:
        f.write(struct.pack('<III',0x46546C67,2,12+8+len(js)+8+len(binb)))
        f.write(struct.pack('<II',len(js),0x4E4F534A)); f.write(js)
        f.write(struct.pack('<II',len(binb),0x004E4942)); f.write(bytes(binb))
# ---------------------------------------------------------------- per-NPC clip sets
def build(name):
    C={}
    C['idle']=clip_retarget(KNIGHT,'town_idle')
    C['walk']=clip_retarget(KNIGHT,'town_walk')
    C['talk']=clip_talk()
    st=clip_retarget(KNIGHT,'town_talk')
    C['sit']=damp(st,0.25); C['sit_talk']=st
    if name=='wolcen':
        C['work_hammer']=clip_hammer()
        C['sleep']=clip_sleep(st)
    if name=='quill':
        C['work_write']=loop_fade(clip_write())
        C['sleep']=clip_sleep(st)
    for k in ('idle','talk','sit','sit_talk','sleep'):
        if k in C: C[k]=loop_fade(C[k])
    vis_none=set()
    for k in C:
        if not k.startswith('work_'): with_props(C[k],vis_none)
    return C
if __name__=='__main__':
    C=build(NAME); foot_fix(C)
    for k,v in C.items(): print('CLIP',k,len(v),'frames',round((len(v)-1)/FPS,2),'s')
    write(C,OUT)
    print('WROTE',OUT,os.path.getsize(OUT))
