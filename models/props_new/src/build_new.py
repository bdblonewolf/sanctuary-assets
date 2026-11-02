# blender -b -P build_new.py -- [name ...]  -> props_new/*.glb and props_new/breakables/*.glb
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from glib import *
import lib, hull as HL
from mathutils import Quaternion
lib.TEX='/workspace/pnwork/tex'; lib.RES='512'
lib.PROPS.setdefault('maiden_iron',(0.68,0.35))
OUT=lib.ROOT; OUTB=lib.ROOT+'/breakables'
RA='/workspace/repos/sanctuary-assets'; PH='/workspace/sanctuary/assets3d/overworld/polyhaven'
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
REG={}
def prop(*names):
    def d(f): REG[f.__name__]=(f,names); return f
    return d
RNG=random.Random(7)
def rnd(a,b): return RNG.uniform(a,b)
def start(name): reset(); MATS.clear(); return root_empty(name)
def void(): return flat('m_void',(0.012,0.010,0.008),rough=1.0)
def place_obj(o,rot,loc):
    o.rotation_euler=rot; o.location=loc; bpy.context.view_layer.update(); apply_tf(o); return o
def beam(name,p0,p1,w,h,m,roll=0.0,grain='x'):
    p0=Vector(p0); p1=Vector(p1); d=p1-p0
    o=box(name,(d.length,w,h),(0,0,0),m,uvscale=0.8,grain=grain)
    q=Vector((1,0,0)).rotation_difference(d.normalized()); o.rotation_mode='QUATERNION'
    o.rotation_quaternion=q@Quaternion((1,0,0),roll); o.location=(p0+p1)/2; bpy.context.view_layer.update(); apply_tf(o); return o
def splinters(name,p,dirv,m,n=3,L=0.14,r=0.022,seed=0):
    rr=random.Random(seed); out=[]; d=Vector(dirv).normalized()
    for i in range(n):
        j=Vector((rr.uniform(-.5,.5),rr.uniform(-.5,.5),rr.uniform(-.5,.5)))*0.6
        out.append(spike(f'{name}{i}',Vector(p)+Vector((rr.uniform(-.025,.025),rr.uniform(-.025,.025),0)),d+j,L*rr.uniform(0.5,1.0),r*rr.uniform(0.6,1.0),m))
    return out
def mound(name,r,loc,scale,m,seed=0,sub=2):
    return blob(name,r,loc,m,sub=sub,amp=0.2,freq=1.4,seed=seed,scale=scale,flatten_bottom=0.0)
def stone(name,r,loc,m,seed,scale=(1,1,0.7),sub=1,amp=0.22):
    return blob(name,r,loc,m,sub=sub,amp=amp,freq=1.6,seed=seed,scale=scale)
def emis_tex(name,png,base=(0.02,0.03,0.03)):
    if name in MATS: return MATS[name]
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(*base,1); b.inputs['Roughness'].default_value=0.6
    ti=nt.nodes.new('ShaderNodeTexImage'); ti.image=lib._img(f'{lib.TEX}/{png}')
    nt.links.new(ti.outputs[0],b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=1.0
    MATS[name]=m; return m
def ground(objs):
    """shift meshes so lowest visual vertex sits at z=0; returns dz applied"""
    bpy.context.view_layer.update()
    mz=min((o.matrix_world@v.co).z for o in objs if o.type=='MESH' for v in o.data.vertices)
    for o in objs: o.location.z-=mz
    bpy.context.view_layer.update(); return -mz
def imp(path,keep=None,target=None,px=512,drop_col=True):
    """import a GLB (read-only), return its mesh objects un-parented with world transforms applied; optional decimate to target tris"""
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=path)
    new=[o for o in bpy.data.objects if o not in before]
    out=[]
    for o in new:
        if o.type=='MESH' and (keep is None or o.name.split('.')[0] in keep) and not (drop_col and o.name.startswith('col_')):
            mw=o.matrix_world.copy(); o.parent=None; o.matrix_world=mw; out.append(o)
    for o in new:
        if o not in out: bpy.data.objects.remove(o,do_unlink=True)
    for o in out:
        bpy.context.view_layer.update(); apply_tf(o)
        for k in list(o.keys()): del o[k]
    if target:
        tot=sum(tris(o) for o in out)
        if tot>target:
            for o in out: decimate(o,target/tot)
    for im in bpy.data.images:
        if im.size[0]>px: im.scale(px,int(im.size[1]*px/im.size[0]))
    return out
def M():
    return dict(wd=mat('wood_dark'),pl=mat('wood_planks'),wr=mat('wood_rough',tint=(0.7,0.62,0.52),name='m_wood_weathered'),
        ir=mat('iron'),irw=mat('maiden_iron',tint=(0.95,0.9,0.85),name='m_iron_worn',rough=0.7,metal=0.4),
        st=mat('stone_mossy'),sb=mat('stone_block',tint=(0.75,0.72,0.68),name='m_stone_soot'),
        rope=mat('cloth_hessian',tint=(0.55,0.48,0.38),name='m_rope',normal=False),
        hes=mat('cloth_hessian',tint=(0.38,0.33,0.26),name='m_sack'),clay=mat('clay',tint=(0.62,0.48,0.38),name='m_urn_clay'))
# ======================================================================= (a) MAP BOARD
@prop('map_board_known_roads')
def map_board_known_roads(state=None):
    R=start('map_board_known_roads'); m=M(); P=[]
    W,H,z0=1.5,1.0,0.8   # board 1.5 x 1.0 m, bottom edge 0.8 m
    for sx in (-1,1):
        P.append(beam(f'post{sx}',(sx*0.85,0.0,0.0),(sx*0.85,0.0,2.05),0.11,0.11,m['wd'],grain='z'))
        P.append(beam(f'brace{sx}',(sx*0.85,0.42,0.0),(sx*0.85,0.04,0.7),0.06,0.06,m['wd']))
        P.append(stone(f'foot{sx}',0.2,(sx*0.85,0,0.03),m['st'],seed=sx+5,scale=(1.2,1.1,0.45)))
    P.append(box('backing',(W+0.1,0.04,H+0.1),(0,0.02,z0+H/2),m['pl'],uvscale=1.0,grain='x'))
    for z in (z0-0.02,z0+H+0.02): P.append(box(f'fr{z:.2f}',(W+0.2,0.07,0.07),(0,-0.01,z),m['wd'],uvscale=0.8,grain='x'))
    for sx in (-1,1): P.append(box(f'frs{sx}',(0.07,0.07,H+0.1),(sx*(W/2+0.07),-0.01,z0+H/2),m['wd'],uvscale=0.8,grain='z'))
    # little plank roof
    for sy in (-1,1):
        P.append(box(f'roof{sy}',(1.95,0.36,0.04),(0,sy*0.15,2.1),m['wr'],rot=(sy*math.radians(-28),0,0),uvscale=0.8,grain='x'))
    P.append(box('ridge',(1.95,0.06,0.06),(0,0,2.19),m['wd'],uvscale=0.8,grain='x'))
    # pins
    for x,z in ((-0.7,z0+0.95),(0.7,z0+0.95),(-0.7,z0+0.05),(0.7,z0+0.05)): P.append(blob(f'pin{x}{z}',0.018,(x,-0.035,z),m['ir'],sub=1,amp=0.05))
    bd=J(P,'board',R); ground([bd])
    # swappable map plane (own material + 0..1 UVs)
    mm=mat('map',name='m_map_slot',rough=0.85,normal=False,res='1k')
    V=[(-W/2,-0.003,z0),(W/2,-0.003,z0),(W/2,-0.003,z0+H),(-W/2,-0.003,z0+H)]
    ms=obj_uvv('map_slot',V,[(0,1,2,3)],[(0,0),(1,0),(1,1),(0,1)],mm,angle=89); ms.parent=R
    ms['map_slot']='swap baseColorTexture of material m_map_slot (UV 0..1, image aspect 3:2 recommended 1024x768 / 1536x1024)'
    empty('interact',(0,-0.9,0),parent=R,kind='read_map',label='The known roads',note='stand point in front of the board, facing +Z(board)')
    collider('col_map_board',(1.9,0.5,2.2),(0,0.05,1.1),parent=R)
    return finish('map_board_known_roads',R,OUT,notes='Standing map board "The known roads". Front faces +Z. map_slot = separate quad (1.5 x 1.0 m) with own material m_map_slot; swap its texture in code.',category='interactable',interactable='map')
