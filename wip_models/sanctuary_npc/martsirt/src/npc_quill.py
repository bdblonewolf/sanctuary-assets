# Quill the scribe -- geometry, weights, masks. Then lib_fin.py does UV/bake/export.
import sys
SRC='/workspace/sanctuary_npc/martsirt/src'
exec(open(SRC+'/lib_bl.py').read()); exec(open(SRC+'/lib_mat.py').read())
NAME='quill'; BODY_BUDGET=int(os.environ.get('BODY_BUDGET','9500')); STAGE=sys.argv[-1] if len(sys.argv)>1 else 'fit'
init_body(SRC+'/bodies/male_skinny.glb'); L=landmarks()
exec(open(SRC+'/lib_detail.py').read())
# face character (pipeline copy only): lean, sharp cheekbones, hollow cheeks, sunken temples, defined brow, long jaw
_ez=L['eye_z']; _ey=L['eyeL_front'][1]; _ex=L['eye_x']; _n=L['nose']; _c=L['chin']
sculpt([((s_*(_ex+0.014),_ey+0.010,_ez-0.024),(0.016,0.016,0.009),0.0020) for s_ in (1,-1)]+          # cheekbones
       [((s_*(_ex+0.008),_ey+0.022,_ez-0.050),(0.016,0.018,0.016),-0.0026) for s_ in (1,-1)]+         # hollow cheeks
       [((s_*(_ex+0.030),_ey+0.030,_ez+0.012),(0.012,0.016,0.014),-0.0016) for s_ in (1,-1)]+         # sunken temples
       [((s_*(_ex+0.002),_ey-0.002,_ez+0.019),(0.022,0.016,0.008),0.0018) for s_ in (1,-1)]+          # brow ridge
       [((s_*_ex,_ey+0.006,_ez-0.002),(0.013,0.014,0.008),-0.0014) for s_ in (1,-1)]+                 # deeper sockets
       [((0,_n[1]+0.012,_n[2]+0.022),(0.008,0.02,0.010),0.0014)]+                                     # thin high nose bridge
       [((s_*0.040,_c[1]+0.040,_c[2]+0.016),(0.016,0.03,0.012),0.0014) for s_ in (1,-1)])             # jaw angle
L=landmarks()
PIECES=[]
def add(o,mat,wfn,kind='opaque'): PIECES.append((o,mat,wfn,kind)); return o
torso_b={S+n for n in ('Hips','Spine','Spine1','Spine2','LeftShoulder','RightShoulder')}
leg_b=lambda Lr:{S+Lr+n for n in ('UpLeg','Leg','Foot','ToeBase')}
domA=np.array(dom)
sel_torso=np.isin(domA,list(torso_b)); sel_neck=np.isin(domA,[S+'Neck'])
sel_legs=np.isin(domA,list(leg_b('Left')|leg_b('Right')))
cz=L['crotch_z']; ZB=1.03      # belt line
ZTOP=1.50                       # coat collar ring (neck base)
# ================= hose (dark wool) =================
zs=np.linspace(ZB+0.02,cz+0.035,12)
r=tube([Vector((0,0,z)) for z in zs],Z,sel_torso|sel_legs,64,0.006,center_fn=cen_bbox,smooth=2)
pelvis=grid_mesh('pelvis',r,wrap=True); close_tube(pelvis)
legs=[]
for Lr,sg in (('Left',1),('Right',-1)):
    up=bonesH[S+Lr+'UpLeg']; kn=bonesH[S+Lr+'Leg']; an=bonesH[S+Lr+'Foot']
    sel=np.isin(domA,list(leg_b(Lr)|{S+'Hips'}))&(side==sg)
    zs=np.linspace(cz+0.07,0.30,34); st=[];ax=[]
    for z in zs:
        if z>kn.z: t=(z-kn.z)/(up.z-kn.z); c=kn.lerp(up,t); a=(up-kn).normalized()
        else: t=(kn.z-z)/(kn.z-an.z); c=kn.lerp(an,t); a=(kn-an).normalized()
        st.append(c); ax.append(Vector((0,0,1)).lerp(a,0.6).normalized())
    r=tube(st,ax,sel&(P[:,2]>0.2),32,0.005,center_fn=cen_bbox,smooth=2)
    lo=grid_mesh('leg'+Lr,r,wrap=True); close_tube(lo); legs.append(lo)
