# blender -b -P render.py -- spec.json ; spec: {out, res:[w,h], samples, items:[{glb,loc,rotz,label,scale}], cam:{loc,target,lens}, mode:'sheet'|'scene', extra:'boats'}
import bpy, sys, json, math, os
from mathutils import Vector
spec=json.load(open(sys.argv[sys.argv.index('--')+1]))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.samples=spec.get('samples',96); sc.cycles.use_denoising=True
try: sc.cycles.device='CPU'
except: pass
sc.render.resolution_x,sc.render.resolution_y=spec.get('res',[1600,900]); sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
sc.view_settings.exposure=spec.get('exposure',0.0)
W=bpy.data.worlds.new('w'); sc.world=W; W.use_nodes=True; bg=W.node_tree.nodes['Background']; bg.inputs[0].default_value=(*spec.get('world',(0.012,0.014,0.02)),1); bg.inputs[1].default_value=1.0
def look(o,t):
    d=Vector(t)-o.location; o.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
def light(kind,loc,energy,color,size=1.0,target=(0,0,0),spot=None):
    L=bpy.data.lights.new(kind+str(len(bpy.data.lights)),kind); L.energy=energy; L.color=color
    if kind=='AREA': L.size=size
    if kind=='SPOT': L.spot_size=math.radians(spot or 50); L.spot_blend=0.6; L.shadow_soft_size=size
    if kind=='POINT': L.shadow_soft_size=size
    if kind=='SUN': L.angle=math.radians(size)
    o=bpy.data.objects.new(L.name,L); sc.collection.objects.link(o); o.location=loc; look(o,target); return o
def imp(item):
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=item['glb']); new=[o for o in bpy.data.objects if o not in before]
    roots=[o for o in new if o.parent is None]
    for r in roots:
        r.rotation_mode='XYZ'; r.location=Vector(item.get('loc',(0,0,0))); r.rotation_euler=(0,0,math.radians(item.get('rotz',0)))
        if 'scale' in item: r.scale=(item['scale'],)*3
        if 'tilt' in item: r.rotation_euler=(math.radians(item['tilt'][0]),math.radians(item['tilt'][1]),math.radians(item.get('rotz',0)))
    for o in new:
        if o.name.startswith('col_'): o.hide_render=True; o.hide_set(True)
    return new
def label(text,loc,size=0.22,rot=(math.radians(60),0,0)):
    cu=bpy.data.curves.new('t','FONT'); cu.body=text; cu.size=size; cu.align_x='CENTER'
    o=bpy.data.objects.new('lbl',cu); sc.collection.objects.link(o); o.location=loc; o.rotation_euler=rot
    m=bpy.data.materials.new('lbl'); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value=(0.55,0.5,0.42,1)
    b.inputs['Emission Color'].default_value=(0.5,0.45,0.38,1); b.inputs['Emission Strength'].default_value=0.6; cu.materials.append(m)
LROT=(math.radians(spec.get('label_rot',60)),0,0)
for it in spec['items']:
    imp(it)
    if it.get('label'): label(it['label'],it.get('label_loc',(it['loc'][0],it['loc'][1]-it.get('label_off',1.0),0.02)),it.get('label_size',0.2),LROT)
for e in spec.get('extra_glb',[]): imp(e)
for lb in spec.get('labels',[]): label(lb['text'],lb['loc'],lb.get('size',0.2),LROT)
if spec.get('floor',True):
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,spec.get('floor_z',0))); fl=bpy.context.active_object
    m=bpy.data.materials.new('floor'); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    tx=nt.nodes.new('ShaderNodeTexImage'); tx.image=bpy.data.images.load(spec.get('floor_tex','/workspace/gothwork/tex/stone_block_a.jpg'))
    tc=nt.nodes.new('ShaderNodeTexCoord'); mp=nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=(1/spec.get('floor_tile',3),)*3
    nt.links.new(tc.outputs['Object'],mp.inputs[0]); nt.links.new(mp.outputs[0],tx.inputs[0])
    mx=nt.nodes.new('ShaderNodeMix'); mx.data_type='RGBA'; mx.blend_type='MULTIPLY'; mx.inputs[0].default_value=1; mx.inputs[7].default_value=(*spec.get('floor_mul',(0.5,0.5,0.5)),1)
    nt.links.new(tx.outputs[0],mx.inputs[6]); nt.links.new(mx.outputs[2],b.inputs['Base Color']); b.inputs['Roughness'].default_value=0.95
    fl.data.materials.append(m)
