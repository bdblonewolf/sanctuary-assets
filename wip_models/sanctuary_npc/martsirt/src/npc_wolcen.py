# Wolcen the smith -- geometry, weights, masks. Then lib_fin.py does UV/bake/export.
import sys
SRC='/workspace/sanctuary_npc/martsirt/src'
exec(open(SRC+'/lib_bl.py').read()); exec(open(SRC+'/lib_mat.py').read())
NAME='wolcen'; BODY_BUDGET=int(os.environ.get('BODY_BUDGET','10500')); STAGE=sys.argv[-1] if len(sys.argv)>1 else 'fit'
init_body(SRC+'/bodies/male_brute_heavy.glb'); L=landmarks()
exec(open(SRC+'/lib_detail.py').read())
# face character (pipeline copy only): heavy brow ridge, once-broken nose, broad jaw, deeper eye sockets
_ez=L['eye_z']; _ey=L['eyeL_front'][1]; _ex=L['eye_x']; _n=L['nose']; _c=L['chin']
sculpt([((s_*(_ex+0.004),_ey-0.004,_ez+0.021),(0.026,0.02,0.010),0.0032) for s_ in (1,-1)]+
       [((s_*_ex,_ey+0.006,_ez-0.002),(0.014,0.015,0.008),-0.0018) for s_ in (1,-1)]+
       [((0,_n[1]+0.014,_n[2]+0.024),(0.011,0.02,0.009),0.0022,(0.0012,0,0)),
        ((0,_n[1]+0.004,_n[2]+0.002),(0.018,0.02,0.012),0.0015)]+
       [((s_*0.048,_c[1]+0.035,_c[2]+0.018),(0.028,0.035,0.022),0.0030) for s_ in (1,-1)]+
       [((s_*0.040,_ey+0.012,_ez-0.034),(0.02,0.02,0.012),-0.0015) for s_ in (1,-1)])
L=landmarks()
PIECES=[]   # (obj, material name, weight fn, kind) kind: 'opaque'|'cards'|'keepsake'|('prop',bone)
def add(o,mat,wfn,kind='opaque'): PIECES.append((o,mat,wfn,kind)); return o
torso_b={S+n for n in ('Hips','Spine','Spine1','Spine2','LeftShoulder','RightShoulder')}
leg_b=lambda Lr:{S+Lr+n for n in ('UpLeg','Leg','Foot','ToeBase')}
domA=np.array(dom)
sel_torso=np.isin(domA,list(torso_b))
sel_legs=np.isin(domA,list(leg_b('Left')|leg_b('Right')))
cz=L['crotch_z']
# ================= trousers (dark wool) =================
zs=np.linspace(1.17,cz+0.035,16)
r=tube([Vector((0,0,z)) for z in zs],Z,sel_torso|sel_legs,72,lambda t,a:0.007+0.004*t,center_fn=cen_bbox,smooth=2)
pelvis=grid_mesh('pelvis',r,wrap=True); close_tube(pelvis)
legs=[]
for Lr,sg in (('Left',1),('Right',-1)):
    up=bonesH[S+Lr+'UpLeg']; kn=bonesH[S+Lr+'Leg']; an=bonesH[S+Lr+'Foot']
    sel=np.isin(domA,list(leg_b(Lr)|{S+'Hips'}))&(side==sg)
    zs=np.linspace(cz+0.07,0.30,40); st=[];ax=[]
    for z in zs:
        if z>kn.z: t=(z-kn.z)/(up.z-kn.z); c=kn.lerp(up,t); a=(up-kn).normalized()
        else: t=(kn.z-z)/(kn.z-an.z); c=kn.lerp(an,t); a=(kn-an).normalized()
        st.append(c); ax.append(Vector((0,0,1)).lerp(a,0.6).normalized())
    def off(t,a): return 0.009+0.004*math.sin(t*math.pi)
    r=tube(st,ax,sel&(P[:,2]>0.2),40,off,center_fn=cen_bbox,smooth=2)
    lo=grid_mesh('leg'+Lr,r,wrap=True); close_tube(lo); legs.append(lo)