for o in [pelvis]+legs: fix_normals_out(o)
hose=join([pelvis]+legs,'hose')
m=hose.modifiers.new('r','REMESH'); m.mode='VOXEL'; m.voxel_size=0.006; apply_mod(hose,m)
bm=bmesh.new(); bm.from_mesh(hose.data)
for pz,pn in ((ZB+0.02,(0,0,1)),(0.30,(0,0,-1))):
    bmesh.ops.bisect_plane(bm,geom=bm.verts[:]+bm.edges[:]+bm.faces[:],plane_co=(0,0,pz),plane_no=pn,clear_outer=True)
bm.to_mesh(hose.data); bm.free()
decimate(hose,1300)
crumple(hose,0.005,40,lambda c:ss(0.30,0.36,c.z)*(1-ss(0.44,0.52,c.z)),seed=3); crumple(hose,0.002,70,None,seed=6); push_out(hose,0.005)
add(hose,'wool_hose',w_bodyT(['Hips','LeftUpLeg','RightUpLeg','LeftLeg','RightLeg','Spine']))
HOSE_TREE=tree_of([hose])
# ================= long black wool coat: fitted body, split skirts to mid-calf, back vent, ragged hem =================
ZHEM=0.36
zs=np.linspace(ZTOP,ZB-0.03,15)
r=tube([Vector((0,0,z)) for z in zs],Z,sel_torso|sel_neck|sel_legs,40,lambda t,a:0.009+0.004*t,center_fn=cen_bbox,smooth=2,drape=False)
r=fold_rows(r,0.0025,6,ZTOP-0.15,ZB,seed=31)
coat=grid_mesh('coat',r,wrap=True); fix_normals_out(coat)
push_out(coat,0.006,[HOSE_TREE])
add(coat,'coat_wool',lambda c:(body_w(c,{S+n for n in ('Hips','Spine','Spine1','Spine2','Neck','LeftShoulder','RightShoulder','LeftArm','RightArm')}) or {S+'Spine1':1}))
# skirts: open tube (gap at the front) that hangs (radius never shrinks going down), flares, folds, spreads open at the front
zs2=np.concatenate([np.linspace(ZB+0.03,ZB-0.10,5),np.linspace(ZB-0.13,ZHEM,24)])
GAP=D(3)
r=tube([Vector((0,0,z)) for z in zs2],Z,sel_torso|sel_legs,52,lambda t,a:0.012+0.012*t,th_range=(D(90)+GAP,D(450)-GAP),center_fn=cen_bbox,smooth=2,drape=False)
c0=r[2].mean(0); nt=r.shape[1]
for i in range(3,len(zs2)):
    t=(zs2[2]-zs2[i])/(zs2[2]-ZHEM)
    for j in range(nt):
        v=r[i,j,:2]-c0[:2]; vp=r[i-1,j,:2]-c0[:2]
        rr=max(np.linalg.norm(v),np.linalg.norm(vp)*0.998)*(1+0.012*t)
        r[i,j,:2]=c0[:2]+v/max(np.linalg.norm(v),1e-6)*rr
for _ in range(2): r[1:-1]=0.5*r[1:-1]+0.25*(r[:-2]+r[2:])
r=fold_rows(r,0.014,8,ZB-0.05,ZHEM+0.1,seed=33,phase_drift=0.9)
for i in range(len(zs2)):   # front edges part toward the hem (inverted V) and turn back a little
    sp=0.075*ss(ZB-0.06,ZHEM,zs2[i])**0.8
    for j in range(nt):
        w=math.exp(-j/3.5)-math.exp(-(nt-1-j)/3.5)
        r[i,j,0]+=-sp*w if False else sp*(-math.exp(-j/3.5)+math.exp(-(nt-1-j)/3.5))
        r[i,j,1]+=0.25*sp*(math.exp(-j/3.5)+math.exp(-(nt-1-j)/3.5))
r=rag_hem(r,0.05,seed=34,rows=4,teeth=(2,5))
for i in range(len(zs2)):   # hem lifts slightly at the opening edges
    for j in (0,1,nt-2,nt-1): pass
