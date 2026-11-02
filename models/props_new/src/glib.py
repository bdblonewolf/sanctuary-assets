# extra shape helpers for gothic props / loot (Blender side)
from lib import *
import lib
def applymods(objs):
    for o in objs:
        if o.type!='MESH': continue
        for md in list(o.modifiers):
            bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
            bpy.ops.object.modifier_apply(modifier=md.name)
def J(objs,name,parent=None):
    objs=[o for o in objs if o is not None]; applymods(objs); o=join(objs,name); apply_tf(o)
    if parent: o.parent=parent
    return o
def slab(name,pts,th,m=None,loc=(0,0,0),rot=(0,0,0),uvscale=1.0,grain='z',bevel=0.0):
    """extrude 2D outline pts[(x,z)] along Y by th (centred)"""
    n=len(pts); V=[(x,-th/2,z) for x,z in pts]+[(x,th/2,z) for x,z in pts]
    F=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
    o=obj_from(name,V,F,m)
    bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(o.data); bm.free()
    if bevel>0:
        md=o.modifiers.new('bv','BEVEL'); md.width=bevel; md.segments=1; md.limit_method='ANGLE'
    place(o,loc,rot)
    if m is not None: box_uv(o,uvscale,grain)
    smooth(o,30); return o
def arch_pts(w,hs,ha,n=6,base=0.0):
    """gothic pointed arch outline (x,z) from bottom-left, CCW-ish: left side up, arch to apex, right side down"""
    r=w  # equilateral arch: centres at +-w/2 with radius w
    L=[(-w/2,base),(w/2,base),(w/2,hs)]
    # right arc: centre (-w/2,hs), from angle 0 to apex
    a1=math.atan2(ha-hs,w/2+w/2)  # angle to apex from left centre... use generic: centre cx=-w/2+... keep simple with lerp spline
    R=[]
    for i in range(1,n+1):
        t=i/n; x=w/2*(1-t); z=hs+(ha-hs)*math.sin(t*math.pi/2)**0.8
        R.append((x,z))
    Lf=[(-x,z) for x,z in reversed(R[:-1])]
    return L+R+Lf+[(-w/2,hs)]
def ring(name,r,rt,m,loc=(0,0,0),rot=(0,0,0),n=16,sides=6,uvscale=1.0,squash=None):
    path=[(r*math.cos(2*math.pi*i/n),r*math.sin(2*math.pi*i/n),0) for i in range(n+1)]
    o=tube(name,path,rt,sides,m,cap=False,uvscale=uvscale,squash=[squash]*(n+1) if squash else None,angle=80); weld(o); place(o,loc,rot); return o
def link(name,L,W,rt,m,loc,rot):
    """oval chain link lying in XZ-plane, long axis Z"""
    path=[]
    for i in range(7):
        a=2*math.pi*i/6; path.append((W/2*math.cos(a),0,L/2*math.sin(a)))
    o=tube(name,path,rt,4,m,cap=False,uvscale=0.2,angle=80); weld(o); place(o,loc,rot); return o
def chain(name,p0,p1,m,link_len=0.09,rt=0.012,sag=0.0):
    p0=Vector(p0);p1=Vector(p1); d=(p1-p0); n=max(2,int(d.length/(link_len*0.78))); out=[]
    for i in range(n):
        t=(i+0.5)/n; p=p0.lerp(p1,t); p.z-=sag*4*t*(1-t)
        t2=min(1,(i+1.5)/n); q=p0.lerp(p1,t2); q.z-=sag*4*t2*(1-t2); dirv=(q-p) if i<n-1 else (p-p0.lerp(p1,(i-0.5)/n))
        rq=Vector((0,0,1)).rotation_difference(dirv.normalized()).to_euler()
        o=link(f'{name}{i}',link_len,link_len*0.55,rt,m,p,rq)
        o.rotation_mode='XYZ'
        if i%2: o.rotation_euler.rotate_axis('Z',math.pi/2)
        out.append(o)
    bpy.context.view_layer.update()
    for o in out: apply_tf(o)
    return J(out,name)
def flame(name,loc,h=0.11):
    m=cutout('cut_flame','flame_q.png',rough=1.0,emissive=True); w=h*0.45; o=[]
    for k in range(2):
        a=k*math.pi/2; c,s=math.cos(a)*w/2,math.sin(a)*w/2
        V=[(-c,-s,0),(c,s,0),(c,s,h),(-c,-s,h)]; UV=[(0,0),(1,0),(1,1),(0,1)]
        q=obj_uvv(f'{name}{k}',V,[(0,1,2,3)],UV,m,angle=89); o.append(q)
    f=join(o,name); place(f,loc); bpy.context.view_layer.update(); apply_tf(f); return f
def candle(name,loc,h=0.22,r=0.03,lit=True,m=None):
    m=m or mat('bone',tint=(0.95,0.9,0.75),name='m_wax',normal=False)
    drip=[(r,0),(r*1.08,0.02),(r,0.04),(r,h*0.85),(r*1.05,h*0.9),(r*0.85,h),(r*0.2,h*0.97)]
    c=lathe(name,drip,8,m,loc=loc,uvscale=0.3)
    parts=[c]
    if lit: parts.append(flame(name+'_fl',(loc[0],loc[1],loc[2]+h*0.93)))
    return parts