for o in [pelvis]+legs: fix_normals_out(o)
trous=join([pelvis]+legs,'trousers')
# bridge the crotch gap: voxel remesh unites pelvis + legs into one clean shell
m=trous.modifiers.new('r','REMESH'); m.mode='VOXEL'; m.voxel_size=0.006; apply_mod(trous,m)
bm=bmesh.new(); bm.from_mesh(trous.data)
for pz,pn in ((1.17,(0,0,1)),(0.30,(0,0,-1))):
    bmesh.ops.bisect_plane(bm,geom=bm.verts[:]+bm.edges[:]+bm.faces[:],plane_co=(0,0,pz),plane_no=pn,clear_outer=True)
bm.to_mesh(trous.data); bm.free()
decimate(trous,1450)
def _tmask(c):
    return max(ss(0.42,0.50,c.z)*(1-ss(0.58,0.66,c.z)),ss(0.30,0.34,c.z)*(1-ss(0.40,0.46,c.z)))
crumple(trous,0.006,38,_tmask,seed=2); crumple(trous,0.0025,70,None,seed=4)
push_out(trous,0.006)
add(trous,'wool_trousers',w_bodyT(['Hips','LeftUpLeg','RightUpLeg','LeftLeg','RightLeg','Spine']))
# ================= sleeveless linen shirt =================
ZT=L['chin'][2]-0.075; print('SHIRT_TOP',ZT,'chin',L['chin'][2])
zs=np.linspace(ZT,1.03,21)
sh_sel=sel_torso|np.isin(domA,[S+'Neck'])
def soff(t,a): return 0.006+0.004*t
r=tube([Vector((0,0,z)) for z in zs],Z,sh_sel,36,soff,center_fn=cen_bbox,smooth=2)
r=fold_rows(r,0.004,7,1.42,1.10,seed=21)
# collar: pull the top ring in onto the neck base
shirt=grid_mesh('shirt',r,wrap=True); fix_normals_out(shirt)
bm=bmesh.new(); bm.from_mesh(shirt.data); bm.faces.ensure_lookup_table()
zt=1.735; zV=zt-0.13; dl=[]
for f in bm.faces:
    c=f.calc_center_median()
    pass   # crew neck: the stair-stepped V cut read as jagged plates
bmesh.ops.delete(bm,geom=list(set(dl)),context='FACES'); bm.to_mesh(shirt.data); bm.free()
push_out(shirt,0.005)
add(shirt,'linen_shirt',w_bodyT(['Spine2','Spine1','Spine','Hips','LeftShoulder','RightShoulder','Neck','LeftArm','RightArm']))
# ragged rolled cap at each armhole: short tube around the upper arm root
for Lr,sg in (('Left',1),('Right',-1)):
    a=bonesH[S+Lr+'Arm']; b=bonesH[S+Lr+'ForeArm']; ax=(b-a).normalized()
    sel=np.isin(domA,[S+Lr+'Arm',S+Lr+'Shoulder'])&(side==sg)
    la=(b-a).length; sel=np.isin(domA,[S+Lr+'Arm',S+Lr+'ForeArm'])&(side==sg)
    st=[a+ax*t for t in np.linspace(0.03*la,0.62*la,12)]
    r=tube(st,ax,sel,22,lambda t,an:0.008+0.006*t+0.0025*math.sin(an*3+t*11)*t,center_fn=cen_bbox,smooth=1)
    o=grid_mesh('sleeve'+Lr,r,wrap=True); fix_normals_out(o); push_out(o,0.006)
    add(o,'linen_shirt',w_bodyT([Lr+'Arm',Lr+'Shoulder','Spine2']))
    st=[a+ax*t for t in np.linspace(0.55*la,0.70*la,7)]   # thick rolled-up cuff
    r=tube(st,ax,sel,22,lambda t,an:0.011+0.011*math.sin(math.pi*t)**0.7+0.002*math.sin(an*4+1),center_fn=cen_bbox,smooth=0)
    o=grid_mesh('roll'+Lr,r,wrap=True); close_tube(o); fix_normals_out(o); push_out(o,0.007)
    add(o,'linen_shirt',w_bodyT([Lr+'Arm',Lr+'ForeArm']))
