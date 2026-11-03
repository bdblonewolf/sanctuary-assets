import bpy,sys,math,json,numpy as np
sys.path.insert(0,'/workspace/sanctuary_art/monsters/rigwork')
import rigcore as rc, bear_spec as bs
from rigcore import V,rot,about,T,eul,smooth,smoother,lerp,mix_mat
from curves import Keys,track
from mathutils import Matrix,Vector
OUT=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else '/workspace/sanctuary_art/monsters/rigwork/grove_mauler_bear_anim.glb'
ONLY=sys.argv[sys.argv.index('--')+2].split(',') if '--' in sys.argv and len(sys.argv)>sys.argv.index('--')+2 else None
bpy.ops.wm.open_mainfile(filepath=f'/workspace/sanctuary_art/monsters/rigwork/{bs.NAME}_rigged.blend')
ob=bpy.data.objects[bs.NAME]; ao=bpy.data.objects['rig']
rc.add_controls(ao,bs.controls())
for s in 'LR':
    rc.setup_ik(ao,f'forearm.{s}',f'ikF.{s}',f'poleF.{s}',f'fpaw.{s}')
    rc.setup_ik(ao,f'shin.{s}',f'ikH.{s}',f'poleH.{s}',f'hfoot.{s}')
EXPORT=[b.name for b in ao.data.bones if not (b.name.startswith('ik') or b.name.startswith('pole'))]
ev=rc.Evaluator(ao,EXPORT); R=ev.rest
LEGS={'LF':dict(ik='ikF.L',paw='fpaw.L',toe='ftoe.L',s=1,front=True,scap='scapula.L'),
      'RF':dict(ik='ikF.R',paw='fpaw.R',toe='ftoe.R',s=-1,front=True,scap='scapula.R'),
      'LH':dict(ik='ikH.L',paw='hfoot.L',toe='htoe.L',s=1,front=False),
      'RH':dict(ik='ikH.R',paw='hfoot.R',toe='htoe.R',s=-1,front=False)}
for k,l in LEGS.items():
    l['ball']=R[l['paw']].to_translation()+ (R[l['toe']].to_translation()-R[l['paw']].to_translation())  # toe head
    l['ball']=ao.data.bones[l['paw']].tail_local.copy(); l['wrist']=ao.data.bones[l['paw']].head_local.copy()
HIP=V(0,0.66,0.95)
def leg_world(l,d=(0,0,0),phi=0,roll=0,yaw=0,pivot='ball'):
    p=l['ball'] if pivot=='ball' else l['wrist']
    return T(d)@about(p,eul(phi,roll,yaw))
def body_M(dy=0,dz=0,dx=0,pitch=0,roll=0,yaw=0,pivot=(0,0.15,0.98)):
    return T((dx,dy,dz))@about(pivot,eul(pitch,roll,yaw))

def apply(st):
    ev.reset()
    W=st.get('W',Matrix())
    ev.set_world('body',W)
    for b,Q in st.get('fk',{}).items(): ev.set_fk(b,Q)
    for k,l in LEGS.items():
        M=st['legs'][k]; ev.set_world(l['ik'],M)
        tq=st.get('toe',{}).get(k,0); ev.set_fk(l['toe'],rot('X',tq))
    for s in 'LR':
        ev.set_world(f'poleF.{s}',W); ev.set_world(f'poleH.{s}',W)
    out,P=ev.capture()
    sl={k:(P[l['paw']].to_translation()-P[l['ik']].to_translation()).length for k,l in LEGS.items()}
    slip=max(sl.values()); global LASTSL; LASTSL=sl
    return out,slip,P

