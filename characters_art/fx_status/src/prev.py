import bpy,math
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='/workspace/fxs/out/ice_shards.glb')
sc=bpy.context.scene
obs=sorted([o for o in bpy.data.objects if o.type=='MESH'],key=lambda o:o.name)
for i,o in enumerate(obs): o.location=(-0.8+i*0.2,0.15,0)
T='/workspace/fxs/out/textures/'
def mat(p,emit=False):
    m=bpy.data.materials.new(p); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    def tex(n,non=True):
        t=nt.nodes.new('ShaderNodeTexImage'); t.image=bpy.data.images.load(T+n+'.png')
        if non: t.image.colorspace_settings.name='Non-Color'
        tc=nt.nodes.new('ShaderNodeTexCoord'); mp=nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=(2,2,2); nt.links.new(tc.outputs['UV'],mp.inputs[0]); nt.links.new(mp.outputs[0],t.inputs[0])
        return t
    c=tex(p+'_bc',False); n=tex(p+'_n'); o=tex(p+'_orm')
    nt.links.new(c.outputs[0],b.inputs['Base Color']); sp=nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(o.outputs[0],sp.inputs[0]); nt.links.new(sp.outputs[1],b.inputs['Roughness'])
    nm=nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(n.outputs[0],nm.inputs['Color']); nt.links.new(nm.outputs[0],b.inputs['Normal'])
    if emit:
        e=tex('char_ember'); mu=nt.nodes.new('ShaderNodeMixRGB'); mu.blend_type='MULTIPLY'; mu.inputs[0].default_value=1; mu.inputs[2].default_value=(1.0,0.32,0.06,1); nt.links.new(e.outputs[0],mu.inputs[1]); nt.links.new(mu.outputs[0],b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=3
    return m
for k,(p,x,e) in enumerate([('char',-0.5,False),('char',0.0,True),('ice',0.5,False)]):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2,location=(x,-0.55,0.2)); s=bpy.context.object; bpy.ops.object.shade_smooth(); s.data.materials.append(mat(p,e))
bpy.ops.mesh.primitive_plane_add(size=8); g=bpy.context.object; m=bpy.data.materials.new('g'); m.use_nodes=True; m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(0.2,0.2,0.22,1); g.data.materials.append(m)
bpy.ops.object.light_add(type='SUN',rotation=(math.radians(50),0,math.radians(30))); bpy.context.object.data.energy=3.5
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; w.node_tree.nodes['Background'].inputs[1].default_value=0.5
bpy.ops.object.camera_add(location=(0,-2.2,1.1)); cam=bpy.context.object; sc.camera=cam
d=Vector((0,0,0.15))-cam.location; cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); cam.data.lens=45
sc.render.engine='CYCLES'; sc.cycles.samples=48; sc.render.resolution_x=1400; sc.render.resolution_y=800; sc.render.filepath='/workspace/fxs/out/preview_fx_status.png'
bpy.ops.render.render(write_still=True)