def cloth_grid(name,w,h,nu,nv,fn,m,uvs=(1,1)):
    """grid in local XZ: fn(u,v)->(x,y,z)"""
    V=[];F=[];UV=[]
    for j in range(nv+1):
        for i in range(nu+1):
            u,v=i/nu,j/nv; V.append(fn(u,v)); UV.append((u*uvs[0],(1-v)*uvs[1]))
    for j in range(nv):
        for i in range(nu): a=j*(nu+1)+i; F.append((a,a+1,a+nu+2,a+nu+1))
    return obj_uvv(name,V,F,UV,m,angle=89)
def spike(name,loc,dirv,L,r,m,sides=4):
    o=lathe(name,[(r,0),(0.0,L)],sides,m,cap_bot=True,uvscale=0.2,angle=89)
    o.rotation_euler=Vector((0,0,1)).rotation_difference(Vector(dirv).normalized()).to_euler(); o.location=loc
    bpy.context.view_layer.update(); apply_tf(o); return o
def dark_tx():
    return mat('rock_dark',tint=(0.07,0.06,0.05),name='m_socket',normal=False)
def skull_hd(name,s,m,jaw=True,lo=False):
    """skull at origin, base z=0, faces -Y. lo=True for loot budget (~190 tris)"""
    dk=dark_tx(); P=[]
    P.append(blob(name+'c',0.1*s,(0,0.012*s,0.1*s),m,sub=2,amp=0.06,freq=2.0,seed=hash(name)%40,scale=(0.8,1.0,0.86)))
    P.append(blob(name+'f',0.066*s,(0,-0.062*s,0.058*s),m,sub=1 if lo else 2,amp=0.05,seed=3,scale=(0.98,0.8,0.82)))
    P.append(tube(name+'br',[(-0.058*s,-0.098*s,0.098*s),(0,-0.112*s,0.106*s),(0.058*s,-0.098*s,0.098*s)],[0.013*s,0.016*s,0.013*s],4 if lo else 5,m,uvscale=0.2))
    for sx in (-1,1):
        P.append(blob(name+f'e{sx}',0.029*s,(sx*0.034*s,-0.108*s,0.078*s),dk,sub=1,amp=0.05,scale=(1,0.8,0.95)))
        if not lo: P.append(blob(name+f'z{sx}',0.022*s,(sx*0.062*s,-0.08*s,0.055*s),m,sub=1,amp=0.05,scale=(1.2,1.1,0.7)))
    P.append(blob(name+'n',0.015*s,(0,-0.124*s,0.05*s),dk,sub=1,amp=0.04,scale=(0.75,0.7,1.35)))
    # upper teeth (zigzag strip) + dark mouth gap
    tw=0.032*s; n=4 if lo else 6
    pts=[(-tw,0.0)]+[(-tw+2*tw*(k+0.5)/n, -0.013*s if k%2==0 else -0.010*s) for k in range(n)]+[(tw,0.0)]
    tpts=[(-tw,0.012*s)]+[(x,z) for x,z in [(-tw,0.0)]]
    teeth=[(-tw,0.012*s),(tw,0.012*s),(tw,0.0)]+[(-tw+2*tw*(k+1)/n,(-0.012*s if k%2==0 else -0.004*s)) for k in range(n-1)][::-1]+[(-tw,0.0)]
    t=slab(name+'t',teeth,0.012*s,(mat('bone',tint=(0.62,0.58,0.5),name='m_teeth') if m.name.startswith('m_bone') else m),uvscale=0.1); t.location=(0,-0.112*s,0.028*s); bpy.context.view_layer.update(); apply_tf(t); P.append(t)
    if jaw:
        P.append(tube(name+'j',[(-0.05*s,-0.03*s,0.045*s),(-0.046*s,-0.07*s,0.008*s),(0,-0.104*s,0.004*s),(0.046*s,-0.07*s,0.008*s),(0.05*s,-0.03*s,0.045*s)],[0.011*s,0.013*s,0.016*s,0.013*s,0.011*s],4,m,uvscale=0.2))
    else:
        P.append(blob(name+'g',0.012*s,(0,-0.1*s,0.02*s),dk,sub=1,amp=0.0,scale=(2.6,0.6,0.5)))
    return J(P,name)
def skull(name,loc,s=1.0,rotz=0.0,m=None,tilt=(0,0)):
    o=skull_hd(name,s,m or mat('bone'),jaw=True)
    o.rotation_euler=(tilt[0],tilt[1],rotz); o.location=loc; bpy.context.view_layer.update(); apply_tf(o); return o
def bone(name,p0,p1,r=0.022,m=None):
    m=m or mat('bone'); p0=Vector(p0);p1=Vector(p1); d=p1-p0
    sh=tube(name,[p0,p0+d*0.15,p0+d*0.5,p0+d*0.85,p1],[r*1.5,r*0.95,r*0.8,r*0.95,r*1.5],5,m,uvscale=0.3)
    k0=blob(name+'_k0',r*1.5,tuple(p0),m,sub=1,amp=0.1,scale=(1.3,1,1)); k1=blob(name+'_k1',r*1.5,tuple(p1),m,sub=1,amp=0.1,scale=(1.3,1,1))
    return J([sh,k0,k1],name)

def pivot_at(o,p):
    p=Vector(p); o.data.transform(Matrix.Translation(-p)); o.location=p; o.data.update(); return o
