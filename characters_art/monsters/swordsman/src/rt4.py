# usage: blender -b --python rt4.py -- model.glb out.glb cfg.json
# Retargets Mixamo X Bot FBX clips onto a mixamorig model (world-rotation transfer with bone-direction alignment;
# adapted from sanctuary_npc/monsters/swordsman/scripts/retarget.py). Exports NLA tracks, 30 fps.
import bpy, sys, json
from mathutils import Matrix, Vector
A=sys.argv[sys.argv.index('--')+1:]; MODEL,OUT,CFGP=A
CFG=json.load(open(CFGP)); R='/workspace/sanctuary/assets3d/mixamo/'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.fps=30
def imp(path,fbx=False):
    before=set(bpy.data.objects)
    if fbx: bpy.ops.import_scene.fbx(filepath=path)
    else: bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before]
knew=imp(MODEL)
for o in list(knew):
    if o.type=='MESH' and o.name.startswith('Icosphere'): bpy.data.objects.remove(o,do_unlink=True); knew.remove(o)
K=[o for o in knew if o.type=='ARMATURE'][0]
for a in list(bpy.data.actions): bpy.data.actions.remove(a)
K.animation_data_clear(); K.animation_data_create()
for pb in K.pose.bones: pb.rotation_mode='QUATERNION'
tb=K.data.bones; order=[b.name for b in tb]; Trest={b.name:b.matrix_local.copy() for b in tb}
kw=K.matrix_world; kwi=kw.inverted()
def rot(m): return m.to_quaternion().normalized()
def bdir(mw,b):
    if b.children:
        c=min(b.children,key=lambda c:abs(c.head_local.x)); v=c.head_local-b.head_local
        if v.length>1e-6: return (mw.to_3x3()@v).normalized()
    return (mw.to_3x3()@(b.tail_local-b.head_local)).normalized()
H='mixamorig:Hips'
def sample(f,mode,fstart=None,fend=None):
    """returns list of frames: each {bone: world quat (target space)}, hips offset vector; plus travel info"""
    new=imp(R+f,True); arm=[o for o in new if o.type=='ARMATURE'][0]
    a=arm.animation_data.action; mw=arm.matrix_world
    O={}
    for n in order:
        if n not in arm.data.bones: continue
        sb=arm.data.bones[n]; Sr=rot(mw@sb.matrix_local); Tr=rot(kw@tb[n].matrix_local)
        Sref=bdir(mw,sb).rotation_difference(bdir(kw,tb[n]))@Sr
        O[n]=Sref.inverted()@Tr
    sh=(mw@arm.data.bones['mixamorig:LeftUpLeg'].head_local).z; th=(kw@tb['mixamorig:LeftUpLeg'].head_local).z
    scale=th/sh; srest=mw@arm.data.bones[H].head_local
    f0,f1=map(int,a.frame_range)
    if fstart is not None: f0=f0+fstart
    if fend is not None: f1=min(f1,int(a.frame_range[0])+fend)
    sc.frame_set(f0); p0=(mw@arm.pose.bones[H].head).copy()
    sc.frame_set(f1); p1=(mw@arm.pose.bones[H].head).copy()
    N=f1-f0+1; out=[]
    for i,fi in enumerate(range(f0,f1+1)):
        sc.frame_set(fi)
        Wr={n:rot(mw@arm.pose.bones[n].matrix)@o for n,o in O.items()}
        hp=mw@arm.pose.bones[H].head
        t=i/(N-1) if N>1 else 0
        ref=p0.lerp(p1,t) if mode=='inplace' else p0
        off=Vector((hp.x-ref.x, hp.y-ref.y, hp.z-srest.z))*scale
        out.append((Wr,off))
    trav=((p1-p0)*scale); trav.z=0
    for o in new: bpy.data.objects.remove(o,do_unlink=True)
    bpy.data.actions.remove(a)
    return out,trav.length,N
def write(name,frames):
    act=bpy.data.actions.new(name); act.use_fake_user=True; K.animation_data.action=act
    for i,(Wr,off) in enumerate(frames):
        hpos=kw@Trest[H].translation+off; M={}
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
            M[n]=Mm; pb=K.pose.bones[n]
            pb.rotation_quaternion=basis.to_quaternion(); pb.keyframe_insert('rotation_quaternion',frame=i)
            if b.parent is None: pb.location=basis.to_translation(); pb.keyframe_insert('location',frame=i)
    K.animation_data.action=None; tr=K.animation_data.nla_tracks.new(); tr.name=name; tr.strips.new(name,0,act)
def blend(fa,fb,n):
    """concat fa+fb with n-frame crossfade"""
    out=fa[:-n]
    for k in range(n):
        t=(k+1)/(n+1); (wa,oa)=fa[len(fa)-n+k]; (wb,ob)=fb[k]
        out.append(({x:wa[x].slerp(wb[x],t) for x in wa},oa.lerp(ob,t)))
    return out+fb[n:]
made=[]
for name,spec in CFG['clips'].items():
    parts=spec if isinstance(spec[0],list) else [spec]
    fr=None; trav=0; srcs=[]
    for p in parts:
        f,mode=p[0],p[1]; fs=p[2] if len(p)>2 else None; fe=p[3] if len(p)>3 else None
        s,tl,N=sample(f,mode,fs,fe); srcs.append(f); trav+=tl
        fr=s if fr is None else blend(fr,s,4)
    write(name,fr)
    made.append({'name':name,'sources':srcs,'frames':len(fr),'duration_s':round((len(fr)-1)/30,3),'mode':parts[0][1],'src_travel_m':round(trav,3)})
    print('CLIP',name,len(fr),round(trav,3),flush=True)
K.animation_data.action=None
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
    if o==K or o.parent==K: o.select_set(True)
json.dump(made,open(OUT.replace('.glb','_clips.json'),'w'),indent=1)
bpy.ops.export_scene.gltf(filepath=OUT,export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_force_sampling=True,export_optimize_animation_size=False,export_morph=False,export_image_format='AUTO')
print('EXPORTED')
