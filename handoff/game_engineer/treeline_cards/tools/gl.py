import pygltflib,numpy as np
CT={5126:np.float32,5123:np.uint16,5121:np.uint8,5125:np.uint32,5122:np.int16,5120:np.int8}
NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
def acc(g,i):
    a=g.accessors[i]; bv=g.bufferViews[a.bufferView]; blob=g.binary_blob()
    dt=np.dtype(CT[a.componentType]); n=NC[a.type]
    off=(bv.byteOffset or 0)+(a.byteOffset or 0)
    stride=bv.byteStride or dt.itemsize*n
    raw=np.frombuffer(blob,dtype=np.uint8,count=stride*(a.count-1)+dt.itemsize*n,offset=off)
    arr=np.lib.stride_tricks.as_strided(raw,(a.count,stride),(stride,1))[:,:dt.itemsize*n].copy().view(dt).reshape(a.count,n)
    if a.normalized:
        arr=arr.astype(np.float32)/np.iinfo(dt).max
    return arr
def comps(P,I):
    import scipy.sparse as sp, scipy.sparse.csgraph as cg
    # merge coincident verts
    q=np.round(P,4); _,inv=np.unique(q,axis=0,return_inverse=True); inv=inv.ravel()
    F=inv[I.reshape(-1,3)]
    n=inv.max()+1
    r=np.r_[F[:,0],F[:,1],F[:,2]]; c=np.r_[F[:,1],F[:,2],F[:,0]]
    A=sp.coo_matrix((np.ones(len(r)),(r,c)),shape=(n,n))
    k,lab=cg.connected_components(A,directed=False)
    return k, lab[inv]   # per original vertex label
