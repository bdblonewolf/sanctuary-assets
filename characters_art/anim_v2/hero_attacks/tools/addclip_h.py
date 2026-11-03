# usage: blender -b --python addclip.py -- in.glb out.glb recipe1.py [recipe2.py ...]
# Imports a live GLB (keeps every clip as its NLA track), adds new clips from recipes, exports NLA_TRACKS.
import bpy, sys, os, math, json, random
from mathutils import Matrix, Vector, Quaternion, Euler
A=sys.argv[sys.argv.index('--')+1:]; INP,OUT,RECIPES=A[0],A[1],A[2:]
MIX='/workspace/sanctuary/assets3d/mixamo/'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.fps=30
bpy.ops.import_scene.gltf(filepath=INP)
for o in list(bpy.data.objects):
    if o.type=='MESH' and o.name.startswith('Icosphere'): bpy.data.objects.remove(o,do_unlink=True)
arm=[o for o in bpy.data.objects if o.type=='ARMATURE'][0]
if not arm.animation_data: arm.animation_data_create()
P='mixamorig:'; H=P+'Hips'
tb=arm.data.bones; order=[b.name for b in tb]; Trest={b.name:b.matrix_local.copy() for b in tb}
kw=arm.matrix_world; kwi=kw.inverted()
for pb in arm.pose.bones: pb.rotation_mode='QUATERNION'
def depth(b):
    d=0
    while b.parent: b=b.parent; d+=1
    return d
BYDEPTH=sorted(order,key=lambda n:depth(tb[n]))
def smooth(t): t=max(0,min(1,t)); return t*t*(3-2*t)
def pw(keys,f):
    """piecewise-smooth interpolation of [[frame, v...],...]"""
    if not keys: return None
    if f<=keys[0][0]: return list(keys[0][1:])
    for a,b in zip(keys,keys[1:]):
        if f<=b[0]:
            t=smooth((f-a[0])/(b[0]-a[0])) if b[0]>a[0] else 1
            return [x+(y-x)*t for x,y in zip(a[1:],b[1:])]
    return list(keys[-1][1:])
def mute_all():
    arm.animation_data.action=None
    for t in arm.animation_data.nla_tracks: t.mute=True
def rest_pose():
    mute_all()
    for pb in arm.pose.bones: pb.rotation_quaternion=(1,0,0,0); pb.location=(0,0,0); pb.scale=(1,1,1)
    bpy.context.view_layer.update()
def live_action(name):
    for t in arm.animation_data.nla_tracks:
        if t.name==name: return t.strips[0].action
    raise KeyError(name)
def live_pose(name,f):
    """local basis of every bone from live clip `name` at frame f (0-based, clip frames start at 1)"""
    rest_pose(); act=live_action(name); arm.animation_data.action=act
    fs=act.frame_range[0]+f; sc.frame_set(int(math.floor(fs)),subframe=fs-math.floor(fs))
    out={n:(arm.pose.bones[n].rotation_quaternion.copy(),arm.pose.bones[n].location.copy()) for n in order}
    arm.animation_data.action=None; return out
def live_len(name):
    a=live_action(name); return int(round(a.frame_range[1]-a.frame_range[0]))+1
# ---------- Mixamo FBX retarget (same method as starter/_pipeline/retarget2.py) ----------
_src={}
def load_src(f):
    if f in _src: return _src[f]
    before=set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=MIX+f)
    nw=[o for o in bpy.data.objects if o not in before]; s=[o for o in nw if o.type=='ARMATURE'][0]
    for b in s.data.bones:
        if ':' in b.name and not b.name.startswith(P): b.name=P+b.name.split(':')[-1]
    for o in nw:
        if o.type!='ARMATURE': bpy.data.objects.remove(o,do_unlink=True)
    _src[f]=s; return s
def rot(m): return m.to_quaternion().normalized()
def bdir(mw,b):
    if b.children:
        c=min([c for c in b.children if c.name.startswith(P)] or list(b.children),key=lambda c:abs(c.head_local.x)); v=c.head_local-b.head_local
        if v.length>1e-6: return (mw.to_3x3()@v).normalized()
    return (mw.to_3x3()@(b.tail_local-b.head_local)).normalized()
