import pygltflib, numpy as np
from scipy.spatial.transform import Rotation as R
def acc(g,i):
    a=g.accessors[i]; bv=g.bufferViews[a.bufferView]; blob=g.binary_blob()
    n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a.type]
    dt={5126:np.float32,5123:np.uint16,5121:np.uint8,5125:np.uint32,5122:np.int16,5120:np.int8}[a.componentType]
    stride=bv.byteStride or n*np.dtype(dt).itemsize
    off=(bv.byteOffset or 0)+(a.byteOffset or 0)
    raw=np.frombuffer(blob,dtype=np.uint8,count=stride*(a.count-1)+n*np.dtype(dt).itemsize,offset=off)
    arr=np.lib.stride_tricks.as_strided(raw.view(dt) if stride==n*np.dtype(dt).itemsize else np.frombuffer(blob,dt,count=a.count*n,offset=off), shape=(a.count,n)) if stride==n*np.dtype(dt).itemsize else np.array([np.frombuffer(blob,dt,count=n,offset=off+k*stride) for k in range(a.count)])
    arr=np.array(arr,dtype=np.float64)
    if a.normalized:
        if dt==np.int16: arr=np.maximum(arr/32767,-1)
        elif dt==np.int8: arr=np.maximum(arr/127,-1)
        elif dt==np.uint16: arr=arr/65535
        elif dt==np.uint8: arr=arr/255
    return arr
class Skel:
    def __init__(s,path):
        g=s.g=pygltflib.GLTF2().load(path)
        sk=g.skins[0]; s.joints=list(sk.joints)
        s.names=[g.nodes[j].name for j in s.joints]
        s.idx={n:i for i,n in enumerate(s.names)}
        par={}
        for i,n in enumerate(g.nodes):
            for c in (n.children or []): par[c]=i
        s.par=[s.joints.index(par[j]) if par.get(j) in s.joints else -1 for j in s.joints]
        s.rootnode=par.get(s.joints[s.par.index(-1)])
        # check root has identity transform
        rn=g.nodes[s.rootnode] if s.rootnode is not None else None
        s.root_tf=(rn.translation,rn.rotation,rn.scale) if rn else None
        s.T=np.array([g.nodes[j].translation or [0,0,0] for j in s.joints],float)
        s.Q=np.array([g.nodes[j].rotation or [0,0,0,1] for j in s.joints],float)
        s.S=np.array([g.nodes[j].scale or [1,1,1] for j in s.joints],float)
        s.children=[[k for k,p in enumerate(s.par) if p==i] for i in range(len(s.joints))]
        s.order=[]; 
        def rec(i):
            s.order.append(i); [rec(c) for c in s.children[i]]
        for i,p in enumerate(s.par):
            if p==-1: rec(i)
    def fk(s,Q,T):
        """Q:(F,J,4) local quats xyzw, T:(F,J,3) -> global rot (Rotation list per joint as quats (F,J,4)), pos (F,J,3). ignores scale (assumed ~1)"""
        F,J=Q.shape[:2]; GQ=np.zeros((F,J,4)); GP=np.zeros((F,J,3))
        for i in s.order:
            p=s.par[i]; rl=R.from_quat(Q[:,i])
            if p<0: GQ[:,i]=rl.as_quat(); GP[:,i]=T[:,i]
            else:
                rp=R.from_quat(GQ[:,p]); GQ[:,i]=(rp*rl).as_quat(); GP[:,i]=GP[:,p]+rp.apply(T[:,i])
        return GQ,GP
    def clip(s,name,fps=30):
        g=s.g; a=[a for a in g.animations if a.name==name][0]
        tracks={}; tmax=0
        for ch in a.channels:
            smp=a.samplers[ch.sampler]; t=acc(g,smp.input)[:,0]; v=acc(g,smp.output)
            tracks[(g.nodes[ch.target.node].name,ch.target.path)]=(t,v,smp.interpolation); tmax=max(tmax,t[-1])
        n=int(round(tmax*fps))+1; ts=np.linspace(0,tmax,n)
        F=len(ts); Q=np.repeat(s.Q[None],F,0).copy(); T=np.repeat(s.T[None],F,0).copy()
        for (nm,path),(t,v,interp) in tracks.items():
            if nm not in s.idx: continue
            j=s.idx[nm]
            if interp=='CUBICSPLINE': v=v[1::3]
            if path=='rotation':
                Q[:,j]=slerp_s(t,v,ts)
            elif path=='translation':
                T[:,j]=np.stack([np.interp(ts,t,v[:,k]) for k in range(3)],1)
        return ts,Q,T,tracks
def slerp_s(t,v,ts):
    v=v/np.linalg.norm(v,axis=1,keepdims=True)
    if len(t)==1: return np.repeat(v,len(ts),0)
    from scipy.spatial.transform import Slerp
    # ensure continuity
    for k in range(1,len(v)):
        if np.dot(v[k],v[k-1])<0: v[k]=-v[k]
    return Slerp(t,R.from_quat(v))(np.clip(ts,t[0],t[-1])).as_quat()
