# sculpted figure helpers (v1 fix pass): parametric surfaces, faces, praying hands, robed figures, recumbent effigy, skulls
from glib import *
import lib
lib.PROPS.setdefault('maiden_iron',(0.68,0.35))
def sstep(a,b,x):
    t=min(1.0,max(0.0,(x-a)/(b-a))); return t*t*(3-2*t)
def psurf(name,nu,nv,fn,m,cap0=False,cap1=False,uvs=(1,1),angle=70,mats=None,matfn=None,closed=True):
    """grid surface fn(u,v)->(x,y,z); u wraps (closed) with a UV seam column. caps fan the v=0 / v=1 rings."""
    V=[];UV=[];F=[];FM=[]
    cols=nu+1
    for j in range(nv+1):
        v=j/nv
        for i in range(cols):
            u=i/nu; V.append(tuple(fn(u if (i<nu or not closed) else 0.0,v))); UV.append((u*uvs[0],v*uvs[1]))
    for j in range(nv):
        for i in range(nu):
            a=j*cols+i; F.append((a,a+1,a+cols+1,a+cols)); FM.append(matfn((i+0.5)/nu,(j+0.5)/nv) if matfn else 0)
    for cap,j,flip in ((cap0,0,True),(cap1,nv,False)):
        if not cap: continue
        ring=[j*cols+i for i in range(nu)]; c=Vector((0,0,0))
        for k in ring: c+=Vector(V[k])
        c/=len(ring); ci=len(V); V.append(tuple(c)); UV.append((0.5*uvs[0],(j/nv)*uvs[1]))
        for i in range(nu):
            f=(ring[i],ring[(i+1)%nu],ci); F.append(f[::-1] if flip else f); FM.append(FM[-1] if FM else 0)
    if mats: o=obj_uvv(name,V,F,UV,None,angle=angle,mats=mats,fmat=FM)
    else: o=obj_uvv(name,V,F,UV,m,angle=angle)
    return o
RECUMB=Matrix(((0,0,-1),(1,0,0),(0,-1,0)))   # local: face -Y,up +Z  ->  face +Z, up -X (lying, head toward -X)
def xf(o,M3,loc=(0,0,0),pre=None):
    if pre is not None: o.data.transform(pre.to_4x4())
    o.data.transform(M3.to_4x4()); o.data.transform(Matrix.Translation(Vector(loc))); o.data.update(); return o
def _bump(n,c,s,a): return a*math.exp(-((n-c).length/s)**2)
def face_disp(n,sorrow=1.0,closed_eyes=True):
    C=Vector; f=0.0
    f+=_bump(n,C((0,-0.95,-0.1)),0.13,0.17)    # nose
    f+=_bump(n,C((0,-0.98,0.12)),0.12,0.05)    # bridge
    for s in (-1,1):
        f+=_bump(n,C((s*0.36,-0.85,0.29)),0.15,0.08)          # brow
        f+=_bump(n,C((s*0.14,-0.93,0.33)),0.10,0.05*sorrow)   # sorrowful inner brow lift
        f+=_bump(n,C((s*0.33,-0.88,0.07)),0.15,-0.15)         # eye socket
        if closed_eyes: f+=_bump(n,C((s*0.34,-0.9,0.03)),0.07,0.045)  # heavy lid
        f+=_bump(n,C((s*0.52,-0.78,-0.22)),0.2,0.04)          # cheek
        f+=_bump(n,C((s*0.2,-0.9,-0.48)),0.08,-0.03*sorrow)   # down-turned mouth corners
    f+=_bump(n,C((0,-0.93,-0.4)),0.07,-0.04)     # mouth line
    f+=_bump(n,C((0,-0.9,-0.33)),0.07,0.025)     # upper lip
    f+=_bump(n,C((0,-0.84,-0.66)),0.15,0.06)     # chin
    return f