# ---------- gait ----------
def gait_leg(p,L,duty,h,front,peel=28,y0=0.0,run=False):
    p%=1.0
    if p<duty:
        s=p/duty; y=y0-L/2+L*s; z=0
        phi=peel*smooth((s-0.62)/0.38)**1.3; toe=-phi
        pass
        return V(0,y,z),phi,toe
    u=(p-duty)/(1-duty)
    y=y0+L/2-L*smoother(u); z=h*math.sin(math.pi*min(1,u*1.08))**0.9
    if front:
        fl=60 if run else 50
        phi=track([(0,peel),(0.3,fl),(0.62,22),(0.85,-5),(1.0,0)],u)
        toe=track([(0,-peel),(0.3,18),(0.7,5),(1.0,0)],u)
    else:
        fl=55 if run else 40
        phi=track([(0,peel),(0.35,fl),(0.7,8),(0.9,-2),(1.0,0)],u)
        toe=track([(0,-peel),(0.35,15),(0.8,0),(1.0,0)],u)
    return V(0,y,z),phi,toe

def fkset(**kw):
    return {b:eul(*v) for b,v in kw.items()}

def clip_walk(N=36):
    duty=0.68; L=0.64; frames=[]
    ph={'LH':0.0,'LF':0.25,'RH':0.5,'RF':0.75}
    y0={'LF':-0.02,'RF':-0.02,'LH':-0.14,'RH':-0.14}
    for f in range(N+1):
        p=f/N; tau=2*math.pi*p
        legs={}; toe={}; dys={}
        for k,l in LEGS.items():
            d,phi,tq=gait_leg(p+0-ph[k],L,duty,0.17 if l['front'] else 0.13,l['front'],y0=y0[k])
            legs[k]=leg_world(l,d,phi); toe[k]=tq; dys[k]=d.y-y0[k]
        bob=-0.018*math.cos(2*tau-0.6)
        W=body_M(dz=bob-0.04,dx=0.012*math.sin(tau-1.2),roll=2.2*math.sin(tau-1.0),yaw=1.2*math.sin(tau+0.3),pitch=0.8*math.cos(2*tau))
        fk={}
        for k in ('LF','RF'):
            fk[LEGS[k]['scap']]=eul(16*dys[k]/(L/2),-2*LEGS[k]['s']*math.sin(tau),0)
        fk['pelvis']=eul(1.0*math.cos(2*tau),3.0*math.sin(tau+0.4),-3.5*math.cos(tau))
        fk['spine1']=eul(0,0,1.5*math.cos(tau))
        fk['spine2']=eul(0,-0.8*math.sin(tau),1.2*math.cos(tau+1))
        fk['chest']=eul(0,-1.2*math.sin(tau+1.6),2.5*math.cos(tau+2.2))
        fk['neck']=eul(7+2.5*math.cos(2*tau+0.9),0,3.5*math.sin(tau+2.6))
        fk['head']=eul(-4-2.5*math.cos(2*tau+1.4),1.5*math.sin(tau),2.0*math.sin(tau+2.9))
        fk['tail1']=eul(0,0,6*math.sin(tau+1.5)); fk['tail2']=eul(0,0,8*math.sin(tau+0.8))
        frames.append(dict(W=W,fk=fk,legs=legs,toe=toe))
    return frames

