# Replace every trees_* child mesh with painted pine-canopy silhouette cards.
# Same node (name/parent/TRS), same local AABB. Parent meshes, col_* and all other nodes untouched.
import sys, json, zlib, math, io
sys.path.insert(0,'/tmp')
import numpy as np, pygltflib
from gl import acc, comps
from pygltflib import GLTF2, Accessor, BufferView, Mesh, Primitive, Attributes, Material, PbrMetallicRoughness, TextureInfo, Image as GImage, Texture, Sampler
ATLAS='/workspace/treecards/atlas_{}.png'
def h01(*a): return (zlib.crc32(repr(a).encode())&0xffffffff)/2**32

def cones_of(g,node):
    P=[];C=[];I=[];off=0
    for p in g.meshes[node.mesh].primitives:
        pp=acc(g,p.attributes.POSITION).astype(np.float64)
        cc=acc(g,p.attributes.COLOR_0) if p.attributes.COLOR_0 is not None else np.ones((len(pp),4))
        if cc.shape[1]==3: cc=np.c_[cc,np.zeros(len(cc))]
        ii=acc(g,p.indices).ravel() if p.indices is not None else np.arange(len(pp))
        P.append(pp);C.append(cc);I.append(ii+off);off+=len(pp)
    P=np.concatenate(P);C=np.concatenate(C);I=np.concatenate(I)
    k,lab=comps(P,I)
    out=[]
    for i in range(k):
        m=lab==i; Q=P[m]; c=C[m]
        if len(Q)<3: continue
        out.append(dict(x=Q[:,0].mean(),z=Q[:,2].mean(),by=Q[:,1].min(),ty=Q[:,1].max(),
            w=max(np.ptp(Q[:,0]),np.ptp(Q[:,2])),col=c[:,:3].mean(0),a=c[:,3].mean()))
    return P,out

