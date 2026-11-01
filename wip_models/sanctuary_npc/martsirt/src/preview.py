import os
# Cycles previews in warm town light.  usage: blender -b --python preview.py -- GLB OUTPREFIX MODE [height]
#   MODE=stills : front / 3-4 / side / back / face (idle frame if animated, else rest)
#   MODE=clips  : contact sheet frames for every action (2 frames each) -> OUTPREFIX_clip_<name>_<i>.png
import bpy,sys,math,os
from mathutils import Vector,Euler
a=sys.argv[sys.argv.index('--')+1:]; GLB,OUT,MODE=a[0],a[1],a[2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
sc=bpy.context.scene
arm=next((o for o in sc.objects if o.type=='ARMATURE'),None)
meshes=[o for o in sc.objects if o.type=='MESH']
# engine default: hide body regions covered by the default outfit (HIDE=torso,legs,feet)
_hide=[r for r in os.environ.get('HIDE','').split(',') if r]
for o in list(meshes):
    if any(o.name.endswith('_body_'+r) for r in _hide) or (os.environ.get('BARE') and ('_outfit_' in o.name or '_prop_' in o.name or o.name.endswith('_keepsake'))): o.hide_render=True; o.hide_set(True); meshes.remove(o)
# bounds from rest
H=max((o.matrix_world@Vector(c)).z for o in meshes if '_prop_' not in o.name for c in o.bound_box)
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=int(os.environ.get('SAMPLES','48')); sc.cycles.use_denoising=True
try: sc.cycles.denoiser='OPENIMAGEDENOISE'
except: pass
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
sc.render.film_transparent=False
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; bg=w.node_tree.nodes['Background']; bg.inputs[0].default_value=(0.05,0.045,0.04,1); bg.inputs[1].default_value=1.0
def light(kind,loc,rot,col,en,size=1.0):
    d=bpy.data.lights.new(kind,kind); d.color=col; d.energy=en
    if kind=='AREA': d.size=size
    if kind=='SUN': d.angle=math.radians(3)
    o=bpy.data.objects.new(kind,d); sc.collection.objects.link(o); o.location=loc; o.rotation_euler=Euler([math.radians(x) for x in rot]); return o
light('SUN',(0,0,10),(55,0,-35),(1.0,0.84,0.66),3.4)          # low warm evening sun, from front-left
light('AREA',(-3,3,2.5),(70,0,-135),(0.55,0.65,0.85),120,4)    # cool sky fill from back-right (rim)
light('POINT',(1.6,-1.6,1.9),(0,0,0),(1.0,0.62,0.34),110)      # torch / brazier bounce
# ground: dark worn cobbles
bpy.ops.mesh.primitive_plane_add(size=12); g=bpy.context.object
m=bpy.data.materials.new('ground'); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
vo=nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value=4.0
cr=nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color=(0.03,0.028,0.025,1); cr.color_ramp.elements[1].color=(0.11,0.095,0.08,1); cr.color_ramp.elements[0].position=0.02; cr.color_ramp.elements[1].position=0.12
nt.links.new(vo.outputs['Distance'],cr.inputs[0]); nt.links.new(cr.outputs[0],b.inputs['Base Color']); b.inputs['Roughness'].default_value=0.85
g.data.materials.append(m)
def env_box(name,center_gl,size_gl,col):   # environment stand-in (glTF coords -> Blender), preview only
    cx,cy,cz=center_gl; sx,sy,sz=size_gl
    bpy.ops.mesh.primitive_cube_add(size=1,location=(cx,-cz,cy)); o=bpy.context.object; o.scale=(sx,sz,sy); o.name=name
    mm=bpy.data.materials.new(name); mm.use_nodes=True; mm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=col+(1,)
    mm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=0.6; o.data.materials.append(mm); return o
ENV={}
if os.environ.get('ANVIL'):
    ENV['work_hammer']=[env_box('anvil',(-0.02,0.80,0.53),(0.50,0.16,0.17),(0.05,0.05,0.055)),env_box('anvil_base',(-0.02,0.36,0.53),(0.30,0.72,0.30),(0.12,0.08,0.05))]
if os.environ.get('BENCH'):
    ENV['sit']=[env_box('bench',(0,float(os.environ['BENCH'])/2,-0.05),(1.2,float(os.environ['BENCH']),0.35),(0.15,0.10,0.06))]
    ENV['sit_talk']=ENV['sit']; ENV['sleep']=ENV['sit']
if os.environ.get('LECTERN'):
    ENV['work_write']=[env_box('lectern',tuple(map(float,os.environ['LECTERN'].split(','))),(0.55,0.04,0.40),(0.18,0.12,0.07))]
def show_env(clip):
    vis={id(o) for o in ENV.get(clip,[])}
    for k,l in ENV.items():
        for o in l: o.hide_render=id(o) not in vis
cam_d=bpy.data.cameras.new('c'); cam=bpy.data.objects.new('c',cam_d); sc.collection.objects.link(cam); sc.camera=cam
def shoot(path,az,dist,tz,lens,res=(768,1024),el=0.0):
    sc.render.resolution_x,sc.render.resolution_y=res
    cam_d.lens=lens; t=Vector((0,0,tz)); r=math.radians(az)
    cam.location=t+Vector((math.sin(r)*dist,-math.cos(r)*dist,el))
    cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=path; bpy.ops.render.render(write_still=True); print('WROTE',path)
acts=list(bpy.data.actions)
def set_action(name,frame):
    if not arm: return
    ac=bpy.data.actions.get(f'{name}_{arm.name}') or bpy.data.actions.get(name)
    if ac is None: return False
    (arm.animation_data or arm.animation_data_create()).action=ac
    for o in sc.objects:
        if o.parent==arm and o.parent_type=='BONE':
            aa=bpy.data.actions.get(f'{name}_{o.name}')
            ad=o.animation_data or o.animation_data_create(); ad.action=aa
    sc.frame_set(frame); return ac
for o in sc.objects:
    if o.name.startswith('Icosphere'): o.hide_render=True
os.makedirs(os.path.dirname(OUT) or '.',exist_ok=True)
if MODE=='stills':
    if acts: set_action('idle',1)
    show_env('idle')
    dg=bpy.context.evaluated_depsgraph_get(); zs=[]
    for o in meshes:
        if '_prop_' in o.name or o.name.startswith('Icosphere'): continue
        oe=o.evaluated_get(dg); me=oe.to_mesh(); zs+= [(oe.matrix_world@v.co).z for v in me.vertices]; oe.to_mesh_clear()
    H=max(zs); print('H_EVAL',H)
    shoot(OUT+'_front.png',0,H*1.95,H*0.52,50)
    shoot(OUT+'_q.png',-38,H*1.95,H*0.52,50)
    shoot(OUT+'_side.png',-90,H*1.95,H*0.52,50)
    shoot(OUT+'_back.png',180,H*1.95,H*0.52,50)
    eye=H-0.11
    shoot(OUT+'_face.png',-22,0.95,eye-0.04,85,res=(768,768))
else:
    names=[n for n in os.environ.get('CLIPS','').split(',') if n] or sorted({x.name[:-len(arm.name)-1] for x in acts if x.name.endswith(arm.name)})
    for n in names:
        ac=bpy.data.actions.get(f'{n}_{arm.name}')
        if not ac: print('MISSING',n); continue
        f0,f1=ac.frame_range
        for i,f in enumerate([f0+(f1-f0)*float(x) for x in os.environ.get('FRACS','0.25,0.65').split(',')]):
            set_action(n,int(f)); show_env(n)
            E=os.environ.get; shoot(f'{OUT}_clip_{n}_{i}.png',float(E('AZ',-35)),float(E('DIST',H*2.1)),float(E('TZ',H*0.48)),float(E('LENS',50)),res=(480,640))
