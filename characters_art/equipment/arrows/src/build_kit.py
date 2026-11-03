import bpy,bmesh,math,random,sys
from mathutils import Vector,Matrix
OUT='/workspace/arrows_v2/out'; import os; os.makedirs(OUT,exist_ok=True)
random.seed(7)
sc=bpy.context.scene
TEX='/workspace/gothwork/tex/'
def img(p,non=False):
    i=bpy.data.images.load(p); 
    if non: i.colorspace_settings.name='Non-Color'
    return i
# ---------- leather material ----------
L=bpy.data.materials.new('q_leather'); L.use_nodes=True; nt=L.node_tree; b=nt.nodes['Principled BSDF']
tc=nt.nodes.new('ShaderNodeTexImage'); tc.image=img(TEX+'leather_a_512.jpg')
tn=nt.nodes.new('ShaderNodeTexImage'); tn.image=img(TEX+'leather_n_512.jpg',True)
nm=nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(tn.outputs[0],nm.inputs['Color']); nt.links.new(nm.outputs[0],b.inputs['Normal'])
mul=nt.nodes.new('ShaderNodeMixRGB'); mul.blend_type='MULTIPLY'; mul.inputs[0].default_value=0.55; mul.inputs[2].default_value=(0.32,0.2,0.13,1)
nt.links.new(tc.outputs[0],mul.inputs[1]); nt.links.new(mul.outputs[0],b.inputs['Base Color']); b.inputs['Roughness'].default_value=0.72
D=bpy.data.materials.new('q_darkleather'); D.use_nodes=True; nt=D.node_tree; b=nt.nodes['Principled BSDF']
tc=nt.nodes.new('ShaderNodeTexImage'); tc.image=bpy.data.images['leather_a_512.jpg']
mul=nt.nodes.new('ShaderNodeMixRGB'); mul.blend_type='MULTIPLY'; mul.inputs[0].default_value=0.8; mul.inputs[2].default_value=(0.12,0.08,0.06,1)
nt.links.new(tc.outputs[0],mul.inputs[1]); nt.links.new(mul.outputs[0],b.inputs['Base Color']); b.inputs['Roughness'].default_value=0.6
IRON=bpy.data.materials['w_dark']
# ---------- quiver body ----------
H=0.56; SEG=14
bm=bmesh.new()
rings=[]
for k,(z,r) in enumerate([(0,0.050),(0.02,0.056),(0.25,0.060),(0.5,0.064),(H,0.066)]):
    ring=[bm.verts.new((r*math.cos(2*math.pi*i/SEG)*1.0, r*0.82*math.sin(2*math.pi*i/SEG)+0.0, z)) for i in range(SEG)]
    rings.append(ring)
for a,c in zip(rings,rings[1:]):
    for i in range(SEG): bm.faces.new((a[i],a[(i+1)%SEG],c[(i+1)%SEG],c[i]))
bm.faces.new(list(reversed(rings[0])))
# inner wall (open top, thin lip)
inner=[bm.verts.new((v.co.x*0.9,v.co.y*0.9,H-0.004)) for v in rings[-1]]
for i in range(SEG): bm.faces.new((rings[-1][i],rings[-1][(i+1)%SEG],inner[(i+1)%SEG],inner[i]))
deep=[bm.verts.new((v.co.x,v.co.y,0.3)) for v in inner]
for i in range(SEG): bm.faces.new((inner[i],inner[(i+1)%SEG],deep[(i+1)%SEG],deep[i]))
bm.faces.new(deep)
# jitter for worn look
for v in bm.verts:
    if 0.03<v.co.z<H-0.01: v.co.x+=random.uniform(-0.002,0.002); v.co.y+=random.uniform(-0.002,0.002)
me=bpy.data.meshes.new('quiver_body'); bm.to_mesh(me); bm.free()
Q=bpy.data.objects.new('quiver_body',me); sc.collection.objects.link(Q); me.materials.append(L)
for p in me.polygons: p.use_smooth=True
# bands (rim + 2 strap rings), dark leather / iron studs
def band(z,r,h,t,mat,name):
    bm=bmesh.new(); bmesh.ops.create_cone(bm,cap_ends=False,segments=SEG,radius1=r+t,radius2=r+t,depth=h)
    for v in bm.verts: v.co.y*=0.82; v.co.z+=z
    m=bpy.data.meshes.new(name); bm.to_mesh(m); bm.free(); o=bpy.data.objects.new(name,m); sc.collection.objects.link(o); m.materials.append(mat)
    for p in m.polygons: p.use_smooth=True
    return o