def build_cards(cones,kind,season,seed,aabb):
    C=7.0 if kind=='kit' else 15.0
    cells={}
    for c in cones: cells.setdefault((math.floor(c['x']/C),math.floor(c['z']/C)),[]).append(c)
    V=[];N=[];UV=[];COL=[];F=[]
    for key,cs in sorted(cells.items()):
        X=np.array([[c['x'],c['z']] for c in cs]); W=np.array([c['w'] for c in cs])
        BY=np.array([c['by'] for c in cs]); TY=np.array([c['ty'] for c in cs])
        cen=X.mean(0)
        if kind=='kit': f=np.array([0.0,1.0])
        else:
            f=-cen/ (np.linalg.norm(cen)+1e-6)
        hmax=float((TY-BY).max())
        wts=np.array([max(c['ty']-c['by'],0.1)*max(c['w'],0.1)**2 for c in cs])
        rust=float(np.sum(wts*np.array([(c['col'][0]>1.6*c['col'][1] and c['col'][0]>0.04) for c in cs]))/wts.sum())
        alt=1 if h01(seed,key,'s')<0.5 else -1
        angs=[0, alt*(40 if kind=='kit' else 32)]
        for j,a in enumerate(angs):
            a=math.radians(a+ (h01(seed,key,j)-0.5)*10)
            n=np.array([f[0]*math.cos(a)-f[1]*math.sin(a), f[0]*math.sin(a)+f[1]*math.cos(a)])
            t=np.array([n[1],-n[0]])
            s=(X-cen)@t
            lo=float((s-W*0.5).min()); hi=float((s+W*0.5).max())
            wid=max(hi-lo, C*0.9)*1.12; mid=(lo+hi)*0.5
            # ground line under the card from the cone bases (gentle slope only -> trees stay upright)
            if len(cs)>=2 and np.ptp(s)>1e-3:
                k1=float(np.clip(np.polyfit(s,BY,1)[0],-0.3,0.3))
            else: k1=0.0
            bury=max(0.6,0.12*hmax)
            k0=float((BY-k1*s).min())-bury          # line sits under every cone base
            sL=mid-wid/2; sR=mid+wid/2
            yL=k0+k1*sL; yR=k0+k1*sR
            Hc=float((TY-(k0+k1*s)).max())/0.93
            lean=-n*Hc*math.tan(math.radians(10))
            c3=lambda sv,y,top: np.array([cen[0]+t[0]*sv+(lean[0] if top else 0), y, cen[1]+t[1]*sv+(lean[1] if top else 0)])
            q=[c3(sL,yL,0),c3(sR,yR,0),c3(sR,yR+Hc,1),c3(sL,yL+Hc,1)]
            if season=='autumn' and kind=='ring' or season=='autumn':
                tile=0 if rust<0.25 else 1 if rust<0.50 else 2 if rust<0.80 else 3
            else: tile=int(h01(seed,key,j,'t')*4)%4
            u0=(tile%2)*0.5; v0=(tile//2)*0.5
            ua,ub=u0+0.008,u0+0.492
            if h01(seed,key,j,'f')<0.5: ua,ub=ub,ua
            vt,vb=v0+0.008,v0+0.4985
            uv=[(ua,vb),(ub,vb),(ub,vt),(ua,vt)]
            nn=np.array([n[0]*0.85,0.40,n[1]*0.85]); nn/=np.linalg.norm(nn)
            jit=0.86+0.14*h01(seed,key,j,'c')
            al=255 if kind=='kit' else int(round(float(np.mean([c['a'] for c in cs]))*255))
            b=len(V)
            V+=q; N+=[nn]*4; UV+=uv; COL+=[[round(255*jit)]*3+[al]]*4
            F+=[[b,b+1,b+2],[b,b+2,b+3]]
    V=np.array(V);F=np.array(F,dtype=np.uint32)
    # exact AABB match (per-axis affine remap onto the original trees_* bounds)
    lo,hi=V.min(0),V.max(0); olo,ohi=aabb
    V=olo+(V-lo)*((ohi-olo)/np.maximum(hi-lo,1e-9))
    return V.astype(np.float32),np.array(N,np.float32),np.array(UV,np.float32),np.array(COL,np.uint8),F

class Blob:
    def __init__(s): s.b=bytearray(); s.views=[]
    def add(s,data,target=None):
        while len(s.b)%4: s.b.append(0)
        off=len(s.b); s.b+=data
        s.views.append(BufferView(buffer=0,byteOffset=off,byteLength=len(data),target=target)); return len(s.views)-1

def rebuild(g, new_prims, tex_png, matname):
    """compact: copy every still-referenced bufferView, then append new data"""
    old=g.binary_blob()
    used_acc=set()
    for m in g.meshes:
        for p in m.primitives:
            for k,v in p.attributes.__dict__.items():
                if isinstance(v,int): used_acc.add(v)
            if p.indices is not None: used_acc.add(p.indices)
            for tg in (p.targets or []):
                for v in (tg.values() if isinstance(tg,dict) else tg.__dict__.values()):
                    if isinstance(v,int): used_acc.add(v)
    for sk in g.skins or []:
        if sk.inverseBindMatrices is not None: used_acc.add(sk.inverseBindMatrices)
    for an in g.animations or []:
        for sm in an.samplers: used_acc|={sm.input,sm.output}
    used_bv={g.accessors[a].bufferView for a in used_acc}|{im.bufferView for im in (g.images or []) if im.bufferView is not None}
    bl=Blob(); bvmap={}
    for i,bv in enumerate(g.bufferViews):
        if i in used_bv:
            d=old[(bv.byteOffset or 0):(bv.byteOffset or 0)+bv.byteLength]
            j=bl.add(d,bv.target); bl.views[j].byteStride=bv.byteStride; bl.views[j].name=bv.name; bvmap[i]=j
    accmap={}; accs=[]
    for i,a in enumerate(g.accessors):
        if i in used_acc:
            a.bufferView=bvmap[a.bufferView]; accmap[i]=len(accs); accs.append(a)
    def ra(v): return accmap[v]
    for m in g.meshes:
        for p in m.primitives:
            for k,v in list(p.attributes.__dict__.items()):
                if isinstance(v,int): setattr(p.attributes,k,ra(v))
            if p.indices is not None: p.indices=ra(p.indices)
    for sk in g.skins or []:
        if sk.inverseBindMatrices is not None: sk.inverseBindMatrices=ra(sk.inverseBindMatrices)
    for an in g.animations or []:
        for sm in an.samplers: sm.input=ra(sm.input); sm.output=ra(sm.output)
    for im in g.images or []:
        if im.bufferView is not None: im.bufferView=bvmap[im.bufferView]
    g.accessors=accs
    # new texture + material
    ib=bl.add(tex_png)
    g.images.append(GImage(bufferView=ib,mimeType='image/png',name=matname.replace('ms_','t_')))
    g.samplers=g.samplers or []
    g.samplers.append(Sampler(magFilter=9729,minFilter=9987,wrapS=33071,wrapT=33071))
    g.textures.append(Texture(sampler=len(g.samplers)-1,source=len(g.images)-1))
    g.materials.append(Material(name=matname,alphaMode='MASK',alphaCutoff=0.5,doubleSided=True,
        pbrMetallicRoughness=PbrMetallicRoughness(baseColorTexture=TextureInfo(index=len(g.textures)-1),
        baseColorFactor=[1,1,1,1],metallicFactor=0.0,roughnessFactor=0.95)))
    mat=len(g.materials)-1
    def addacc(arr,ctype,typ,norm=False,target=34962,mm=False):
        j=bl.add(arr.tobytes(),target)
        a=Accessor(bufferView=j,byteOffset=0,componentType=ctype,count=len(arr),type=typ,normalized=norm or None)
        if mm: a.min=arr.min(0).tolist(); a.max=arr.max(0).tolist()
        g.accessors.append(a); return len(g.accessors)-1
    out=[]
    for (node_i,meshname,V,N,UV,COL,F) in new_prims:
        pa=addacc(V,5126,'VEC3',mm=True); na=addacc(N,5126,'VEC3'); ta=addacc(UV,5126,'VEC2')
        ca=addacc(COL,5121,'VEC4',norm=True)
        idx=F.ravel().astype(np.uint16 if len(V)<65535 else np.uint32)
        ia=addacc(idx.reshape(-1,1),5123 if idx.dtype==np.uint16 else 5125,'SCALAR',target=34963)
        g.meshes.append(Mesh(name=meshname,primitives=[Primitive(attributes=Attributes(POSITION=pa,NORMAL=na,TEXCOORD_0=ta,COLOR_0=ca),indices=ia,material=mat,mode=4)]))
        g.nodes[node_i].mesh=len(g.meshes)-1
    g.bufferViews=bl.views
    g.buffers=[pygltflib.Buffer(byteLength=len(bl.b))]
    g.set_binary_blob(bytes(bl.b))

def drop_unused(g):
    # remove meshes no node references (the old cone meshes) and materials no primitive references
    usedm={n.mesh for n in g.nodes if n.mesh is not None}
    keep=[i for i in range(len(g.meshes)) if i in usedm]; mm={o:i for i,o in enumerate(keep)}
    g.meshes=[g.meshes[i] for i in keep]
    for n in g.nodes:
        if n.mesh is not None: n.mesh=mm[n.mesh]
    usedmat={p.material for m in g.meshes for p in m.primitives if p.material is not None}
    keep=[i for i in range(len(g.materials)) if i in usedmat]; mt={o:i for i,o in enumerate(keep)}
    g.materials=[g.materials[i] for i in keep]
    for m in g.meshes:
        for p in m.primitives:
            if p.material is not None: p.material=mt[p.material]

def process(path,outpath):
    g=GTF=GLTF2().load(path)
    assert not (g.extensionsUsed and any('draco' in e.lower() or 'meshopt' in e.lower() for e in g.extensionsUsed)), g.extensionsUsed
    base=path.rsplit('/',1)[1][:-4]; season=base.rsplit('_',1)[1]
    kind='kit' if base.startswith('bk_') else 'ring'
    key=kind+'_'+season
    matname=('ms_bk_treecard_' if kind=='kit' else 'ms_bd5_treecard_')+season
    targets=[i for i,n in enumerate(g.nodes) if n.name and n.name.startswith('trees_') and n.mesh is not None]
    if not targets: return None
    rep=[]; stats=[]
    for i in targets:
        n=g.nodes[i]
        P,cones=cones_of(g,n)
        aabb=(P.min(0),P.max(0))
        V,N,UV,COL,F=build_cards(cones,kind,season,base+n.name,aabb)
        rep.append((i,g.meshes[n.mesh].name,V,N,UV,COL,F))
        stats.append(dict(node=n.name,cones=len(cones),old_verts=len(P),new_verts=len(V),new_tris=len(F),cards=len(F)//2,
                          aabb_min=[round(float(x),4) for x in aabb[0]],aabb_max=[round(float(x),4) for x in aabb[1]]))
    # detach old meshes, then compact, then add new
    for i,_,*r in rep: g.nodes[i].mesh=None
    drop_unused(g)
    rebuild(g,rep,open(ATLAS.format(key),'rb').read(),matname)
    g.save_binary(outpath)
    return dict(file=base,kind=kind,season=season,atlas=key,material=matname,nodes=stats)

if __name__=='__main__':
    import glob
    res=[]
    for p in sys.argv[2:]:
        r=process(p, sys.argv[1]+'/'+p.rsplit('/',1)[1])
        print(p, 'skip (no trees_)' if r is None else sum(x['new_verts'] for x in r['nodes']), flush=True)
        if r: res.append(r)
    json.dump(res,open(sys.argv[1]+'/build_report.json','w'),indent=1)
