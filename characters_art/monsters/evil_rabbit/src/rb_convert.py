import bpy
bpy.ops.wm.open_mainfile(filepath='/workspace/free_packs/opengameart_rabbit_cdmir/rabbit.blend')
sc=bpy.context.scene
for o in list(bpy.data.objects):
    if o.name not in ('Armature','Rabbit'): bpy.data.objects.remove(o)
arm=bpy.data.objects['Armature']; body=bpy.data.objects['Rabbit']
print('DEFORM',[b.name for b in arm.data.bones if b.use_deform])
print('VG',[g.name for g in body.vertex_groups])
print('PARENTS',{b.name:(b.parent.name if b.parent else None) for b in arm.data.bones if b.use_deform})
print('CONSTR',{pb.name:[c.type for c in pb.constraints] for pb in arm.pose.bones if pb.constraints})
print('MATS',[s.material.name for s in body.material_slots])
ad=arm.animation_data; print('CUR',ad.action.name if ad and ad.action else None, [t.name for t in ad.nla_tracks] if ad else None)
keep=['Running','Jump','Dying.000','Dying.001','Guarding','Sitting.000','Basic']
for t in list(ad.nla_tracks): ad.nla_tracks.remove(t)
ad.action=None
for a in list(bpy.data.actions):
    if a.name not in keep: bpy.data.actions.remove(a)
    else: a.use_fake_user=True
sc.render.fps=24
bpy.ops.object.select_all(action='DESELECT'); arm.select_set(True); body.select_set(True)
bpy.ops.export_scene.gltf(filepath='/workspace/wl5/rabbit_src.glb',use_selection=True,export_animations=True,export_animation_mode='ACTIONS',
   export_force_sampling=True,export_frame_range=False,export_anim_slide_to_zero=True,export_def_bones=True,export_yup=True,export_skins=True,export_morph=False,export_image_format='AUTO')
