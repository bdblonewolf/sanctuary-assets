from gl import *
import trimesh
from scipy.spatial.transform import Slerp
M='mixamorig:'
FPS=30
PRIMARY={'Hips':'Spine','Spine2':'Neck','LeftHand':'LeftHandMiddle1','RightHand':'RightHandMiddle1','LeftFoot':'LeftToeBase','RightFoot':'RightToeBase','Head':'HeadTop_End','LeftToeBase':'LeftToe_End','RightToeBase':'RightToe_End'}
def Rq(q): return R.from_quat(q)
def minrot(a,b):
    a=a/np.linalg.norm(a,axis=-1,keepdims=True); b=b/np.linalg.norm(b,axis=-1,keepdims=True)
    ax=np.cross(a,b); s=np.linalg.norm(ax,axis=-1); c=np.sum(a*b,-1)
    ang=np.arctan2(s,c); ax=ax/np.maximum(s,1e-9)[...,None]
    return R.from_rotvec(ax*ang[...,None])
def smooth(x): x=np.clip(x,0,1); return x*x*x*(x*(x*6-15)+10)
def ease(x): x=np.clip(x,0,1); return x*x*(3-2*x)

class Body:
    def __init__(s,path,name,mesh=None):
        s.name=name; s.sk=Skel(path); sk=s.sk
        s.J=len(sk.names)
        GQ,GP=sk.fk(sk.Q[None],sk.T[None]); s.GQr=GQ[0]; s.GPr=GP[0]
        s.i=lambda n: sk.idx[M+n]
        s.dir={}
        for j,nm in enumerate(sk.names):
            b=nm[len(M):]; ch=sk.children[j]
            c=None
            if b in PRIMARY and (M+PRIMARY[b]) in sk.idx: c=sk.idx[M+PRIMARY[b]]
            elif len(ch)==1: c=ch[0]
            elif ch: c=ch[0]
            if c is not None: s.dir[nm]=s.GPr[c]-s.GPr[j]
        y=lambda n:s.GPr[s.i(n)][1]
        s.hip_y=y('Hips'); s.ankle_y=(y('LeftFoot')+y('RightFoot'))/2; s.toe_y=(y('LeftToeBase')+y('RightToeBase'))/2
        L=lambda a,b: np.linalg.norm(s.GPr[s.i(a)]-s.GPr[s.i(b)])
        s.l1=L('LeftUpLeg','LeftLeg'); s.l2=L('LeftLeg','LeftFoot')
        s.leg=s.l1+s.l2+s.ankle_y
        s.thigh_r=None
        try:
            sc=trimesh.load(mesh or path); V=np.concatenate([g.vertices for g in sc.dump()]) if hasattr(sc,'dump') else sc.vertices
            s.height=V[:,1].max(); 
            up=s.GPr[s.i('LeftUpLeg')]; rs=[]
            for side in ('Left','Right'):
                up=s.GPr[s.i(side+'UpLeg')]
                m=(V[:,1]<up[1]-0.25*s.l1)&(V[:,1]>up[1]-0.55*s.l1)&(np.abs(V[:,0]-up[0])<0.09)
                rs.append(up[2]-V[m,2].min())
            s.thigh_r=float(np.mean(rs))
        except Exception as e: print('mesh fail',e)
    def info(s): return dict(hip_y=round(s.hip_y,3),leg=round(s.leg,3),height=round(float(s.height),3),thigh_r=round(s.thigh_r,3) if s.thigh_r else None)

def retarget(src,dst,Q,T):
    """src,dst Body; Q,T source local per frame -> dst local Q (F,J,4), hips pos (F,3)"""
    F=Q.shape[0]; GQs,GPs=src.sk.fk(Q,T)
    out=np.zeros((F,dst.J,4)); G=np.zeros((F,dst.J,4))
    for j in dst.sk.order:
        nm=dst.sk.names[j]; p=dst.sk.par[j]
        if nm in src.sk.idx:
            js=src.sk.idx[nm]
            if nm[len(M):] in ('LeftShoulder','RightShoulder'):
                Rb=R.identity()
            elif nm in dst.dir and nm in src.dir:
                Rb=minrot(dst.dir[nm],src.dir[nm])
            else:
                Rb=dst._Rb[dst.sk.names[p]] if p>=0 else R.identity()
            dst.__dict__.setdefault('_Rb',{})[nm]=Rb
            Gt=Rq(GQs[:,js])*Rq(src.GQr[js]).inv()*Rb*Rq(dst.GQr[j])
            G[:,j]=Gt.as_quat()
        else:
            G[:,j]=(Rq(G[:,p])*Rq(dst.sk.Q[j])).as_quat() if p>=0 else dst.sk.Q[j]
    k=dst.leg/src.leg
    hips=GPs[:,src.i('Hips')]*k
    return g2l(dst,G),hips

def g2l(b,G):
    L=np.zeros_like(G)
    for j in range(b.J):
        p=b.sk.par[j]
        L[:,j]=G[:,j] if p<0 else (Rq(G[:,p]).inv()*Rq(G[:,j])).as_quat()
    return L
def fk(b,L,hips):
    T=np.repeat(b.sk.T[None],len(L),0).copy(); T[:,b.i('Hips')]=hips
    return b.sk.fk(L,T)
def contact(b,GP):
    """per-frame lowest foot offset vs rest standing (m); 0 = flat foot on ground"""
    c=[]
    for side in ('Left','Right'):
        f=GP[:,b.i(side+'Foot'),1]-b.GPr[b.i(side+'Foot')][1]
        t=GP[:,b.i(side+'ToeBase'),1]-b.GPr[b.i(side+'ToeBase')][1]
        c.append(np.minimum(f,t))
    return np.minimum(c[0],c[1]), c

