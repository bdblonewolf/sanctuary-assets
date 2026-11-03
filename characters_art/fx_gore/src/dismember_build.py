# blender -b --python dismember_build.py -- in.glb outdir name
import bpy, bmesh, sys, os, json, math, random
from mathutils import Vector, Matrix, noise
A=sys.argv[sys.argv.index('--')+1:]; SRC,OUT,NAME=A
os.makedirs(OUT,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
for o in list(bpy.data.objects):
    if o.name.startswith('Icosphere'): bpy.data.objects.remove(o,do_unlink=True)
K=[o for o in bpy.data.objects if o.type=='ARMATURE'][0]
for o in bpy.data.objects: o.rotation_mode='XYZ' if o.type!='ARMATURE' else o.rotation_mode
# rest pose for measuring
if K.animation_data:
    keep_act=K.animation_data.action; K.animation_data.action=None
    for t in K.animation_data.nla_tracks: t.mute=True
for pb in K.pose.bones: pb.matrix_basis.identity()
bpy.context.view_layer.update()
M='mixamorig:'
def sub(root):
    b=K.data.bones.get(M+root); out=[]
    if not b: return out
    st=[b]
    while st:
        x=st.pop(); out.append(x.name); st+=list(x.children)
    return out
PART_ROOT={'head':'Neck','arm_l':'LeftArm','arm_r':'RightArm','leg_l':'LeftUpLeg','leg_r':'RightUpLeg','upper_torso':'Spine1'}
bone2part={}
for p in ['upper_torso','head','arm_l','arm_r','leg_l','leg_r']:   # order: children override
    for bn in sub(PART_ROOT[p]): bone2part[bn]=p
for b in K.data.bones:
    if b.name not in bone2part: bone2part[b.name]='lower_body'
PARTS=['head','arm_l','arm_r','upper_torso','lower_body','leg_l','leg_r']
# cuts: (part, neighbour part, stump-side bone, severed-side bone)
CUTS={'head':('upper_torso',M+'Spine2',M+'Neck'),'arm_l':('upper_torso',M+'LeftShoulder',M+'LeftArm'),'arm_r':('upper_torso',M+'RightShoulder',M+'RightArm'),
      'leg_l':('lower_body',M+'Hips',M+'LeftUpLeg'),'leg_r':('lower_body',M+'Hips',M+'RightUpLeg'),'waist':('lower_body',M+'Spine',M+'Spine1')}
CAPKIND={'head':'gore_cap_neck','arm_l':'gore_cap_limb_a','arm_r':'gore_cap_limb_b','leg_l':'gore_cap_limb_c','leg_r':'gore_cap_limb_a','waist':'gore_cap_waist'}
SEVKIND={'head':'gore_sev_b','arm_l':'gore_sev_a','arm_r':'gore_sev_b','leg_l':'gore_sev_a','leg_r':'gore_sev_b','waist':'gore_cap_waist'}
meshes=[o for o in bpy.data.objects if o.type=='MESH']
random.seed(3)
def vpart(o,v):
    sc={}
    for g in v.groups:
        bn=o.vertex_groups[g.group].name
        if bn in bone2part: sc[bone2part[bn]]=sc.get(bn and bone2part[bn],0)+g.weight
    if not sc: return 'lower_body'
    co=o.matrix_world@v.co
    nz=noise.noise(co*18.0)*0.22+noise.noise(co*45.0)*0.1
    best=max(sc,key=lambda p:sc[p]+(nz if p in ('head','arm_l','arm_r','leg_l','leg_r') else -nz))
    return best
info={'name':NAME,'source':os.path.basename(SRC),'parts':{},'cuts':{}}
boundary={k:[] for k in CUTS}
pieces={p:[] for p in PARTS}
for o in meshes:
    me=o.data; vp=[vpart(o,v) for v in me.vertices]
    fp=[]
    for f in me.polygons:
        c={}
        for vi in f.vertices: c[vp[vi]]=c.get(vp[vi],0)+1
        fp.append(max(sorted(c),key=lambda p:c[p]))
    # boundary verts: vertices used by faces of two parts
    vf={}
    for f,p in zip(me.polygons,fp):
        for vi in f.vertices: vf.setdefault(vi,set()).add(p)
    for vi,s in vf.items():
        if len(s)<2: continue
        for k,(nb,_,_) in CUTS.items():
            part=k if k!='waist' else 'upper_torso'
            if part in s and nb in s: boundary[k].append(o.matrix_world@me.vertices[vi].co)
    for p in PARTS:
        idx=[i for i,x in enumerate(fp) if x==p]
        if not idx: continue
        d=o.copy(); d.data=me.copy(); bpy.context.scene.collection.objects.link(d)
        bm=bmesh.new(); bm.from_mesh(d.data); bm.faces.ensure_lookup_table()
        keep=set(idx); bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.index not in keep],context='FACES')
        bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
        bm.to_mesh(d.data); bm.free(); pieces[p].append(d)
    bpy.data.objects.remove(o,do_unlink=True)