SHIRT_TREE=tree_of([shirt])
# ================= scorched leather apron (panel) =================
def panel(zs,hw_fn,off_fn,sel,nth=30,hang_below=None,flare=0.0,ac=D(90),hang_dir=-1):
    em=sel[EDG[:,0]]&sel[EDG[:,1]]; EA=P[EDG[em,0]]; EB=P[EDG[em,1]]
    rows=[]
    for i,z in enumerate(zs):
        pts=section(Vector((0,0,z)),Vector((0,0,1)),sel,EA,EB); p2=pts[:,:2]*np.array([1,-1])   # (x, -y): angle 90 = front
        h=hull2d(p2); c=cen_bbox(p2); hw=hw_fn(z)
        row=[]
        for a in np.linspace(ac-hw,ac+hw,nth):
            rr=ray_r(h,c,a)+off_fn(z,a)
            row.append((c[0]+rr*math.cos(a),-(c[1]+rr*math.sin(a)),z))
        rows.append(np.array(row))
    R=np.array(rows)
    if hang_below is not None:   # below the belly the panel hangs instead of following the body in
        for i in range(1,len(zs)):
            if zs[i]<hang_below:
                R[i,:,1]=np.minimum(R[i,:,1],R[i-1,:,1]+0.0015) if hang_dir<0 else np.maximum(R[i,:,1],R[i-1,:,1]-0.0015)
                if flare: R[i,:,0]=R[i,:,0]*(1+flare*(zs[i-1]-zs[i]))
    return R
zs=np.linspace(1.56,0.53,34)
def hw(z):
    if z>1.32: return D(30)
    if z>1.16: return D(30)+(D(78)-D(30))*ss(1.32,1.16,z)
    return D(78)
sel_ap=sel_torso|sel_legs
R=panel(zs,hw,lambda z,a:0.016,sel_ap,nth=30,hang_below=1.22,flare=0.10)
if os.environ.get('DBG'):
    for i in range(0,len(zs),3): print('ROW',round(zs[i],3),np.round(R[i,::6],3).tolist())
# smooth vertical profile
for _ in range(3): R[1:-1]=0.5*R[1:-1]+0.25*(R[:-2]+R[2:])
R=fold_rows(R,0.011,2.6,1.14,0.80,seed=7,phase_drift=0.8)
R=rag_hem(R,0.05,seed=11,rows=4,teeth=(2,5))
apron=grid_mesh('apron',R); fix_normals_out(apron)
burn_holes(apron,[(0.07,-0.2,0.74),(-0.11,-0.2,0.66),(0.02,-0.2,0.62),(-0.05,-0.2,0.93)],[0.016,0.022,0.013,0.010])
push_out(apron,0.014,[SHIRT_TREE]); solidify(apron,0.005,offset=1); decimate(apron,2300)
# back panel (smock back, under the crossed straps)
zs2=np.linspace(1.50,0.58,24)
def hw2(z): return D(36) if z>1.30 else D(36)+(D(66)-D(36))*ss(1.30,1.14,z)
R2=panel(zs2,hw2,lambda z,a:0.016,sel_ap,nth=22,hang_below=1.05,flare=0.06,ac=D(270),hang_dir=1)
for _ in range(3): R2[1:-1]=0.5*R2[1:-1]+0.25*(R2[:-2]+R2[2:])
R2=fold_rows(R2,0.009,2.2,1.05,0.75,seed=8,phase_drift=0.6); R2=rag_hem(R2,0.04,seed=12,rows=3)
apb=grid_mesh('apron_back',R2); fix_normals_out(apb); push_out(apb,0.014,[SHIRT_TREE]); solidify(apb,0.005,offset=1); decimate(apb,1100)
add(apb,'leather_apron',lambda c:(body_w(c,{S+n for n in ('Hips','Spine','Spine1','Spine2')}) or {S+'Spine':1}) if c.z>1.12 else
    {S+'Hips':1-ss(1.05,0.6,c.z)*0.5,S+'LeftUpLeg':ss(1.05,0.6,c.z)*0.5*ss(-0.08,0.08,c.x),S+'RightUpLeg':ss(1.05,0.6,c.z)*0.5*(1-ss(-0.08,0.08,c.x))})
