import bpy,bmesh,math,random
from mathutils import Vector,Matrix
random.seed(11)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; T='/workspace/fxs/out/textures/'
M=bpy.data.materials.new('fx_ice'); M.use_nodes=True; nt=M.node_tree; b=nt.nodes['Principled BSDF']
def tex(n,non=True):
    t=nt.nodes.new('ShaderNodeTexImage'); t.image=bpy.data.images.load(T+n+'.png')
    if non: t.image.colorspace_settings.name='Non-Color'
    return t
c=tex('ice_bc',False); n=tex('ice_n'); o=tex('ice_orm')
nt.links.new(c.outputs[0],b.inputs['Base Color'])
sp=nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(o.outputs[0],sp.inputs[0]); nt.links.new(sp.outputs[1],b.inputs['Roughness']); nt.links.new(sp.outputs[2],b.inputs['Metallic'])
nm=nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(n.outputs[0],nm.inputs['Color']); nt.links.new(nm.outputs[0],b.inputs['Normal'])
b.inputs['Emission Color'].default_value=(0.35,0.6,0.9,1); b.inputs['Emission Strength'].default_value=0.12
def shard(name,length,rad,sides,tilt,seed):
    random.seed(seed); bm=bmesh.new()
    angs=sorted(random.uniform(0,2*math.pi) for _ in range(sides)) if sides>4 else [i*2*math.pi/sides+random.uniform(-0.3,0.3) for i in range(sides)]
    rs=[rad*random.uniform(0.7,1.15) for _ in angs]
    base=[bm.verts.new((r*math.cos(a),r*math.sin(a),-0.02*length)) for a,r in zip(angs,rs)]
    mid_h=length*random.uniform(0.55,0.75)
    mid=[bm.verts.new((r*0.85*math.cos(a),r*0.85*math.sin(a),mid_h*random.uniform(0.85,1.1))) for a,r in zip(angs,rs)]
    tip=bm.verts.new((random.uniform(-0.25,0.25)*rad,random.uniform(-0.25,0.25)*rad,length))
    k=len(base)
    for i in range(k):
        j=(i+1)%k; bm.faces.new((base[i],base[j],mid[j],mid[i])); bm.faces.new((mid[i],mid[j],tip))
    bm.faces.new(list(reversed(base)))
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name,me); sc.collection.objects.link(ob); me.materials.append(M)
    ob.rotation_euler=(tilt[0],tilt[1],random.uniform(0,6.28))
    return ob
specs=[(0.32,0.045,6),(0.24,0.04,5),(0.18,0.03,6),(0.14,0.028,4),(0.11,0.022,5),(0.36,0.05,7),(0.08,0.018,4),(0.21,0.035,5)]
objs=[]
for i,(L,r,s) in enumerate(specs):
    objs.append(shard(f'ice_shard_{i+1:02d}',L,r,s,(random.uniform(-0.15,0.15),random.uniform(-0.15,0.15)),100+i))
# cluster: 5 shards fanned out on a base
parts=[]
for i,(L,r,s,ax,ay) in enumerate([(0.30,0.045,6,0,0),(0.2,0.035,5,0.5,0.1),(0.17,0.03,5,-0.45,0.25),(0.13,0.025,4,0.15,-0.55),(0.1,0.02,5,-0.2,-0.5)]):
    p=shard(f'cl{i}',L,r,s,(ax,ay),200+i); p.location=(math.sin(ay)*0.03,-math.sin(ax)*0.03,0); parts.append(p)
bpy.ops.object.select_all(action='DESELECT')
for p in parts: p.select_set(True)
bpy.context.view_layer.objects.active=parts[0]; bpy.ops.object.join(); parts[0].name='ice_cluster_a'; parts[0].data.name='ice_cluster_a'; objs.append(parts[0])
for ob in objs:
    bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active=ob
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.cube_project(cube_size=0.25); bpy.ops.object.mode_set(mode='OBJECT')
    for f in ob.data.polygons: f.use_smooth=False
for i,ob in enumerate(objs): ob.location=(0,0,0)
import json
info={ob.name:{'tris':sum(len(p.vertices)-2 for p in ob.data.polygons),'height_m':round(ob.dimensions.z,3)} for ob in objs}
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath='/workspace/fxs/out/ice_shards.glb',export_format='GLB',use_selection=True,export_image_format='JPEG',export_jpeg_quality=90,export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath='/workspace/fxs/out/ice_shards.blend')
json.dump(info,open('/workspace/fxs/out/ice_shards_info.json','w'),indent=1); print('SHOK',info)