# ======================================================================= (b) ROWBOAT
@prop('rowboat_ferry')
def rowboat_ferry(state=None):
    R=start('rowboat_ferry'); m=M(); P=[]
    H=HL.HullSpec(L=4.0,B=0.66,keel_mid=0.0,keel_rise=0.22,gun_mid=0.52,gun_rise=0.16,nst=5,ncol=18,th=0.018,tin=0.025,bow_exp=1.7,stern_exp=3.2,bow_rake=0.25,stern_rake=0.05)
    tar=mat('wood_planks',tint=(0.55,0.5,0.45),name='m_hull_tarred'); D=HL.build(H,None)
    for key,mt in (('outer_lo',tar),('outer_hi',m['pl']),('inner',m['pl']),('cap',m['wd'])):
        V,F,UV=D[key]
        if F: P.append(obj_uvv(f'h_{key}',V,F,UV,mt,angle=30))
    B=lambda x,s,z:(x,-s,z)
    keel=[B(0,s,H.keel(s/(H.L/2))-0.03) for s in np.linspace(-H.L/2*0.9,H.L/2*0.9,10)]
    P.append(tube('keel',keel,0.045,4,m['wd'],uvscale=1.2))
    P.append(tube('stem',[B(0,1.8,H.keel(0.9)),B(0,2.02,0.35),B(0,2.12,H.gun(1)+0.08)],[0.045,0.045,0.04],6,m['wd'],uvscale=1.0))
    # transom board (crafted plank) at stern
    tz0,tz1=H.keel(-0.97)+0.03,H.gun(-0.97)
    P.append(slab('transom',[(-0.36,tz1),(0.36,tz1),(0.18,tz0),(-0.18,tz0)],0.04,m['pl'],loc=(0,1.94,0),uvscale=0.6,grain='x'))
    # thwarts + floorboards
    for s in (0.9,0.0,-1.2):
        z=H.gun(s/2)-0.16; w=H.inner_halfwidth(s/2,z)
        P.append(box(f'thwart{s}',(2*w,0.22,0.035),B(0,s,z),m['pl'],uvscale=0.8,grain='x'))
    for x in (-0.18,0,0.18): P.append(box(f'floor{x}',(0.12,2.8,0.02),B(x,0,0.1),m['wd'],uvscale=1.0,grain='y'))
    # oarlocks
    locks=[]
    for sd in (1,-1):
        z=H.gun(0)+0.0; x=H.B_(0)*sd
        P.append(tube(f'lock{sd}',[(x,-0.35,z),(x,-0.35,z+0.07)],0.012,4,m['ir']))
        locks.append(Vector((x,-0.35,z+0.05)))
    P.append(tube('mooring',[B(0,2.05,0.6),B(0.15,2.2,0.35),B(0.1,2.4,0.15)],0.012,4,m['rope'],cap=False))
    hullm=J(P,'hull',R); dz=ground([hullm])
    for sd,L in ((1,locks[0]),(-1,locks[1])):
        L=L+Vector((0,0,dz))
        sh=tube(f'sh{sd}',[(-sd*0.7,0,0.05),(0,0,0),(sd*1.6,0,-0.38)],[0.025,0.03,0.025],6,m['wd'],uvscale=1.0)
        bl=box(f'bl{sd}',(0.5,0.14,0.02),(sd*1.75,0,-0.42),m['wd'],rot=(0,sd*math.radians(13),0),uvscale=0.6)
        o=J([sh,bl],f'oar_{"L" if sd>0 else "R"}'); o.location=L; o.parent=R
        o['anim']='pivot = oarlock; rotate about local Z (sweep) and Y (lift)'
    zwl=0.2+dz
    empty('waterline',(0,0,0.2),parent=R,note='sink the boat so this node sits at the water surface (draft ~0.2 m)')
    empty('seat_rower',(0,0.0,H.gun(0)-0.16+dz+0.02),parent=R,kind='seat',facing='stern(+Z)')
    empty('seat_passenger',(0,1.2,H.gun(0.6)-0.16+dz+0.02),parent=R,kind='seat')
    empty('player_board',(0.95,0,0),parent=R,kind='board',note='+X side')
    collider('col_boat',(1.4,4.2,0.7),(0,0.05,0.35),parent=R)
    return finish('rowboat_ferry',R,OUT,notes="Holt's ferry rowboat, 4.1 m, clinker hull from the longship hull generator (props_gothic_v1). Bow faces -Z. Base (keel) at y=0; node waterline = y 0.2. Oars oar_L/oar_R pivot at oarlocks.",category='vehicle',interactable='ferry')
# ======================================================================= (c) WELL
def well(heal):
    name='well_stone_heal' if heal else 'well_stone'; R=start(name); m=M(); P=[]; RNG.seed(21)
    rin,rout=0.55,0.85; k=0
    for c in range(3):
        n=11; z=0.16+c*0.26
        for i in range(n):
            a=2*math.pi*(i+0.5*(c%2))/n; r=(rin+rout)/2
            P.append(stone(f's{c}_{i}',0.2,(r*math.cos(a),r*math.sin(a),z),m['st'] if c<2 else m['sb'],seed=k,scale=(1.05,1.35*0.8,0.78),amp=0.18)); k+=1
            P[-1].rotation_euler.z=a+math.pi/2; bpy.context.view_layer.update(); apply_tf(P[-1])
    # coping ring (rounded, no flat faces)
    P.append(ring('coping',0.7,0.1,m['sb'],loc=(0,0,0.86),n=20,sides=6,squash=None))
    # dark shaft
    sh=lathe('shaft',[(0.6,-1.2),(0.6,0.84)],14,void(),cap_top=False,cap_bot=True); 
    bm=bmesh.new(); bm.from_mesh(sh.data); bmesh.ops.reverse_faces(bm,faces=bm.faces); bm.to_mesh(sh.data); bm.free(); P.append(sh)
    if heal:
        wm=flat('m_heal_water',(0.05,0.18,0.16),rough=0.08,emit=(0.25,0.85,0.7))
        P.append(lathe('water',[(0.0,0.5),(0.56,0.5)],16,wm,cap_top=False,cap_bot=False))
        rm=emis_tex('m_heal_runes','runes_e.png'); 
        band=lathe('runes',[(0.795,0.62),(0.795,0.78)],22,rm,cap_top=False,cap_bot=False)
        me=band.data; me.uv_layers.new(name='UVMap'); uvl=me.uv_layers[0].data
        for p in me.polygons:
            for li in p.loop_indices:
                v=me.vertices[me.loops[li].vertex_index].co; a=(math.atan2(v.y,v.x)/(2*math.pi))%1.0
                if a<0.02 and any(math.atan2(me.vertices[me.loops[l].vertex_index].co.y,me.vertices[me.loops[l].vertex_index].co.x)/(2*math.pi)%1>0.5 for l in p.loop_indices): a=1.0
                uvl[li].uv=(a*2,(v.z-0.62)/0.16)
        P.append(band)
    else:
        P.append(lathe('water',[(0.0,-0.4),(0.58,-0.4)],16,flat('m_well_water',(0.01,0.015,0.018),rough=0.05),cap_top=False,cap_bot=False))
    # frame: posts, beam, plank roof, winch
    for sx in (-1,1):
        P.append(beam(f'post{sx}',(sx*0.78,0,0.7),(sx*0.78,0,2.3),0.12,0.12,m['wd'],grain='z'))
    for sy in (-1,1):
        P.append(box(f'roof{sy}',(2.0,0.62,0.045),(0,sy*0.27,2.42),m['wr'],rot=(sy*math.radians(-32),0,0),uvscale=0.8,grain='x'))
    P.append(box('ridge',(2.0,0.08,0.08),(0,0,2.6),m['wd'],uvscale=0.8,grain='x'))
    P.append(tube('winch',[(-0.78,0,1.75),(0.78,0,1.75)],0.07,8,m['wd'],uvscale=0.6))
    P.append(ring('rope_coil',0.085,0.02,m['rope'],loc=(0,0,1.75),rot=(0,math.pi/2,0),n=10,sides=4))
    P.append(tube('crank',[(0.84,0,1.75),(0.95,0,1.75),(0.95,0,1.5),(1.06,0,1.5)],0.022,5,m['ir']))
    J(P,'well',R)
    # bucket: reuse Poly Haven wooden_bucket_01 (decimated), as a pivot node
    bk=imp(f'{PH}/wooden_bucket_01.glb',target=600)
    for o in bk: o.scale=(0.85,)*3; bpy.context.view_layer.update(); apply_tf(o)
    b=J(bk,'bucket'); top=max(v.co.z for v in b.data.vertices)
    rp=tube('bucket_rope',[(0,0,top),(0,0,1.68-1.1)],0.012,4,m['rope'],cap=False); rp.location=(0,0,1.1); apply_tf(rp)
    b.location=(0,0,1.1); bpy.context.view_layer.update(); apply_tf(b)
    b=J([b,rp],'bucket'); pivot_at(b,(0,0,1.68)); b.parent=R
    b['anim']='pivot = rope top under winch (y 1.68); translate along -Y to lower into shaft (~1.6 m), winch spins about X'
    empty('interact',(0,-1.2,0),parent=R,kind='heal_well' if heal else 'well')
    if heal: empty('fx_heal_glow',(0,0,0.75),parent=R,color='#40d9b3',intensity=0.8,distance=4.0,note='soft point light / motes; material emissive stays <= 1.0')
    collider('col_well',(1.9,1.9,0.95),(0,0,0.47),parent=R)
    collider('col_well_posts',(1.8,0.25,2.4),(0,0,1.2),parent=R)
    return finish(name,R,OUT,notes=('Healing well: glowing water disc + rune band (emissive <= 1.0), fx_heal_glow node. ' if heal else 'Town stone well. ')+'Rubble-stone ring (no flat faces), plank roof, winch; bucket node pivot at rope top.',category='interactable',interactable='well_heal' if heal else 'well')
