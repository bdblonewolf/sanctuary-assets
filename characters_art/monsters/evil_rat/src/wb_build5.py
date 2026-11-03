# Generic wildlife builder. usage: blender -b --python wb_build.py -- config.json
import bpy,sys,json,math,os,mathutils,random
cfg=json.load(open(sys.argv[sys.argv.index('--')+1]))
OUT=cfg['out_dir']; os.makedirs(OUT,exist_ok=True); TEX=cfg.get('tex',1024)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
bpy.ops.import_scene.gltf(filepath=cfg['src'])
for o in list(sc.objects):
    if o.name.startswith('Icosphere'): bpy.data.objects.remove(o)
arm=[o for o in sc.objects if o.type=='ARMATURE'][0]
meshes=[o for o in sc.objects if o.type=='MESH']
for o in sc.objects: o.rotation_mode='XYZ' if o.type!='EMPTY' or True else o.rotation_mode
# rest pose
arm.animation_data_create()
for t in list(arm.animation_data.nla_tracks): arm.animation_data.nla_tracks.remove(t)
arm.animation_data.action=None
for pb in arm.pose.bones: pb.location=(0,0,0); pb.rotation_quaternion=(1,0,0,0); pb.rotation_euler=(0,0,0); pb.scale=(1,1,1)
bpy.context.view_layer.update()
# bone-parented rigid meshes -> skinned to that bone
for o in meshes:
    if o.parent==arm and o.parent_type=='BONE':
        mw=o.matrix_world.copy(); bn=o.parent_bone; o.parent=None; o.parent=arm; o.parent_type='OBJECT'; o.matrix_parent_inverse.identity(); o.matrix_world=mw
        o.vertex_groups.new(name=bn).add(list(range(len(o.data.vertices))),1.0,'REPLACE')
        md=o.modifiers.new('Armature','ARMATURE'); md.object=arm
        if cfg.get('rigid_mat',{}).get(o.name):
            nm=bpy.data.materials.new(cfg['rigid_mat'][o.name]); o.data.materials.clear(); o.data.materials.append(nm)
        print('RIGID',o.name,'->',bn)
bpy.context.view_layer.update()
# unparent from RootNode keeping transform
for o in [arm]+meshes:
    if o.parent and o.parent.type=='EMPTY':
        mw=o.matrix_world.copy(); o.parent=None; o.matrix_world=mw
for o in list(sc.objects):
    if o.type=='EMPTY': bpy.data.objects.remove(o)
bpy.context.view_layer.update()
# measure rest height
def wpts(objs):
    dg=bpy.context.evaluated_depsgraph_get(); P=[]
    for o in objs:
        e=o.evaluated_get(dg); m=e.to_mesh(); P+=[e.matrix_world@v.co for v in m.vertices]; e.to_mesh_clear()
    return P
P=wpts(meshes); H0=max(p.z for p in P)-min(p.z for p in P)
k=cfg['height']/H0
old_scale=arm.matrix_world.to_scale()[0]
print('H0',H0,'k',k,'armscale',old_scale)
# scale arm about origin
arm.matrix_world=mathutils.Matrix.Scale(k,4)@arm.matrix_world
bpy.context.view_layer.update()
# apply transforms to arm and meshes
bpy.ops.object.select_all(action='DESELECT')
for o in [arm]+meshes: o.select_set(True)
bpy.context.view_layer.objects.active=arm
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
locfac=old_scale*k
# floor at z=0 and centre xy
P=wpts(meshes); zmin=min(p.z for p in P)
print('after apply H',max(p.z for p in P)-zmin,'zmin',zmin)
# ---------- actions: build clips
src_actions={a.name:a for a in bpy.data.actions}
FS=30/24.0
clips={}
for cname,spec in cfg['clips'].items():
    if spec.get('src'):
        sa=src_actions[spec['src']]
        na=sa.copy(); na.name=cname
        for fc in na.fcurves:
            isloc=fc.data_path.endswith('location')
            for kp in fc.keyframe_points:
                kp.co.x*=FS*spec.get('stretch',1.0); kp.handle_left.x*=FS*spec.get('stretch',1.0); kp.handle_right.x*=FS*spec.get('stretch',1.0)
                if isloc: kp.co.y*=locfac; kp.handle_left.y*=locfac; kp.handle_right.y*=locfac
        clips[cname]=na
    elif spec.get('concat'):
        na=bpy.data.actions.new(cname); off=0.0
        for (an,s0,s1) in spec['concat']:
            sa=src_actions[an]
            for fc in sa.fcurves:
                nf=na.fcurves.find(fc.data_path,index=fc.array_index) or na.fcurves.new(fc.data_path,index=fc.array_index,action_group=fc.group.name if fc.group else '')
                isloc=fc.data_path.endswith('location')
                for f in range(s0,s1+1):
                    v=fc.evaluate(f)*(locfac if isloc else 1.0)
                    nf.keyframe_points.insert((off+f-s0)*FS,v,options={'FAST'})
            off+=s1-s0+1
        for fc in na.fcurves: fc.update()
        clips[cname]=na
