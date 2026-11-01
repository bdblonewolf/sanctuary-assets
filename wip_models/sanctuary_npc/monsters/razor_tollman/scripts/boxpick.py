import bpy,sys,json,numpy as np
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=a[0])
o=[x for x in bpy.data.objects if x.type=='MESH' and not x.name.startswith('Ico')][0]
M=o.matrix_world; out=[]
box=np.array([float(v) for v in a[1].split(',')]).reshape(2,3)
for p in o.data.polygons:
    c=np.array(M@p.center)
    if (c>=box[0]).all() and (c<=box[1]).all(): out.append(p.index)
print('PICK',len(out)); json.dump(out,open(a[2],'w'))