@prop('well_stone')
def well_stone(state=None): return well(False)
@prop('well_stone_heal')
def well_stone_heal(state=None): return well(True)
# ======================================================================= (d) TRAPDOOR
@prop('closed','opened')
def trapdoor_ashen_coast(state):
    nm=f'trapdoor_ashen_coast_{state}'; R=start(nm); m=M(); P=[]; RNG.seed(41); op=state=='opened'
    W,D=1.2,1.0   # inn cellar hatch footprint (col_cellar_hatch 1.2 x 1.0)
    soot=mat('stone_block',tint=(0.55,0.52,0.5),name='m_stone_rubble_soot'); k=0
    for side in range(4):
        n=5 if side%2==0 else 4
        for i in range(n):
            t=(i+0.5)/n
            if side==0: p=(-W/2-0.12+t*(W+0.24),-D/2-0.13)
            elif side==2: p=(-W/2-0.12+t*(W+0.24),D/2+0.13)
            elif side==1: p=(W/2+0.14,-D/2+t*D)
            else: p=(-W/2-0.14,-D/2+t*D)
            s=stone(f'f{k}',0.17,(p[0],p[1],0.02),soot,seed=k+40,scale=(1.0,0.9,0.3),amp=0.15); k+=1; P.append(s)
    # frame timbers (crafted)
    for sy in (-1,1): P.append(box(f'fx{sy}',(W+0.08,0.07,0.08),(0,sy*(D/2+0.0),0.03),m['wd'],uvscale=0.8,grain='x'))
    for sx in (-1,1): P.append(box(f'fy{sx}',(0.07,D,0.08),(sx*(W/2+0.0),0,0.03),m['wd'],uvscale=0.8,grain='y'))
    # shaft + ladder top (below y=0)
    sh=box('shaft',(W-0.06,D-0.06,1.6),(0,0,-0.78),void()); bm=bmesh.new(); bm.from_mesh(sh.data)
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.normal.z>0.5],context='FACES'); bmesh.ops.reverse_faces(bm,faces=bm.faces); bm.to_mesh(sh.data); bm.free(); P.append(sh)
    for sx in (-1,1): P.append(beam(f'lad{sx}',(sx*0.22,0.38,-1.5),(sx*0.22,0.44,0.05),0.05,0.05,m['wd'],grain='z'))
    for z in np.linspace(-1.3,-0.1,5): P.append(tube(f'rung{z:.2f}',[(-0.22,0.38+0.06*(z+1.5)/1.55,z),(0.22,0.38+0.06*(z+1.5)/1.55,z)],0.018,5,m['wd']))
    J(P,'surround',R)
    # lid: planks + iron bands + ring, pivot at hinge (back edge, glTF -Z)
    L=[]; lw,ld=W-0.1,D-0.08
    for i in range(5): L.append(box(f'pk{i}',(lw/5-0.008,ld,0.05),(-lw/2+lw/10+i*lw/5,0,0.05),m['pl'],uvscale=0.9,grain='y'))
    for y in (-0.3,0.3): L.append(box(f'band{y}',(lw+0.02,0.06,0.012),(0,y,0.081),m['ir'],uvscale=0.5))
    for y in (-0.3,0.3):
        for x in np.linspace(-lw/2+0.06,lw/2-0.06,5): L.append(blob(f'nl{x:.2f}{y}',0.011,(x,y,0.088),m['ir'],sub=1,amp=0.0,scale=(1,1,0.6)))
    L.append(ring('ringh',0.07,0.011,m['ir'],loc=(0,-0.3,0.09),n=10,sides=4))
    for sx in (-0.35,0.35): L.append(box(f'hinge{sx}',(0.06,0.18,0.015),(sx,ld/2-0.06,0.083),m['ir']))
    lid=J(L,'lid'); hinge=(0,ld/2,0.05); pivot_at(lid,hinge); lid.parent=R
    if op: lid.rotation_euler=(math.radians(-112),0,0)
    lid['anim']='hinge pivot = node origin (back edge); open = rotate about local X by -112 deg (opened file); trapdoor below y=0 holds a 1.5 m dark shaft + ladder'
    empty('hinge',hinge,parent=R); empty('nav_down',(0,0,0),parent=R,kind='stairs:trap',dest='ashen_coast',note='same spot as inn nav_cellar_down when placed at cellar_hatch')
    if not op: collider('col_trapdoor',(1.2,1.0,0.12),(0,0,0.03),parent=R)
    else: collider('col_trapdoor_lid',(1.2,0.12,1.0),(0,0.5,0.5),parent=R)
    collider('col_click',(1.3,1.1,0.4),(0,0,0.2),parent=R,extras={'pick':'interact'})
    return finish(nm,R,OUT,extras={'state':state,'pair':'trapdoor_ashen_coast'},notes='Ashen Coast trapdoor, derived from the inn cellar hatch (1.2 x 1.0 m, soot rubble stone). Place origin at inn node cellar_hatch. Shaft/ladder extend 1.55 m below y=0.',category='interactable',interactable='trapdoor')
# ======================================================================= (e) CART
def wheel(name,m,r=0.5):
    P=[ring(name+'rim',r-0.03,0.035,m['wd'],n=18,sides=5,rot=(0,math.pi/2,0),squash=None),
       ring(name+'tyre',r-0.005,0.014,m['ir'],n=18,sides=4,rot=(0,math.pi/2,0)),
       lathe(name+'hub',[(0.0,-0.1),(0.07,-0.1),(0.09,-0.05),(0.09,0.05),(0.07,0.1),(0.0,0.1)],8,m['wd'],rot=(0,math.pi/2,0))]
    for i in range(8):
        a=2*math.pi*i/8; P.append(tube(name+f'sp{i}',[(0,0.08*math.cos(a),0.08*math.sin(a)),(0,(r-0.05)*math.cos(a),(r-0.05)*math.sin(a))],[0.025,0.02],5,m['wd']))
    return J(P,name)
