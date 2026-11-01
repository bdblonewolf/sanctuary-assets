# Shared Blender helpers for the Martsirt NPC pipeline. exec() into a build script namespace.
# Coordinates: Blender Z-up, character faces -Y (glTF +Z after export), character left = +X.
import bpy, bmesh, math, os, sys, json
import numpy as np
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree
from mathutils.interpolate import poly_3d_calc
S='mixamorig:'; D=math.radians; Z=Vector((0,0,1))
RNG=np.random.default_rng(11)
def isarm(n): return any(k in n for k in ('Arm','Hand','Shoulder'))
# ------------------------------------------------------------------ body
def init_body(path):
    global arm,body,BM,P,NRM,Wt,dom,EDG,POLYS,PMAT,bvh,bonesH,bonesT,NV,side,MATN
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    for o in list(bpy.data.objects):
        if o.name.startswith('Icosphere'): bpy.data.objects.remove(o)
    arm=[o for o in bpy.data.objects if o.type=='ARMATURE'][0]
    body=[o for o in bpy.data.objects if o.type=='MESH'][0]
    BM=body.data; gname={g.index:g.name for g in body.vertex_groups}; NV=len(BM.vertices)
    P=np.array([v.co[:] for v in BM.vertices]); NRM=np.array([v.normal[:] for v in BM.vertices])
    Wt=[{gname[g.group]:g.weight for g in v.groups if g.weight>0} for v in BM.vertices]
    dom=[max(w,key=w.get) if w else '' for w in Wt]
    EDG=np.array([e.vertices[:] for e in BM.edges])
    POLYS=[p.vertices[:] for p in BM.polygons]; PMAT=[p.material_index for p in BM.polygons]
    MATN=[m.name for m in BM.materials]
    bvh=BVHTree.FromPolygons([Vector(p) for p in P],POLYS)
    bonesH={b.name:b.head_local.copy() for b in arm.data.bones}; bonesT={b.name:b.tail_local.copy() for b in arm.data.bones}
    side=np.sign(P[:,0])
    return arm,body
def BH(n): return bonesH[S+n].copy()
def landmarks():
    L={}
    mi=MATN.index('eye'); ev=set(i for p,m in zip(POLYS,PMAT) if m==mi for i in p); ev=np.array(sorted(ev))
    E=P[ev]
    for nm,sg in (('eyeL',1),('eyeR',-1)):
        q=E[np.sign(E[:,0])==sg]; c=q.mean(0); f=q[np.argmin(q[:,1])]
        L[nm]=c; L[nm+'_front']=f; L[nm+'_r']=float(np.linalg.norm(q-c,axis=1).max())
    head=np.array([d==S+'Head' for d in dom])
    ez=0.5*(L['eyeL'][2]+L['eyeR'][2]); L['eye_z']=ez; L['eye_x']=abs(L['eyeL'][0])
    mid=head&(np.abs(P[:,0])<0.012)
    q=P[mid&(P[:,2]<ez)&(P[:,2]>ez-0.07)]; L['nose']=q[np.argmin(q[:,1])]
    q=P[mid&(P[:,2]<L['nose'][2]-0.02)&(P[:,2]>L['nose'][2]-0.06)]
    # mouth: upper lip region = local forward max below the nose; approx 0.033 below nose tip
    L['mouth']=np.array([0,0,L['nose'][2]-0.032]); hit=bvh.ray_cast(Vector((0,-0.5,L['mouth'][2])),Vector((0,1,0))); L['mouth']=np.array(hit[0][:])
    q=P[head&(np.abs(P[:,0])<0.02)]; qq=q[q[:,1]<L['eyeL'][1]+0.02]; L['chin']=qq[np.argmin(qq[:,2])]
    L['head_top']=P[head][np.argmax(P[head][:,2])]
    hp=P[head]; L['head_c']=np.array([0,hp[:,1].mean(),ez+0.01])
    L['head_rx']=float(np.abs(hp[:,0]).max())
    # crotch
    q=P[(np.abs(P[:,0])<0.03)&(P[:,2]>0.5)&(P[:,2]<1.2)&np.array(['Leg' in d or 'Hips' in d for d in dom])]
    L['crotch_z']=float(q[:,2].min())
    return L
