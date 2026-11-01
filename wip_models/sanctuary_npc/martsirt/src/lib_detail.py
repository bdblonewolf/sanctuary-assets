# Detail geometry helpers (quality pass): face sculpt, strand cards, braids, folds, ragged hems, soles, pouches, rivets.
# exec after lib_bl (+ lib_head for masks).
def refresh_body():
    global P,NRM,bvh
    BM.update(); P=np.array([v.co[:] for v in BM.vertices]); NRM=np.array([v.normal[:] for v in BM.vertices])
    bvh=BVHTree.FromPolygons([Vector(p) for p in P],POLYS)
def sculpt(ops,head_only=True):
    """ops: list of (center xyz, radii xyz, amount m along vertex normal (+out), optional extra vector offset)."""
    hd=np.array([d==S+'Head' or d==S+'Neck' for d in dom])
    D_=np.zeros((NV,3))
    for op in ops:
        c,r,amt=np.array(op[0]),np.array(op[1]),op[2]; vec=np.array(op[3]) if len(op)>3 else None
        q=((P-c)/r)**2; w=np.exp(-2.5*q.sum(1)); w[q.sum(1)>4]=0
        if head_only: w*=hd
        D_+=NRM*(w*amt)[:,None]
        if vec is not None: D_+=w[:,None]*vec[None,:]
    for v,d in zip(BM.vertices,D_): v.co=Vector(v.co)+Vector(d)
    refresh_body(); print('SCULPT max',float(np.abs(D_).max()))
def _pick_roots(mask_fn,n,rng,thresh=0.55,weight_fn=None):
    m=mask_fn(P); skin=MATN.index('skin'); cand=[];wa=[]
    for i,(pl,mt) in enumerate(zip(POLYS,PMAT)):
        if mt!=skin: continue
        mm=float(np.mean(m[list(pl)]))
        if mm<thresh: continue
        a=BM.polygons[i].area*(weight_fn(P[list(pl)].mean(0)) if weight_fn else 1.0); cand.append(i); wa.append(a)
    wa=np.array(wa); wa/=wa.sum(); pick=rng.choice(len(cand),n,p=wa); out=[]
    for k in pick:
        pl=POLYS[cand[k]]; b=rng.dirichlet(np.ones(len(pl))); p=(P[list(pl)]*b[:,None]).sum(0)
        nrm=Vector(BM.polygons[cand[k]].normal); out.append((Vector(p),nrm))
    return out
def hair_cards(name,mask_fn,n,length_fn,width,segs,flow_fn,off0=0.003,off_gain=0.004,hang_z=None,gravity=0.0,seed=1,taper=0.55,
               thresh=0.55,weight_fn=None,layer_fn=None,uspan=0.4,curl=0.0,trees=None,minoff=0.002):
    """Strand cards: roots sampled on the body skin where mask>thresh; each card follows the scalp (snapped at off) then,
    below hang_z, hangs (only pushed out). attribute card=1; UV v=1 at root."""
    rng=np.random.default_rng(seed); roots=_pick_roots(mask_fn,n,rng,thresh,weight_fn)
    bm=bmesh.new(); uvl=bm.loops.layers.uv.new('UVMap')
    for p0,n0 in roots:
        d=Vector(flow_fn(np.array(p0[:]),np.array(n0[:]))); d=(d-n0*d.dot(n0))
        if d.length<1e-6: continue
        d.normalize(); L_=float(length_fn(np.array(p0[:])))*rng.uniform(0.75,1.2)
        lay=float(layer_fn(np.array(p0[:]))) if layer_fn else 0.0
        pts=[p0+n0*(off0*0.4)]; nrs=[n0]; dc=d; twist=rng.normal(0,0.25)
        for k in range(1,segs+1):
            t=k/segs; q=pts[-1]+dc*(L_/segs)
            h=bvh.find_nearest(q); so=off0+off_gain*t+lay
            nn=nrs[-1]
            if h[0] is not None:
                nn=h[1].normalized(); dist=(q-h[0]).dot(nn)
                if hang_z is None or q.z>hang_z: q=h[0]+nn*so
                elif dist<max(so*0.6,minoff): q=h[0]+nn*max(so*0.6,minoff)
            for tr in (trees or []):
                h2=tr.find_nearest(q,0.03)
                if h2[0] is not None and (q-h2[0]).dot(h2[1])<minoff: q=h2[0]+h2[1].normalized()*minoff
            dn=(q-pts[-1]).normalized()
            if gravity and (hang_z is None or q.z<hang_z+0.03): dn=(dn+Vector((0,0,-gravity*t))).normalized()
            if curl: dn=(dn+nn.cross(dn)*curl*math.sin(k*1.7+twist*5)).normalized()
            pts.append(q); nrs.append(nn); dc=dn
        u0=rng.uniform(0,1-uspan); ring=[]
        for k,(q,nn) in enumerate(zip(pts,nrs)):
            t=k/segs; tg=(pts[min(k+1,segs)]-pts[max(k-1,0)]).normalized()
            sd=nn.cross(tg).normalized(); sd=(sd+nn*twist*t).normalized()
            w=width*(1-(1-taper)*t)*0.5
            ring.append((bm.verts.new(q+sd*w),bm.verts.new(q-sd*w),t))
        for k in range(segs):
            a,b,ta=ring[k]; c,d_,tb=ring[k+1]
            f=bm.faces.new((a,b,d_,c))
            for l,uv in zip(f.loops,((u0,1-ta),(u0+uspan,1-ta),(u0+uspan,1-tb),(u0,1-tb))): l[uvl].uv=uv
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o=link(bpy.data.objects.new(name,me))
    set_attr(o,'card',lambda c:np.ones(len(c))); set_attr(o,'hedge',lambda c:np.ones(len(c)))
    for p_ in me.polygons: p_.use_smooth=True
    print('CARDS',name,len(roots),tris(o)); return o