@prop('intact','broken')
def cart(state):
    nm=f'cart_{state}'; R=start(nm); m=M(); RNG.seed(61); br=state=='broken'
    r=0.5; ax=(0.0,0.15,r); P=[]; SPX=[]
    # bed (crafted planks) 2.0 x 1.2, top of floor at 0.78
    zb=0.72
    for i in range(6): P.append(box(f'fl{i}',(0.2-0.006,2.0,0.04),(-0.5+i*0.2,0,zb),m['pl'],uvscale=1.0,grain='y'))
    for sx in (-1,1):
        P.append(beam(f'rail{sx}',(sx*0.55,-1.0,zb-0.06),(sx*0.55,1.0,zb-0.06),0.08,0.08,m['wd']))
        for z in (0.1,0.27): P.append(box(f'side{sx}{z}',(0.035,2.0,0.15),(sx*0.6,0,zb+z),m['wr'],uvscale=1.0,grain='y'))
        for y in (-0.95,0,0.95): P.append(box(f'stake{sx}{y}',(0.05,0.05,0.42),(sx*0.62,y,zb+0.16),m['wd'],grain='z'))
    for z in (0.1,0.27): P.append(box(f'back{z}',(1.2,0.035,0.15),(0,1.0,zb+z),m['wr'],uvscale=1.0,grain='x'))
    P.append(tube('axle',[(-0.7,ax[1],r),(0.7,ax[1],r)],0.04,6,m['wd']))
    # shafts forward (-Y), tips resting on the ground
    sh=[]
    for sx in (-1,1):
        if br and sx>0:
            sh.append(beam('shaftR',(sx*0.35,-0.9,zb-0.08),(sx*0.38,-1.7,0.42),0.07,0.07,m['wd'])); sh+=splinters('spS',(sx*0.38,-1.7,0.42),(0,-1,-0.4),m['wd'],n=3,L=0.13,seed=2)
            sh.append(beam('shaftR_tip',(0.55,-2.0,0.035),(0.8,-2.9,0.035),0.07,0.07,m['wd'],roll=0.3))
        else: sh.append(beam(f'shaft{sx}',(sx*0.35,-0.9,zb-0.08),(sx*0.42,-2.9,0.04),0.07,0.07,m['wd']))
    (SPX if br else P).extend(sh)
    SP=list(SPX)
    if br:
        # load spilled: sacks + broken crate boards
        hes=m['hes']
        for i,(p,rz) in enumerate([((0.95,-0.3,0.0),0.4),((1.2,0.4,0.0),1.6)]):
            s=blob(f'sk{i}',0.28,(0,0,0),hes,sub=2,amp=0.22,freq=1.6,seed=i+3,scale=(0.95,0.65,0.4),flatten_bottom=-0.05,uvscale=0.6); place_obj(s,(0,0,rz),(p[0],p[1],0.1)); SP.append(s)
        SP.append(mound('grain',0.3,(1.25,-0.1,0),(1.5,1.1,0.1),mat('rock_dark',tint=(0.55,0.47,0.33),name='m_grain'),seed=7))
        for i in range(4): SP.append(box(f'deb{i}',(0.5,0.12,0.025),(rnd(0.7,1.5),rnd(-0.9,0.9),0.013),m['wr'],rot=(0,0,rnd(0,3)),uvscale=0.6))
        # one side board knocked off
        SP.append(box('sidefall',(0.035,1.6,0.15),(1.05,0.9,0.02),m['wr'],rot=(0,math.pi/2,0.3),uvscale=1.0,grain='y'))
    body=J(P,'cart_body',R)
    wl=wheel('wheel_L',m,r); wr=wheel('wheel_R',m,r)
    for w,sx in ((wl,1),(wr,-1)): w.location=(sx*0.72,ax[1],r); bpy.context.view_layer.update(); apply_tf(w); pivot_at(w,(sx*0.72,ax[1],r)); w.parent=R
    for w in (wl,wr): w['anim']='pivot = axle centre; spin about local X'
    if br:
        # right (+X?) wheel = wheel_L at +X came off: lying flat; body rolls onto that corner
        wl.rotation_mode='XYZ'; wl.location=(1.45,-1.1,0.1); wl.rotation_euler=(0,math.radians(84),0.5); wl['anim']='detached (broken state)'
        piv=Vector((-0.72,ax[1],r)); ang=math.radians(26)
        Mx=Matrix.Translation(piv)@Matrix.Rotation(ang,4,'Y')@Matrix.Translation(-piv)
        bpy.context.view_layer.update()
        for o in (body,wr):
            mw=o.matrix_world.copy(); o.data.transform(Mx@mw); o.matrix_world=Matrix.Identity(4)
        bpy.context.view_layer.update()
        dz=ground([body,wr]); pivot_at(wr,Mx@Vector((-0.72,ax[1],r))+Vector((0,0,dz)))
        sp=J(SP,'spill'); bpy.context.view_layer.update(); body=J([body,sp],'cart_body',R) if False else body
        sp.parent=R
        wl.rotation_euler=(0,math.radians(86),0.5); wl.location=(1.5,-1.1,0.0); bpy.context.view_layer.update(); ground([wl])
    empty('axle',ax,parent=R,note='wheel_L (+X) / wheel_R (-X) spin about X at y=0.5')
    empty('hitch',(0,-2.9,0.05),parent=R,note='shaft tips; horse/puller attach')
    if br: collider('col_cart',(2.6,3.2,0.9),(0.3,-0.4,0.45),parent=R)
    else: collider('col_cart',(1.6,3.9,1.2),(0,-0.9,0.6),parent=R)
    collider('col_click',(2.2,3.0,1.4),(0.2,-0.5,0.7),parent=R,extras={'pick':'loot'})
    return finish(nm,R,OUT,extras={'state':state,'pair':'cart'},notes='Two-wheel hand/ox cart, bed 2.0 x 1.2 m, shafts forward (-Z... see README). Intact: wheels as nodes. Broken: +X wheel off and flat, body rolled onto that side, shaft snapped, sacks/grain/boards spilled. Footprint matches town prop_cart_broken.',category='breakable',interactable='breakable')