def w_apron(c):
    if c.z>1.15: w=body_w(c,{S+n for n in ('Hips','Spine','Spine1','Spine2')}); return w or {S+'Spine':1}
    t=ss(1.10,0.55,c.z)*0.5; l=ss(-0.08,0.08,c.x)
    return {S+'Hips':1-t,S+'LeftUpLeg':t*l,S+'RightUpLeg':t*(1-l)}
add(apron,'leather_apron',w_apron)
APRON_TREE=tree_of([apron,apb])
RIV=[]
# neck straps of the apron (flat leather)
for sg in (1,-1):
    top=R[0,0 if sg>0 else -1]; top=Vector(top)
    btop=Vector(R2[0,-1 if sg>0 else 0])
    tp=[top+Vector((0,0,-0.01)),Vector((sg*0.115,-0.12,1.62)),Vector((sg*0.10,-0.05,1.72)),Vector((sg*0.065,0.03,1.745)),Vector((sg*0.02,0.10,1.66)),Vector((-sg*0.06,0.12,1.56)),btop+Vector((0,0,0.012))]
    RIV.append((top+Vector((0,-0.006,-0.018)),(0,-1,0))); RIV.append((btop+Vector((0,0.006,0.0)),(0,1,0)))
    pts=[]
    for i in range(len(tp)-1):
        for t in np.linspace(0,1,5,endpoint=False): pts.append(tp[i].lerp(tp[i+1],t))
    pts.append(tp[-1])
    pts=[surfp(pp,(pp-Vector((0,-0.01,1.6))).normalized(),0.009,0.2,tree=SHIRT_TREE) if i>0 else pp for i,pp in enumerate(pts)]
    o=strap('apstrap',pts,0.026,0.003,up=lambda p:(p-Vector((0,-0.01,1.55))).normalized())
    add(o,'leather_apron',w_bodyT(['Spine2','Neck','Spine1']))
# ================= wide belt + iron buckle =================
zb=1.165
st=[Vector((0,0,z)) for z in np.linspace(zb+0.036,zb-0.036,5)]
r=tube(st,Z,sel_torso|sel_legs,44,0.004,center_fn=cen_bbox,smooth=1)
belt=grid_mesh('belt',r,wrap=True); fix_normals_out(belt); push_out(belt,0.006,[APRON_TREE,tree_of([trous])])
solidify(belt,0.006,offset=1)
add(belt,'leather_belt',w_bodyT(['Hips','Spine']))
BELT_TREE=tree_of([belt])
bp=surfp((0,0,zb),(0,-1,0),0.006,0.3,tree=BELT_TREE)
bk=prim('cube',loc=bp,scale=(0.085,0.012,0.08))
bm=bmesh.new(); bm.from_mesh(bk.data); fr=[f for f in bm.faces if f.normal.y<-0.9]
bmesh.ops.inset_region(bm,faces=fr,thickness=0.014); bmesh.ops.translate(bm,vec=(0,0.009,0),verts=list({v for f in fr for v in f.verts})); bm.to_mesh(bk.data); bm.free()
pin=prim('cylinder',loc=bp+Vector((0.012,-0.008,0)),rot=(0,D(90),0),vertices=8,radius=0.004,depth=0.05)
add(join([bk,pin],'buckle'),'iron_dark',lambda c:{S+'Hips':1})
for nm,ang,w_,h_ in (('pouchL',D(-28),0.10,0.11),('pouchR',D(150),0.08,0.09)):
    dv=Vector((math.cos(ang),-math.sin(ang),0)) if False else Vector((math.cos(ang),math.sin(ang),0))
    pc=surfp((0,0,zb+0.02),dv,0.008,0.4,tree=BELT_TREE); pz=pouch(nm,pc,dv,w=w_,h=h_)
    push_out(pz,0.008,[APRON_TREE]); add(pz,'leather_pouch',lambda c:{S+'Hips':1})