# ------------------------------------------------------------------ hull/tube
def hull2d(pts):
    pts=sorted(set(map(tuple,np.round(pts,5))))
    if len(pts)<3: return np.array(pts)
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return np.array(lo[:-1]+up[:-1])
def ray_r(h,c,ang):
    d=np.array([math.cos(ang),math.sin(ang)]); best=0; n=len(h)
    for i in range(n):
        a=h[i]-c; b=h[(i+1)%n]-c; e=b-a
        den=d[0]*(-e[1])-d[1]*(-e[0])
        if abs(den)<1e-12: continue
        t=(a[0]*(-e[1])-a[1]*(-e[0]))/den; s=(d[0]*a[1]-d[1]*a[0])/den
        if t>0 and -1e-6<=s<=1+1e-6: best=max(best,t)
    return best
def frame(axis,ref=None):
    axis=Vector(axis).normalized(); ref=ref or (Vector((1,0,0)) if abs(axis.x)<0.9 else Vector((0,1,0)))
    e1=(ref-axis*ref.dot(axis)).normalized(); e2=e1.cross(axis)   # axis=+Z: e1=+X(left), e2=-Y(front)
    return e1,e2
def cen_bbox(p2): return np.array([0.5*(p2[:,0].max()+p2[:,0].min()),0.5*(p2[:,1].max()+p2[:,1].min())])
def section(st,ax,sel,EA=None,EB=None):
    st=np.array(st[:]); AX=np.array(ax[:])
    da=(EA-st)@AX; db=(EB-st)@AX; cx=(da*db)<0
    tt=(da[cx]/(da[cx]-db[cx]))[:,None]; pts=EA[cx]+(EB[cx]-EA[cx])*tt
    if len(pts)<3:
        Q=P[sel]; d=(Q-st)@AX; pts=Q[np.argsort(np.abs(d))[:12]]
    return pts
def tube(stations, axes, sel, nth, off, th_range=(0,2*math.pi), center_fn=None, drape=False, smooth=2, minr=0.0, flare=None, ref=None):
    """Generic slice-hull tube. stations: list of Vectors; axes: one Vector or list (per-station). Returns rings (ns,nth,3).
    theta measured in the station frame (e1,e2); for axis=+Z: 0=+X (char left), 90deg=-Y (front), 180=right, 270=back."""
    ns=len(stations)
    if isinstance(axes,Vector): axes=[axes]*ns
    em=sel[EDG[:,0]]&sel[EDG[:,1]]; EA=P[EDG[em,0]]; EB=P[EDG[em,1]]
    frames=[]; e1p=None
    for a in axes:
        a=a.normalized()
        if e1p is None: e1,e2=frame(a,ref)
        else:
            e1=(e1p-a*e1p.dot(a)).normalized(); e2=e1.cross(a)
        frames.append((e1,e2,a)); e1p=e1
    full=(th_range[1]-th_range[0])>6.28
    angs=np.linspace(th_range[0],th_range[1],nth,endpoint=not full)
    R=[];C=[]
    for st,(e1,e2,a) in zip(stations,frames):
        pts=section(st,a,sel,EA,EB); s0=np.array(st[:])
        p2=np.stack([(pts-s0)@np.array(e1[:]),(pts-s0)@np.array(e2[:])],1); h=hull2d(p2)
        c=np.zeros(2) if center_fn is None else center_fn(p2)
        R.append([max(ray_r(h,c,an),minr) for an in angs]); C.append(c)
    R=np.array(R); C=np.array(C)
    for _ in range(smooth):
        Rm=R.copy(); Rm[1:-1]=np.maximum(np.maximum(R[:-2],R[2:]),R[1:-1]); R=0.5*R+0.5*Rm
        if full: R=np.maximum(R,0.5*(np.roll(R,1,1)+np.roll(R,-1,1)))
    if drape:
        for i in range(1,ns): R[i]=np.maximum(R[i],R[i-1]*0.99)
    out=np.zeros((ns,nth,3))
    for i,(st,(e1,e2,a)) in enumerate(zip(stations,frames)):
        s0=np.array(st[:]); E1=np.array(e1[:]); E2=np.array(e2[:]); cc=s0+C[i][0]*E1+C[i][1]*E2
        for j,an in enumerate(angs):
            o=off(i/(ns-1),an) if callable(off) else off
            fl=flare(i/(ns-1)) if flare else 1.0
            out[i,j]=cc+(R[i,j]*fl+o)*(math.cos(an)*E1+math.sin(an)*E2)
    return out
