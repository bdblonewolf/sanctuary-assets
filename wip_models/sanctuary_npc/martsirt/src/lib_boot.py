# heavy boot builder (shaft hull + foot hull, voxel-unioned). exec after lib_bl.
def boots(TOP,shaft_off=0.006,foot_off=0.006,cuff=0.04,cuff_off=0.012,straps=(),strap_off=0.012,heel=True,mat='leather_boot',
          metal='iron_dark',slouch=0.0,budget=1300,sole_mat='leather_sole',sole_h=0.022,heel_h=0.012,toe=0.006,crease=0.0035,cuff_budget=220):
    out=[]
    for Lr,sg in (('Left',1),('Right',-1)):
        legs={S+Lr+n for n in ('UpLeg','Leg','Foot','ToeBase')}
        sel=np.isin(np.array(dom),list(legs))&(side==sg)
        kn=bonesH[S+Lr+'Leg']; an=bonesH[S+Lr+'Foot']
        def cen_at(z):
            t=(kn.z-z)/(kn.z-an.z); return kn.lerp(an,t)
        zs=np.linspace(TOP+0.03,0.045,40); st=[cen_at(z) for z in zs]; st=[Vector((c.x,c.y,z)) for c,z in zip(st,zs)]
        def so(t,a):
            o=shaft_off
            if slouch: o+=slouch*(0.5+0.5*math.sin(a*3+sg))*max(0,1-abs(t-0.25)*3)
            return o
        r=tube(st,Z,sel&(P[:,2]>0.07),48,so,center_fn=cen_bbox,smooth=2)
        r[-6:]=r[-7]
        sh=grid_mesh('shaft',r,wrap=True); close_tube(sh)
        fsel=sel&(P[:,2]<0.13); Q=P[fsel]; y0=Q[:,1].max()+0.004; y1=Q[:,1].min()-0.008
        st=[Vector((an.x,y,0.05)) for y in np.linspace(y0,y1,34)]
        ty=lambda t:foot_off+toe*ss(0.55,0.9,t)*(1-ss(0.93,1.0,t))   # roomy toe box
        r=tube(st,Vector((0,-1,0)),fsel,40,lambda t,a:ty(t),center_fn=cen_bbox,smooth=2)
        r[...,2]=np.maximum(r[...,2],0.0)
        ft=grid_mesh('foot',r,wrap=True); close_tube(ft)
        b=join([sh,ft],'boot'+Lr)
        m=b.modifiers.new('r','REMESH'); m.mode='VOXEL'; m.voxel_size=0.004; apply_mod(b,m)
        bm=bmesh.new(); bm.from_mesh(b.data)
        bmesh.ops.bisect_plane(bm,geom=bm.verts[:]+bm.edges[:]+bm.faces[:],plane_co=(0,0,TOP),plane_no=(-0.10*sg,0.10,1),clear_outer=True)
        for v in bm.verts:
            if v.co.z<0.0: v.co.z=0.0
        bm.to_mesh(b.data); bm.free()
        decimate(b,budget)
        from mathutils import noise as _mn
        for v in b.data.vertices:   # ankle / instep creases + scuffed irregularity
            z=v.co.z; w=ss(0.07,0.10,z)*(1-ss(0.20,0.26,z))
            v.co=v.co+v.normal*(crease*w*math.sin(z*210+3*_mn.noise(v.co*25))+0.0012*_mn.noise(v.co*60))
        for v in b.data.vertices:
            h=bvh.find_nearest(v.co)
            if h[0] is not None and v.co.z>0.0:
                d=v.co-h[0]; mn=shaft_off if v.co.z>0.12 else 0.003
                if d.dot(h[1])<mn: v.co=h[0]+h[1]*mn
        # thick sole: flatten the bottom to y=0 contact (feet at y=0 means sole bottom at z=0)
        out.append(add(b,mat,w_bodyT([Lr+'Leg',Lr+'Foot',Lr+'ToeBase'])))
        BT=tree_of([b])
        if cuff:
            c=cen_at(TOP); st=[Vector((c.x,c.y,z)) for z in np.linspace(TOP+0.004,TOP-cuff,4)]
            r=tube(st,Z,sel&(np.abs(P[:,2]-TOP)<0.08),28,lambda t,a:cuff_off+0.004*math.sin(t*math.pi),center_fn=cen_bbox,smooth=1)
            r=rag_hem(r,0.012,seed=9+sg,rows=1,teeth=(3,6)) if cuff>0.035 else r
            o=grid_mesh('cuff'+Lr,r,wrap=True); fix_normals_out(o); solidify(o,0.004); decimate(o,cuff_budget,sym=False)
            out.append(add(o,mat,w_bodyT([Lr+'Leg'])))
        for z in straps:
            c=cen_at(z); pts=wrap_ring(Vector((c.x,c.y,z)),Vector((0,0,1)),0.003,18,BT,reach=0.2)
            o=strap('bstrap',pts+[pts[0]],0.018,0.0035,up=lambda p,c=c:(p-Vector((c.x,c.y,p.z))).normalized())
            out.append(add(o,'leather_dark',w_bodyT([Lr+'Leg',Lr+'Foot'])))
            bp=surfp((c.x,c.y,z),(sg*0.75,-0.66,0),0.006,0.2,tree=BT)
            k=prim('cube',loc=bp,rot=(0,0,-math.atan2(sg*0.75,0.66)),scale=(0.026,0.008,0.024))
            out.append(add(k,metal,lambda c_,Lr=Lr:{S+Lr+'Leg':1}))
        so_=sole('sole'+Lr,[v.co[:] for v in b.data.vertices],0.0,sole_h,lip=0.006)
        if heel:
            for v in so_.data.vertices:
                if v.co.z>0.001 and v.co.y>an.y-0.025: v.co.z+=heel_h
        rigid_w=lambda c_,Lr=Lr:{S+Lr+'Foot':1.0} if c_.y>an.y-0.06 else {S+Lr+'Foot':0.5,S+Lr+'ToeBase':0.5}
        out.append(add(so_,sole_mat,w_bodyT([Lr+'Foot',Lr+'ToeBase'])))
    return out