for k in range(10):
    a_=D(-75+k*35); dv=Vector((math.cos(a_),math.sin(a_),0))
    if abs(math.degrees(a_)+90)<25 or abs(math.degrees(a_)-270)<20: continue
    RIV.append((surfp((0,0,zb+0.022),dv,0.006,0.4,tree=BELT_TREE),dv)); RIV.append((surfp((0,0,zb-0.022),dv,0.006,0.4,tree=BELT_TREE),dv))
add(rivets('rivets',[p for p,n in RIV],[n for p,n in RIV]),'iron_dark',w_bodyT(['Hips','Spine','Spine2']))
# hanging tongs on the right hip (static, part of the outfit)
# apron loop (left hip) for the keepsake hammer
lc=surfp((0.15,0,zb),(0.55,-0.83,0),0.006,0.3,tree=BELT_TREE)
lp=prim('torus',loc=lc+Vector((0,-0.006,-0.035)),rot=(D(90),0,D(-30)),major_radius=0.016,minor_radius=0.0045,major_segments=10,minor_segments=5)
add(lp,'leather_belt',lambda c:{S+'Hips':1})
exec(open(SRC+'/lib_boot.py').read())
boots(0.42,shaft_off=0.008,foot_off=0.009,cuff=0.05,cuff_off=0.015,straps=(0.32,0.17),budget=740,toe=0.008,cuff_budget=170,crease=0.004)
# ================= bracers (leather gauntlet cuffs, bare hands) =================
for Lr,sg in (('Left',1),('Right',-1)):
    a=bonesH[S+Lr+'ForeArm']; b=bonesH[S+Lr+'Hand']; ax=(b-a)
    sel=np.isin(domA,[S+Lr+'ForeArm',S+Lr+'Hand'])&(side==sg)
    st=[a+ax*t for t in np.linspace(0.30,0.98,30)]
    r=tube(st,ax.normalized(),sel,20,lambda t,an,sg=sg:0.005+0.008*t**2+0.0028*max(0.0,math.sin(sg*an+t*6.283*6.5))**0.6,center_fn=cen_bbox,smooth=1)
    o=grid_mesh('bracer'+Lr,r,wrap=True); fix_normals_out(o); push_out(o,0.005); solidify(o,0.003)
    def wb(c,Lr=Lr,a=a,b=b):
        t=(c-a).dot((b-a).normalized())/(b-a).length; h=ss(0.85,1.02,t)*0.5
        return {S+Lr+'ForeArm':1-h,S+Lr+'Hand':h}
    add(o,'leather_bracer',wb)
    BT=tree_of([o])
    for t in (0.64,):
        c=a+ax*t; pts=wrap_ring(c,ax.normalized(),0.002,16,BT,reach=0.15)
        s_=strap('brstrap',pts+[pts[0]],0.014,0.003,up=lambda p,c=c,ax=ax:((p-c)-ax.normalized()*(p-c).dot(ax.normalized())).normalized())
        add(s_,'leather_dark',wb)
exec(open(SRC+'/lib_head.py').read())
# ================= hair: short dark-grey crop + back braid, braided full beard (strand cards) =================
hk=dict(front=0.050,temple=0.038,side=0.026,behind=-0.03,back=-0.09)
scalp=shell_from_body('hair',lambda c:scalp_mask(c,**hk),lambda c,m:0.0005+0.0030*sm(0.35,1.0,m)); decimate(scalp,380)
def rehedge(o,mfn):   # decimation drops attributes: re-evaluate the mask at the nearest body point
    pts=np.array([bvh.find_nearest(v.co)[0][:] for v in o.data.vertices]); mk=mfn(pts); set_attr(o,'hedge',lambda c:mk)
