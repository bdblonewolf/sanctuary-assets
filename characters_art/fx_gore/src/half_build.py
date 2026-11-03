# blender -b X_dismember.blend --python half_build.py -- outdir name
import bpy, sys, math, json, os
from mathutils import Vector, Matrix, Quaternion, Euler
OUT,N=sys.argv[sys.argv.index('--')+1:]
K=[o for o in bpy.data.objects if o.type=='ARMATURE'][0]
keep={f'{N}_upper_torso',f'{N}_arm_l',f'{N}_arm_r',f'{N}_head',f'{N}_sevcap_waist'}
for o in list(bpy.data.objects):
    if o.type=='MESH' and o.name not in keep: bpy.data.objects.remove(o,do_unlink=True)
bpy.data.objects[f'{N}_sevcap_waist'].name=f'{N}_cap_waist_half'
if K.animation_data:
    for t in list(K.animation_data.nla_tracks): K.animation_data.nla_tracks.remove(t)
    K.animation_data.action=None
for a in list(bpy.data.actions): bpy.data.actions.remove(a)
M='mixamorig:'; B=lambda n:K.data.bones[M+n]; P=lambda n:K.pose.bones[M+n]
for pb in K.pose.bones: pb.rotation_mode='QUATERNION'; pb.matrix_basis.identity()
sc=bpy.context.scene; sc.render.fps=30
def H(n): return B(n).head_local.copy()
def about(pt,R): return Matrix.Translation(pt)@R.to_4x4()@Matrix.Translation(-pt)
def Rx(a): return Matrix.Rotation(math.radians(a),3,'X')
def Ry(a): return Matrix.Rotation(math.radians(a),3,'Y')
def Rz(a): return Matrix.Rotation(math.radians(a),3,'Z')
def eul(x=0,y=0,z=0): return Rz(z)@Ry(y)@Rx(x)
waist=H('Spine1')
SIDES={'l':'Left','r':'Right'}
L1={s:(H(f'{S}ForeArm')-H(f'{S}Arm')).length for s,S in SIDES.items()}
L2={s:(H(f'{S}Hand')-H(f'{S}ForeArm')).length for s,S in SIDES.items()}
def frame(d,n):
    d=d.normalized(); n=(n-d*n.dot(d)).normalized(); return Matrix((d,n,d.cross(n))).transposed()
def solve(S,T,l1,l2,pole):
    v=T-S; dist=min(v.length,(l1+l2)*0.985); dist=max(dist,abs(l1-l2)+0.02); d=v.normalized(); T=S+d*dist
    a=(l1*l1-l2*l2+dist*dist)/(2*dist); h=math.sqrt(max(l1*l1-a*a,1e-6))
    pp=(pole-d*pole.dot(d)).normalized(); return S+d*a+pp*h, T
setm={}
def put(name,Mw):
    setm[name]=Mw
