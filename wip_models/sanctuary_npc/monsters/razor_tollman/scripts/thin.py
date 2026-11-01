import bpy,sys,numpy as np,math,bmesh
from mathutils.bvhtree import BVHTree
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; src=a[0]; box=np.array([float(v) for v in a[1].split(',')]).reshape(2,3); TH=float(a[2]); out=a[3]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=src)
for o in list(bpy.data.objects):
    if o.name.startswith('Ico'): bpy.data.objects.remove(o)
o=[x for x in bpy.data.objects if x.type=='MESH'][0]
bpy.context.view_layer.objects.active=o; o.select_set(True); bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bm=bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
bvh=BVHTree.FromBMesh(bm)
sel=[]
for f in bm.faces:
    c=f.calc_center_median()
    if not ((np.array(c)>=box[0]).all() and (np.array(c)<=box[1]).all()): continue
    n=f.normal; h=bvh.ray_cast(c-n*0.001,-n,0.5)
    t=h[3] if h[0] else 9
    if t<TH: sel.append(f.index)
# components by welded positions
S=set(sel); key=lambda v:tuple(np.round(v.co,5))
vf={}
for i in sel:
    for v in bm.faces[i].verts: vf.setdefault(key(v),[]).append(i)
par={i:i for i in sel}
def fd(i):
    while par[i]!=i: par[i]=par[par[i]]; i=par[i]
    return i
for k,l in vf.items():
    for j in l[1:]: par[fd(j)]=fd(l[0])
comp={}
for i in sel: comp.setdefault(fd(i),[]).append(i)
cs=sorted(comp.values(),key=len,reverse=True)
print('THIN',len(sel),'comps',[len(c) for c in cs[:8]])
for k,c in enumerate(cs[:4]):
    Pp=np.array([bm.faces[i].calc_center_median() for i in c]); print('C',k,len(c),Pp.min(0).round(2),Pp.max(0).round(2))
import json; json.dump(cs[0],open(out,'w'))
if len(a)>4:
    ids=[i for k in map(int,a[4].split(',')) for i in cs[k]]
    Pp=np.array([bm.faces[i].calc_center_median() for i in ids]); c0=Pp.mean(0); u,s,vt=np.linalg.svd(Pp-c0); n=vt[2]
    print('PLANE',c0.round(3),n.round(3),s.round(2))
    d=(Pp-c0)@n; print('dspread',np.percentile(d,[1,50,99]).round(3))
    e1,e2=vt[0],vt[1]; UV=np.c_[(Pp-c0)@e1,(Pp-c0)@e2]
    pts=sorted(map(tuple,UV.round(5)))
    def cr(o,a_,b):return (a_[0]-o[0])*(b[1]-o[1])-(a_[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    H=lo[:-1]+up[:-1]
    class _h:
        def find_simplex(self,q):
            q=q[0]; return [0 if all(cr(H[i],H[(i+1)%len(H)],q)/max(1e-9,((H[(i+1)%len(H)][0]-H[i][0])**2+(H[(i+1)%len(H)][1]-H[i][1])**2)**.5)>=-DIL for i in range(len(H))) else -1]
    hull=_h(); DIL=float(a[6]) if len(a)>6 else 0
    pick=[]
    for f in bm.faces:
        c=np.array(f.calc_center_median()); dd=(c-c0)@n
        if abs(dd)<float(a[5]) and hull.find_simplex([[ (c-c0)@e1,(c-c0)@e2 ]])[0]>=0: pick.append(f.index)
    print('PICK',len(pick)); json.dump(pick,open(out,'w'))