partobj={}
for p in PARTS:
    if not pieces[p]: continue
    bpy.ops.object.select_all(action='DESELECT')
    for d in pieces[p]: d.select_set(True)
    bpy.context.view_layer.objects.active=pieces[p][0]
    if len(pieces[p])>1: bpy.ops.object.join()
    ob=bpy.context.view_layer.objects.active; ob.name=f'{NAME}_{p}'; ob.data.name=ob.name
    ob.data.calc_loop_triangles(); partobj[p]=ob
    info['parts'][ob.name]={'part':p,'follows_bone':M+PART_ROOT.get(p,'Hips') if p!='lower_body' else M+'Hips','tris':len(ob.data.loop_triangles),'materials':[m.name for m in ob.data.materials]}
# gore caps (append from kit)
with bpy.data.libraries.load('/workspace/dmg/gore/gore_kit.blend') as (src,dst): dst.objects=[n for n in src.objects if n.startswith('gore_')]
kit={o.name:o for o in dst.objects}
def bone_dir(bn):
    b=K.data.bones[bn]; ch=[c for c in b.children if c.name.startswith(M)]
    t=(ch[0].head_local if ch else b.tail_local)
    if bn==M+'Neck': t=K.data.bones[M+'Head'].head_local
    if bn==M+'Spine1': t=K.data.bones[M+'Spine2'].head_local
    return (K.matrix_world.to_3x3()@(t-b.head_local)).normalized()
def place_cap(kind,name,loc,nrm,radius,bone):
    c=kit[kind].copy(); c.data=kit[kind].data.copy(); c.name=name; c.data.name=name; bpy.context.scene.collection.objects.link(c)
    q=Vector((0,0,1)).rotation_difference(nrm); s=radius/0.05*1.08
    c.matrix_world=Matrix.Translation(loc)@q.to_matrix().to_4x4()@Matrix.Diagonal((s,s,s,1))
    bpy.context.view_layer.objects.active=c; bpy.ops.object.select_all(action='DESELECT'); c.select_set(True)
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    vg=c.vertex_groups.new(name=bone); vg.add(list(range(len(c.data.vertices))),1.0,'REPLACE')
    c.parent=K; md=c.modifiers.new('Armature','ARMATURE'); md.object=K
    c.data.calc_loop_triangles(); return c
caps=[]
for k,(nb,stump_b,sev_b) in CUTS.items():
    pts=boundary[k]
    if len(pts)<3: print('NO BOUNDARY',k); continue
    ctr=sum(pts,Vector())/len(pts); d=bone_dir(sev_b)
    rad=sorted([((p-ctr)-d*(p-ctr).dot(d)).length for p in pts])[int(len(pts)*0.8)]
    rad=min(rad,{'head':0.075,'arm_l':0.08,'arm_r':0.08,'leg_l':0.11,'leg_r':0.11,'waist':0.17}[k])
    ctr=ctr+d*0.004
    a=place_cap(CAPKIND[k],f'{NAME}_cap_{k}',ctr,d,rad,stump_b)
    b=place_cap(SEVKIND[k],f'{NAME}_sevcap_{k}',ctr-d*0.008,-d,rad,sev_b)
    caps+=[a,b]
    info['cuts'][k]={'removed_part':k if k!='waist' else 'lower_body (half body keeps upper)','stump_cap':a.name,'stump_bone':stump_b,'severed_cap':b.name,'severed_bone':sev_b,
                     'center_bind_m':[round(x,4) for x in (ctr.x,ctr.z,-ctr.y)],'radius_m':round(rad,4),'stump_cap_tris':len(a.data.loop_triangles),'severed_cap_tris':len(b.data.loop_triangles)}
