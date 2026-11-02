import bpy, sys, json, math, mathutils
argv=sys.argv[sys.argv.index('--')+1:]
body,clipsf,out,spec=argv[0],argv[1],argv[2],json.loads(argv[3])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=body)
barm=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'][0]
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)]
before=set(bpy.data.actions)
before_objs=set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=clipsf)
for o in set(bpy.context.scene.objects)-before_objs: bpy.data.objects.remove(o,do_unlink=True)
acts={a.name:a for a in bpy.data.actions if a not in before}
print('ACTIONS',list(acts))
sc=bpy.context.scene; sc.render.fps=30
sc.render.engine='BLENDER_WORKBENCH'; sc.display.shading.light='STUDIO'; sc.display.shading.color_type='MATERIAL'
sc.render.resolution_x=spec.get('w',220); sc.render.resolution_y=spec.get('h',320)
sc.render.image_settings.file_format='PNG'
world=bpy.data.worlds.new('w'); sc.world=world
# ground plane & seat box
bpy.ops.mesh.primitive_plane_add(size=4); gp=bpy.context.object
if spec.get('seat'):
    bpy.ops.mesh.primitive_cube_add(size=1); s=bpy.context.object; s.scale=(0.9,0.4,0.45); s.location=(0,0.12,0.225)  # blender coords: y = -gltf z
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam
H=spec.get('height',1.8); side=spec.get('side',True)
cam.data.type='ORTHO'; cam.data.ortho_scale=H*1.08
cam.location=(4 if side else 2.2, -0.0 if side else -3.2, H*0.5)
d=mathutils.Vector((0,spec.get('cz',0),H*0.5))-cam.location
cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
res={}
import os
tiles=[]
for clip,frames in spec['clips']:
    suf=[k[4:] for k in acts if k.startswith('idle_') or k.startswith('town_idle_')][0] if spec.get('suf') is None else spec['suf']
    a=acts.get(clip) or acts.get(clip+suf) or [v for k,v in acts.items() if k.startswith(clip+'_')][0]
    barm.animation_data_create(); barm.animation_data.action=a
    f0,f1=[int(x) for x in a.frame_range]
    # mesh min-height check over all frames
    mins=[]
    dg=bpy.context.evaluated_depsgraph_get()
    for f in range(f0,f1+1):
        sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get()
        m=1e9
        for o in meshes:
            e=o.evaluated_get(dg); me=e.to_mesh()
            mw=e.matrix_world
            import numpy as np
            co=np.zeros(len(me.vertices)*3,dtype=np.float32); me.vertices.foreach_get('co',co); co=co.reshape(-1,3)
            M=np.array(mw); z=co@M[2,:3]+M[2,3]
            m=min(m,float(z.min())); e.to_mesh_clear()
        mins.append(m)
    res[clip]=dict(frames=f1-f0+1,mesh_min_z=[round(min(mins),3),round(max(mins),3)])
    for k in range(frames):
        f=f0+round((f1-f0)*k/max(1,frames-1)); sc.frame_set(f)
        p='/tmp/prev_%s_%d.png'%(clip,k); sc.render.filepath=p; bpy.ops.render.render(write_still=True); tiles.append((clip,k,p))
json.dump(dict(res=res,tiles=tiles),open(out+'.json','w'))