# ======================================================================= (f) PLAYER ROOM
@prop('wardrobe')
def wardrobe(state=None):
    R=start('wardrobe'); m=M(); P=[]; Wd,Dp,Ht=1.2,0.6,2.05
    P.append(box('carcass_back',(Wd,0.03,Ht-0.1),(0,Dp/2-0.015,0.1+(Ht-0.1)/2),m['pl'],grain='z'))
    for sx in (-1,1): P.append(box(f'side{sx}',(0.04,Dp,Ht-0.1),(sx*(Wd/2-0.02),0,0.1+(Ht-0.1)/2),m['wd'],grain='z'))
    P.append(box('base',(Wd+0.04,Dp+0.04,0.1),(0,0,0.05),m['wd'],grain='x',bevel=0.01))
    P.append(box('top',(Wd+0.1,Dp+0.08,0.06),(0,0,Ht-0.03),m['wd'],grain='x',bevel=0.012))
    P.append(box('crown',(Wd+0.16,Dp+0.11,0.05),(0,0,Ht+0.02),m['wd'],grain='x',bevel=0.015))
    P.append(box('floor',(Wd-0.08,Dp-0.06,0.03),(0,0,0.12),m['pl'],grain='x'))
    P.append(box('shelf',(Wd-0.08,Dp-0.06,0.03),(0,0,1.65),m['pl'],grain='x'))
    P.append(tube('rail',[(-Wd/2+0.05,0,1.55),(Wd/2-0.05,0,1.55)],0.015,6,m['ir']))
    P.append(box('inside',(Wd-0.08,0.01,Ht-0.2),(0,Dp/2-0.04,1.05),void()))
    for sx in (-1,1): P.append(blob(f'foot{sx}',0.05,(sx*(Wd/2-0.04),-Dp/2+0.04,0.02),m['wd'],sub=1,amp=0.05,scale=(1,1,0.6)))
    J(P,'wardrobe_body',R)
    for sx,nmd in ((-1,'door_L'),(1,'door_R')):
        D=[box(nmd+'p',(Wd/2-0.02,0.03,Ht-0.2),(sx*(Wd/4),-Dp/2+0.005,0.15+(Ht-0.2)/2),m['pl'],grain='z')]
        for z in (0.45,1.5): D.append(box(nmd+f'f{z}',(Wd/2-0.08,0.02,0.05),(sx*Wd/4,-Dp/2-0.018,z),m['wd'],grain='x'))
        D.append(box(nmd+'st',(0.05,0.02,Ht-0.3),(sx*0.05,-Dp/2-0.018,1.05),m['wd'],grain='z'))
        D.append(ring(nmd+'pull',0.03,0.007,m['ir'],loc=(sx*0.06,-Dp/2-0.035,1.05),rot=(math.pi/2,0,0),n=8,sides=4))
        for z in (0.35,1.75): D.append(box(nmd+f'h{z}',(0.02,0.04,0.08),(sx*(Wd/2-0.015),-Dp/2-0.01,z),m['ir']))
        d=J(D,nmd); pivot_at(d,(sx*(Wd/2-0.01),-Dp/2-0.01,0.15)); d.parent=R
        d['anim']=f'hinge pivot at outer edge; open = rotate about Y(up) by {"-" if sx<0 else "+"}100 deg'
    empty('interact',(0,-0.9,0),parent=R,kind='wardrobe')
    collider('col_wardrobe',(Wd+0.1,Dp+0.06,Ht+0.05),(0,0,(Ht+0.05)/2),parent=R)
    return finish('wardrobe',R,OUT,notes='Oak wardrobe 1.26 x 2.07 x 0.71 m for the inn north hall (player room). Front +Z, back flat to wall. door_L/door_R hinge nodes.',category='furniture',interactable='wardrobe')
@prop('nightstand')
def nightstand(state=None):
    R=start('nightstand'); m=M(); P=[]; W,Dp,H=0.5,0.42,0.6
    for sx in (-1,1):
        for sy in (-1,1): P.append(box(f'leg{sx}{sy}',(0.045,0.045,H-0.03),(sx*(W/2-0.03),sy*(Dp/2-0.03),(H-0.03)/2),m['wd'],grain='z'))
    for sx in (-1,1): P.append(box(f'side{sx}',(0.02,Dp-0.06,0.3),(sx*(W/2-0.03),0,H-0.2),m['pl'],grain='y'))
    P.append(box('back',(W-0.06,0.02,0.3),(0,Dp/2-0.03,H-0.2),m['pl'],grain='x'))
    P.append(box('top',(W+0.04,Dp+0.04,0.035),(0,0,H-0.015),m['wd'],grain='x',bevel=0.008))
    P.append(box('shelf',(W-0.06,Dp-0.06,0.02),(0,0,0.12),m['pl'],grain='x'))
    P+=candle('cdl',(0.12,0.05,H),h=0.16,r=0.028,lit=True,m=mat('bone',tint=(0.85,0.8,0.68),name='m_wax'))
    P.append(lathe('dish',[(0.0,H),(0.07,H),(0.075,H+0.015),(0.06,H+0.012)],10,m['ir'],loc=(0.12,0.05,0)))
    P.append(box('book',(0.15,0.2,0.04),(-0.1,0.0,H+0.02),mat('leather',tint=(0.35,0.15,0.12),name='m_book_red'),rot=(0,0,0.3)))
    J(P,'nightstand_body',R)
    D=[box('drw',(W-0.08,Dp-0.08,0.15),(0,0.02,H-0.12),m['pl'],grain='x'),box('drwf',(W-0.06,0.02,0.17),(0,-Dp/2+0.03,H-0.12),m['wd'],grain='x'),
       blob('knob',0.018,(0,-Dp/2+0.01,H-0.12),m['ir'],sub=1,amp=0.0)]
    d=J(D,'drawer'); pivot_at(d,(0,-Dp/2+0.03,H-0.12)); d.parent=R; d['anim']='slide along +Z (out) up to 0.3 m'
    empty('fx_candle',(0.12,0.05,H+0.2),parent=R,kind='candle')
    collider('col_nightstand',(W+0.04,Dp+0.04,H),(0,0,H/2),parent=R)
    return finish('nightstand',R,OUT,notes='Bedside table 0.54 x 0.6 x 0.46 m with drawer node and a lit candle (fx_candle).',category='furniture')
@prop('desk')
def desk(state=None):
    R=start('desk'); m=M(); P=[]
    # derived: Poly Haven wooden_table_02 (196 tris) stretched to a 1.3 x 0.7 m writing desk
    tb=imp(f'{PH}/wooden_table_02.glb')
    for o in tb: o.scale=(1.14,1.0,0.95); bpy.context.view_layer.update(); apply_tf(o)
    P+=tb; H=0.8*0.95
    P.append(box('drawer_box',(0.5,0.55,0.12),(0.3,0.0,H-0.12),m['wd'],grain='x'))
    P.append(box('drawer_front',(0.48,0.02,0.1),(0.3,-0.285,H-0.12),m['pl'],grain='x')); P.append(blob('knob',0.016,(0.3,-0.3,H-0.12),m['ir'],sub=1,amp=0))
    pp=mat('book_pages',name='m_paper',normal=False) if os.path.exists(f'{lib.TEX}/book_pages_a_512.jpg') else flat('m_paper',(0.55,0.5,0.4))
    for i in range(3): P.append(box(f'paper{i}',(0.21,0.29,0.003),(-0.25+i*0.07,-0.05+i*0.02,H+0.002+i*0.003),pp,rot=(0,0,rnd(-0.4,0.4))))
    P.append(lathe('ink',[(0.0,H),(0.035,H),(0.04,H+0.03),(0.015,H+0.05),(0.018,H+0.06),(0,H+0.06)],8,flat('m_inkglass',(0.02,0.03,0.04),rough=0.2),loc=(0.1,0.15,0)))
    P.append(tube('quill',[(0.1,0.15,H+0.05),(0.0,0.2,H+0.25)],[0.004,0.012],4,mat('bone',name='m_quill',normal=False)))
    P.append(box('book',(0.2,0.28,0.06),(0.45,0.1,H+0.03),mat('leather',tint=(0.25,0.2,0.15),name='m_book'),rot=(0,0,-0.2)))
    P+=candle('cdl',(-0.5,0.2,H),h=0.2,r=0.03,lit=True,m=mat('bone',tint=(0.85,0.8,0.68),name='m_wax'))
    J(P,'desk_body',R); empty('fx_candle',(-0.5,0.2,H+0.24),parent=R,kind='candle'); empty('interact',(0,-0.75,0),parent=R,kind='desk')
    collider('col_desk',(1.32,0.72,0.8),(0,0,0.4),parent=R)
    return finish('desk',R,OUT,notes='Writing desk derived from Poly Haven wooden_table_02 (CC0) scaled to 1.3 x 0.7 x 0.76 m, plus drawer, papers, ink, book and candle.',category='furniture')
@prop('rug')
def rug(state=None):
    R=start('rug'); W,D=2.4,1.6; rm=mat('rug',name='m_rug',rough=0.97,res='1k')
    def fn(u,v):
        x=(u-0.5)*W; y=(v-0.5)*D; z=0.008+0.006*math.sin(u*17+v*5)*math.sin(v*11)
        if u>0.93 and v<0.25: z+=0.035*((u-0.93)/0.07)*((0.25-v)/0.25)   # turned-up corner
        return (x,y,z)
    o=cloth_grid('rug',W,D,24,16,fn,rm)
    # cloth_grid builds in XZ? we built XY directly via fn
    o.parent=R
    collider('col_rug',(W,D,0.02),(0,0,0.01),parent=R,extras={'walkable':True,'blocking':False})
    return finish('rug',R,OUT,notes='Worn oxblood carpet 2.4 x 1.6 m (fits the 5.3 m deep north hall in front of the bed). Texture from Poly Haven dirty_carpet fibres + painted medallion.',category='furniture')