def clip_run(N=16):
    duty=0.36; L=0.80; frames=[]
    ph={'LH':0.0,'RH':0.11,'RF':0.47,'LF':0.58}
    y0={'LF':-0.06,'RF':-0.06,'LH':-0.24,'RH':-0.24}
    for f in range(N+1):
        p=f/N; tau=2*math.pi*p
        legs={}; toe={}; dys={}
        for k,l in LEGS.items():
            d,phi,tq=gait_leg(p-ph[k],L,duty,0.30 if l['front'] else 0.26,l['front'],peel=40,y0=y0[k],run=True)
            legs[k]=leg_world(l,d,phi); toe[k]=tq; dys[k]=d.y-y0[k]
        flex=math.cos(tau-2*math.pi*0.93)   # +1 gathered (hinds forward) just before hind contact
        W=body_M(dz=-0.05+0.04*math.cos(tau-2*math.pi*0.30),pitch=-3.5*math.cos(tau-2*math.pi*0.2),roll=2.5*math.sin(tau+0.5),yaw=1.5*math.sin(tau),pivot=(0,0.1,0.98))
        fk={}
        for k in ('LF','RF'):
            fk[LEGS[k]['scap']]=eul(20*dys[k]/(L/2),-2*LEGS[k]['s']*math.sin(tau+0.5),0)
        fk['pelvis']=eul(-9*flex,2.5*math.sin(tau),-2.5*math.cos(tau))
        fk['spine1']=eul(-4.5*flex,0,1.5*math.cos(tau))
        fk['spine2']=eul(2.5*flex,0,1.0*math.cos(tau+1))
        fk['chest']=eul(2.0*flex,-1.5*math.sin(tau+1.6),2.0*math.cos(tau+2.0))
        fk['neck']=eul(4-6*math.cos(tau-2*math.pi*0.62),0,2.0*math.sin(tau+2.6))
        fk['head']=eul(-2+5*math.cos(tau-2*math.pi*0.55),0,1.5*math.sin(tau))
        fk['jaw']=eul(4+3*math.cos(tau),0,0)
        fk['tail1']=eul(-8*flex,0,5*math.sin(tau)); fk['tail2']=eul(-6*flex,0,6*math.sin(tau-0.8))
        frames.append(dict(W=W,fk=fk,legs=legs,toe=toe))
    return frames

def planted():
    return {k:leg_world(l) for k,l in LEGS.items()}

def clip_idle(N=90):
    frames=[]
    for f in range(N+1):
        p=f/N; tau=2*math.pi*p
        br=math.sin(2*tau)  # 2 breaths
        W=body_M(dz=-0.006+0.006*br,dx=0.012*math.sin(tau),roll=0.9*math.sin(tau),pitch=0.4*br)
        fk=dict(spine2=eul(-0.6*br,0,0.8*math.sin(tau)),chest=eul(-0.8*br,0,0),
                neck=eul(3+2.5*math.sin(tau+0.5)+1.2*math.sin(3*tau),0,7*math.sin(tau+0.2)),
                head=eul(-1-3.5*math.sin(3*tau+1.0)-1.0*math.sin(tau),2.5*math.sin(tau+0.7),5*math.sin(tau-0.4)),
                jaw=eul(1.5+1.5*math.sin(2*tau-0.5),0,0),
                pelvis=eul(0,0.6*math.sin(tau),0),
                tail1=eul(0,0,4*math.sin(tau)),tail2=eul(0,0,6*math.sin(2*tau)))
        for k in ('LF','RF'): fk[LEGS[k]['scap']]=eul(0,-1.0*LEGS[k]['s']*math.sin(tau),0)
        frames.append(dict(W=W,fk=fk,legs=planted(),toe={}))
    return frames