def braid(name,path,r0,r1,lobes=9,seg=6,ring=5):
    """three-strand look: chain of tilted, alternating ellipsoid lobes along a polyline path"""
    path=[Vector(p) for p in path]; L_=sum((path[i+1]-path[i]).length for i in range(len(path)-1))
    def at(s):
        acc=0
        for i in range(len(path)-1):
            l=(path[i+1]-path[i]).length
            if acc+l>=s: t=(s-acc)/l; return path[i].lerp(path[i+1],t),(path[i+1]-path[i]).normalized()
            acc+=l
        return path[-1],(path[-1]-path[-2]).normalized()
    objs=[]
    for k in range(lobes):
        s=(k+0.5)/lobes*L_; c,tg=at(s); r=r0+(r1-r0)*k/max(lobes-1,1)
        e1,e2=frame(tg); sg=1 if k%2 else -1
        o=prim('uv_sphere',loc=(0,0,0),segments=seg,ring_count=ring,radius=1.0)
        q=tg.to_track_quat('Z','Y'); M=Matrix.Translation(c+e1*sg*r*0.35)@(Matrix.Rotation(D(28)*sg,4,e2)@q.to_matrix().to_4x4())@Matrix.Diagonal((r*1.05,r*0.8,L_/lobes*0.85,1))
        o.data.transform(M); objs.append(o)
    o=join(objs,name); set_attr(o,'hedge',lambda c:np.ones(len(c))); set_attr(o,'card',lambda c:np.zeros(len(c)))
    return o
def fold_rows(R,amp,nf,z0=None,z1=None,seed=3,vertical=True,phase_drift=1.5):
    """displace a panel/tube grid R (rows=z, cols=around) along its local outward normal with hanging folds.
    amp grows from z0 (0) to z1 (full)."""
    rng=np.random.default_rng(seed); ns,nt,_=R.shape; out=R.copy()
    ph=rng.uniform(0,6.28,4); fr=[nf,nf*1.7,nf*2.9]
    for i in range(ns):
        z=R[i,:,2].mean(); g=1.0 if z0 is None else ss(z0,z1,z)
        for j in range(nt):
            u=j/(nt-1); tdrift=i/(ns-1)*phase_drift
            v=0.65*math.sin(u*6.283*fr[0]+ph[0]+tdrift)+0.25*math.sin(u*6.283*fr[1]+ph[1]-tdrift*1.3)+0.10*math.sin(u*6.283*fr[2]+ph[2])
            jp=max(j-1,0); jn=min(j+1,nt-1); tg=R[i,jn]-R[i,jp]; tg/=np.linalg.norm(tg)+1e-9
            nrm=np.cross(np.array([0,0,1.0]),tg); nrm/=np.linalg.norm(nrm)+1e-9
            out[i,j]+=nrm*amp*g*v
    return out