def link(o):
    bpy.context.scene.collection.objects.link(o); return o
def grid_mesh(name, rings, wrap=False, uvrect=(0,0,1,1)):
    ns,nt,_=rings.shape; bm=bmesh.new(); V=[[bm.verts.new(rings[i,j]) for j in range(nt)] for i in range(ns)]
    uvl=bm.loops.layers.uv.new('UVMap'); x0,y0,x1,y1=uvrect
    def uv(i,j): return (x0+(x1-x0)*j/(nt if wrap else nt-1), 1-(y0+(y1-y0)*i/(ns-1)))
    for i in range(ns-1):
        for j in range(nt if wrap else nt-1):
            j2=(j+1)%nt; f=bm.faces.new((V[i][j],V[i][j2],V[i+1][j2],V[i+1][j]))
            for l,(ii,jj) in zip(f.loops,((i,j),(i,j+1),(i+1,j+1),(i+1,j))): l[uvl].uv=uv(ii,jj)
    me=bpy.data.meshes.new(name); bm.normal_update(); bm.to_mesh(me); bm.free()
    o=bpy.data.objects.new(name,me); link(o); return o
def fix_normals_out(o):
    me=o.data; flip=0; tot=0
    for p in me.polygons:
        r=bvh.find_nearest(p.center)
        if r[0] is None: continue
        tot+=1; flip+=(p.normal.dot(p.center-r[0])<0)
    if flip>tot/2:
        bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.reverse_faces(bm,faces=bm.faces); bm.to_mesh(me); bm.free()
    return o
def snug(o,off,blend=None):
    for v in o.data.vertices:
        h=bvh.find_nearest(v.co)
        if h[0] is not None:
            t=1.0 if blend is None else blend(v.co)
            v.co=v.co.lerp(h[0]+h[1].normalized()*off,t)
def push_out(o,mn,others=None):
    """keep every vertex at least mn outside the body (and optional extra BVHs)."""
    trees=[bvh]+(others or [])
    for v in o.data.vertices:
        for k,tr in enumerate(trees):
            h=tr.find_nearest(v.co) if k==0 else tr.find_nearest(v.co,0.03)
            if h[0] is None: continue
            d=v.co-h[0]
            if d.dot(h[1])<mn: v.co=h[0]+h[1].normalized()*mn
def apply_mod(o,m):
    bpy.ops.object.select_all(action='DESELECT'); bpy.context.view_layer.objects.active=o; o.select_set(True)
    bpy.ops.object.modifier_apply(modifier=m.name); o.select_set(False)
def solidify(o,t,rim=True,offset=1.0):
    m=o.modifiers.new('s','SOLIDIFY'); m.thickness=t; m.offset=offset; m.use_rim=rim; m.use_even_offset=True; m.use_quality_normals=True
    apply_mod(o,m); return o
def close_tube(o):
    bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.holes_fill(bm,edges=bm.edges,sides=0); bm.to_mesh(o.data); bm.free()
def to_mesh_obj(ob):
    bpy.ops.object.select_all(action='DESELECT'); bpy.context.view_layer.objects.active=ob; ob.select_set(True)
    bpy.ops.object.convert(target='MESH'); ob=bpy.context.view_layer.objects.active; ob.select_set(False); return ob