# ======================================================================= URNS (breakable)
URNS={'a':[(0.0,0.0),(0.1,0.0),(0.13,0.03),(0.2,0.2),(0.22,0.36),(0.19,0.5),(0.12,0.6),(0.08,0.66),(0.09,0.7),(0.11,0.72)],
      'b':[(0.0,0.0),(0.14,0.0),(0.17,0.04),(0.27,0.16),(0.29,0.26),(0.25,0.38),(0.16,0.44),(0.13,0.47),(0.15,0.5)],
      'c':[(0.0,0.0),(0.08,0.0),(0.1,0.04),(0.12,0.2),(0.17,0.5),(0.19,0.7),(0.15,0.85),(0.07,0.95),(0.06,1.05),(0.09,1.1)]}
@prop('intact','broken')
def urn(state):
    for k,prof in URNS.items():
        nm=f'urn_{k}_{state}'; R=start(nm); m=M(); P=[]; RNG.seed(ord(k)); br=state=='broken'
        tint={'a':(0.62,0.48,0.38),'b':(0.5,0.42,0.36),'c':(0.45,0.36,0.3)}[k]
        c=mat('clay',tint=tint,name=f'm_urn_clay_{k}'); top=prof[-1][1]; rmax=max(r for r,z in prof)
        if not br:
            P.append(lathe('urn',prof,16,c,cap_top=False,uvscale=0.5))
            P.append(lathe('dk',[(prof[-1][0]-0.01,top-0.02),(0.0,top-0.02)],12,void(),cap_top=False,cap_bot=False))
            P.append(ring('band',rmax*0.98,0.01,m['rope'] if k!='c' else c,loc=(0,0,[z for r,z in prof if r==rmax][0]),n=16,sides=4))
            if k=='c':
                for sx in (-1,1): P.append(tube(f'hdl{sx}',[(sx*0.15,0,0.82),(sx*0.24,0,0.84),(sx*0.22,0,0.66),(sx*0.18,0,0.62)],0.018,5,c))
        else:
            cut=top*0.42; low=[(r,z) for r,z in prof if z<=cut]; rc=np.interp(cut,[z for r,z in prof],[r for r,z in prof]); low.append((rc,cut))
            u=lathe('urnlow',low,16,c,cap_top=False,uvscale=0.5); zt=max(v.co.z for v in u.data.vertices)
            for v in u.data.vertices:
                if v.co.z>zt-1e-3:
                    a=math.atan2(v.co.y,v.co.x); v.co.z-=cut*0.35*abs(math.sin(a*2.5+ord(k)))+0.02*((int(a*7))%2)
            u.data.update(); P.append(u)
            inn=lathe('urnin',[(r*0.9,z+0.015) for r,z in low[1:]],16,c,cap_top=False,cap_bot=False,uvscale=0.5)
            bm=bmesh.new(); bm.from_mesh(inn.data); bmesh.ops.reverse_faces(bm,faces=bm.faces); bm.to_mesh(inn.data); bm.free(); P.append(inn)
            ash=mat('bone',tint=(0.26,0.25,0.24),name='m_ash')
            P.append(mound('spill',rmax*1.2,(rmax*1.3,-rmax,0),(1.4,0.9,0.12),ash,seed=4))
            for i in range(8):
                a=rnd(0,6.28); rr=rnd(rmax*1.2,rmax*2.8); w=rnd(0.05,0.12)
                sh=slab(f'sh{i}',[(-w,0),(w*0.9,0.01),(w*0.5,w*1.3),(-w*0.3,w*1.1)],0.014,c,uvscale=0.5)
                P.append(place_obj(sh,(math.pi/2+rnd(-.3,.3),rnd(-.4,.4),a),(rr*math.cos(a),rr*math.sin(a),0.01)))
            if k=='c':
                P.append(tube('hdl',[(0.5,0.1,0.02),(0.58,0.2,0.03),(0.55,0.3,0.02)],0.018,5,c))
        J(P,'mesh',R)
        hz=top if not br else 0.3
        collider('col_click',(rmax*2+0.15,rmax*2+0.15,hz+0.05) if not br else (rmax*6,rmax*6,0.3),(0,0,(hz+0.05)/2) if not br else (0,0,0.15),parent=R,extras={'pick':'loot'})
        if not br: collider(f'col_urn',(rmax*2,rmax*2,top),(0,0,top/2),parent=R)
        finish(nm,R,OUTB,extras={'state':state,'pair':f'urn_{k}'},notes=f'Clay urn variant {k.upper()} (h {top:.2f} m), breakable. Broken: lower third stays, shards + ash spill. Method derived from props_gothic_v1 burial_urn.',category='breakable',interactable='breakable')
# ======================================================================= WEAPON RACK (breakable)
@prop('intact','broken')
def weapon_rack(state):
    nm=f'weapon_rack_{state}'; R=start(nm); m=M(); P=[]; RNG.seed(111); br=state=='broken'; wd=mat('wood_rough',tint=(0.6,0.52,0.42),name='m_rack_wood')
    # reused weapons (read-only imports, decimated): spear, hatchet, swordsman sword, kite shield
    W={}
    W['spear']=J(imp(f'{RA}/models/weapons/weapon_mourning_spear.glb',target=500),'loot_spear')
    W['hatchet']=J(imp(f'{RA}/models/weapons/weapon_briar_hatchet.glb',target=400),'loot_hatchet')
    W['sword']=J(imp(f'{RA}/characters_art/monsters/swordsman/swordsman.glb',keep=['swordsman_sword'],target=400),'loot_sword')
    W['shield']=J(imp(f'{RA}/characters_art/props/kite_shield_sanctuary.glb',target=700),'loot_shield')
    PRE={'spear':-math.pi/2,'hatchet':math.pi/2}
    for k,o in W.items():
        if k in PRE: o.data.transform(Matrix.Rotation(PRE[k],4,'X')); o.data.update()
    for o in W.values():
        bb=[o.matrix_world@Vector(c) for c in o.bound_box]; cx=sum(v.x for v in bb)/8; cy=sum(v.y for v in bb)/8; mz=min(v.z for v in bb)
        o.data.transform(Matrix.Translation((-cx,-cy,-mz))); o.data.update()
    def put(o,loc,rot): o.rotation_mode='XYZ'; o.rotation_euler=rot; o.location=loc; bpy.context.view_layer.update()
    if not br:
        for sx in (-1,1):
            P.append(beam(f'leg{sx}a',(sx*0.75,-0.35,0),(sx*0.75,0,1.5),0.07,0.07,wd)); P.append(beam(f'leg{sx}b',(sx*0.75,0.35,0),(sx*0.75,0,1.5),0.07,0.07,wd))
        P.append(beam('rail_top',(-0.82,-0.05,1.32),(0.82,-0.05,1.32),0.07,0.07,wd))
        P.append(beam('rail_low',(-0.82,-0.17,0.45),(0.82,-0.17,0.45),0.06,0.06,wd))
        P.append(beam('rail_back',(-0.82,0.2,0.7),(0.82,0.2,0.7),0.06,0.06,wd))
        for x in np.linspace(-0.6,0.6,6): P.append(tube(f'peg{x:.2f}',[(x,-0.08,1.33),(x,-0.2,1.36)],0.012,4,wd))
        # spear leaning against the top rail (spear points +Z in Blender after import? spear length along Y in glTF -> along -Y/Z) - auto orient by bbox
        put(W['spear'],(-0.45,-0.32,0.0),(math.radians(-12),0,0)); put(W['sword'],(0.05,-0.3,0.0),(math.radians(-14),0,0)); put(W['hatchet'],(0.45,-0.28,0.0),(math.radians(-14),0,0))
        for k in ("spear","sword","hatchet"): ground([W[k]])
        put(W['shield'],(0.0,0.3,0.02),(math.radians(-8),0,math.pi))
    else:
        P.append(beam('legLa',(-0.95,-0.05,0.04),(-0.55,1.2,0.05),0.07,0.07,wd,roll=0.2)); P.append(beam('legLb',(-0.8,-0.6,0.035),(-0.3,-0.1,0.04),0.07,0.07,wd))
        P.append(beam('legRa',(0.85,-0.55,0.75),(0.75,0.0,0.0),0.07,0.07,wd)); P+=splinters('spR',(0.85,-0.55,0.75),(0.1,-0.6,1),wd,n=3,L=0.14,seed=3)
        P.append(beam('legRb',(0.75,0.35,0),(0.78,0.0,0.6),0.07,0.07,wd)); P+=splinters('spRb',(0.78,0.0,0.6),(0,-0.3,1),wd,n=2,L=0.12,seed=4)
        P.append(beam('rail_topA',(-0.8,0.25,0.035),(0.15,0.05,0.04),0.07,0.07,wd)); P+=splinters('spT',(0.15,0.05,0.04),(1,-0.2,0.05),wd,n=2,L=0.1,seed=6)
        P.append(beam('rail_topB',(0.25,0.0,0.04),(0.8,-0.25,0.65),0.07,0.07,wd,roll=0.3))
        P.append(beam('rail_low',(-0.6,-0.9,0.03),(0.5,-0.75,0.03),0.06,0.06,wd))
        for i in range(5): P.append(box(f'spl{i}',(0.22,0.03,0.02),(rnd(-0.7,0.7),rnd(-1.05,-0.55),0.01),wd,rot=(0,0,rnd(0,3)),uvscale=0.5))
        put(W['spear'],(-0.2,-0.4,0.06),(math.radians(-88),0,math.radians(70))); put(W['sword'],(0.4,-0.9,0.04),(math.radians(-90),0,math.radians(-30)))
        put(W['hatchet'],(-0.7,-1.0,0.05),(math.radians(-90),0,math.radians(120))); put(W['shield'],(0.2,0.6,0.06),(math.radians(-87),0,math.radians(20)))
    if br:
        for o in W.values(): ground([o])
    J(P,'rack',R)
    for k,o in W.items(): o.parent=R; o['loot']=k; o['note']='separate node: hide on pickup'
    bpy.context.view_layer.update()
    collider('col_click',(1.9,1.0,1.7) if not br else (2.2,2.2,0.4),(0,0,0.85) if not br else (0,-0.2,0.2),parent=R,extras={'pick':'loot'})
    collider('col_rack',(1.7,0.8,1.5) if not br else (1.8,1.8,0.25),(0,0,0.75) if not br else (0,-0.2,0.12),parent=R)
    return finish(nm,R,OUTB,extras={'state':state,'pair':'weapon_rack'},notes='Breakable weapon rack. Reuses (decimated copies) weapon_mourning_spear, weapon_briar_hatchet, swordsman sword and kite_shield_sanctuary as loot_* nodes. Broken: trestles snapped, weapons on the floor. Derived from props_gothic_v1 weapon_rack_wreck.',category='breakable',interactable='breakable')