def head(name,r,m,nu=24,nv=16,sorrow=1.0,closed_eyes=True,sub=None,amp=1.4):
    """sculpted human head (sphere grid denser at the face), faces -Y, centre at origin; r ~ half height"""
    def fn(u,v):
        w=2*u-1; a=math.pi*math.copysign(abs(w)**1.8,w)        # a=0 front(-Y), seam at back
        th=math.pi*(1-v)                                       # pole to pole (v=0 bottom)
        el=th-math.pi/2; el=math.copysign(abs(el/(math.pi/2))**1.5,el)*math.pi/2
        n=Vector((math.cos(el)*math.sin(a),-math.cos(el)*math.cos(a),math.sin(el)))
        x,y,z=n
        sx=0.80*(1-0.22*max(0,-z)**1.3); sy=0.95*(0.9 if y<0 else 1.0); sz=1.1
        q=Vector((x*sx,y*sy,z*sz))+Vector((0,-1,0))*amp*face_disp(n,sorrow,closed_eyes)
        return tuple(q*r)
    o=psurf(name,nu,nv,fn,m,uvs=(0.5,0.5),angle=80,closed=True)
    weld(o,1e-5*r); return o
def praying_hands(name,s,m,sides=10):
    """two palms pressed together pointing +Z; base (wrist) at origin; ~0.18*s tall"""
    zs=[0,0.03,0.06,0.10,0.14,0.17,0.185]; wx=[0.034,0.036,0.037,0.034,0.028,0.016,0.004]; dy=[0.026,0.036,0.042,0.034,0.026,0.014,0.003]
    def fn(u,v):
        k=v*(len(zs)-1); i=min(int(k),len(zs)-2); t=k-i
        z=zs[i]+(zs[i+1]-zs[i])*t; w=wx[i]+(wx[i+1]-wx[i])*t; d=dy[i]+(dy[i+1]-dy[i])*t
        a=2*math.pi*u; x=w*math.sin(a); y=-d*math.cos(a)
        y*=1-0.35*math.exp(-(math.sin(a)/0.28)**2)   # crease where palms meet (front/back)
        if math.cos(a)>0.3 and v<0.55: y-=0.012*math.cos(a)*(1-v/0.55)  # thumbs bulge at front
        return (x*s,(y-0.01*v)*s,z*s)
    return psurf(name,sides,6,fn,m,cap0=True,cap1=True,uvs=(0.3,0.3),angle=80)
