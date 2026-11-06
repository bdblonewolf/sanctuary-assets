import sys; sys.path.insert(0,'/tmp')
from gl import *
import hashlib
def sig(g):
    par={c:i for i,n in enumerate(g.nodes) for c in (n.children or [])}
    out={}
    for i,n in enumerate(g.nodes):
        d=dict(parent=g.nodes[par[i]].name if i in par else None,children=sorted(g.nodes[c].name for c in (n.children or [])),
               trs=(n.translation,n.rotation,n.scale,n.matrix),extras=n.extras)
        if n.mesh is not None:
            prims=[]; mn=[]
            for p in g.meshes[n.mesh].primitives:
                a={k:hashlib.md5(acc(g,v).tobytes()).hexdigest() for k,v in p.attributes.__dict__.items() if isinstance(v,int)}
                if p.indices is not None: a['IDX']=hashlib.md5(acc(g,p.indices).astype(np.uint32).tobytes()).hexdigest()
                mat=g.materials[p.material] if p.material is not None else None
                if mat:
                    m=mat.to_dict() if hasattr(mat,'to_dict') else str(mat)
                    tex=mat.pbrMetallicRoughness.baseColorTexture
                    a['MAT']=(mat.name,)
                    # image hash of all textures referenced
                    ims=[]
                    for ti in [tex,mat.normalTexture,mat.occlusionTexture,mat.emissiveTexture,mat.pbrMetallicRoughness.metallicRoughnessTexture]:
                        if ti is not None:
                            im=g.images[g.textures[ti.index].source]; bv=g.bufferViews[im.bufferView]
                            ims.append(hashlib.md5(g.binary_blob()[bv.byteOffset or 0:(bv.byteOffset or 0)+bv.byteLength]).hexdigest())
                    a['TEX']=ims
                prims.append(a)
            d['mesh']=prims
            P=np.concatenate([acc(g,p.attributes.POSITION) for p in g.meshes[n.mesh].primitives])
            d['aabb']=(P.min(0),P.max(0))
        out[n.name]=d
    return out,[n.name for n in g.nodes]
bad=0
for a,b in zip(sys.argv[1::2],sys.argv[2::2]):
    A,oa=sig(pygltflib.GLTF2().load(a)); B,ob=sig(pygltflib.GLTF2().load(b))
    assert oa==ob, 'node order/name changed'
    for k in A:
        x,y=A[k],B[k]
        if k.startswith('trees_'):
            ok=x['parent']==y['parent'] and x['trs']==y['trs'] and np.allclose(x['aabb'][0],y['aabb'][0],atol=1e-3) and np.allclose(x['aabb'][1],y['aabb'][1],atol=1e-3)
        else:
            ok=all(x[f]==y[f] for f in ['parent','children','trs','extras']) and (('mesh' not in x) or (x['mesh']==y['mesh']))
        if not ok: bad+=1; print('MISMATCH',b,k)
    print('ok' if not bad else 'BAD', b.split('/')[-1], len(A),'nodes')
sys.exit(1 if bad else 0)