def ik2(H,K,A,Atgt,l1,l2,bias=None):
    """world positions (F,3): hip, knee(fk), ankle(fk), target. returns rotation deltas (Rup, new knee pos)"""
    d=Atgt-H; dl=np.linalg.norm(d,axis=1,keepdims=True); dn=d/dl
    dl=np.clip(dl,abs(l1-l2)+1e-3,l1+l2-1e-3)
    a=(l1*l1-l2*l2+dl*dl)/(2*dl); h=np.sqrt(np.maximum(l1*l1-a*a,0))
    pole=K-H
    if bias is not None: pole=pole/np.linalg.norm(pole,axis=1,keepdims=True)+bias
    pole=pole-np.sum(pole*dn,1,keepdims=True)*dn
    pole=pole/np.maximum(np.linalg.norm(pole,axis=1,keepdims=True),1e-9)
    Kn=H+dn*a+pole*h; An=H+dn*dl
    return Kn,An

def limb_ik(b,L,hips,chain,Atgt,foot_global=None,w=None):
    """chain=(upper,lower,end) names. Atgt (F,3) target pos for end joint. w (F,) blend 0..1"""
    F=len(L); GQ,GP=fk(b,L,hips)
    u,l,e=[b.i(n) for n in chain]
    bias=None
    if 'UpLeg' in chain[0]: bias=np.stack([np.sign(GP[:,u,0])*0.35,0*GP[:,u,0],0*GP[:,u,0]],1)
    Kn,An=ik2(GP[:,u],GP[:,l],GP[:,e],Atgt,np.linalg.norm(b.GPr[l]-b.GPr[u]),np.linalg.norm(b.GPr[e]-b.GPr[l]),bias)
    if w is not None:
        # blend target in position space
        pass
    G=GQ.copy()
    r1=minrot(GP[:,l]-GP[:,u],Kn-GP[:,u]); G[:,u]=(r1*Rq(GQ[:,u])).as_quat()
    lg=Rq(G[:,u])*Rq(L[:,l]); dl=lg.apply(b.sk.T[l]*0+ (b.sk.T[e]))  # direction lower->end in world
    r2=minrot(dl,An-Kn); G[:,l]=(r2*lg).as_quat()
    endG=Rq(GQ[:,e]) if foot_global is None else Rq(foot_global)
    G[:,e]=endG.as_quat()
    L2=L.copy()
    pu=b.sk.par[u]
    L2[:,u]=(Rq(GQ[:,pu]).inv()*Rq(G[:,u])).as_quat()
    L2[:,l]=(Rq(G[:,u]).inv()*Rq(G[:,l])).as_quat()
    L2[:,e]=(Rq(G[:,l]).inv()*Rq(G[:,e])).as_quat()
    if w is not None:
        for j in (u,l,e):
            for f in range(F):
                if w[f]<1: L2[f,j]=Slerp([0,1],R.from_quat([L[f,j],L2[f,j]]))(w[f]).as_quat()
    return L2

def world_pre(b,L,j,rot):
    """apply world-space rotation rot (Rotation, F) to joint j's global orientation (children follow)"""
    GQ,_=fk(b,L,np.zeros((len(L),3)))
    p=b.sk.par[j]; Gp=Rq(GQ[:,p]) if p>=0 else R.identity(len(L))
    L=L.copy(); L[:,j]=(Gp.inv()*rot*Gp*Rq(L[:,j])).as_quat(); return L

def ground_standing(b,L,hips,smooth_n=3):
    GQ,GP=fk(b,L,hips); c,_=contact(b,GP)
    if smooth_n>1:
        k=np.ones(smooth_n)/smooth_n; cp=np.pad(c,(smooth_n//2,smooth_n//2),mode='wrap'); c=np.convolve(cp,k,'valid')
    hips=hips.copy(); hips[:,1]-=c; return hips

SEAT=0.45
def seat_fix(b,L,hips,ref_frame=0):
    """lower/raise hips so thigh underside sits on SEAT, IK feet to ground"""
    GQ,GP=fk(b,L,hips)
    up=(GP[ref_frame,b.i('LeftUpLeg'),1]+GP[ref_frame,b.i('RightUpLeg'),1])/2
    dy=(SEAT+b.thigh_r)-up
    hips=hips.copy(); hips[:,1]+=dy
    for side in ('Left','Right'):
        GQ,GP=fk(b,L,hips)
        A=GP[:,b.i(side+'Foot')].copy(); A[:,1]=b.GPr[b.i(side+'Foot')][1]
        L=limb_ik(b,L,hips,(side+'UpLeg',side+'Leg',side+'Foot'),A)
    return L,hips,dy

def resample(L,hips,ts,newdur):
    F=max(2,int(round(newdur*FPS))+1); tn=np.linspace(0,ts[-1],F)
    Ln=np.zeros((F,)+L.shape[1:])
    for j in range(L.shape[1]): Ln[:,j]=slerp_s(ts,L[:,j].copy(),tn)
    hn=np.stack([np.interp(tn,ts,hips[:,k]) for k in range(3)],1)
    return np.linspace(0,newdur,F),Ln,hn

def walk_speed(b,L,hips,ts):
    GQ,GP=fk(b,L,hips); sp=[]
    for side in ('Left','Right'):
        y=GP[:,b.i(side+'ToeBase'),1]-b.GPr[b.i(side+'ToeBase')][1]
        z=GP[:,b.i(side+'Foot'),2]
        vz=np.gradient(z,ts)
        m=(y<0.02)&(vz<0)
        if m.sum()>2: sp.append(-np.median(vz[m]))
    return float(np.mean(sp))