def retarget(f,tmap,hipxy=0.0):
    """tmap: list of source frames (floats, absolute FBX frame numbers) -> list of local poses"""
    s=load_src(f); mw=s.matrix_world; rest_pose()
    O={}
    for n in order:
        if n not in s.data.bones: continue
        sb=s.data.bones[n]; Sr=rot(mw@sb.matrix_local); Tr=rot(kw@tb[n].matrix_local)
        O[n]=(bdir(mw,sb).rotation_difference(bdir(kw,tb[n]))@Sr).inverted()@Tr
    scale=(kw@tb[P+'LeftUpLeg'].head_local).z/(mw@s.data.bones[P+'LeftUpLeg'].head_local).z
    srest=mw@s.data.bones[H].head_local
    def at(fr): sc.frame_set(int(math.floor(fr)),subframe=fr-math.floor(fr))
    at(tmap[0]); p0=(mw@s.pose.bones[H].head).copy()
    poses=[]
    for fr in tmap:
        at(fr)
        Wr={n:rot(mw@s.pose.bones[n].matrix)@o for n,o in O.items()}
        hp=mw@s.pose.bones[H].head
        off=Vector(((hp.x-p0.x)*hipxy,(hp.y-p0.y)*hipxy,hp.z-srest.z))*scale
        hpos=kw@Trest[H].translation+off
        M={}; pose={}
        for n in order:
            b=tb[n]
            if b.parent is None:
                Rq=rot(kwi.to_3x3().to_4x4()@Wr[n].to_matrix().to_4x4())
                Mm=Matrix.Translation(kwi@hpos)@Rq.to_matrix().to_4x4(); basis=Trest[n].inverted()@Mm
            else:
                rel=Trest[b.parent.name].inverted()@Trest[n]; base=M[b.parent.name]@rel
                Rq=rot(kwi.to_3x3().to_4x4()@Wr[n].to_matrix().to_4x4()) if n in Wr else rot(base)
                Mm=Matrix.Translation(base.translation)@Rq.to_matrix().to_4x4()
                basis=rel.inverted()@M[b.parent.name].inverted()@Mm
            M[n]=Mm; pose[n]=(basis.to_quaternion(),basis.to_translation() if b.parent is None else Vector())
        poses.append(pose)
    return poses
def blend(pa,pb_,w):
    out={}
    for n in order:
        qa,la=pa[n]; qb,lb=pb_[n]
        if qa.dot(qb)<0: qb=-qb
        out[n]=(qa.slerp(qb,w),la.lerp(lb,w))
    return out
def concat(segs,xf=4):
    """concatenate pose lists with an xf-frame crossfade (overlap)"""
    out=list(segs[0])
    for s in segs[1:]:
        k=min(xf,len(out),len(s))
        for j in range(k):
            w=smooth((j+1)/(k+1)); out[len(out)-k+j]=blend(out[len(out)-k+j],s[j],w)
        out+=s[k:]
    return out
def fade_ends(poses,start=None,end=None,nin=4,nout=6):
    N=len(poses)
    for i in range(N):
        if start is not None and i<nin: poses[i]=blend(start,poses[i],smooth(i/nin))
        if end is not None and i>N-1-nout: poses[i]=blend(end,poses[i],smooth((N-1-i)/nout))
    return poses
# ---------- baking ----------
def apply_pose(pose):
    for n,(q,l) in pose.items():
        pb=arm.pose.bones[n]; pb.rotation_quaternion=q; pb.location=l
    bpy.context.view_layer.update()
def world_rot(bn,deg):
    pb=arm.pose.bones[P+bn]
    e=Euler([math.radians(x) for x in deg],'XYZ').to_matrix().to_4x4(); h=pb.head.copy()
    pb.matrix=Matrix.Translation(h)@e@Matrix.Translation(-h)@pb.matrix
    bpy.context.view_layer.update()
def bake(name,poses,overlay=None,cloth=None,keyloc_all=False,post=None):
    mute_all(); act=bpy.data.actions.new(name); act.use_fake_user=True; arm.animation_data.action=act
    N=len(poses); st={}
    for i,pose in enumerate(poses):
        apply_pose(pose)
        if overlay: overlay(i,N)
        if post: post(i,N)
        if cloth: cloth_step(cloth,st)
        for n in order:
            pb=arm.pose.bones[n]; pb.keyframe_insert('rotation_quaternion',frame=i+1)
            if keyloc_all or tb[n].parent is None or (cloth and n.split(':')[-1].startswith(tuple(c['name'] for c in cloth))):
                pb.keyframe_insert('location',frame=i+1)
    arm.animation_data.action=None
    tr=arm.animation_data.nla_tracks.new(); tr.name=name; s=tr.strips.new(name,1,act); tr.mute=True
    print('NEWCLIP',name,N,flush=True); return act