def robed_figure(name,H,m,mh,seed=0,bow=0.42,nu=24,nv=12):
    """standing hooded monk/saint facing -Y, hem at z=0, praying hands, bowed head. m: robe, mh: ds_ hood material.
    returns list of objects (not joined)"""
    rnd=random.Random(seed); ph=[rnd.uniform(0,6.28) for _ in range(5)]
    sc=H/1.2; Hb=0.82*H
    vv=[0,0.12,0.35,0.55,0.72,0.86,0.94,1.0]
    RX=[0.24,0.21,0.18,0.165,0.17,0.185,0.15,0.06]; RY=[0.17,0.155,0.13,0.12,0.125,0.12,0.1,0.055]
    def cy(v): return -0.05*sstep(0.55,1.0,v)*sc
    def rxy(v): return np.interp(v,vv,RX)*sc,np.interp(v,vv,RY)*sc
    def body(u,v):
        a=2*math.pi*u; rx,ry=rxy(v)
        A=0.03*(1-v)**1.2+0.005
        f=A*math.sin(7*a+0.8*math.sin(3*a+ph[0])+ph[1])+0.35*A*math.sin(13*a+ph[2])
        if math.cos(a)<0: ry*=0.82
        x=rx*math.sin(a)*(1+f); y=cy(v)-ry*math.cos(a)*(1+f)
        z=v*Hb+(0.01*sc*math.sin(7*a+ph[1]) if v==0 else 0)
        return (x,y,max(0.0,z))
    O=[psurf(name+'_robe',nu,nv,body,m,cap0=True,uvs=(1.4,1.6),angle=80)]
    # rope cincture + hanging cord
    zc=0.55*Hb; rxc,ryc=rxy(0.55)
    bl=ring(name+'_belt',1.0,0.011*sc,m,loc=(0,0,0),n=18,sides=4); bl.data.transform(Matrix.Diagonal((rxc*1.05,ryc*1.05,1,1))); bl.data.transform(Matrix.Translation((0,cy(0.55),zc))); O.append(bl)
    O.append(tube(name+'_cord',[(0.03*sc,cy(0.55)-ryc*1.02,zc),(0.04*sc,cy(0.45)-ryc*1.12,zc-0.14*sc),(0.035*sc,cy(0.35)-ryc*1.18,zc-0.3*sc)],[0.011*sc,0.01*sc,0.008*sc],4,m,uvscale=0.3))
    # capelet (mozzetta) over the shoulders, draped folds
    N=Vector((0,cy(1.0),Hb))
    def cape(u,v):
        a=2*math.pi*u; vb=1.0-0.33*v                       # robe height it covers (v=0 top at neck)
        rx,ry=rxy(vb); rx+=(0.02+0.03*v)*sc; ry+=(0.02+0.03*v)*sc
        if math.cos(a)<0: ry*=0.85
        f=0.018*sc*v*math.sin(9*a+ph[3])
        z=Hb*vb-0.02*sc*v*(1+math.cos(a))*0.5               # hangs slightly lower at front
        return (math.sin(a)*(rx+f),cy(vb)-math.cos(a)*(ry+f),z+0.01*sc)
    O.append(psurf(name+'_cape',nu,3,cape,mh,uvs=(1.2,0.4),angle=80))
    # hood: cowl around the bowed head with a front opening
    hv=[0,0.25,0.5,0.75,0.9,1.0]
    HR=[0.115,0.128,0.13,0.112,0.07,0.0]; HZ=[-0.02,0.07,0.16,0.25,0.31,0.335]
    def openang(v): return 0.85*sstep(0.0,0.3,v)*(1-sstep(0.68,0.97,v))
    def hood(u,v):
        op=openang(v); a=op+(2*math.pi-2*op)*u
        r=np.interp(v,hv,HR)*sc; z=np.interp(v,hv,HZ)*sc
        x=r*math.sin(a)*(1+0.03*math.sin(5*a+ph[4])*(1-v)); y=-r*math.cos(a)*1.08+0.05*sc*v**2+0.035*sc*(1-v)
        if math.cos(a)<-0.3: y+=0.03*sc*v*(v<0.95)          # soft back peak
        p=Matrix.Rotation(bow*sstep(0.0,0.5,v),3,'X')@Vector((x,y,z))
        return tuple(N+p)
    O.append(psurf(name+'_hood',18,10,hood,mh,uvs=(1.0,0.6),angle=85,closed=False))
    hd=head(name+'_head',0.08*sc,m)
    hd.data.transform(Matrix.Rotation(bow*1.1,4,'X')); hd.data.transform(Matrix.Translation(N+Matrix.Rotation(bow,3,'X')@Vector((0,-0.012*sc,0.1*sc)))); O.append(hd)
    # bell sleeves: shoulders -> elbows at the sides -> wrists meeting at the chest
    chest=cy(0.74)-rxy(0.74)[1]
    hz=0.72*Hb; hy=chest-0.045*sc
    for sx in (-1,1):
        path=[(sx*0.16*sc,cy(0.9),0.9*Hb),(sx*0.2*sc,cy(0.78)-0.0*sc,0.74*Hb),(sx*0.18*sc,cy(0.66)-0.06*sc,0.635*Hb),(sx*0.1*sc,chest-0.06*sc,0.64*Hb),(sx*0.035*sc,hy,hz-0.025*sc)]
        sl=tube(name+f'_sleeve{sx}',path,[0.048*sc,0.05*sc,0.054*sc,0.058*sc,0.064*sc],10,m,uvscale=0.6,angle=80,squash=[(1,0.85)]*5)
        O.append(sl)
    hs=praying_hands(name+'_hands',1.12*sc,m); hs.data.transform(Matrix.Rotation(-0.2,4,'X')); hs.data.transform(Matrix.Translation((0,hy-0.012*sc,hz-0.005*sc))); O.append(hs)
    return O