rehedge(scalp,lambda c:scalp_mask(c,**hk))
hc=Vector(L['head_c'])
def flow_scalp(p,n):
    x,y,z=p; up=z-L['eye_z']
    if y<hc.y-0.035 and up>0.045: return np.array([0.3*np.sign(x),1.0,0.25])+RNG.normal(0,0.10,3)   # fringe swept back, never over the brow
    return np.array([0.25*np.sign(x)*(abs(x)>0.04),1.0,-0.25-0.9*(up<0.06)])+RNG.normal(0,0.18,3)
hcards=hair_cards('hcards',lambda c:scalp_mask(c,**hk),170,lambda p:0.032+0.012*(p[2]<L['eye_z']+0.05),0.016,3,flow_scalp,
                  off0=0.0035,off_gain=0.0035,seed=3,thresh=0.65,uspan=0.45)
# back braid: from the crown down the back of the skull, hanging onto the nape
bp_=[]
for t in np.linspace(D(55),D(150),7):
    d=Vector((0,math.sin(t),math.cos(t))); bp_.append(surfp(hc,d,0.010,0.3))
bp_+= [bp_[-1]+Vector((0,0.012,-0.05)),bp_[-1]+Vector((0,0.02,-0.10))]
hbraid=braid('hbraid',bp_,0.013,0.009,lobes=7,seg=5,ring=4); push_out(hbraid,0.006)
hair=join([scalp,hcards,hbraid],'hair')
bmask=lambda c:beard_mask(c)
def boff(c,m):
    x,y,z,phi=face_frame(c); ch=L['chin']; mo=L['mouth']
    chin=sm(mo[2]-0.01,ch[2]-0.01,z)*(1-sm(0.02,0.07,np.abs(x)))
    return sm(0.25,1.0,m)*(0.0035+0.016*chin)+0.0005
beard=shell_from_body('beard',bmask,boff); decimate(beard,420); rehedge(beard,bmask)
def flow_beard(p,n):
    x=p[0]; up=p[2]-L['mouth'][2]
    if up>-0.004 and abs(x)<0.035: return np.array([np.sign(x)*0.9,-0.1,-1.0])   # moustache sweeps out/down
    return np.array([np.sign(x)*0.12,-0.25,-1.0])+RNG.normal(0,0.15,3)
ch=L['chin']
bcards=hair_cards('bcards',lambda c:beard_mask(c),165,lambda p:0.022+0.040*sm(ch[2]+0.05,ch[2]-0.01,np.array([p[2]]))[0]*(1-sm(0.02,0.06,np.array([abs(p[0])]))[0]),
                  0.014,3,flow_beard,off0=0.004,off_gain=0.004,hang_z=ch[2]+0.012,gravity=0.6,seed=5,thresh=0.6,uspan=0.4)
cb0=Vector((0,ch[1]-0.016,ch[2]-0.030)); cbp=[cb0,cb0+Vector((0,-0.006,-0.04)),cb0+Vector((0,-0.004,-0.085))]
cbraid=braid('cbraid',cbp,0.011,0.007,lobes=5,seg=5,ring=4)
ring=prim('torus',loc=cb0+Vector((0,-0.006,-0.062)),major_radius=0.0105,minor_radius=0.0028,major_segments=10,minor_segments=4)
def brow_mask(c):
    x,y,z,phi=face_frame(c); ex=L['eye_x']; ez=L['eye_z']
    e=((np.abs(x)-ex-0.002)/0.022)**2+((z-ez-0.019+0.004*((np.abs(x)-ex)/0.02))/0.0055)**2
    return np.clip(1.4-e,0,1)*(phi<70)