def overlay_from(spec):
    """spec: {'rot':{bone:[[f,x,y,z],..]}, 'hip':[[f,dx,dy,dz],..]} world-space, applied parent-first"""
    rb=sorted(spec.get('rot',{}),key=lambda n:depth(tb[P+n]))
    def ov(i,N):
        if spec.get('hip'):
            d=pw(spec['hip'],i); pb=arm.pose.bones[H]; m=pb.matrix.copy(); m.translation+=Vector(d); pb.matrix=m; bpy.context.view_layer.update()
        for bn in rb:
            v=pw(spec['rot'][bn],i)
            if v and any(abs(x)>1e-4 for x in v): world_rot(bn,v)
    return ov
def cloth_step(cloth,st):
    for c in cloth:
        pre=c['name']; L,Rr=c['side_bones']; hp=arm.pose.bones[c['hips']]; hb=tb[c['hips']]
        dl=[(arm.pose.bones[n].tail-arm.pose.bones[n].head).normalized() for n in (L,Rr)]
        Dh=hp.matrix@hb.matrix_local.inverted()
        for s,sgn in (('F',-1),('B',1)):
            bn=pre+'_'+s
            if bn not in tb: continue
            b=tb[bn]; pb=arm.pose.bones[bn]
            M0=Dh@b.matrix_local; r=(Dh.to_3x3()@(tb[L].tail_local-tb[L].head_local)).normalized()
            pick=min(dl,key=lambda d:d.y) if sgn<0 else max(dl,key=lambda d:d.y)
            avg=(dl[0]+dl[1]).normalized(); tgt=(0.65*pick+0.35*avg).normalized()
            tgt=r.lerp(tgt,c.get('follow',0.8)).normalized()
            prev=st.get(s+pre,tgt); cur=prev.lerp(tgt,c.get('damp',0.45)).normalized(); st[s+pre]=cur
            q=r.rotation_difference(cur); h=M0.translation
            pb.matrix=Matrix.Translation(h)@q.to_matrix().to_4x4()@Matrix.Translation(-h)@M0
            bpy.context.view_layer.update()
# ---------- measurement helpers ----------
def mesh_minz():
    dg=bpy.context.evaluated_depsgraph_get(); mz=1e9
    for o in bpy.data.objects:
        if o.type=='MESH' and o.parent==arm:
            e=o.evaluated_get(dg); me=e.to_mesh(); mw=o.matrix_world
            mz=min(mz,min((mw@v.co).z for v in me.vertices)); e.to_mesh_clear()
    return mz
def clip_report(name,bones=('Hips','Head','LeftHand','RightHand','LeftFoot','RightFoot')):
    mute_all(); act=live_action(name); arm.animation_data.action=act; N=live_len(name); rows=[]
    for i in range(N):
        sc.frame_set(i+1); bpy.context.view_layer.update()
        rows.append({'f':i,'minz':round(mesh_minz(),3),**{b:[round(x,3) for x in (kw@arm.pose.bones[P+b].head)] for b in bones}})
    arm.animation_data.action=None; return rows
G=dict(globals())
REPORT={}
for r in RECIPES:
    g=dict(G); g['REPORT']=REPORT; exec(open(r).read(),g)
# ---------- export ----------
KEEP=set(REPORT.get('_new_clips',[]))
for t in list(arm.animation_data.nla_tracks):
    if t.name not in KEEP: arm.animation_data.nla_tracks.remove(t)
for t in arm.animation_data.nla_tracks: t.mute=False
arm.animation_data.action=None
rest_pose()
for t in arm.animation_data.nla_tracks: t.mute=False
def _exp(path,with_mesh):
    bpy.ops.object.select_all(action='DESELECT')
    for o in bpy.data.objects:
        if o==arm or (o.parent==arm and (with_mesh or o.type=='EMPTY')): o.select_set(True)
    bpy.context.view_layer.objects.active=arm
    bpy.ops.export_scene.gltf(filepath=path,export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',
        export_force_sampling=True,export_optimize_animation_size=False,export_morph=False,export_image_format='AUTO',export_frame_range=False,export_anim_slide_to_zero=True,export_bake_animation=False,export_skins=True)
_exp(OUT,False)
_exp(OUT[:-4]+'_withmesh.glb',True)
REPORT.pop('_new_clips',None)
json.dump(REPORT,open(OUT[:-4]+'_report.json','w'),indent=1)
print('EXPORTED',OUT)