def pose(p):
    """p: dict with P (waist world pos), yaw, roll, lean, spine2/neck/head (x,y,z) extras, arms: dict side->(target, pole, palm_weight, shrug)"""
    G=Matrix.Translation(p['P'])@(Rz(p.get('yaw',0))@Ry(p.get('roll',0))@Rx(90-p.get('lean',12))).to_4x4()@Matrix.Translation(-waist)
    W={}
    W['Hips']=G; W['Spine']=G
    W['Spine1']=G@about(H('Spine1'),eul(*p.get('sp1',(0,0,0))))
    W['Spine2']=W['Spine1']@about(H('Spine2'),eul(*p.get('sp2',(0,0,0))))
    W['Neck']=W['Spine2']@about(H('Neck'),eul(*p.get('neck',(0,0,0))))
    W['Head']=W['Neck']@about(H('Head'),eul(*p.get('head',(0,0,0))))
    for n in ['Hips','Spine','Spine1','Spine2','Neck','Head']: put(n,W[n]@B(n).matrix_local)
    for s,S in SIDES.items():
        tgt,pole,pw,shrug=p['arms'][s]
        sh=W['Spine2']@about(H(f'{S}Shoulder'),eul(*shrug)); put(f'{S}Shoulder',sh@B(f'{S}Shoulder').matrix_local)
        S0,E0,W0=H(f'{S}Arm'),H(f'{S}ForeArm'),H(f'{S}Hand')
        Sw=sh@S0; E1,T1=solve(Sw,tgt,L1[s],L2[s],pole)
        R3=sh.to_3x3()
        n0=R3@(W0-S0).cross(E0-S0); n1=(T1-Sw).cross(E1-Sw)
        Ru=frame(E1-Sw,n1)@frame(R3@(E0-S0),n0).inverted()
        Wu=Matrix.Translation(Sw)@Ru.to_4x4()@Matrix.Translation(-S0)@Matrix(((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)))
        Wu=Matrix.Translation(Sw)@(Ru@R3).to_4x4()@Matrix.Translation(-S0)
        put(f'{S}Arm',Wu@B(f'{S}Arm').matrix_local)
        Rf=frame(T1-E1,n1)@frame(Ru@R3@(W0-E0),n0).inverted()
        Wf=Matrix.Translation(E1)@(Rf@Ru@R3).to_4x4()@Matrix.Translation(-E0)
        put(f'{S}ForeArm',Wf@B(f'{S}ForeArm').matrix_local)
        # hand: blend between follow forearm and palm-down flat
        I0,P0=H(f'{S}HandIndex1'),H(f'{S}HandPinky1'); hd0=(H(f'{S}HandMiddle1')-W0)
        R4=Wf.to_3x3(); sgn=-1 if s=='l' else 1
        palm0=(R4@(I0-P0)).cross(R4@hd0)*sgn
        fwd=(T1-E1); fwd.z=0
        if fwd.length<1e-4: fwd=Vector((0,-1,0))
        fwd=fwd.normalized(); fwd.z=-0.25
        Rflat=frame(fwd,Vector((0,0,-1)))@frame(R4@hd0,palm0).inverted()
        qa=Quaternion(); qb=Rflat.to_quaternion(); Rh=qa.slerp(qb,pw).to_matrix()@eul(*p.get('wrist_'+s,(0,0,0)))
        Wh=Matrix.Translation(T1)@(Rh@R4).to_4x4()@Matrix.Translation(-W0)
        put(f'{S}Hand',Wh@B(f'{S}Hand').matrix_local)
        # fingers: claw curl about their own local X (mixamo curl axis)
        for b in K.data.bones:
            if b.name.startswith(M+f'{S}Hand') and b.name!=M+f'{S}Hand':
                setm[b.name[len(M):]]=('curl',p.get('curl',25))
ORDER=['Hips','Spine','Spine1','Spine2','Neck','Head','LeftShoulder','LeftArm','LeftForeArm','LeftHand','RightShoulder','RightArm','RightForeArm','RightHand']
prevq={}
def key(f):
    for n in ORDER:
        pb=P(n); pb.matrix=setm[n]; bpy.context.view_layer.update()
    for b,v in setm.items():
        if isinstance(v,tuple): 
            pb=P(b); 
            if 'Thumb' in b: pb.rotation_quaternion=Euler((0,0,math.radians(v[1]*0.3*(1 if 'Left' in b else -1)))).to_quaternion()
            else: pb.rotation_quaternion=Euler((math.radians(v[1]),0,0)).to_quaternion()
    for pb in K.pose.bones:
        q=pb.rotation_quaternion.copy()
        if pb.name in prevq and prevq[pb.name].dot(q)<0: q.negate(); pb.rotation_quaternion=q
        prevq[pb.name]=q.copy()
        pb.keyframe_insert('rotation_quaternion',frame=f)
        if pb.name in (M+'Hips',): pb.keyframe_insert('location',frame=f)
# rest heights / geometry
shy=Vector((0,0,0))
def lerp(a,b,t): return a+(b-a)*t
def smooth(t): t=max(0,min(1,t)); return t*t*(3-2*t)
def ss(f,a,b): return smooth((f-a)/(b-a))
ARMLEN=(L1['l']+L2['l'])
SW=abs(H('LeftArm').x)
GROUND=0.045
def base(f=0):
    return dict(P=Vector((0,0.0,0.16)),lean=14,sp1=(-4,0,0),sp2=(-6,0,0),neck=(-14,0,0),head=(-16,0,0),curl=30)