def clip_attack(N=36):
    K=Keys(dict(
      dy=[(0,0),(11,0.08),(15,-0.17),(18,-0.20),(24,-0.10),(36,0)],
      dx=[(0,0),(11,0.06),(15,-0.02),(18,-0.04),(26,0),(36,0)],
      dz=[(0,0),(11,0.02),(15,-0.05),(18,-0.07),(26,-0.02),(36,0)],
      pitch=[(0,0),(11,-5),(15,6),(18,8),(26,2),(36,0)],
      roll=[(0,0),(11,6),(15,1),(18,-2),(26,0),(36,0)],
      yaw=[(0,0),(11,-8),(15,6),(18,11),(26,3),(36,0)],
      neck_p=[(0,0),(11,-10),(15,8),(18,12),(26,3),(36,0)],
      neck_y=[(0,0),(11,-12),(15,4),(18,8),(26,2),(36,0)],
      head_p=[(0,0),(11,-8),(15,4),(19,6),(26,0),(36,0)],
      head_y=[(0,0),(11,-6),(15,4),(18,6),(36,0)],
      jaw=[(0,1),(8,6),(13,14),(18,10),(26,3),(36,1)],
      # right front paw path (offset from rest, armature space)
      px=[(0,0),(4,-0.03),(11,-0.18),(14,0.06),(16,0.30),(18,0.36),(22,0.12),(26,0.02),(36,0)],
      py=[(0,0),(4,0.02),(11,0.06),(14,-0.30),(16,-0.42),(18,-0.36),(22,-0.24),(26,-0.10),(36,0)],
      pz=[(0,0),(3,0.12),(5,0.22),(11,0.50),(14,0.42),(16,0.22),(18,0.06),(22,0.0),(26,0.08),(30,0),(36,0)],
      pphi=[(0,0),(3,10),(6,40),(11,70),(14,-20),(16,-30),(18,0),(22,0),(26,20),(30,0),(36,0)],
      pyaw=[(0,0),(11,-25),(14,10),(16,35),(18,40),(22,10),(36,0)],
      proll=[(0,0),(11,-20),(14,-10),(16,15),(18,10),(26,0),(36,0)],
      scap=[(0,0),(11,12),(14,-22),(16,-24),(18,-14),(26,-5),(36,0)],
      ))
    frames=[]
    for f in range(N+1):
        W=body_M(dx=K('dx',f),dy=K('dy',f),dz=K('dz',f),pitch=K('pitch',f),roll=K('roll',f),yaw=K('yaw',f),pivot=(0,0.3,0.98))
        legs=planted(); toe={}
        l=LEGS['RF']
        legs['RF']=T((K('px',f),K('py',f),K('pz',f)))@about(l['wrist'],eul(K('pphi',f),K('proll',f),K('pyaw',f)))
        toe['RF']=-0.4*K('pphi',f) if K('pphi',f)<0 else 0.2*K('pphi',f)
        fk=dict(neck=eul(K('neck_p',f),0,K('neck_y',f)),head=eul(K('head_p',f),0,K('head_y',f)),jaw=eul(K('jaw',f),0,0),
                chest=eul(0,0.5*K('roll',f),0.4*K('yaw',f)),spine2=eul(0,0,0.3*K('yaw',f)),
                **{'scapula.R':eul(K('scap',f),0,0),'scapula.L':eul(-0.3*K('scap',f),0,0)},
                tail1=eul(0,0,-0.5*K('yaw',f)))
        frames.append(dict(W=W,fk=fk,legs=legs,toe=toe))
    return frames

def clip_attack2(N=54):
    K=Keys(dict(
      pitch=[(0,0),(6,4),(17,-36),(23,-40),(27,-14),(29,7),(32,10),(40,4),(54,0)],
      dy=[(0,0),(6,0.03),(17,0.06),(23,0.06),(27,-0.10),(29,-0.22),(32,-0.24),(42,-0.12),(54,0)],
      dz=[(0,0),(6,-0.04),(17,0.0),(23,0.02),(29,-0.06),(32,-0.10),(40,-0.04),(54,0)],
      roll=[(0,0),(17,2),(23,-2),(29,0),(54,0)],
      neck_p=[(0,0),(6,6),(17,22),(23,24),(27,10),(29,20),(32,24),(42,8),(54,0)],
      head_p=[(0,0),(6,2),(17,-6),(21,-12),(27,4),(32,10),(42,2),(54,0)],
      jaw=[(0,1),(10,4),(17,10),(21,16),(25,14),(30,10),(38,3),(54,1)],
      # front paws: blend to body frame (b) while reared
      b=[(0,0),(5,0),(13,1),(24,1),(29,0),(54,0)],
      ly=[(0,0),(17,-0.30),(23,-0.36),(29,0),(54,0)],
      lz=[(0,0),(6,0.06),(10,0.18),(17,0.30),(23,0.38),(29,0),(54,0)],
      lphi=[(0,0),(6,8),(13,60),(17,45),(23,-10),(26,-40),(29,0),(54,0)],
      sx=[(0,0),(17,0.05),(23,0.08),(29,0.0),(54,0)],
      # slam target on ground (world)
      gy=[(0,0),(24,-0.42),(29,-0.42),(40,-0.42),(46,-0.12),(52,0),(54,0)],
      scap=[(0,0),(17,-22),(23,-26),(27,-18),(29,-10),(40,-6),(54,0)],
      ))
    def step(f,f0,f1,h=0.12):
        u=(f-f0)/(f1-f0)
        return 0 if u<=0 or u>=1 else h*math.sin(math.pi*u)
    frames=[]
    for f in range(N+1):
        W=body_M(dy=K('dy',f),dz=K('dz',f),pitch=K('pitch',f),roll=K('roll',f),pivot=HIP)
        legs=planted(); toe={}
        b=K('b',f)
        for k,stp in (('LF',(40,47)),('RF',(43,50))):
            l=LEGS[k]
            gy=K('gy',f)
            if f>=40: gy=-0.42+0.42*smooth((f-stp[0])/(stp[1]-stp[0]))
            Wg=T((0,gy,step(f,*stp)))@about(l['ball'],eul(25*step(f,*stp)/0.12,0,0))
            Wb=W@T((l['s']*K('sx',f),K('ly',f),K('lz',f)))@about(l['wrist'],eul(K('lphi',f),0,0))
            legs[k]=mix_mat(Wg,Wb,b) if b>0 else Wg
            toe[k]=0.25*K('lphi',f) if b>0 else 0
        fk=dict(neck=eul(K('neck_p',f),0,0),head=eul(K('head_p',f),0,0),jaw=eul(K('jaw',f),0,0),
                spine1=eul(0.15*K('pitch',f),0,0),
                **{'scapula.L':eul(K('scap',f),0,0),'scapula.R':eul(K('scap',f),0,0)},
                tail1=eul(-0.4*K('pitch',f),0,0))
        frames.append(dict(W=W,fk=fk,legs=legs,toe=toe))
    return frames