def rope(name,pts,rad=0.002,res=1,closed=False):
    cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; cu.bevel_depth=rad; cu.bevel_resolution=res; cu.resolution_u=2; cu.use_fill_caps=True
    sp=cu.splines.new('POLY'); sp.points.add(len(pts)-1); sp.use_cyclic_u=closed
    for q,pp in zip(sp.points,pts): q.co=(pp[0],pp[1],pp[2],1)
    ob=bpy.data.objects.new(name,cu); link(ob); return to_mesh_obj(ob)
def strap(name,pts,width,thick,up=None):
    """flat strap ribbon along pts; 'up' = function(point)->normal direction of the strap face"""
    bm=bmesh.new(); rows=[]
    for i,p in enumerate(pts):
        p=Vector(p); t=(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(i-1,0)])).normalized()
        n=up(p) if up else Vector((0,0,1)); n=(n-t*n.dot(t)).normalized(); b=t.cross(n).normalized()
        rows.append([bm.verts.new(p+b*width/2),bm.verts.new(p-b*width/2)])
    for i in range(len(rows)-1): bm.faces.new((rows[i][0],rows[i][1],rows[i+1][1],rows[i+1][0]))
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o=link(bpy.data.objects.new(name,me))
    return solidify(o,thick,offset=0)
def surfp(c,d,off=0.004,reach=0.25,tree=None):
    c=Vector(c); d=Vector(d).normalized(); h=(tree or bvh).ray_cast(c+d*reach,-d)
    return (h[0]+d*off) if h[0] is not None else c+d*off
def wrap_ring(c,ax,off,n=32,tree=None,rad=0.003,reach=0.2):
    e1,e2=frame(ax); pts=[]
    for a in np.linspace(0,2*math.pi,n,endpoint=False):
        d=e1*math.cos(a)+e2*math.sin(a); pts.append(surfp(c,d,off,reach,tree))
    return pts
def prim(kind,loc=(0,0,0),rot=(0,0,0),scale=(1,1,1),**kw):
    if kind=='cube' and 'size' not in kw: kw['size']=1.0
    getattr(bpy.ops.mesh,'primitive_'+kind+'_add')(location=loc,rotation=rot,**kw); o=bpy.context.active_object
    o.scale=scale; bpy.ops.object.transform_apply(location=True,rotation=True,scale=True); o.select_set(False); return o
def join(objs,name):
    objs=[o for o in objs if o is not None]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]; bpy.ops.object.join(); o=bpy.context.view_layer.objects.active
    o.name=name; o.data.name=name; o.select_set(False); return o
def tris(o): return sum(len(p.vertices)-2 for p in o.data.polygons)
def tree_of(objs):
    V=[];F=[]
    for o in objs:
        M=o.matrix_world; b=len(V); V+=[M@v.co for v in o.data.vertices]; F+=[[b+i for i in p.vertices] for p in o.data.polygons]
    return BVHTree.FromPolygons(V,F)
# ------------------------------------------------------------------ weights
def body_w(co,allowed=None):
    loc,nor,fi,dist=bvh.find_nearest(co)
    poly=POLYS[fi]; vs=[Vector(P[i]) for i in poly]
    bw=poly_3d_calc(vs,loc); out={}
    for vi,b in zip(poly,bw):
        for g,w in Wt[vi].items():
            if allowed is None or g in allowed: out[g]=out.get(g,0)+w*b
    return out