parts=[band(H-0.018,0.066,0.036,0.004,D,'q_rim'),band(0.40,0.063,0.03,0.004,D,'q_ring_hi'),band(0.12,0.058,0.03,0.004,D,'q_ring_lo'),band(0.008,0.053,0.016,0.003,IRON,'q_foot')]
# strap stubs (flat loops on back side, -Y)
for z in (0.40,0.12):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,-0.058,z)); s=bpy.context.object; s.scale=(0.035,0.012,0.03); s.name=f'q_strap_{z}'
    s.data.materials.append(D); parts.append(s)
def cyl_uv(o):
    me=o.data
    uv=me.uv_layers.new(name='UVMap')
    for p in me.polygons:
        us=[]
        for li in p.loop_indices:
            co=me.vertices[me.loops[li].vertex_index].co; u=(math.atan2(co.y,co.x)/(2*math.pi))%1.0; us.append(u)
        fix=max(us)-min(us)>0.5
        for li,u in zip(p.loop_indices,us):
            co=me.vertices[me.loops[li].vertex_index].co
            if fix and u<0.5: u+=1
            uv.data[li].uv=(u*2.0, co.z*3.0 if abs(p.normal.z)<0.7 else co.x*3+0.5)
for o in [Q]+[p for p in parts if not p.name.startswith('q_strap')]: cyl_uv(o)
# ---------- arrows in quiver: nock ends of the arrow mesh ----------
A=bpy.data.objects['arrow']
spots=[(0.022,0.012),(-0.02,0.016),(0.0,-0.015),(0.03,-0.012),(-0.032,-0.008),(0.008,0.03),(-0.01,0.0)]
for i,(x,y) in enumerate(spots):
    c=A.copy(); c.data=A.data.copy(); sc.collection.objects.link(c)
    bm=bmesh.new(); bm.from_mesh(c.data)
    bmesh.ops.bisect_plane(bm,geom=bm.verts[:]+bm.edges[:]+bm.faces[:],plane_co=(0,-0.30,0),plane_no=(0,1,0),clear_inner=True)
    bm.to_mesh(c.data); bm.free()
    c.parent=None
    up=random.uniform(0.17,0.24)
    c.matrix_world=Matrix.Translation((x,y,H+up))@Matrix.Rotation(random.uniform(-0.12,0.12),4,'Y')@Matrix.Rotation(random.uniform(-0.12,0.12),4,'X')@Matrix.Rotation(math.radians(90),4,'X')@Matrix.Rotation(random.uniform(0,6.28),4,'Y')
    parts.append(c)
bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
Q.select_set(True); bpy.context.view_layer.objects.active=Q
for o in parts:
    o.select_set(True)
bpy.ops.object.convert(target='MESH')
bpy.ops.object.join(); Q.name='quiver'; Q.data.name='quiver'
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
# ---------- shared atlas bake ----------
EXP=['arrow','arrow_stuck_deep','arrow_stuck_short','arrow_stuck_snapped','quiver']
objs=[bpy.data.objects[n] for n in EXP]
for o in objs:
    if 'atlas' not in o.data.uv_layers:
        uv0=o.data.uv_layers[0]
        if not uv0.name: uv0.name='UVMap'
        at=o.data.uv_layers.new(name='atlas'); at.active=True; o.data.uv_layers[0].active_render=True
bpy.ops.object.select_all(action='DESELECT')
for o in objs: o.select_set(True)
bpy.context.view_layer.objects.active=objs[-1]
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(60),island_margin=0.004,scale_to_bounds=False)
bpy.ops.uv.pack_islands(margin=0.004,rotate=True)
bpy.ops.object.mode_set(mode='OBJECT')
RES=1024
sc.render.engine='CYCLES'; sc.cycles.samples=8; sc.cycles.device='CPU'; sc.render.bake.margin=6
imgs={k:bpy.data.images.new('arrows_atlas_'+k,RES,RES) for k in ('bc','n','orm')}
imgs['n'].colorspace_settings.name='Non-Color'; imgs['orm'].colorspace_settings.name='Non-Color'
mats=set(m for o in objs for m in o.data.materials)
def src(b,name):
    s=b.inputs[name]; return s.links[0].from_socket if s.is_linked else None
saved={}
for m in mats:
    nt=m.node_tree; b=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'); out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
    saved[m]=(b,out,out.inputs['Surface'].links[0].from_socket)