skirt=grid_mesh('skirt',r); fix_normals_out(skirt)
bm=bmesh.new(); bm.from_mesh(skirt.data); bm.faces.ensure_lookup_table()
jb=int(np.argmax(r[len(zs2)//2,:,1])); dl=[]
for i_ in range(len(zs2)-1):   # back vent: one clean column strip open up the back seam
    if r[i_,jb,2]<0.80: dl.append(bm.faces[i_*(nt-1)+jb])
print('VENT col',jb,len(dl))
bmesh.ops.delete(bm,geom=dl,context='FACES'); bm.to_mesh(skirt.data); bm.free()
push_out(skirt,0.008,[HOSE_TREE]); solidify(skirt,0.004,offset=1); decimate(skirt,2500,sym=False)
add(skirt,'coat_wool',w_skirt(ZB,ZHEM,0.85,x_split=0.08))
COAT_TREE=tree_of([coat,skirt])
zV=ZTOP-0.11
# ================= sleeves + inked linen cuffs + cold-iron bands =================
def arm_chain(Lr,t0,t1,n):
    a=bonesH[S+Lr+'Arm']; f=bonesH[S+Lr+'ForeArm']; h=bonesH[S+Lr+'Hand']
    l1=(f-a).length; l2=(h-f).length; T=l1+l2; st=[];ax=[]
    for s_ in np.linspace(t0,t1,n):
        d=s_*T
        if d<l1: c=a.lerp(f,d/l1)
        else: c=f.lerp(h,(d-l1)/l2)
        w=ss(l1-0.05,l1+0.05,d); axv=((f-a).normalized()*(1-w)+(h-f).normalized()*w).normalized()
        st.append(c); ax.append(axv)
    return st,ax,l1/T
SLEEVE_END=0.84; CUFF=(0.74,0.955); BAND=0.90
cuff_trees={}
for Lr,sg in (('Left',1),('Right',-1)):
    sel=np.isin(domA,[S+Lr+'Arm',S+Lr+'ForeArm',S+Lr+'Hand',S+Lr+'Shoulder'])&(side==sg)
    end=SLEEVE_END if Lr=='Left' else SLEEVE_END-0.05
    st,ax,el=arm_chain(Lr,-0.05,end,22)
    def soff(t,a,el=el): return 0.012+0.006*t+0.004*math.sin(a*5)*t
    r=tube(st,ax,sel,26,soff,center_fn=cen_bbox,smooth=2)
    o=grid_mesh('sleeve'+Lr,r,wrap=True); fix_normals_out(o); push_out(o,0.005,[COAT_TREE])
    wsl=w_bodyT([Lr+'Arm',Lr+'ForeArm',Lr+'Shoulder',Lr+'Hand'])
    add(o,'coat_wool',wsl)
    if Lr=='Right':   # burned sleeve edge (the tome): charred, ragged ring
        st,ax,_=arm_chain(Lr,end-0.012,SLEEVE_END+0.005,4)
        r=tube(st,ax,sel,26,lambda t,a:0.0175+0.004*math.sin(a*5),center_fn=cen_bbox,smooth=1)
        for j in range(r.shape[1]):
            d=(r[-1,j]-r[0,j]); r[-1,j]=r[0,j]+d*RNG.uniform(0.15,1.0); r[-2,j]=r[0,j]+(r[-2,j]-r[0,j])*RNG.uniform(0.5,1.0)
        b=grid_mesh('burn'+Lr,r,wrap=True); fix_normals_out(b); push_out(b,0.004)
        add(b,'coat_burnt',wsl)
    # linen cuff, ink-stained, reaching past the wrist
    st,ax,_=arm_chain(Lr,CUFF[0],CUFF[1],8)
    r=tube(st,ax,sel,22,lambda t,a:0.016+0.010*t+0.002*math.sin(a*5),center_fn=cen_bbox,smooth=1)
    for j in range(r.shape[1]): r[-1,j]+= (r[-1,j]-r[-2,j])*RNG.uniform(-0.3,0.2)
    cf=grid_mesh('cuff'+Lr,r,wrap=True); fix_normals_out(cf); push_out(cf,0.004)
    def wc(c,Lr=Lr):
        f=bonesH[S+Lr+'ForeArm']; h=bonesH[S+Lr+'Hand']; t=(c-f).dot((h-f).normalized())/(h-f).length; k=ss(0.88,1.05,t)*0.6
        return {S+Lr+'ForeArm':1-k,S+Lr+'Hand':k}
    cf=solidify(cf,0.003,offset=1) or cf
    add(cf,'cuff_ink',wc); cuff_trees[Lr]=(tree_of([cf]),wc)
# ================= ragged capelet over the shoulders =================
sel_cap=sel_torso|sel_neck|(np.isin(domA,[S+'LeftArm',S+'RightArm',S+'LeftShoulder',S+'RightShoulder'])&(np.abs(P[:,0])<0.235))
zs=np.linspace(ZTOP+0.012,1.24,14)
r=tube([Vector((0,0,z)) for z in zs],Z,sel_cap,56,lambda t,a:0.022+0.014*t,center_fn=cen_bbox,smooth=3,drape=True)
r=fold_rows(r,0.009,9,ZTOP-0.05,1.26,seed=41,phase_drift=0.7)
r=rag_hem(r,0.045,seed=42,rows=3,teeth=(2,4))
cap=grid_mesh('capelet',r,wrap=True); fix_normals_out(cap)
push_out(cap,0.010,[COAT_TREE]+[tree_of([o]) for o,_,_,_ in PIECES if o.name.startswith('sleeve')])
solidify(cap,0.0035,offset=1); decimate(cap,1700,sym=False)
add(cap,'coat_capelet',w_bodyT(['Spine2','Neck','LeftShoulder','RightShoulder','LeftArm','RightArm']))
CAP_TREE=tree_of([cap])
# ================= hood, thrown back: bunched cowl round the neck + hood hanging on the back =================
zs=np.linspace(ZTOP+0.075,ZTOP-0.02,8)
def hoff(t,a):
    back=max(0.0,-math.sin(a)); return 0.016+0.020*back*(0.4+t)+0.006*t+0.003*math.sin(a*6)
r=tube([Vector((0,0,z)) for z in zs],Z,sel_torso|sel_neck,40,hoff,center_fn=cen_bbox,smooth=2,drape=True)
r=fold_rows(r,0.004,7,None,None,seed=43)
cowl=grid_mesh('cowl',r,wrap=True); fix_normals_out(cowl); push_out(cowl,0.008,[CAP_TREE]); solidify(cowl,0.004,offset=1)
add(cowl,'coat_capelet',w_bodyT(['Neck','Spine2','LeftShoulder','RightShoulder']))
# hood bag lying on the shoulder blades, narrowing to the point
zs=np.linspace(ZTOP+0.05,1.22,16)
hwh=lambda z:D(40)*(1-ss(ZTOP-0.02,1.21,z))**0.9+D(4)
em=sel_cap[EDG[:,0]]&sel_cap[EDG[:,1]]; EA_=P[EDG[em,0]]; EB_=P[EDG[em,1]]
rows=[]
for z in zs:
    pts=section(Vector((0,0,z)),Vector((0,0,1)),sel_cap,EA_,EB_); p2=pts[:,:2]*np.array([1,-1]); h=hull2d(p2); c=cen_bbox(p2); row=[]
    for a in np.linspace(D(270)-hwh(z),D(270)+hwh(z),18):
        rr=ray_r(h,c,a)+0.050+0.025*math.sin(math.pi*ss(ZTOP+0.05,1.22,z))*math.cos(a-D(270))
        row.append((c[0]+rr*math.cos(a),-(c[1]+rr*math.sin(a)),z))
    rows.append(np.array(row))
R=np.array(rows); R=fold_rows(R,0.005,2.5,None,None,seed=44)
hood=grid_mesh('hood',R); fix_normals_out(hood); push_out(hood,0.010,[CAP_TREE,tree_of([cowl])]); solidify(hood,0.004,offset=1)
add(hood,'coat_capelet',w_bodyT(['Spine2','Spine1','Neck']))
CAP_TREE=tree_of([cap,cowl,hood])
# ================= belt, pouch, ink horn, pen case; satchel with scrolls (right hip) on a cross strap =================
exec(open(SRC+'/lib_props.py').read())
st=[Vector((0,0,z)) for z in np.linspace(ZB+0.024,ZB-0.024,4)]
r=tube(st,Z,sel_torso|sel_legs,44,0.004,center_fn=cen_bbox,smooth=1)
belt=grid_mesh('belt',r,wrap=True); fix_normals_out(belt); push_out(belt,0.006,[COAT_TREE]); solidify(belt,0.005,offset=1)
add(belt,'leather_belt',w_bodyT(['Hips','Spine']))
BELT_TREE=tree_of([belt])
bp=surfp((0.0,0,ZB),(0,-1,0),0.005,0.3,tree=BELT_TREE)
bk=prim('cube',loc=bp,scale=(0.050,0.008,0.054))
bm=bmesh.new(); bm.from_mesh(bk.data); fr=[f for f in bm.faces if f.normal.y<-0.9]
bmesh.ops.inset_region(bm,faces=fr,thickness=0.009); bmesh.ops.translate(bm,vec=(0,0.006,0),verts=list({v for f in fr for v in f.verts})); bm.to_mesh(bk.data); bm.free()
pin=prim('cylinder',loc=bp+Vector((0.006,-0.006,0)),rot=(0,D(90),0),vertices=6,radius=0.0028,depth=0.034)
tongue=prim('cube',loc=bp+Vector((0.05,-0.002,0)),scale=(0.05,0.004,0.036))
add(join([bk,pin],'buckle'),'iron_dark',lambda c:{S+'Hips':1}); add(tongue,'leather_belt',lambda c:{S+'Hips':1})
RIV=[]
for nm,ang,w_,h_ in (('pouchL',D(-35),0.075,0.085),):
    dv=Vector((math.cos(ang),math.sin(ang),0))
    pc=surfp((0,0,ZB+0.015),dv,0.007,0.4,tree=BELT_TREE); pz=pouch(nm,pc,dv,w=w_,h=h_,d=0.035,flap=0.04)
    push_out(pz,0.006,[COAT_TREE]); add(pz,'leather_pouch',lambda c:{S+'Hips':1})
# ink horn + pen case hanging on thongs at the left front
ic=surfp((0.115,0,ZB-0.02),(0.45,-0.89,0),0.012,0.3,tree=COAT_TREE)
horn=prim('cone',loc=ic+Vector((0,-0.012,-0.085)),rot=(D(8),D(-6),0),vertices=8,radius1=0.010,radius2=0.019,depth=0.07)
cap_=prim('cylinder',loc=ic+Vector((0,-0.012,-0.046)),rot=(D(8),D(-6),0),vertices=8,radius=0.021,depth=0.012)
add(join([horn,cap_],'inkhorn'),'horn_ink',lambda c:{S+'Hips':0.7,S+'LeftUpLeg':0.3})
pcs=surfp((0.075,0,ZB-0.02),(0.2,-0.98,0),0.012,0.3,tree=COAT_TREE)
case=prim('cylinder',loc=pcs+Vector((0,-0.01,-0.11)),rot=(D(4),D(10),0),vertices=8,radius=0.011,depth=0.16)
ccap=prim('cylinder',loc=pcs+Vector((0,-0.01,-0.03)),rot=(D(4),D(10),0),vertices=8,radius=0.0125,depth=0.024)
add(join([case,ccap],'pencase'),'leather_dark',lambda c:{S+'Hips':0.7,S+'LeftUpLeg':0.3})
for q in (ic,pcs):
    th=strap('thong',[q+Vector((0,-0.004,0.03)),q+Vector((0,-0.008,-0.005)),q+Vector((0,-0.011,-0.035))],0.007,0.002,up=lambda p:Vector((0,-1,0)))
    add(th,'leather_dark',lambda c:{S+'Hips':1})
# satchel (right hip, character -X), soft leather bag with flap, scrolls sticking out the top
sdv=Vector((-0.94,-0.34,0)).normalized()
sc_=surfp((0,0,ZB-0.035),sdv,0.010,0.4,tree=COAT_TREE)
sat=pouch('satchel',sc_,sdv,w=0.18,h=0.20,d=0.085,flap=0.12)
crumple(sat,0.004,30,None,seed=9); push_out(sat,0.008,[COAT_TREE,BELT_TREE])
add(sat,'leather_satchel',lambda c:{S+'Hips':0.6,S+'RightUpLeg':0.4})
SAT_TREE=tree_of([sat])
sd_=Vector((0,0,1)).cross(sdv).normalized(); sco=[]
for k,(du,ln,rr,tilt) in enumerate(((-0.045,0.20,0.017,D(-8)),(-0.012,0.24,0.020,D(4)),(0.030,0.17,0.015,D(12)))):
    c=sc_+sdv*0.035+sd_*du+Vector((0,0,0.02))
    o=prim('cylinder',loc=c,vertices=8,radius=rr,depth=ln); o.data.transform(Matrix.Translation(-c)); o.data.transform(Matrix.Translation(c)@Matrix.Rotation(tilt,4,sdv))
    sco.append(o)
scr=join(sco,'scrolls'); add(scr,'parchment',lambda c:{S+'Hips':0.6,S+'RightUpLeg':0.4})
# cross strap: satchel (right hip) -> chest -> over the LEFT shoulder -> back -> satchel
tp=[sc_+Vector((0,0,0.0)),Vector((-0.17,-0.07,1.12)),Vector((-0.07,-0.125,1.26)),Vector((0.05,-0.13,1.37)),Vector((0.13,-0.09,1.45)),
    Vector((0.155,0.0,1.50)),Vector((0.12,0.08,1.46)),Vector((0.03,0.115,1.34)),Vector((-0.09,0.12,1.18)),Vector((-0.17,0.09,ZB+0.0)),sc_+Vector((0,0.02,0.0))]
pts=[]
for i_ in range(len(tp)-1):
    for t in np.linspace(0,1,4,endpoint=False): pts.append(tp[i_].lerp(tp[i_+1],t))
pts.append(tp[-1])
pts=[surfp(pp,(pp-Vector((0,0,pp.z))).normalized() if abs(pp.x)+abs(pp.y)>1e-3 else Vector((0,-1,0)),0.007,0.25,tree=tree_of([coat,cap,belt,hood,cowl])) for pp in pts]
o=strap('satstrap',pts,0.032,0.004,up=lambda p:(p-Vector((0,0,p.z))).normalized())
add(o,'leather_satchel',w_bodyT(['Spine2','Spine1','Spine','LeftShoulder','Hips']))
exec(open(SRC+'/lib_boot.py').read())
boots(0.40,shaft_off=0.008,foot_off=0.007,cuff=0.06,cuff_off=0.016,straps=(),slouch=0.010,heel=True,heel_h=0.008,budget=760,toe=0.007,crease=0.0045,cuff_budget=170)
exec(open(SRC+'/lib_head.py').read())
# ================= hair: dark, swept back, falling to the collar (strand cards) =================
hk=dict(front=0.060,temple=0.046,side=0.026,behind=-0.04,back=-0.10)
scalp=shell_from_body('hair',lambda c:scalp_mask(c,**hk),lambda c,m:0.0006+0.0040*sm(0.35,1.0,m)); decimate(scalp,440)
def rehedge(o,mfn):
    pts=np.array([bvh.find_nearest(v.co)[0][:] for v in o.data.vertices]); mk=mfn(pts); set_attr(o,'hedge',lambda c:mk)
rehedge(scalp,lambda c:scalp_mask(c,**hk))
ez=L['eye_z']; hc=Vector(L['head_c'])
def flow_q(p,n):
    x,y,z=p; dh=np.array([x,y-hc.y,0.0]); dh/=np.linalg.norm(dh)+1e-6
    if y<hc.y-0.035: return np.array([0.35*np.sign(x),1.0,0.15])+RNG.normal(0,0.10,3)       # swept back off the brow
    if z>ez+0.07: return np.array([0.55*dh[0],0.55*max(dh[1],0.45),-0.50])+RNG.normal(0,0.12,3)
    return np.array([0.40*dh[0],0.40*max(dh[1],0.0)+0.30,-1.0])+RNG.normal(0,0.08,3)
def len_q(p):
    x,y,z=p
    return 0.105+0.075*sm(ez+0.11,ez+0.02,np.array([z]))[0]+0.035*(y>hc.y)
hcards=hair_cards('hcards',lambda c:scalp_mask(c,**hk),210,len_q,0.025,4,flow_q,off0=0.004,off_gain=0.009,hang_z=ez+0.0,gravity=0.55,
                  seed=13,thresh=0.6,uspan=0.5,taper=0.45,curl=0.10,trees=[CAP_TREE],minoff=0.004,layer_fn=lambda p:0.003*(p[2]>ez+0.08))
# a few loose strands falling over the brow / temples
fl=None
hair=join([scalp,hcards],'hair')
add(hair,'hair_quill',w_bodyT(['Head','Neck']),'cards')
exec(open(SRC+'/lib_props.py').read())
# ================= keepsake: cold-iron wrist bands (both wrists) + signet ring turned inward =================
kparts=[]
for Lr,sg in (('Left',1),('Right',-1)):
    ct,wc=cuff_trees[Lr]
    sel=np.isin(domA,[S+Lr+'ForeArm',S+Lr+'Hand'])&(side==sg)
    st,ax,_=arm_chain(Lr,BAND-0.022,BAND+0.022,3)
    r=tube(st,ax,sel,18,0.016,center_fn=cen_bbox,smooth=1)
    b=grid_mesh('band'+Lr,r,wrap=True); fix_normals_out(b); push_out(b,0.0025,[ct]); solidify(b,0.004,offset=1)
    add(b,'iron_cold',wc)
r1=bonesH[S+'RightHandRing1']; r2=bonesH[S+'RightHandRing2']; fa=(r2-r1).normalized(); rc=r1.lerp(r2,0.45)
MRH=hand_frame('Right'); palm=Vector((MRH[0][2],MRH[1][2],MRH[2][2]))
rg=prim('torus',major_radius=0.0092,minor_radius=0.0017,major_segments=12,minor_segments=4)
rg.data.transform(Matrix.Translation(rc)@Vector((0,0,1)).rotation_difference(fa).to_matrix().to_4x4()); rg.data.update()
bz=prim('cube',scale=(0.0045,0.0045,0.0022))
bz.data.transform(Matrix.Translation(rc+palm*0.0105)@Vector((0,0,1)).rotation_difference(palm).to_matrix().to_4x4()); bz.data.update()
ring=join([rg,bz],'signet'); add(ring,'iron_signet',None,('prop','RightHandRing1','quill_keepsake'))
# ================= work prop: the quill pen (hidden except in work_write) =================
pen=cyl(0.0028,0.20,(0.045,0,0),'X',6)
for v in pen.data.vertices:
    t=(v.co.x+0.055)/0.20
    if t<0.12: v.co.y*=t/0.12; v.co.z*=t/0.12
vane=cyl(0.011,0.13,(0.085,0,0.0),'X',8)
for v in vane.data.vertices: v.co.z*=0.12; v.co.y*=1.0-0.6*abs((v.co.x-0.085)/0.065)
penm=join([pen,vane],'prop_quill')
# canonical: nib at x=-0.055 (pointing -X = toward the pinky side? no: we want the nib beyond the index side)
penm.data.transform(Matrix.Rotation(D(180),4,'Z')); penm.data.update()     # nib now at +0.055, feather toward -X
MR=hand_frame('Right'); place(penm,MR@Matrix.Translation((0.0,-0.012,-0.012)))
add(penm,'quill_feather',None,('prop','RightHand','quill_prop_quill'))
def make_mats():
    m_skin('skin_quill',L,tone=(0.66,0.56,0.49),mott=(0.58,0.46,0.41),lip=(0.48,0.34,0.32),red=0.22,socket=(0.30,0.22,0.22),socket_amt=0.6,
           brow=(0.10,0.09,0.085),brow_amt=0.85,stub=(0.20,0.18,0.17),stub_amt=0.6,ink=1.0,age=0.95,grime=0.35,skin_det=0.6)
    m_eye('eye_quill',L,iris=(0.30,0.28,0.22))
    m_cloth('wool_hose',(0.10,0.09,0.085),(0.06,0.055,0.05),grime=0.5,hem_z=0.30,hem_h=0.2,stain=0.4,sw='wool',sws=6.0,swamt=0.8,fold=1.0,foldv=3.0)
    m_cloth('coat_wool',(0.085,0.083,0.088),(0.045,0.044,0.048),grime=0.55,fade=((0.16,0.155,0.15),0.5),stain=0.45,hem_z=ZHEM,hem_h=0.26,
            dirt=(0.13,0.11,0.09),sw='wool',sws=4.5,swamt=0.95,fold=1.3,foldv=4.0,thread=(0.10,0.09,0.08),fray=(0.11,0.10,0.09))
    m_cloth('coat_capelet',(0.075,0.073,0.078),(0.04,0.039,0.043),grime=0.5,fade=((0.15,0.145,0.14),0.5),stain=0.45,
            dirt=(0.13,0.11,0.09),sw='wool',sws=4.5,swamt=0.95,fold=1.2,foldv=4.0,thread=(0.10,0.09,0.08),fray=(0.11,0.10,0.09))
    m_cloth('coat_burnt',(0.06,0.055,0.05),(0.03,0.028,0.025),grime=0.4,soot=1.0,rough=0.95,sw='wool',sws=4.5)
    m_cloth('linen_shirt',(0.44,0.40,0.34),(0.32,0.29,0.24),grime=0.6,stain=0.5,sw='linen',sws=7.0)
    m_cloth('cuff_ink',(0.07,0.085,0.15),(0.035,0.045,0.09),grime=0.45,stain=0.4,ink=1.0,sw='wool',sws=5.0,swamt=0.9,fold=1.2,thread=(0.12,0.12,0.16))
    m_leather('leather_belt',(0.15,0.095,0.055),wear=0.75,rough=0.52,oil=0.7)
    m_leather('leather_satchel',(0.21,0.13,0.075),wear=0.85,rough=0.58,oil=0.6,fold=1.0)
    m_leather('leather_pouch',(0.17,0.105,0.06),wear=0.8,rough=0.56,oil=0.5)
    m_leather('leather_dark',(0.09,0.065,0.045),wear=0.6,rough=0.55)
    m_leather('leather_boot',(0.13,0.09,0.062),wear=0.85,rough=0.6,oil=0.4,fold=1.1)
    m_leather('leather_sole',(0.06,0.045,0.035),wear=0.3,rough=0.8,stitch=True,oil=0.1)
    m_iron('iron_dark',rust=0.4); m_iron('iron_cold',col=(0.085,0.085,0.09),rust=0.15,rough=0.62); m_iron('iron_signet',col=(0.16,0.15,0.13),rust=0.05,rough=0.4)
    m_flat('quill_feather',(0.55,0.52,0.47),rough=0.7)
    m_flat('parchment',(0.62,0.55,0.42),rough=0.8)
    m_flat('horn_ink',(0.20,0.15,0.10),rough=0.35)
    m_hair('hair_quill',(0.075,0.068,0.062),grey=0.35,stretch=(1,1,1),scale=650)
if STAGE=='fit':
    exec(open(SRC+'/lib_fit.py').read())
    os.makedirs(SRC+'/work/fit',exist_ok=True)
    fit_render(SRC+'/work/fit/quill')
    fit_render(SRC+'/work/fit/quill_face',views=(('front',0),('q',40),('back',180)),focus=((0,-0.06,1.60),0.75),res=(600,600))
    for o,mat,wfn,kind in PIECES: print('PIECE',o.name,mat,kind,tris(o))
    sys.exit(0)
make_mats(); exec(open(SRC+'/lib_fin.py').read())
OUT=SRC+'/work/'+NAME; os.makedirs(OUT,exist_ok=True)
def _tip(Lr,f):
    k3=bonesH[S+Lr+'Hand'+f+'3']; k4=bonesH.get(S+Lr+'Hand'+f+'4'); k2=bonesH[S+Lr+'Hand'+f+'2']
    return np.array((k4 if k4 is not None else k3+(k3-k2))[:]), np.array(k3[:])
INK_PTS=[(_tip('Right',f),1.0) for f in ('Index','Middle','Thumb')]+[(_tip('Left',f),0.6) for f in ('Index','Thumb')]
def ink_fn(c):
    m=np.zeros(len(c))
    for (tp,k3),amt in INK_PTS:
        for q,r_ in ((tp,0.016),(0.5*(tp+k3),0.014)):
            d=np.linalg.norm(c-q,axis=1); m=np.maximum(m,amt*(1-sm(r_*0.6,r_,d)))
    return m
hk_lo={k:v-0.007 for k,v in hk.items()}
stub_fn=lambda c:np.clip(np.maximum(beard_mask(c)*0.9,scalp_mask(c,**hk_lo)*0.9),0,1)
for o,mat,wfn,kind in PIECES:
    tgt={'belt':440,'cuffLeft':300,'cuffRight':300,'coat':1100,'cowl':500,'hood':500,'sleeveLeft':720,'sleeveRight':720,'hose':1100}.get(o.name)
    if tgt: decimate(o,tgt,sym=False); push_out(o,0.004)
def slot_fn(o,m):
    if m=='wool_hose': return 'legs'
    if m=='iron_cold': return 'hands'
    if max((o.matrix_world@Vector(c)).z for c in o.bound_box)<0.58: return 'feet'
    return 'torso'
main,cards,kp,pro,imgs,mats=finalize(NAME,BODY_BUDGET,inner_hide=[],slot_fn=slot_fn,
    body_attrs={'stubble':stub_fn,'ink':ink_fn},strip=False,out=OUT)
parts=finish_export(NAME,main,cards,kp,pro,OUT+'/raw.glb',OUT,cards_mats={'hair_quill'})
write_meta(NAME,parts,pro,OUT)