def assign(o,fn,smooth=3,allowed=None):
    me=o.data; n=len(me.vertices); ws=[]
    for v in me.vertices:
        w=fn(v.co.copy())
        if allowed is not None: w={g:x for g,x in w.items() if g in allowed}
        ws.append({g:x for g,x in w.items() if x>1e-4})
    adj=[[] for _ in range(n)]
    for e in me.edges: a,b=e.vertices; adj[a].append(b); adj[b].append(a)
    for _ in range(200):
        emp=[i for i in range(n) if not ws[i]]
        if not emp: break
        upd={}
        for i in emp:
            acc={}
            for j in adj[i]:
                for g,x in ws[j].items(): acc[g]=acc.get(g,0)+x
            if acc: t=sum(acc.values()); upd[i]={g:x/t for g,x in acc.items()}
        if not upd: break
        for i,w in upd.items(): ws[i]=w
    for i in range(n):
        if not ws[i]: ws[i]={S+'Hips':1.0}
    for _ in range(smooth):
        nw=[]
        for i in range(n):
            acc=dict(ws[i]); k=1
            for j in adj[i]:
                for g,x in ws[j].items(): acc[g]=acc.get(g,0)+x
                k+=1
            nw.append({g:x/k for g,x in acc.items()})
        ws=nw
    o.vertex_groups.clear()
    for i,w in enumerate(ws):
        top=sorted(w.items(),key=lambda t:-t[1])[:4]; s=sum(x for _,x in top)
        for g,x in top:
            if x/s<0.01: continue
            vg=o.vertex_groups.get(g) or o.vertex_groups.new(name=g); vg.add([i],x/s,'REPLACE')
    return o
def rigid(o,bone): return assign(o,lambda c:{S+bone:1.0},smooth=0)
def ss(a,b,x):
    t=min(max((x-a)/(b-a),0),1); return t*t*(3-2*t)
def w_bodyT(allowed,limit=None):
    al={S+a for a in allowed}
    def f(c):
        w=body_w(c,al)
        return w if w else {S+allowed[0]:1}
    return f
def w_skirt(ztop,zbot,amt,hip_bone='Hips',x_split=0.10):
    def f(c):
        t=ss(ztop,zbot,c.z)*amt; l=ss(-x_split,x_split,c.x)
        return {S+hip_bone:1-t,S+'LeftUpLeg':t*l,S+'RightUpLeg':t*(1-l)}
    return f
# ------------------------------------------------------------------ body cleanup
def hide_body(cover_objs,maxd=0.07,keep=lambda i:False,eps=0.0015,force=lambda i:False):
    """delete body faces whose every vertex is covered (ray along normal hits a garment within maxd)."""
    tr=tree_of(cover_objs)
    cov=np.zeros(NV,bool)
    for i in range(NV):
        if keep(i): continue
        if force(i): cov[i]=True; continue
        p=Vector(P[i]); n=Vector(NRM[i])
        ok=True
        for d in (n,(n+Vector((0,0,0.35))).normalized(),(n-Vector((0,0,0.35))).normalized()):
            h=tr.ray_cast(p+n*eps,d,maxd)
            if h[0] is None: ok=False; break
        cov[i]=ok
    bm=bmesh.new(); bm.from_mesh(BM); bm.faces.ensure_lookup_table()
    dl=[f for f in bm.faces if all(cov[v.index] for v in f.verts)]
    bmesh.ops.delete(bm,geom=dl,context='FACES')
    loose=[v for v in bm.verts if not v.link_faces]; bmesh.ops.delete(bm,geom=loose,context='VERTS')
    bm.to_mesh(BM); bm.free(); BM.update()
    print('HIDE_BODY removed faces',len(dl))
def decimate(o,target,sym=True):
    t=tris(o)
    if t<=target: return o
    m=o.modifiers.new('d','DECIMATE'); m.ratio=target/t; m.use_symmetry=sym; m.symmetry_axis='X'; m.use_collapse_triangulate=True
    apply_mod(o,m); return o
def triangulate(o):
    m=o.modifiers.new('t','TRIANGULATE'); apply_mod(o,m)
# ------------------------------------------------------------------ attributes (masks used by the shaders at bake time)
def set_attr(o,name,fn):
    me=o.data
    if name in me.attributes: me.attributes.remove(me.attributes[name])
    a=me.attributes.new(name,'FLOAT','POINT')
    co=np.array([v.co[:] for v in me.vertices])
    vals=np.asarray(fn(co),dtype=float)
    a.data.foreach_set('value',vals.astype(np.float32))