def set_target(k):
    for m in mats:
        nt=m.node_tree; t=nt.nodes.get('BAKE') or nt.nodes.new('ShaderNodeTexImage'); t.name='BAKE'; t.image=imgs[k]
        for n in nt.nodes: n.select=False
        t.select=True; nt.nodes.active=t
def emit_mode(k):
    for m in mats:
        nt=m.node_tree; b,out,orig=saved[m]
        e=nt.nodes.get('EMIT') or nt.nodes.new('ShaderNodeEmission'); e.name='EMIT'
        for l in list(e.inputs['Color'].links): nt.links.remove(l)
        if k=='bc':
            s=src(b,'Base Color')
            if s: nt.links.new(s,e.inputs['Color'])
            else: e.inputs['Color'].default_value=b.inputs['Base Color'].default_value
        else:
            cc=nt.nodes.get('ORMC') or nt.nodes.new('ShaderNodeCombineColor'); cc.name='ORMC'
            cc.inputs[0].default_value=1.0
            for idx,nm in ((1,'Roughness'),(2,'Metallic')):
                for l in list(cc.inputs[idx].links): nt.links.remove(l)
                s=src(b,nm)
                if s: nt.links.new(s,cc.inputs[idx])
                else: cc.inputs[idx].default_value=b.inputs[nm].default_value
            nt.links.new(cc.outputs[0],e.inputs['Color'])
        nt.links.new(e.outputs[0],out.inputs['Surface'])
def restore():
    for m in mats:
        b,out,orig=saved[m]; m.node_tree.links.new(orig,out.inputs['Surface'])
bpy.ops.object.select_all(action='DESELECT')
for o in objs: o.select_set(True)
bpy.context.view_layer.objects.active=objs[0]
for k in ('bc','orm'):
    emit_mode(k); set_target(k); bpy.ops.object.bake(type='EMIT',use_clear=True)
restore(); set_target('n'); bpy.ops.object.bake(type='NORMAL',normal_space='TANGENT',use_clear=True)
for k,i in imgs.items():
    i.scale(512,512); i.filepath_raw=f'{OUT}/arrows_atlas_{k}.png'; i.file_format='PNG'; i.save()
# ---------- final single material ----------
F=bpy.data.materials.new('arrows_atlas'); F.use_nodes=True; nt=F.node_tree; b=nt.nodes['Principled BSDF']
def tex(k):
    t=nt.nodes.new('ShaderNodeTexImage'); t.image=bpy.data.images.load(f'{OUT}/arrows_atlas_{k}.png')
    if k!='bc': t.image.colorspace_settings.name='Non-Color'
    return t
c=tex('bc'); n=tex('n'); o=tex('orm'); nt.links.new(c.outputs[0],b.inputs['Base Color'])
sep=nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(o.outputs[0],sep.inputs[0]); nt.links.new(sep.outputs[1],b.inputs['Roughness']); nt.links.new(sep.outputs[2],b.inputs['Metallic'])
nm=nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(n.outputs[0],nm.inputs['Color']); nt.links.new(nm.outputs[0],b.inputs['Normal'])
for ob in objs:
    me=ob.data; me.materials.clear(); me.materials.append(F)
    for p in me.polygons: p.material_index=0
    me.uv_layers.remove(me.uv_layers['UVMap']) if 'UVMap' in me.uv_layers else None
    me.uv_layers['atlas'].active=True; me.uv_layers['atlas'].active_render=True
# keep tip/nock/embed empties as children; export
bpy.ops.wm.save_as_mainfile(filepath='/workspace/arrows_v2/arrows_kit.blend')
def export(path,names):
    bpy.ops.object.select_all(action='DESELECT')
    for nme in names:
        ob=bpy.data.objects[nme]; ob.select_set(True)
        for ch in ob.children: ch.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_animations=False,export_image_format='JPEG',export_jpeg_quality=88,export_extras=False)
export(f'{OUT}/arrows_kit.glb',EXP)
for nme in EXP: export(f'{OUT}/{nme}.glb',[nme])
import json
info={nme:{'tris':sum(len(p.vertices)-2 for p in bpy.data.objects[nme].data.polygons),'dims_m':[round(x,3) for x in bpy.data.objects[nme].dimensions]} for nme in EXP}
json.dump(info,open(f'{OUT}/arrows_info.json','w'),indent=1); print('KITOK',info)
