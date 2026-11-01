import bpy,sys,json,numpy as np,bmesh
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=a[0])
o=[x for x in bpy.data.objects if x.type=='MESH' and not x.name.startswith('Ico')][0]
M=o.matrix_world; sel=json.load(open(a[1]))
key=lambda i:tuple(np.round(np.array(M@o.data.vertices[i].co),5))
vf={}
for f in sel:
    for v in o.data.polygons[f].vertices: vf.setdefault(key(v),[]).append(f)
par={i:i for i in sel}
def fd(i):
    while par[i]!=i: par[i]=par[par[i]]; i=par[i]
    return i
for l in vf.values():
    for j in l[1:]: par[fd(j)]=fd(l[0])
comp={}
for i in sel: comp.setdefault(fd(i),[]).append(i)
cs=sorted(comp.values(),key=len,reverse=True)
for k,c in enumerate(cs[:6]):
    P=np.array([M@o.data.polygons[i].center for i in c]); print('C',k,len(c),P.min(0).round(2),P.max(0).round(2))
keep=[int(x) for x in a[3].split(',')]
json.dump([i for k in keep for i in cs[k]],open(a[2],'w'))