def effigy(name,L,m,kind='knight',s=1.0,seed=0):
    """recumbent figure lying along +X (head at -X), face up (+Z), base z=0 on lid; L ~ head-top to toe (1.9)."""
    rnd=random.Random(seed); ph=[rnd.uniform(0,6.28) for _ in range(3)]
    k=L/1.9*s
    SX=[-0.68,-0.62,-0.45,-0.25,-0.05,0.2,0.45,0.65,0.8]
    SW=[0.09,0.23,0.25,0.205,0.215,0.195,0.165,0.14,0.12]
    SH=[0.08,0.14,0.19,0.17,0.16,0.145,0.12,0.1,0.085]
    def top(x): return np.interp(x/k,SX,SH)*k
    def body(u,v):
        x=(SX[0]+(SX[-1]-SX[0])*v)*k; w=np.interp(x/k,SX,SW)*k; h=top(x)
        a=2*math.pi*u; c=math.cos(a); sn=math.sin(a)
        y=w*c
        if sn<=0: z=0.0
        else:
            z=h*sn**0.6
            leg=sstep(-0.05,0.2,x/k)
            z+=0.012*k*leg*math.sin(9*a+ph[0]+4*v)*sn          # robe folds running lengthwise
            z-=0.03*k*leg*math.exp(-(y/(0.045*k))**2)           # hollow between the legs
            z+=0.008*k*(1-leg)*math.sin(14*a)*sn                # surcoat ripple on chest
        return (x,y,z)
    O=[psurf(name+'_body',26,14,body,m,cap0=True,cap1=True,uvs=(1.0,2.0),angle=80)]
    hx=-0.82*k
    pl=box(name+'_pillow',(0.3*k,0.48*k,0.08*k),(hx+0.02*k,0,0.04*k),m,bevel=0.03*k,seg=2,uvscale=0.5); O.append(pl)
    for sy in (-1,1):
        for sxp in (-1,1): O.append(blob(name+f'_tas{sy}{sxp}',0.02*k,(hx+0.02*k+sxp*0.15*k,sy*0.24*k,0.05*k),m,sub=1,amp=0.1))
    hd=head(name+'_head',0.088*k,m,amp=2.0,nu=20,nv=14); xf(hd,RECUMB,(hx,0,0.155*k)); O.append(hd)
    if kind=='knight': pass
    else:
        mt=slab(name+'_mitre',[(-0.09,0),(0.09,0),(0.1,0.14),(0.0,0.24),(-0.1,0.14)],0.09*k,m,uvscale=0.4)
        xf(mt,RECUMB,(hx-0.08*k,0,0.17*k),pre=Matrix.Diagonal((k,1,k))); O.append(mt)
    # arms: shoulders -> elbows at the sides -> wrists meeting on the chest
    wx=-0.33*k
    for sy in (-1,1):
        path=[(-0.6*k,sy*0.15*k,0.1*k),(-0.56*k,sy*0.215*k,0.105*k),(-0.42*k,sy*0.235*k,0.1*k),(-0.22*k,sy*0.225*k,0.12*k),(-0.24*k,sy*0.12*k,0.2*k),(wx,sy*0.04*k,0.225*k)]
        O.append(blob(name+f'_shoulder{sy}',0.075*k,(-0.57*k,sy*0.19*k,0.12*k),m,sub=2,amp=0.03,scale=(1.0,0.9,0.75)))
        O.append(tube(name+f'_arm{sy}',path,[0.05*k,0.055*k,0.05*k,0.048*k,0.045*k,0.04*k],8,m,uvscale=0.5,angle=80,squash=[(1,0.85)]*6))
    hs=praying_hands(name+'_hands',0.95*k,m,sides=8); xf(hs,Matrix.Rotation(math.radians(18),3,'Y')@RECUMB,(wx+0.01*k,0,0.215*k)); O.append(hs)
    if kind=='knight':  # sword along the body, hilt under the hands
        def sz(x): return top(x)+0.012*k
        gx=-0.2*k
        O.append(tube(name+'_grip',[(wx-0.06*k,0,0.235*k),(gx,0,sz(gx)+0.012*k)],0.017*k,6,m))
        O.append(blob(name+'_pommel',0.03*k,(wx-0.08*k,0,0.24*k),m,sub=1,amp=0.05))
        O.append(box(name+'_guard',(0.035*k,0.3*k,0.035*k),(gx,0,sz(gx)+0.012*k),m,bevel=0.008*k))
        xs=np.linspace(gx+0.02*k,0.62*k,5); bl=[(x,0,sz(x)) for x in xs]
        O.append(tube(name+'_blade',bl,[0.03*k]*4+[0.006*k],4,m,uvscale=0.5,squash=[(1,0.3)]*5,twist=math.pi/4))
    else:
        O.append(tube(name+'_crozier',[(-0.6*k,0.17*k,top(-0.6*k)),(0.78*k,0.15*k,top(0.78*k)+0.01*k)],0.016*k,6,m))
        O.append(box(name+'_stole',(0.9*k,0.08*k,0.02*k),(0.3*k,0,top(0.3*k)),m,bevel=0.006*k))
    # pointed feet, toes up
    for sy in (-1,1):
        O.append(blob(name+f'_foot{sy}',0.06*k,(0.84*k,sy*0.065*k,0.1*k),m,sub=2,amp=0.05,scale=(0.75,0.7,1.55),rot=(0,-0.35,0)))
    return O
# ---------- skulls (better detail, still cheap)