def shoulder_world(p,s):
    G=Matrix.Translation(p['P'])@(Rz(p.get('yaw',0))@Ry(p.get('roll',0))@Rx(90-p.get('lean',12))).to_4x4()@Matrix.Translation(-waist)
    return G@H(SIDES[s]+'Arm')
def pole(s,up=0.6): return Vector(((1 if s=='l' else -1)*0.8,0.35,up))
clips={}
def make(name,nf,fn,loop):
    act=bpy.data.actions.new(name); K.animation_data_create(); K.animation_data.action=act
    prevq.clear()
    for f in range(nf+1 if not loop else nf+1):
        p=fn(f%nf if loop else f); pose(p); key(f)
    tr=K.animation_data.nla_tracks.new(); tr.name=name; st=tr.strips.new(name,0,act); K.animation_data.action=None
    clips[name]={'frames':nf+1 if not loop else nf,'fps':30,'loop':loop}
    return act
# ---------- crawl: 60f loop, left arm reaches at 0, right at 30 ----------
REACH=-0.50*ARMLEN/0.55; BACK=-0.06
def arm_cycle(ph):   # ph 0..1 ; stance 0..0.65 planted sliding back; swing 0.65..1 lifted forward
    if ph<0.65:
        t=ph/0.65; y=lerp(REACH,BACK,t); z=GROUND; pw=1.0
    else:
        t=(ph-0.65)/0.35; y=lerp(BACK,REACH,smooth(t)); z=GROUND+0.13*math.sin(math.pi*t); pw=1-0.6*math.sin(math.pi*t)
    return y,z,pw,t
def crawl(f):
    p=base(); ph=f/60.0
    pull=math.sin(2*math.pi*ph)  # + when left pulling
    p['roll']=5*pull; p['yaw']=4*pull; p['P']=Vector((0.01*pull,0.0,0.16+0.012*abs(math.cos(2*math.pi*ph))))
    p['head']=(-18+3*math.sin(4*math.pi*ph),5*pull,-6*pull); p['neck']=(-12,0,-3*pull)
    p['arms']={}
    for s,off in (('l',0.0),('r',0.5)):
        y,z,pw,t=arm_cycle((ph+off)%1.0); sx=1 if s=='l' else -1
        S=shoulder_world(p,s)
        p['arms'][s]=(Vector((sx*(SW+0.07),S.y+y,z)),pole(s),pw,(0,(-6 if s=='l' else 6)*(y-BACK)/(REACH-BACK),0))
    return p
make('crawl',60,crawl,True)
# ---------- idle_half: 60f loop ----------
def idle(f):
    p=base(); ph=f/60.0; b=math.sin(2*math.pi*ph)
    p['P']=Vector((0,0,0.16+0.008*b)); p['lean']=14+1.5*b; p['sp2']=(-6-2*b,0,0)
    p['head']=(-16+4*math.sin(2*math.pi*ph+1),8*math.sin(2*math.pi*ph*1),-10*math.sin(2*math.pi*ph+0.5)); p['roll']=1.5*math.sin(2*math.pi*ph)
    p['arms']={}
    for s in 'lr':
        sx=1 if s=='l' else -1; S=shoulder_world(p,s)
        p['arms'][s]=(Vector((sx*(SW+0.08),S.y-0.30,GROUND)),pole(s),1.0,(0,0,0))
    p['curl']=30+8*math.sin(2*math.pi*ph*2)
    return p