# ======================================================================= BREAKABLES: barrel / crate / sack
BAR=[(0.0,0.0),(0.25,0.0),(0.29,0.2),(0.31,0.42),(0.29,0.64),(0.25,0.84)]
def barrel_intact(name,m,loc=(0,0,0),s=1.0,rz=0.0):
    prof=[(r*s,z*s) for r,z in BAR]; P=[lathe(name+'b',prof,16,m['pl'],cap_bot=True,cap_top=False,uvscale=0.6)]
    P.append(lathe(name+'t',[(0.24*s,0.82*s),(0.0,0.82*s)],14,m['wd'],cap_top=False,cap_bot=False,uvscale=0.6))
    for z in (0.08,0.28,0.56,0.76):
        r=np.interp(z,[p[1] for p in BAR],[p[0] for p in BAR])*s+0.006; P.append(ring(name+f'h{z}',r,0.012,m['ir'],loc=(0,0,z*s),n=16,sides=4,squash=None))
    o=J(P,name); place_obj(o,(0,0,rz),loc); return o
def barrel_broken(name,m,loc=(0,0,0),s=1.0,rz=0.0,seed=0):
    rr=random.Random(seed); P=[]; prof=[(r*s,z*s) for r,z in BAR[:3]]+[(0.3*s,0.3*s)]
    u=lathe(name+'low',prof,16,m['pl'],cap_bot=True,cap_top=False,uvscale=0.6); zt=max(v.co.z for v in u.data.vertices)
    for v in u.data.vertices:
        if v.co.z>zt-1e-3: a=math.atan2(v.co.y,v.co.x); k=int((a+math.pi)/(2*math.pi)*16); v.co.z-=0.22*s*((k*7+seed)%5)/4
    u.data.update(); P.append(u)
    P.append(lathe(name+'in',[(0.26*s,0.03*s),(0.0,0.03*s)],12,void(),cap_top=False,cap_bot=False))
    P.append(ring(name+'h0',0.262*s,0.012,m['ir'],loc=(0,0,0.08*s),n=16,sides=4))
    for i in range(6):   # loose curved staves on the floor
        a=rr.uniform(0,6.28); d=rr.uniform(0.45,0.9)*s; L=rr.uniform(0.5,0.8)*s
        st=tube(name+f'st{i}',[(0,-L/2,0.0),(0,0,0.03*s),(0,L/2,0.0)],0.05*s,4,m['pl'],squash=[(1,0.25)]*3,uvscale=0.6)
        P.append(place_obj(st,(0,0,a),(d*math.cos(a),d*math.sin(a),0.012)))
    for i in range(2):
        h=ring(name+f'hf{i}',0.3*s,0.012,m['ir'],n=16,sides=4); P.append(place_obj(h,(rr.uniform(-0.2,0.2),rr.uniform(0.1,0.3),0),(rr.uniform(-0.6,0.6)*s,rr.uniform(-0.6,0.6)*s,0.03)))
    lid=lathe(name+'lid',[(0.24*s,0.0),(0.0,0.0)],12,m['wd'],cap_top=False,cap_bot=False)
    P.append(place_obj(lid,(0.15,0.2,0),(0.55*s,-0.45*s,0.05)))
    P.append(mound(name+'wet',0.45*s,(0.25*s,0.3*s,0),(1.5,1.0,0.03),flat('m_spill_wet',(0.02,0.015,0.01),rough=0.15),seed=seed))
    o=J(P,name); place_obj(o,(0,0,rz),loc); return o
def crate_intact(name,m,loc=(0,0,0),s=0.7,rz=0.0):
    P=[]; h=s; t=0.025
    for face in range(4):
        a=face*math.pi/2; c,sn=math.cos(a),math.sin(a)
        for j in range(4):
            z=0.04+j*(h-0.06)/4+(h-0.06)/8
            P.append(place_obj(box(name+f'p{face}{j}',(s-0.02,t,(h-0.06)/4-0.01),(0,0,0),m['pl'],uvscale=0.8,grain='x'),(0,0,a),(-sn*(s/2-t/2),-c*(s/2-t/2) if False else c*(s/2-t/2),z)))
        P.append(place_obj(box(name+f'd{face}',(s*1.25,0.03,0.07),(0,0,0),m['wd'],uvscale=0.8,grain='x'),(0,math.atan2(h-0.1,s-0.1),a),(-sn*(s/2+0.01),c*(s/2+0.01),h/2)))
    for z in (0.02,h-0.02):
        for j in range(4): P.append(box(name+f'tb{z}{j}',(s,(s-0.02)/4-0.01,0.025),(0,-s/2+s/8+j*s/4,z),m['pl'],uvscale=0.8,grain='x'))
    for sx in (-1,1):
        for sy in (-1,1): P.append(box(name+f'c{sx}{sy}',(0.06,0.06,h),(sx*(s/2-0.005),sy*(s/2-0.005),h/2),m['wd'],grain='z'))
    o=J(P,name); place_obj(o,(0,0,rz),loc); return o