brows=hair_cards('brows',brow_mask,50,lambda p:0.011,0.007,2,lambda p,n:np.array([np.sign(p[0]),-0.1,0.3]),off0=0.0012,off_gain=0.001,seed=8,thresh=0.5,uspan=0.3)
beard=join([beard,bcards,cbraid,brows],'beard')
add(hair,'hair_wolcen',w_bodyT(['Head']),'cards'); add(beard,'beard_wolcen',w_bodyT(['Head','Neck']),'cards')
add(ring,'iron_dark',lambda c:{S+'Head':1},'cards')
exec(open(SRC+'/lib_props.py').read())
# ================= keepsake: Odder's small hammer through the apron loop (left hip) =================
w,i=make_hammer('odder',handle=0.22,head=0.085,grip_frac=0.0,face_r=0.012)
# canonical: shaft +X from origin (butt) ; hang: head up at the loop, shaft pointing down
Mk=Matrix.Translation(lc+Vector((0.002,-0.016,-0.02)))@Matrix.Rotation(D(-30),4,'Z')@Matrix.Rotation(D(-90),4,'Y')@Matrix.Translation((-0.21,0,0))
place(w,Mk); place(i,Mk)
for o in (w,i): push_out(o,0.006,[APRON_TREE])
add(w,'wood_handle',None,('prop','Hips','wolcen_keepsake')); add(i,'iron_tool',None,('prop','Hips','wolcen_keepsake'))
# ================= work props (hidden except in the hammer clip) =================
w,i=make_hammer('prop_hammer',handle=0.36,head=0.13,grip_frac=0.22)
MR=hand_frame('Right'); place(w,MR); place(i,MR)
add(w,'wood_handle',None,('prop','RightHand','wolcen_prop_hammer')); add(i,'iron_tool',None,('prop','RightHand','wolcen_prop_hammer'))
# static hanging tongs on the right hip
ht,hb=make_tongs('belt_tongs'); bpy.data.objects.remove(hb)
hp=surfp((-0.16,0,zb),(-0.62,-0.78,0),0.008,0.3,tree=BELT_TREE)
place(ht,Matrix.Translation(hp+Vector((0,-0.02,0.02)))@Matrix.Rotation(D(28),4,'Z')@Matrix.Rotation(D(96),4,'Y')@Matrix.Translation((0.04,0,0)))
push_out(ht,0.008,[APRON_TREE,BELT_TREE])
add(ht,'iron_tool',w_skirt(1.14,0.85,0.25))
t,bar=make_tongs('prop_tongs'); ML=hand_frame('Left'); place(t,ML); place(bar,ML)
add(t,'iron_tool',None,('prop','LeftHand','wolcen_prop_tongs')); add(bar,'iron_hot',None,('prop','LeftHand','wolcen_prop_tongs'))
def make_mats():
    m_skin('skin_wolcen',L,tone=(0.64,0.52,0.44),mott=(0.56,0.42,0.36),lip=(0.46,0.32,0.29),red=0.2,socket=(0.32,0.22,0.2),socket_amt=0.3,
           brow=(0.10,0.09,0.08),brow_amt=0.9,stub=(0.17,0.15,0.13),stub_amt=0.7,soot=0.85,age=0.9,grime=0.45,skin_det=0.6)
    m_eye('eye_wolcen',L,iris=(0.27,0.29,0.28))
    m_cloth('wool_trousers',(0.15,0.13,0.11),(0.09,0.08,0.07),grime=0.6,hem_z=0.30,hem_h=0.25,stain=0.5,soot=0.5,sw='wool',sws=5.0,swamt=0.8,fold=1.0,foldv=3.0)
    m_cloth('linen_shirt',(0.52,0.46,0.36),(0.38,0.33,0.26),grime=0.75,stain=0.6,soot=0.6,dirt=(0.22,0.18,0.14),sw='linen',sws=7.0,swamt=0.9,fold=1.3,foldv=4.0)
    m_leather('leather_apron',(0.24,0.14,0.075),scorch=1.0,wear=0.7,rough=0.58,soot=0.55,sw='leather_apron',sws=3.0,swamt=0.95,oil=0.7,fold=0.8,burns=0.9)
    m_leather('leather_belt',(0.17,0.10,0.055),wear=0.75,rough=0.52,oil=0.8)
    m_leather('leather_pouch',(0.19,0.115,0.06),wear=0.8,rough=0.55,oil=0.6,soot=0.3)
    m_leather('leather_boot',(0.15,0.10,0.065),wear=0.85,rough=0.6,soot=0.45,oil=0.4,fold=1.0)
    m_leather('leather_sole',(0.06,0.045,0.035),wear=0.3,rough=0.8,stitch=True,oil=0.1)
    m_leather('leather_dark',(0.09,0.065,0.045),wear=0.6,rough=0.55)
    m_leather('leather_bracer',(0.20,0.12,0.065),scorch=0.6,wear=0.75,soot=0.5,fold=1.2,oil=0.6)
    m_iron('iron_dark',rust=0.45); m_iron('iron_tool',rust=0.3,rough=0.5)
    m_iron('iron_hot',rust=0.0,hot=lambda s_: s_.mapr(s_.noise(30,3,0.5),0.2,0.8,0.75,1.0))
    m_wood('wood_handle',(0.20,0.13,0.08),axis='X')
    m_hair('hair_wolcen',(0.15,0.13,0.11),grey=0.45,stretch=(1,1,1),scale=700)
    m_hair('beard_wolcen',(0.17,0.13,0.10),grey=0.4,stretch=(1.5,1.5,0.25),scale=500)