for a in list(bpy.data.actions):
    if a.name not in cfg['clips']: bpy.data.actions.remove(a)
# keyframed clips via external python snippet
for cname,spec in cfg['clips'].items():
    if spec.get('key'):
        ns={'bpy':bpy,'arm':arm,'clips':clips,'math':math,'mathutils':mathutils,'cname':cname,'spec':spec}
        exec(open(spec['key']).read(),ns)
        clips[cname]=bpy.data.actions[cname]
for cn in [c for c in list(clips) if c.startswith('_')]:
    bpy.data.actions.remove(clips.pop(cn))
for a in clips.values(): a.use_fake_user=True
# ---------- shape tweaks (rest pose, weighted by vertex group)
for o in meshes:
    for tw in cfg.get('tweaks',[]):
        vg=o.vertex_groups.get(tw['group'])
        if not vg: continue
        bone=arm.data.bones[tw.get('pivot',tw['group'])]
        piv=o.matrix_world.inverted()@(arm.matrix_world@bone.head_local)
        sv=mathutils.Vector(tw['scale'])
        for v in o.data.vertices:
            w=0
            for g in v.groups:
                if g.group==vg.index: w=g.weight
            if w>0:
                d=v.co-piv; nd=mathutils.Vector((d.x*sv.x,d.y*sv.y,d.z*sv.z)); v.co=piv+d.lerp(nd,w)
if cfg.get('mod'):
    ns={'bpy':bpy,'arm':arm,'meshes':meshes,'cfg':cfg,'math':math,'mathutils':mathutils}
    exec(open(cfg['mod']).read(),ns)
# ---------- join meshes, subdivide
bpy.ops.object.select_all(action='DESELECT')
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active=meshes[0]
if len(meshes)>1: bpy.ops.object.join()
body=bpy.context.view_layer.objects.active; body.name=cfg['name']; body.data.name=cfg['name']
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=cfg.get('merge',0.0005))
if cfg.get('quads'): bpy.ops.mesh.tris_convert_to_quads(face_threshold=math.radians(60),shape_threshold=math.radians(60))
bpy.ops.object.mode_set(mode='OBJECT')
print('verts after merge',len(body.data.vertices))
for i in range(cfg.get('subdiv',1)):
    m=body.modifiers.new('sub','SUBSURF'); m.levels=1; m.render_levels=1; m.quality=2
    bpy.ops.object.modifier_move_to_index(modifier='sub',index=0)
    bpy.ops.object.modifier_apply(modifier='sub')
if cfg.get('decimate'):
    m=body.modifiers.new('dec','DECIMATE'); m.ratio=cfg['decimate']; bpy.ops.object.modifier_move_to_index(modifier='dec',index=0); bpy.ops.object.modifier_apply(modifier='dec')
if cfg.get('post_mod'):
    ns={'bpy':bpy,'arm':arm,'body':body,'cfg':cfg,'math':math,'mathutils':mathutils}
    exec(open(cfg['post_mod']).read(),ns); body=ns['body']
for p in body.data.polygons: p.use_smooth=True
body.data.calc_loop_triangles(); TRIS=len(body.data.loop_triangles); print('TRIS',TRIS)
# UV
while body.data.uv_layers: body.data.uv_layers.remove(body.data.uv_layers[0])
body.data.uv_layers.new(name='UVMap')
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(60),island_margin=0.004)
bpy.ops.object.mode_set(mode='OBJECT')
# ---------- procedural bake materials
exec(open(cfg['shader']).read())   # defines build_proc(mat_role, coat) -> material
slot_roles=[cfg['roles'].get(s.material.name if s.material else '', 'fur') for s in body.material_slots]
print('roles',[(s.material.name if s.material else None) for s in body.material_slots],slot_roles)
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=cfg.get('bake_samples',8)
sc.render.bake.margin=8
def bake_set(coat):
    imgs={}
    for kind in ['color','rough','emit','normal']:
        imgs[kind]=bpy.data.images.new(f"{cfg['name']}_{coat}_{kind}",TEX,TEX,alpha=False,float_buffer=False)
        if kind!='color' and kind!='emit': imgs[kind].colorspace_settings.name='Non-Color'
    pmats=[build_proc(r,coat,cfg) for r in slot_roles]
    for i,s in enumerate(body.material_slots): s.material=pmats[i]
    def run(kind,btype,**kw):
        for m in pmats:
            nt=m.node_tree
            for n in nt.nodes:
                if n.type=='TEX_IMAGE' and n.name=='BAKE': nt.nodes.remove(n)
            n=nt.nodes.new('ShaderNodeTexImage'); n.name='BAKE'; n.image=imgs[kind]; nt.nodes.active=n; n.select=True
        bpy.ops.object.select_all(action='DESELECT'); body.select_set(True); bpy.context.view_layer.objects.active=body
        bpy.ops.object.bake(type=btype,**kw)
    run('color','DIFFUSE',pass_filter={'COLOR'})
    run('rough','ROUGHNESS')
    run('emit','EMIT')
    run('normal','NORMAL',normal_space='TANGENT')
    for kk,im in imgs.items():
        im.filepath_raw=os.path.join(OUT,'tex',im.name+'.png'); os.makedirs(os.path.dirname(im.filepath_raw),exist_ok=True); im.file_format='PNG'; im.save()
    return imgs,pmats
