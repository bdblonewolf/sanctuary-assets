from rt import *
def pose(L,f=0): return L[f:f+1]
def blendL(La,Lb,w):
    F=len(w); out=np.zeros((F,)+La.shape[1:])
    for j in range(La.shape[1]):
        q=R.from_quat([La[0,j],Lb[0,j]]); s=Slerp([0,1],q); out[:,j]=s(np.clip(w,0,1)).as_quat()
    return out
def feet_targets(b,L,h):
    GQ,GP=fk(b,L,h); return {s:(GP[0,b.i(s+'Foot')].copy(),GQ[0,b.i(s+'Foot')].copy()) for s in ('Left','Right')}
def solve_legs(b,L,h,tg_a,tg_b,wf):
    for side in ('Left','Right'):
        pa,qa=tg_a[side]; pb,qb=tg_b[side]
        A=pa[None]*(1-wf[:,None])+pb[None]*wf[:,None]
        A[:,1]=pa[1]*(1-wf)+pb[1]*wf
        fq=Slerp([0,1],R.from_quat([qa,qb]))(np.clip(wf,0,1)).as_quat()
        L=limb_ik(b,L,h,(side+'UpLeg',side+'Leg',side+'Foot'),A,foot_global=fq)
    return L
def lean(b,L,deg_spine,deg_hips):
    F=len(L)
    if np.any(deg_hips): L=world_pre(b,L,b.i('Hips'),R.from_euler('x',np.radians(deg_hips)[:,None]))
    for n,f in (('Spine',0.4),('Spine1',0.35),('Spine2',0.25)):
        L=world_pre(b,L,b.i(n),R.from_euler('x',np.radians(deg_spine*f)[:,None]))
    return L
def hands_to_knees(b,L,h,w):
    for side in ('Left','Right'):
        GQ,GP=fk(b,L,h)
        K=GP[:,b.i(side+'Leg')].copy(); out=np.sign(K[:,0:1]) 
        tgt=K+np.array([0,0.07,0.03])*b.leg/1.11; tgt[:,0]+=0.02*np.sign(K[:,0])
        L=limb_ik(b,L,h,(side+'Arm',side+'ForeArm',side+'Hand'),tgt,w=w)
    return L

def sit_down(b,Lidle,hidle,Lsit,hsit,dur=1.0):
    F=int(round(dur*FPS))+1; u=np.linspace(0,1,F)
    tsit=feet_targets(b,Lsit,hsit); tid=feet_targets(b,Lidle,hidle)
    dz=((tsit['Left'][0]+tsit['Right'][0])/2-(tid['Left'][0]+tid['Right'][0])/2)[2]
    hid=hidle[0].copy(); hid[2]+=dz
    for s in tid: tid[s]=(tid[s][0]+np.array([0,0,dz]),tid[s][1])
    w_ub=smooth((u-0.05)/0.85)
    L=blendL(pose(Lidle),pose(Lsit),w_ub)
    h=np.zeros((F,3)); hs=hsit[0]
    h[:,0]=hid[0]+(hs[0]-hid[0])*smooth(u/0.9)
    h[:,2]=hid[2]+(hs[2]-hid[2])*smooth(u/0.85)
    h[:,1]=hid[1]+(hs[1]-hid[1])*smooth((u-0.08)/0.84) - 0.012*np.sin(np.pi*np.clip((u-0.75)/0.25,0,1))*b.leg/1.11
    bump=np.sin(np.pi*np.clip(u/0.92,0,1))
    L=lean(b,L,24*bump,10*bump)
    L=solve_legs(b,L,h,tid,tsit,smooth((u-0.1)/0.7))
    return np.linspace(0,dur,F),L,h,float(dz)
def stand_up(b,Lidle,hidle,Lsit,hsit,dur=1.1):
    F=int(round(dur*FPS))+1; u=np.linspace(0,1,F)
    tsit=feet_targets(b,Lsit,hsit); tid=feet_targets(b,Lidle,hidle)
    dz=((tsit['Left'][0]+tsit['Right'][0])/2-(tid['Left'][0]+tid['Right'][0])/2)[2]
    hid=hidle[0].copy(); hid[2]+=dz
    for s in tid: tid[s]=(tid[s][0]+np.array([0,0,dz]),tid[s][1])
    w_ub=smooth((u-0.3)/0.65)
    L=blendL(pose(Lsit),pose(Lidle),w_ub)
    hs=hsit[0]; h=np.zeros((F,3))
    rise=smooth((u-0.28)/0.57)
    h[:,0]=hs[0]+(hid[0]-hs[0])*rise
    h[:,2]=hs[2]+(hid[2]-hs[2])*smooth((u-0.15)/0.6)
    h[:,1]=hs[1]+(hid[1]-hs[1])*rise
    lean_c=np.where(u<0.35,smooth(u/0.35),1-smooth((u-0.4)/0.55))
    L=lean(b,L,34*lean_c,14*lean_c)
    L=solve_legs(b,L,h,tsit,tid,smooth((u-0.2)/0.6))
    wh=np.where(u<0.5,smooth((u-0.05)/0.3),1-smooth((u-0.5)/0.3))
    L=hands_to_knees(b,L,h,wh)
    return np.linspace(0,dur,F),L,h,float(dz)
def pose_blend(b,La,ha,Lb,hb,dur=1.2):
    F=int(round(dur*FPS))+1; u=np.linspace(0,1,F); w=smooth(u)
    L=blendL(pose(La),pose(Lb),w); h=ha[0][None]*(1-w[:,None])+hb[0][None]*w[:,None]
    ta=feet_targets(b,La,ha); tb=feet_targets(b,Lb,hb)
    L=solve_legs(b,L,h,ta,tb,w)
    return np.linspace(0,dur,F),L,h