def clip_hit(N=18):
    K=Keys(dict(dy=[(0,0),(3,0.07),(7,0.03),(18,0)],dz=[(0,0),(3,-0.035),(8,-0.01),(18,0)],
      pitch=[(0,0),(3,-3),(8,1),(18,0)],roll=[(0,0),(3,3.5),(8,-1),(18,0)],yaw=[(0,0),(3,-4),(9,1),(18,0)],
      neck_p=[(0,0),(3,-9),(8,3),(18,0)],neck_y=[(0,0),(3,-10),(9,2),(18,0)],head_p=[(0,0),(2,-10),(7,4),(18,0)],
      head_y=[(0,0),(2,-8),(9,2),(18,0)],jaw=[(0,1),(3,12),(9,4),(18,1)]))
    frames=[]
    for f in range(N+1):
        W=body_M(dy=K('dy',f),dz=K('dz',f),pitch=K('pitch',f),roll=K('roll',f),yaw=K('yaw',f))
        fk=dict(neck=eul(K('neck_p',f),0,K('neck_y',f)),head=eul(K('head_p',f),0,K('head_y',f)),jaw=eul(K('jaw',f),0,0),
                chest=eul(0.4*K('pitch',f),0,0),tail1=eul(-8*K('dz',f)/0.035,0,0))
        frames.append(dict(W=W,fk=fk,legs=planted(),toe={}))
    return frames