# water plane for boats
if spec.get('water'):
    bpy.ops.mesh.primitive_plane_add(size=300,location=(0,0,0)); w=bpy.context.active_object
    m=bpy.data.materials.new('water'); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(0.006,0.012,0.012,1); b.inputs['Roughness'].default_value=0.08; b.inputs['Transmission Weight'].default_value=0.0
    nz=nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value=1.2; nz.inputs['Detail'].default_value=6
    bmp=nt.nodes.new('ShaderNodeBump'); bmp.inputs['Strength'].default_value=0.12; nt.links.new(nz.outputs[0],bmp.inputs['Height']); nt.links.new(bmp.outputs[0],b.inputs['Normal'])
    w.data.materials.append(m)
# lights

def texmat(tex,mul,tile):
    m=bpy.data.materials.new('bx'); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    tx=nt.nodes.new('ShaderNodeTexImage'); tx.image=bpy.data.images.load(tex); tx.projection='BOX'; tx.projection_blend=0.3
    tc=nt.nodes.new('ShaderNodeTexCoord'); mp=nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=(1/tile,)*3
    nt.links.new(tc.outputs['Object'],mp.inputs[0]); nt.links.new(mp.outputs[0],tx.inputs[0])
    mx=nt.nodes.new('ShaderNodeMix'); mx.data_type='RGBA'; mx.blend_type='MULTIPLY'; mx.inputs[0].default_value=1; mx.inputs[7].default_value=(*mul,1)
    nt.links.new(tx.outputs[0],mx.inputs[6]); nt.links.new(mx.outputs[2],b.inputs['Base Color']); b.inputs['Roughness'].default_value=0.9
    return m
for bx in spec.get('boxes',[]):
    bpy.ops.mesh.primitive_cube_add(size=1,location=bx['loc']); o=bpy.context.active_object; o.scale=bx['size']
    o.rotation_euler=(0,0,math.radians(bx.get('rotz',0))); bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(texmat(bx.get('tex','/workspace/gothwork/tex/stone_block_a.jpg'),bx.get('mul',(0.6,0.6,0.6)),bx.get('tile',2.0)))
for bl in spec.get('blobs',[]):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5,radius=1,location=bl['loc']); o=bpy.context.active_object; o.scale=bl['scale']
    o.rotation_euler=(0,0,math.radians(bl.get('rotz',0)))
    from mathutils import noise as _n
    for v in o.data.vertices:
        p=v.co.copy(); d=_n.fractal(p*bl.get('freq',1.6)+Vector((bl.get('seed',0)*3.1,0,0)),0.6,2.0,5,noise_basis='PERLIN_ORIGINAL'); v.co=p*(1+bl.get('amp',0.3)*d)
    bpy.ops.object.shade_smooth()
    o.data.materials.append(texmat(bl.get('tex','/workspace/gothwork/tex/cliff_a.jpg'),bl.get('mul',(0.6,0.6,0.6)),bl.get('tile',3.0)))
for L in spec.get('lights',[]): light(L['kind'],L['loc'],L['energy'],L.get('color',(1,1,1)),L.get('size',1),L.get('target',(0,0,0)),L.get('spot'))
if spec.get('fog'):
    vol=bpy.data.materials.new('fog'); vol.use_nodes=True; nt=vol.node_tree; nt.nodes.remove(nt.nodes['Principled BSDF'])
    vs=nt.nodes.new('ShaderNodeVolumeScatter'); vs.inputs['Density'].default_value=spec['fog']; vs.inputs['Color'].default_value=(0.6,0.65,0.7,1)
    nt.links.new(vs.outputs[0],nt.nodes['Material Output'].inputs['Volume'])
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,10)); c=bpy.context.active_object; c.scale=(120,120,20); c.data.materials.append(vol)
cam=bpy.data.cameras.new('c'); C=spec['cam']; cam.lens=C.get('lens',35)
if C.get('ortho'): cam.type='ORTHO'; cam.ortho_scale=C['ortho']
co=bpy.data.objects.new('cam',cam); sc.collection.objects.link(co); co.location=C['loc']; look(co,C['target']); sc.camera=co
sc.render.filepath=spec['out']; os.makedirs(os.path.dirname(spec['out']),exist_ok=True)
if spec.get('save_blend'): bpy.ops.wm.save_as_mainfile(filepath=spec['save_blend'])
bpy.ops.render.render(write_still=True)