# restore animation and export
def fixmat():
    for m in bpy.data.materials:
        if m.use_nodes:
            for n in m.node_tree.nodes:
                if n.type=='BSDF_PRINCIPLED':
                    n.inputs['Specular IOR Level'].default_value=0.5; n.inputs['Specular Tint'].default_value=(1,1,1,1); n.inputs['IOR'].default_value=1.5
fixmat()
acts=[a for a in bpy.data.actions]
for a in acts:
    if a.name.endswith('_'+K.name): a.name=a.name[:-len(K.name)-1]
if K.animation_data:
    for t in list(K.animation_data.nla_tracks): K.animation_data.nla_tracks.remove(t)
    for a in acts:
        tr=K.animation_data.nla_tracks.new(); tr.name=a.name; tr.strips.new(a.name,int(a.frame_range[0]),a)
    K.animation_data.action=None
for pb in K.pose.bones: pb.matrix_basis.identity()
info['clips']=[a.name for a in acts]
def export(path,objs,anim=True):
    bpy.ops.object.select_all(action='DESELECT')
    K.select_set(True)
    for o in objs: o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_animations=anim and bool(acts),export_animation_mode='NLA_TRACKS',export_force_sampling=True,export_optimize_animation_size=True,export_morph=False,export_image_format='AUTO')
export(f'{OUT}/{NAME}_dismember.glb',list(partobj.values())+caps)
# half body mesh (upper parts + waist stump cap) saved as blend for the animation step
bpy.ops.wm.save_as_mainfile(filepath=f'{OUT}/{NAME}_dismember.blend')
# severed static pieces in bind space (engine: piece.matrix = bone.matrixWorld * skeleton.boneInverses[i])
sev=[]
for p,k in [('head','head'),('arm_l','arm_l'),('arm_r','arm_r'),('leg_l','leg_l'),('leg_r','leg_r'),('lower_body','waist')]:
    if p not in partobj: continue
    objs=[partobj[p]]+[c for c in caps if c.name==(f'{NAME}_sevcap_{k}' if k!='waist' else f'{NAME}_cap_waist')]
    if p=='lower_body': objs+= [partobj[x] for x in ('leg_l','leg_r') if x in partobj]
    ds=[]
    for o in objs:
        d=o.copy(); d.data=o.data.copy(); bpy.context.scene.collection.objects.link(d)
        d.modifiers.clear(); d.vertex_groups.clear(); d.parent=None; d.matrix_world=o.matrix_world.copy(); ds.append(d)
    bpy.ops.object.select_all(action='DESELECT')
    for d in ds: d.select_set(True)
    bpy.context.view_layer.objects.active=ds[0]; bpy.ops.object.join(); j=bpy.context.view_layer.objects.active
    j.name=f'{NAME}_sev_{p if p!="lower_body" else "legs"}'; j.data.calc_loop_triangles(); sev.append(j)
    info.setdefault('severed_pieces',{})[j.name]={'follow_bone':CUTS[k][2] if k!='waist' else M+'Hips','tris':len(j.data.loop_triangles)}
bpy.ops.object.select_all(action='DESELECT')
for s in sev: s.select_set(True)
bpy.ops.export_scene.gltf(filepath=f'{OUT}/{NAME}_severed.glb',export_format='GLB',use_selection=True,export_animations=False,export_image_format='AUTO')
json.dump(info,open(f'{OUT}/{NAME}_dismember.json','w'),indent=1)
print('INFO',json.dumps({k:v['tris'] for k,v in info['parts'].items()}))