def clip_death(N=78,hold=12):
    E=N-hold
    PV=V(-0.56,0.15,0.10)
    K=Keys(dict(
      dy=[(0,0),(6,0.06),(14,0.02),(24,-0.04),(40,-0.04),(E,-0.04)],
      pitch=[(0,0),(6,-6),(12,-2),(22,12),(30,8),(38,4),(E,3)],
      dz=[(0,0),(6,0.01),(14,-0.04),(24,-0.16),(32,-0.27),(38,-0.30),(E,-0.30)],
      roll=[(0,0),(6,2),(14,-3),(24,-6),(32,-14),(40,-55),(46,-90),(50,-84),(55,-88),(E,-87)],
      yaw=[(0,0),(6,-4),(14,3),(24,2),(E,2)],
      neck_p=[(0,0),(4,-14),(10,-8),(22,18),(30,24),(40,18),(48,8),(E,8)],
      neck_y=[(0,0),(4,-6),(12,4),(30,0),(40,-15),(48,-28),(52,-24),(E,-26)],
      head_p=[(0,0),(4,-12),(10,-4),(22,8),(40,6),(E,6)],
      head_y=[(0,0),(4,-4),(30,0),(42,-10),(48,-22),(52,-18),(E,-20)],
      head_r=[(0,0),(40,0),(48,-12),(E,-14)],
      jaw=[(0,1),(4,14),(12,10),(30,5),(50,7),(E,8)],
      lb=[(0,0),(22,0),(34,0.3),(44,1),(E,1)],   # legs -> body frame
      tail=[(0,0),(30,-10),(46,-25),(E,-20)],
      ))
    frames=[]
    # limp leg poses in body frame (offsets from rest, body-local before roll)
    limp={'LF':(T((-0.22,-0.22,0.12)),35),'RF':(T((0.05,-0.30,0.08)),30),'LH':(T((-0.24,0.22,0.12)),30),'RH':(T((0.04,0.24,0.06)),25)}
    for f in range(N+1):
        ff=min(f,E)
        r=K('roll',ff)
        dz=K('dz',ff)
        W=T((0,K('dy',ff),dz))@about(HIP,eul(K('pitch',ff),0,K('yaw',ff)))
        W=T((0.55*smooth((ff-28)/24),0,0))@about(PV+V(0,0,dz),eul(0,r,0))@W
        legs={}; toe={}
        b=K('lb',ff)
        for k,l in LEGS.items():
            Wg=leg_world(l)
            off,ph=limp[k]
            Wb=W@off@about(l['wrist'],eul(ph,0,0))
            legs[k]=mix_mat(Wg,Wb,smoother(b))
            toe[k]=15*b
        fk=dict(neck=eul(K('neck_p',ff),K('head_r',ff),K('neck_y',ff)),head=eul(K('head_p',ff),K('head_r',ff),K('head_y',ff)),jaw=eul(K('jaw',ff),0,0),
                tail1=eul(K('tail',ff),0,0),tail2=eul(0.6*K('tail',ff),0,0),spine1=eul(0,0,-3*smooth(ff/50)),chest=eul(0,0,-4*smooth(ff/50)))
        frames.append(dict(W=W,fk=fk,legs=legs,toe=toe))
    return frames

def clip_death_sprawl(N=72,hold=14):
    E=N-hold
    K=Keys(dict(
      dy=[(0,0),(5,0.04),(12,0.0),(22,-0.10),(32,-0.18),(E,-0.18)],
      dz=[(0,0),(5,0.01),(12,-0.03),(20,-0.20),(26,-0.30),(34,-0.50),(38,-0.54),(41,-0.52),(E,-0.53)],
      pitch=[(0,0),(5,-6),(12,0),(20,10),(26,9),(34,4),(38,3),(E,3)],
      roll=[(0,0),(5,3),(12,-2),(22,-5),(32,-12),(38,-16),(E,-15)],
      yaw=[(0,0),(5,-4),(14,3),(30,6),(E,6)],
      neck_p=[(0,0),(4,-14),(10,-6),(20,12),(28,16),(36,34),(40,30),(E,31)],
      neck_y=[(0,0),(4,-6),(12,4),(28,-6),(38,-22),(E,-22)],
      head_p=[(0,0),(4,-12),(10,-2),(22,6),(36,18),(40,14),(E,15)],
      head_y=[(0,0),(4,-4),(26,0),(38,-14),(E,-14)],
      head_r=[(0,0),(26,0),(38,-14),(E,-16)],
      jaw=[(0,1),(4,16),(12,10),(30,6),(40,9),(E,9)],
      fb=[(0,0),(12,0),(24,1),(E,1)],     # front legs -> sprawl
      hb=[(0,0),(20,0),(34,1),(E,1)],     # hind legs -> sprawl
      tail=[(0,0),(30,-10),(E,-18)],
      ))
    SPR={'LF':((0.16,-0.30,0.0),0),'RF':((-0.10,-0.22,0.0),0),'LH':((0.14,0.42,0.02),-55),'RH':((-0.12,0.36,0.02),-50)}
    frames=[]
    for f in range(N+1):
        ff=min(f,E)
        W=T((0,K('dy',ff),K('dz',ff)))@about(HIP,eul(K('pitch',ff),K('roll',ff),K('yaw',ff)))
        legs={}; toe={}
        for k,l in LEGS.items():
            Wg=leg_world(l)
            d,ph=SPR[k]; b=K('fb',ff) if l['front'] else K('hb',ff)
            Ws=T((0,K('dy',ff)*0.5,0))@leg_world(l,d=d,phi=ph)
            legs[k]=mix_mat(Wg,Ws,smoother(b)); toe[k]=(10 if l['front'] else 25)*b
        fk=dict(neck=eul(K('neck_p',ff),K('head_r',ff),K('neck_y',ff)),head=eul(K('head_p',ff),K('head_r',ff),K('head_y',ff)),jaw=eul(K('jaw',ff),0,0),
                tail1=eul(K('tail',ff),0,0),tail2=eul(0.6*K('tail',ff),0,0),spine1=eul(0,0,-2*smooth(ff/40)),chest=eul(0,0,-3*smooth(ff/40)))
        frames.append(dict(W=W,fk=fk,legs=legs,toe=toe))
    return frames