def rag_hem(R,depth,seed=5,rows=3,teeth=(2,5)):
    """ragged hem: random jagged tongues on the last rows of a grid"""
    rng=np.random.default_rng(seed); ns,nt,_=R.shape; prof=np.zeros(nt); j=0
    while j<nt:
        w=int(rng.integers(*teeth)); d=rng.uniform(0.2,1.0)*depth
        for k in range(w):
            if j+k<nt: prof[j+k]=d*math.sin(math.pi*(k+0.5)/w)**0.7
        j+=w
    for r_ in range(rows):
        R[ns-1-r_,:,2]-=prof*(1-r_/rows)
        R[ns-1-r_,:,2]+=rng.uniform(0,0.004,nt)*(r_==0)
    return R
def crumple(o,amp,scale,mask=None,seed=0):
    from mathutils import noise as mn
    me=o.data; me.calc_normals() if hasattr(me,'calc_normals') else None
    off=Vector((seed*13.1,seed*7.7,seed*3.3))
    for v in me.vertices:
        w=1.0 if mask is None else mask(v.co)
        if w<=0: continue
        v.co=v.co+v.normal*(amp*w*mn.noise(v.co*scale+off))
def burn_holes(o,centers,rad,rng=None):
    """delete faces of a thin panel near centers -> burn holes (before solidify)"""
    bm=bmesh.new(); bm.from_mesh(o.data); dl=[]
    for f in bm.faces:
        c=f.calc_center_median()
        for cc,r in zip(centers,rad):
            if (c-Vector(cc)).length<r: dl.append(f); break
    bmesh.ops.delete(bm,geom=list(set(dl)),context='FACES'); bm.to_mesh(o.data); bm.free(); return o
def rivets(name,pts,nrms,r=0.0045,h=0.003):
    objs=[]
    for p,n in zip(pts,nrms):
        o=prim('uv_sphere',segments=5,ring_count=3,radius=1.0); n=Vector(n).normalized()
        q=n.to_track_quat('Z','Y'); o.data.transform(Matrix.Translation(Vector(p))@q.to_matrix().to_4x4()@Matrix.Diagonal((r,r,h,1)))
        objs.append(o)
    return join(objs,name)
def pouch(name,c,out,w=0.10,h=0.11,d=0.045,flap=0.05):
    """belt pouch: rounded box body + flap. c=attach point (top centre), out=outward horizontal normal"""
    out=Vector(out).normalized(); up=Vector((0,0,1)); sd=up.cross(out).normalized()
    M=Matrix((sd,out,up)).transposed().to_4x4(); M.translation=Vector(c)+out*(d*0.5)
    b=prim('cube',scale=(w,d,h)); b.data.transform(Matrix.Translation((0,0,-h*0.5)))
    m=b.modifiers.new('b','BEVEL'); m.width=0.012; m.segments=2; apply_mod(b,m)
    for v in b.data.vertices:
        if v.co.z<-h*0.6: v.co.x*=0.9; v.co.y*=0.85
        v.co.y+=0.006*math.sin(v.co.x/w*3.1)   # bulge
    f=prim('cube',scale=(w*1.04,d*1.12,0.006)); f.data.transform(Matrix.Translation((0,0.002,0.0)))
    fl=prim('cube',scale=(w*1.04,0.006,flap)); fl.data.transform(Matrix.Translation((0,d*0.56+0.003,-flap*0.5)))
    for v in fl.data.vertices:
        if v.co.z<-flap*0.9: v.co.x*=0.55
    o=join([b,f,fl],name); o.data.transform(M); return o
def sole(name,feet_obj_pts,z0=0.0,z1=0.026,lip=0.006,n=36):
    """flat outsole slab under a boot: convex hull of boot verts below 3 cm, grown by lip"""
    Q=np.array(feet_obj_pts); Q=Q[Q[:,2]<0.035]; h=hull2d(Q[:,:2]); c=h.mean(0)
    angs=np.linspace(0,2*math.pi,n,endpoint=False); ring=[]
    for a in angs:
        rr=ray_r(h,c,a)+lip; ring.append((c[0]+rr*math.cos(a),c[1]+rr*math.sin(a)))
    bm=bmesh.new(); lo=[bm.verts.new((x,y,z0)) for x,y in ring]; hi=[bm.verts.new((x,y,z1)) for x,y in ring]
    for i in range(n):
        j=(i+1)%n; bm.faces.new((lo[i],lo[j],hi[j],hi[i]))
    bm.faces.new(hi); bm.faces.new(lo[::-1])
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o=link(bpy.data.objects.new(name,me)); return o
