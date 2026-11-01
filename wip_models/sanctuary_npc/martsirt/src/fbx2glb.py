import bpy,sys
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=a[0],automatic_bone_orientation=False)
for o in list(bpy.data.objects):
    if o.type=='MESH': bpy.data.objects.remove(o)
arm=[o for o in bpy.data.objects if o.type=='ARMATURE'][0]
act=arm.animation_data.action; act.name=a[2]
print('RANGE',act.frame_range, bpy.context.scene.render.fps)
bpy.ops.export_scene.gltf(filepath=a[1],export_format='GLB',export_animations=True,export_force_sampling=True,export_frame_range=False,export_anim_single_armature=True)