CLIPS=dict(idle=clip_idle,walk=clip_walk,run=clip_run,attack=clip_attack,attack2=clip_attack2,hit=clip_hit,death=clip_death_sprawl,death_old=clip_death)
def mesh_minz():
    dg=bpy.context.evaluated_depsgraph_get(); e=ob.evaluated_get(dg); me=e.to_mesh()
    a=np.empty(len(me.vertices)*3); me.vertices.foreach_get('co',a); e.to_mesh_clear()
    return float(a.reshape(-1,3)[:,2].min())
def lifted(st,h):
    if abs(h)<1e-5: return st
    L=T((0,0,h)); st=dict(st); st['W']=L@st.get('W',Matrix()); st['legs']={k:L@m for k,m in st['legs'].items()}; return st
GROUND=dict(death=18,death_old=20)
baked={}; report={}
for cn,fn in CLIPS.items():
    if ONLY and cn not in ONLY: continue
    fr=fn(); out=[]; slips=[]
    if cn in GROUND:
        lift=[]
        for i,st in enumerate(fr):
            apply(st); mz=mesh_minz()
            lift.append(0.0 if i<GROUND[cn] else (-mz if i>=GROUND[cn]+18 else max(0.0,-mz)))
        lift=np.array(lift); lift=np.array([lift[max(0,i-2):i+3].max() for i in range(len(lift))])
        k=np.array([1,2,3,2,1],float); k/=k.sum(); lift=np.convolve(np.pad(lift,2,mode='edge'),k,'valid')
        print('LIFT',cn,np.round(lift,3).tolist())
        fr=[lifted(st,h) for st,h in zip(fr,lift)]
    for st in fr:
        o,sl,P=apply(st); out.append(o); slips.append(sl)
        if sl>0.02: print('SLIP',cn,len(slips)-1,{k:round(v,3) for k,v in LASTSL.items() if v>0.02})
    if cn in GROUND: print('MINZ after',cn,round(min(0,mesh_minz()),3))
    baked[cn]=out; report[cn]=dict(frames=len(fr),dur=(len(fr)-1)/30,maxslip=round(max(slips),4),slipframe=int(np.argmax(slips)))
    print('CLIP',cn,report[cn])
ev.reset()
rc.strip_controls(ao,EXPORT)
rc.write_actions(ao,baked)
bpy.context.scene.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=OUT.replace('.glb','.blend'))
rc.export([ao,ob],OUT)
json.dump(report,open(OUT.replace('.glb','_bake.json'),'w'),indent=1)