def crate_broken(name,m,loc=(0,0,0),s=0.7,rz=0.0,seed=0):
    rr=random.Random(seed); P=[]
    for j in range(4): P.append(box(name+f'tb{j}',(s,(s-0.02)/4-0.01,0.025),(0,-s/2+s/8+j*s/4,0.013),m['pl'],uvscale=0.8,grain='x'))
    for sx,sy in ((-1,-1),(1,1)): P.append(box(name+f'c{sx}{sy}',(0.06,0.06,rr.uniform(0.2,0.35)),(sx*(s/2-0.005),sy*(s/2-0.005),0.13),m['wd'],grain='z'))
    P+=splinters(name+'sp',(s/2,s/2,0.28),(0,0,1),m['wd'],n=2,L=0.08,seed=seed)
    P.append(box(name+'side',(s-0.02,0.025,0.22),(0.05,-s/2,0.12),m['pl'],rot=(0.15,0,0),uvscale=0.8,grain='x'))
    for i in range(9):
        a=rr.uniform(0,6.28); d=rr.uniform(0.45,1.0)*s/0.7
        P.append(place_obj(box(name+f'pk{i}',(rr.uniform(0.3,0.68),0.15,0.025),(0,0,0),m['pl'],uvscale=0.8,grain='x'),(0,rr.uniform(-0.15,0.15),a),(d*math.cos(a),d*math.sin(a),0.03)))
    P+=splinters(name+'sq',(0.4,-0.4,0.02),(1,0.3,0.15),m['wd'],n=3,L=0.12,seed=seed+1)
    P.append(mound(name+'straw',0.3,(0,0.05,0.02),(1.3,1.0,0.18),mat('cloth_hessian',tint=(0.5,0.42,0.25),name='m_straw'),seed=seed+5))
    o=J(P,name); place_obj(o,(0,0,rz),loc); return o
def sack_intact(name,m,loc=(0,0,0),rz=0.0,seed=0):
    sk=blob(name+'b',0.3,(0,0,0),m['hes'],sub=2,amp=0.16,freq=1.6,seed=seed+3,scale=(0.85,0.62,1.0),flatten_bottom=-0.18,uvscale=0.6); place_obj(sk,(0,0,0),(0,0,0.27))
    nk=blob(name+'n',0.08,(0,0,0.58),m['hes'],sub=1,amp=0.3,seed=seed,scale=(1.0,0.9,1.3)); tie=ring(name+'t',0.06,0.012,m['rope'],loc=(0,0,0.53),n=8,sides=4)
    o=J([sk,nk,tie],name); ground([o]); place_obj(o,(0,0,rz),(loc[0],loc[1],loc[2]+o.location.z)); return o
def sack_broken(name,m,loc=(0,0,0),rz=0.0,seed=0):
    sk=blob(name+'b',0.33,(0,0,0),m['hes'],sub=2,amp=0.3,freq=1.8,seed=seed+3,scale=(1.0,0.75,0.25),flatten_bottom=-0.02,uvscale=0.6); place_obj(sk,(0,0,0),(0,0,0.07))
    sl=slab(name+'sl',[(-0.17,0),(0.17,0),(0.1,0.035),(-0.12,0.03)],0.02,void(),loc=(0,-0.2,0.11),rot=(math.pi/2-0.3,0,0))
    sp=mound(name+'gr',0.32,(0.05,-0.42,0),(1.4,1.0,0.11),mat('rock_dark',tint=(0.55,0.47,0.33),name='m_grain'),seed=seed+7)
    o=J([sk,sl,sp],name); ground([o]); place_obj(o,(0,0,rz),(loc[0],loc[1],loc[2]+o.location.z)); return o
BRK={ # name: (builder(state,m)->objs, col size/center intact, replaces)
 'barrel':'modular_dungeon_kit BarrelClosed_01/02/03 + BarrelBroken_01/02; characters_art/props/wine_barrel_01_sanctuary.glb (single barrel use)',
 'barrel_group':'models/town/martsirt_v2_2/props/prop_barrel_group.glb (placements: market_barrels, inn_barrels)',
 'crate':'single "crate" stand-ins (audit: crates drawn as kit Barrel) ',
 'crate_stack':'models/town/martsirt_v2_2/props/prop_crate_stack.glb (placements: forge_crates; inn.json crate)',
 'sack':'single sack (new; audit lists sack_pile as crate stand-in)',
 'sack_pile':'models/env_extra/props_gothic_v1/loot/sack_pile_closed/opened.glb (as breakable)'}
@prop('intact','broken')
def breakables(state):
    br=state=='broken'
    for key,rep in BRK.items():
        if ARGS2 and key not in ARGS2: continue
        nm=f'{key}_{state}'; R=start(nm); m=M(); RNG.seed(hash(key)%999)
        if key=='barrel': objs=[(barrel_broken if br else barrel_intact)('barrel',m)]; cs=((0.64,0.64,0.85),(0,0,0.42))
        elif key=='barrel_group':
            L=[((-0.3,0.1,0),1.0,0.3),((0.3,-0.15,0),1.0,1.1),((0.05,-0.75,0),0.8,2.0)]
            objs=[(barrel_broken(f'bar{i}',m,p,s,rz,seed=i) if br else barrel_intact(f'bar{i}',m,p,s,rz)) for i,(p,s,rz) in enumerate(L)]; cs=((1.3,1.4,0.88),(0,-0.25,0.44))
        elif key=='crate': objs=[(crate_broken if br else crate_intact)('crate',m)]; cs=((0.75,0.75,0.72),(0,0,0.36))
        elif key=='crate_stack':
            if not br: objs=[crate_intact('cr0',m,(-0.36,0,0),0.7,0.05),crate_intact('cr1',m,(0.42,0.08,0),0.66,-0.12),crate_intact('cr2',m,(-0.25,0.02,0.7),0.6,0.3)]
            else: objs=[crate_broken('cr0',m,(-0.36,0,0),0.7,0.05,seed=1),crate_broken('cr1',m,(0.5,0.2,0),0.66,1.2,seed=2),crate_intact('cr2',m,(-0.1,-0.75,0),0.6,0.6)]
            objs[-1]['note']=''; cs=((1.5,0.8,1.32),(0.03,0.02,0.66))
        elif key=='sack': objs=[(sack_broken if br else sack_intact)('sack',m,seed=3)]; cs=((0.55,0.42,0.62),(0,0,0.31))
        else:
            base=[((-0.25,-0.05,0.0),0.0),((0.25,0.05,0.0),0.5),((0.0,0.35,0.0),1.2),((0.45,-0.35,0.0),2.0)]
            objs=[(sack_broken(f'sk{i}',m,(p[0]*1.3,p[1]*1.3,0),rz,seed=i) if br else sack_intact(f'sk{i}',m,p,rz,seed=i)) for i,(p,rz) in enumerate(base)]
            if not br: objs.append(sack_intact('sk4',m,(-0.02,0.1,0.3),0.3,seed=4))
            cs=((1.3,1.1,0.85),(0.08,0.0,0.4))
        mesh=J(objs,'mesh',R)
        if not br: collider(f'col_{key}',*cs,parent=R)
        csz,ccen=cs; collider('col_click',(csz[0]+0.2,csz[1]+0.2,csz[2]) if not br else (csz[0]+0.8,csz[1]+0.8,0.35),ccen if not br else (ccen[0],ccen[1],0.17),parent=R,extras={'pick':'loot'})
        finish(nm,R,OUTB,extras={'state':state,'pair':key,'replaces':rep},notes=f'Breakable {key.replace("_"," ")}. Broken: split staves/planks, spills and debris; base at y=0. Replaces: {rep}',category='breakable',interactable='breakable')
ARGS2=[a.split('=')[1] for a in ARGS if a.startswith('only=')]; ARGS=[a for a in ARGS if not a.startswith('only=')]
names=ARGS or list(REG)
for n in names:
    f,states=REG[n]
    for s in (states if states and states[0] in ('closed','intact') else [None]):
        try: f(s)
        except Exception:
            import traceback; traceback.print_exc(); print('FAILED',n,s)