if STAGE=='fit':
    exec(open(SRC+'/lib_fit.py').read())
    os.makedirs(SRC+'/work/fit',exist_ok=True)
    fit_render(SRC+'/work/fit/wolcen')
    fit_render(SRC+'/work/fit/wolcen_face',views=(('front',0),('q',40),('side',90)),focus=((0,-0.08,1.83),0.9),res=(600,600))
    for o,mat,wfn,kind in PIECES: print('PIECE',o.name,mat,kind,tris(o))
    sys.exit(0)

make_mats(); exec(open(SRC+'/lib_fin.py').read())
OUT=SRC+'/work/'+NAME; os.makedirs(OUT,exist_ok=True)
def soot_fn(c):
    x,y,z,phi=face_frame(c)
    arms=sm(0.30,0.45,np.abs(c[:,0]))*0.9
    face=np.where(z>L['chin'][2]-0.02,0.3*(1-sm(60,110,phi)),0)
    return np.clip(arms+face,0,1)
hk_lo={k:v-0.007 for k,v in hk.items()}   # skin painted dark a little below the shell edge -> soft hairline
stub_fn=lambda c:np.clip(np.maximum(beard_mask(c)*1.6,scalp_mask(c,**hk_lo)*0.9),0,1)
for o,mat,wfn,kind in PIECES:
    n=o.name
    tgt={'belt':520,'cuffLeft':220,'cuffRight':220,'bracerLeft':560,'bracerRight':560,'shirt':1700,'sleeveLeft':380,'sleeveRight':380,'rollLeft':220,'rollRight':220}.get(n)
    if tgt: decimate(o,tgt,sym=False); push_out(o,0.005)
def slot_fn(o,m):
    if m=='wool_trousers': return 'legs'
    if o.name.startswith('bracer') or o.name.startswith('brstrap'): return 'hands'
    if max((o.matrix_world@Vector(c)).z for c in o.bound_box)<0.58: return 'feet'
    return 'torso'
main,cards,kp,pro,imgs,mats=finalize(NAME,BODY_BUDGET,inner_hide=[],slot_fn=slot_fn,region_budget=dict(arms=1250,hands=1500),
    body_attrs={'soot':soot_fn,'stubble':stub_fn},strip=False,out=OUT)
parts=finish_export(NAME,main,cards,kp,pro,OUT+'/raw.glb',OUT,cards_mats={'hair_wolcen','beard_wolcen'})
write_meta(NAME,parts,pro,OUT)
