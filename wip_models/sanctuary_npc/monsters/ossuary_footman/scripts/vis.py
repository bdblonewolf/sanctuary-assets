import bpy,sys,json,math
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; src,js,out=a[0],a[1],a[2]; dirs=a[3].split(';'); tgt=Vector(tuple(map(float,a[4].split(',')))); S=float(a[5])
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=src)
for o in list(bpy.data.objects):
    if o.name.startswith('Ico'): bpy.data.objects.remove(o)
o=[x for x in bpy.data.objects if x.type=='MESH'][0]
bpy.context.view_layer.objects.active=o; o.select_set(True); bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
m=bpy.data.materials.new('r'); m.diffuse_color=(1,0,0,1); o.data.materials.append(m); k=len(o.data.materials)-1
for i in json.load(open(js)): o.data.polygons[i].material_index=k
sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'; sc.display.shading.color_type='MATERIAL'; sc.render.resolution_x=sc.render.resolution_y=700
cam=bpy.data.objects.new('c',bpy.data.cameras.new('c')); sc.collection.objects.link(cam); sc.camera=cam; cam.data.type='ORTHO'; cam.data.ortho_scale=S
for i,d in enumerate(dirs):
    d=Vector(tuple(map(float,d.split(',')))).normalized(); cam.location=tgt+d*5; cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=f'{out}_{i}.png'; bpy.ops.render.render(write_still=True)