arm.data.pose_position='REST'
coats=cfg['coats']
baked={}
shared=None
for ci,coat in enumerate(coats):
    imgs,pm=bake_set(coat)
    baked[coat]=imgs
arm.data.pose_position='POSE'
def final_mat(coat):
    imgs=baked[coat]
    m=bpy.data.materials.new(f"{cfg['name']}_{coat}"); m.use_nodes=True; nt=m.node_tree; p=nt.nodes['Principled BSDF']
    def tex(im,loc):
        n=nt.nodes.new('ShaderNodeTexImage'); n.image=im; n.location=loc; return n
    c=tex(imgs['color'],(-600,300)); nt.links.new(c.outputs[0],p.inputs['Base Color'])
    r=tex(imgs['rough'],(-600,0)); nt.links.new(r.outputs[0],p.inputs['Roughness'])
    e=tex(imgs['emit'],(-600,-300)); nt.links.new(e.outputs[0],p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value=1.0
    nm=nt.nodes.new('ShaderNodeNormalMap'); n=tex(imgs['normal'],(-900,-600)); nt.links.new(n.outputs[0],nm.inputs['Color']); nt.links.new(nm.outputs[0],p.inputs['Normal'])
    p.inputs['Metallic'].default_value=0.0; m.use_backface_culling=True
    return m
# collapse to one material slot
bpy.context.view_layer.objects.active=body
for p_ in body.data.polygons: p_.material_index=0
while len(body.material_slots)>1:
    body.active_material_index=len(body.material_slots)-1; bpy.ops.object.material_slot_remove()
sc.render.fps=30
# --------- metrics
def bone_w(name,tail=False):
    b=arm.pose.bones[name]; return arm.matrix_world@(b.tail if tail else b.head)
metrics={'tris':TRIS,'clips':{}}
arm.animation_data.action=None
P=wpts([body]); metrics['height']=max(p.z for p in P)-min(p.z for p in P); metrics['length']=max(p.y for p in P)-min(p.y for p in P)
FWD=cfg.get('fwd_axis',-1)  # -Y forward
for cname,a in clips.items():
    arm.animation_data.action=a
    f0,f1=[int(round(x)) for x in a.frame_range]
    info={'frames':f1-f0+1,'range':[f0,f1]}
    hd=[];feet={}
    for f in range(f0,f1+1):
        sc.frame_set(f)
        h=bone_w(cfg['head_bone'],True); hd.append((f,h.y*FWD,h.z))
        for fb in cfg['feet']:
            feet.setdefault(fb,[]).append(bone_w(fb,True).y*FWD)
    if cname in cfg.get('impact_clips',[]):
        imin=cfg.get('impact_min',{}).get(cname,-999); imax=cfg.get('impact_max',{}).get(cname,9999); hd=[t for t in hd if t[0]<=imax]; info['impact']=max([t for t in hd if t[0]>=imin],key=lambda t:t[1])[0]
    if cname in cfg.get('land_clips',[]):
        fb=cfg['feet'][0]; zs=[]
        for f in range(f0,f1+1):
            sc.frame_set(f); zs.append((f,bone_w(fb,True).z))
        pk=max(zs,key=lambda t:t[1])[0]
        info['impact']=next((f for f,z in zs if f>pk and z<cfg.get('ground_eps',0.05)),pk)
    if cname in ('walk','run'):
        T=(f1-f0)/30.0
        rng=[max(v)-min(v) for v in feet.values()]
        info['speed']=round(sum(rng)/len(rng)/T,2)
    metrics['clips'][cname]=info
arm.animation_data.action=clips['idle']; sc.frame_set(0)
json.dump(metrics,open(os.path.join(OUT,'metrics.json'),'w'),indent=1)
print('METRICS',json.dumps(metrics))
# --------- export per coat
for coat in coats:
    mat=final_mat(coat); body.material_slots[0].material=mat
    for m in list(bpy.data.materials):
        if m.users==0: bpy.data.materials.remove(m)
    fn=os.path.join(OUT,cfg['file_pattern'].format(coat=coat))
    bpy.ops.object.select_all(action='DESELECT'); arm.select_set(True); body.select_set(True)
    bpy.ops.export_scene.gltf(filepath=fn,export_format='GLB',use_selection=True,export_animations=True,
        export_animation_mode='ACTIONS',export_force_sampling=True,export_frame_range=False,export_anim_slide_to_zero=True,
        export_def_bones=True,export_image_format='WEBP' if cfg.get('webp') else 'AUTO',export_jpeg_quality=88,export_apply=False,export_yup=True,export_skins=True,export_morph=False)
    print('EXPORTED',fn,os.path.getsize(fn))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,cfg['name']+'_work.blend'))
