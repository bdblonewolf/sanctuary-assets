import json,struct,sys,os,numpy as np
from scipy.spatial.transform import Rotation as R, Slerp
CT={5120:np.int8,5121:np.uint8,5122:np.int16,5123:np.uint16,5125:np.uint32,5126:np.float32}
NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
class G:
    def __init__(s,p):
        b=open(p,'rb').read();off=12;s.bin=b''
        while off<len(b):
            l,t=struct.unpack('<II',b[off:off+8]);c=b[off+8:off+8+l]
            if t==0x4E4F534A: s.j=json.loads(c)
            else: s.bin=c
            off+=8+l
        s.n=s.j['nodes'];s.par={}
        for i,nd in enumerate(s.n):
            for c in nd.get('children',[]): s.par[c]=i
        s.byname={nd.get('name'):i for i,nd in enumerate(s.n)}
    def acc(s,i):
        a=s.j['accessors'][i];v=s.j['bufferViews'][a['bufferView']];dt=CT[a['componentType']];nc=NC[a['type']]
        st=v.get('byteStride',0);o=v.get('byteOffset',0)+a.get('byteOffset',0);cnt=a['count']
        isz=np.dtype(dt).itemsize*nc
        if st and st!=isz:
            raw=np.frombuffer(s.bin,np.uint8,count=st*(cnt-1)+isz,offset=o)
            arr=np.stack([np.frombuffer(raw[k*st:k*st+isz].tobytes(),dt) for k in range(cnt)])
        else: arr=np.frombuffer(s.bin,dt,count=cnt*nc,offset=o).reshape(cnt,nc)
        if a.get('normalized'):
            arr=arr.astype(np.float32)/np.iinfo(dt).max
        return arr
    def local(s,i,ov=None):
        nd=s.n[i];ov=ov or {}
        t=np.array(ov.get(('t',i),nd.get('translation',[0,0,0])),float)
        q=np.array(ov.get(('r',i),nd.get('rotation',[0,0,0,1])),float)
        sc=np.array(ov.get(('s',i),nd.get('scale',[1,1,1])),float)
        M=np.eye(4);M[:3,:3]=R.from_quat(q).as_matrix()*sc;M[:3,3]=t;return M
    def world(s,ov=None):
        W={}
        def w(i):
            if i in W: return W[i]
            L=s.local(i,ov);W[i]=(w(s.par[i])@L) if i in s.par else L;return W[i]
        for i in range(len(s.n)): w(i)
        return W
    def sample(s,clip,t):
        a=[x for x in s.j['animations'] if x['name']==clip][0];ov={}
        for c in a['channels']:
            sm=a['samplers'][c['sampler']];ti=s.acc(sm['input'])[:,0];va=s.acc(sm['output']).astype(float)
            node=c['target']['node'];path=c['target']['path'];k={'translation':'t','rotation':'r','scale':'s'}[path]
            tt=np.clip(t,ti[0],ti[-1])
            if path=='rotation':
                if len(ti)==1: v=va[0]
                else: v=Slerp(ti,R.from_quat(va))([tt]).as_quat()[0]
            else: v=np.array([np.interp(tt,ti,va[:,d]) for d in range(va.shape[1])])
            ov[(k,node)]=v
        return ov
    def dur(s,clip):
        a=[x for x in s.j['animations'] if x['name']==clip][0]
        return max(s.acc(sm['input'])[:,0].max() for sm in a['samplers'])
    def meshes(s):
        out=[]
        for i,nd in enumerate(s.n):
            if 'mesh' not in nd: continue
            for pr in s.j['meshes'][nd['mesh']]['primitives']:
                at=pr['attributes'];P=s.acc(at['POSITION']).astype(float)
                F=s.acc(pr['indices']).reshape(-1,3) if 'indices' in pr else np.arange(len(P)).reshape(-1,3)
                J=s.acc(at['JOINTS_0']).astype(int) if 'JOINTS_0' in at else None
                Wt=s.acc(at['WEIGHTS_0']).astype(float) if 'WEIGHTS_0' in at else None
                out.append(dict(node=i,skin=nd.get('skin'),P=P,F=F,J=J,W=Wt,mat=pr.get('material'),name=s.j['meshes'][nd['mesh']].get('name')))
        return out
    def skinpose(s,W):
        res=[]
        for m in s.meshes():
            if m['skin'] is None or m['J'] is None:
                P=(W[m['node']]@np.c_[m['P'],np.ones(len(m['P']))].T).T[:,:3]
            else:
                sk=s.j['skins'][m['skin']];IB=s.acc(sk['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1)
                JM=np.stack([W[j]@IB[k] for k,j in enumerate(sk['joints'])])
                ph=np.c_[m['P'],np.ones(len(m['P']))]
                acc=np.zeros((len(ph),4))
                for c in range(4):
                    acc+=m['W'][:,c:c+1]*np.einsum('nij,nj->ni',JM[m['J'][:,c]],ph)
                P=acc[:,:3]
            res.append((m['name'],m['mat'],P,m['F']))
        return res

def rot(M):
    m=M[:3,:3];m=m/np.linalg.norm(m,axis=0);return R.from_matrix(m)
def rotdiff(a,b):
    a=a/np.linalg.norm(a);b=b/np.linalg.norm(b);v=np.cross(a,b);c=np.dot(a,b)
    if np.linalg.norm(v)<1e-8:
        if c>0: return R.identity()
        ax=np.cross(a,[1,0,0]); ax=ax if np.linalg.norm(ax)>1e-6 else np.cross(a,[0,1,0])
        return R.from_rotvec(ax/np.linalg.norm(ax)*np.pi)
    return R.from_rotvec(v/np.linalg.norm(v)*np.arctan2(np.linalg.norm(v),c))
def bdir(g,W,i):
    ch=g.n[i].get('children',[])
    p=W[i][:3,3]
    if ch:
        # mixamorig child closest to center line
        cs=[c for c in ch if g.n[c].get('name','').startswith('mixamorig:')] or ch
        c=min(cs,key=lambda c:abs(g.local(c)[0,3]))
        v=W[c][:3,3]-p
        if np.linalg.norm(v)>1e-6: return v
    return W[i][:3,:3]@np.array([0,1,0])

class Retarget:
    """Rest-corrected retarget by bone name (world-space, bone-direction aligned)."""
    def __init__(s,src,tgt,mode='retarget'):
        s.src,s.tgt,s.mode=src,tgt,mode
        s.SW=src.world();s.TW=tgt.world()
        s.shared=[n for n in tgt.byname if n and n.startswith('mixamorig:') and n in src.byname]
        s.O={}
        for n in s.shared:
            si,ti=src.byname[n],tgt.byname[n]
            Sr=rot(s.SW[si]);Tr=rot(s.TW[ti])
            D=rotdiff(bdir(src,s.SW,si),bdir(tgt,s.TW,ti))
            s.O[n]=(D*Sr).inv()*Tr
        H='mixamorig:Hips';s.H=H
        s.scale=s.TW[tgt.byname[H]][1,3]/s.SW[src.byname[H]][1,3]
    def pose(s,clip,t,inplace=True):
        src,tgt=s.src,s.tgt;ov=src.sample(clip,t);SWt=src.world(ov)
        H=s.H;hs=src.byname[H];ht=tgt.byname[H]
        tov={}
        if s.mode=='naive':
            # three.js style: copy local rotation tracks by name, hips position scaled, no other position tracks
            for n in s.shared:
                k=('r',src.byname[n])
                if k in ov: tov[('r',tgt.byname[n])]=ov[k]
            off=(SWt[hs][:3,3]-s.SW[hs][:3,3])*s.scale
            if inplace: off[0]=off[2]=0
            Tp=tgt.world()
            # set hips local translation so world pos = rest + off
            parW=Tp[tgt.par[ht]] if ht in tgt.par else np.eye(4)
            wp=s.TW[ht][:3,3]+off
            tov[('t',ht)]=(np.linalg.inv(parW)@np.r_[wp,1])[:3]
            return tgt.world(tov)
        # retarget: desired world rotations
        Wd={n:rot(SWt[src.byname[n]])*s.O[n] for n in s.shared}
        off=(SWt[hs][:3,3]-s.SW[hs][:3,3])*s.scale
        if inplace: off[0]=off[2]=0
        W=dict()
        # walk hierarchy top-down
        order=[]
        def visit(i):
            order.append(i)
            for c in tgt.n[i].get('children',[]): visit(c)
        roots=[i for i in range(len(tgt.n)) if i not in tgt.par]
        for r in roots: visit(r)
        for i in order:
            name=tgt.n[i].get('name')
            L=tgt.local(i)
            if i in tgt.par: base=W[tgt.par[i]]@L
            else: base=L
            if name in Wd:
                M=np.eye(4);sc=np.linalg.norm(base[:3,:3],axis=0)
                M[:3,:3]=Wd[name].as_matrix()*sc;M[:3,3]=base[:3,3]
                if name==H: M[:3,3]=s.TW[ht][:3,3]+off
                W[i]=M
            else: W[i]=base
        return W