make('idle_half',60,idle,True)
# ---------- crawl_swipe: 40f, right arm swipe, impact f18 ----------
def swipe(f):
    p=base(); p['arms']={}
    w=ss(f,0,13)*(1-ss(f,24,38))     # windup/raise weight
    p['lean']=14+14*w; p['P']=Vector((0,0,0.16+0.05*w)); p['roll']=-8*w+14*ss(f,13,19)*(1-ss(f,24,38))
    yawv=(-14*ss(f,0,13)+30*ss(f,13,19))*(1-ss(f,24,38)); p['yaw']=yawv
    p['head']=(-24*w-8,0,yawv*0.4); p['neck']=(-14,0,0); p['sp2']=(-6-6*w,0,yawv*0.3)
    # left arm stays planted
    S=shoulder_world(p,'l'); p['arms']['l']=(Vector((SW+0.10,-0.30,GROUND)),pole('l'),1.0,(0,0,0))
    Sr=shoulder_world(p,'r')
    k0=Vector((-(SW+0.08),-0.30,GROUND))
    k1=Vector((-(SW+0.32),Sr.y+0.02,Sr.z+0.22))     # windup: back, out, high
    k2=Vector((-0.10,Sr.y-0.50,0.18))              # mid swipe front
    k3=Vector((0.22,Sr.y-0.32,0.07))               # through, near ground left-front
    if f<=13: t=smooth(f/13); T=k0.lerp(k1,t); pw=1-t
    elif f<=19:
        t=(f-13)/6; t=t*t*(3-2*t)
        a=k1.lerp(k2,t); b=k2.lerp(k3,t); T=a.lerp(b,t); pw=0
    elif f<=26: T=k3; pw=0.3*ss(f,19,26)
    else: t=ss(f,26,38); T=k3.lerp(k0,t); T.z+=0.08*math.sin(math.pi*t); pw=0.3+0.7*t
    p['arms']['r']=(T,Vector((-0.7,0.5,0.6)),pw,(0,14*w,0))
    p['curl']=30+25*ss(f,13,17)*(1-ss(f,22,30))
    return p
make('crawl_swipe',40,swipe,False)
# ---------- hit_half: 20f ----------
def hit(f):
    p=base(); j=math.sin(math.pi*min(1,f/6.0))*(1-ss(f,6,19))+ (1-ss(f,6,19))*0.0
    k=ss(f,0,3)*(1-ss(f,4,19))
    p['P']=Vector((0,0.05*k,0.16-0.03*k)); p['lean']=14-8*k; p['head']=(-16+30*k,12*k,10*k); p['neck']=(-14+10*k,0,0); p['sp2']=(-6+8*k,0,4*k); p['roll']=6*k
    p['arms']={}
    for s in 'lr':
        sx=1 if s=='l' else -1; S=shoulder_world(base()|{'arms':{}},s)
        p['arms'][s]=(Vector((sx*(SW+0.08+0.04*k),S.y-0.30,GROUND)),pole(s),1.0,(0,0,0))
    return p
make('hit_half',20,hit,False)
# ---------- death_half: 50f: brief rear-up, collapse face down, head to side ----------
def death(f):
    p=base(); r=ss(f,0,10)*(1-ss(f,10,24)); c=ss(f,12,30)
    p['lean']=14+10*r-12*c; p['P']=Vector((0,0.03*c,0.16+0.04*r-0.07*c)); p['roll']=8*c
    p['head']=(-16-12*r+8*c,-12*ss(f,22,40),-68*ss(f,22,40)); p['neck']=(-14+10*c,0,-10*c); p['sp2']=(-6+8*c,0,0); p['sp1']=(-4+5*c,0,0)
    p['arms']={}
    for s in 'lr':
        sx=1 if s=='l' else -1; S=shoulder_world(base(),s)
        slide=ss(f,14,34)
        T=Vector((sx*(SW+0.08+0.18*slide),S.y-0.30+0.10*slide,GROUND-0.005*slide))
        p['arms'][s]=(T,pole(s,0.3+0.5*(1-slide)),1.0,(0,0,0))
    p['curl']=30-20*ss(f,30,48)
    return p
make('death_half',50,death,False)
for pb in K.pose.bones: pb.matrix_basis.identity()
for m in bpy.data.materials:
    if m.use_nodes:
        for n in m.node_tree.nodes:
            if n.type=='BSDF_PRINCIPLED': n.inputs['Specular IOR Level'].default_value=0.5; n.inputs['IOR'].default_value=1.5
sc.frame_start=0
bpy.ops.object.select_all(action='DESELECT'); K.select_set(True)
for o in bpy.data.objects:
    if o.type=='MESH': o.select_set(True)
bpy.ops.export_scene.gltf(filepath=f'{OUT}/{N}_half.glb',export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_force_sampling=True,export_morph=False)
bpy.ops.wm.save_as_mainfile(filepath=f'{OUT}/{N}_half.blend')
json.dump(clips,open(f'{OUT}/{N}_half_clips.json','w'),indent=1)
print('HALFOK',clips)
