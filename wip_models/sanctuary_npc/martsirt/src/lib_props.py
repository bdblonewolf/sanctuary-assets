# hand grip frames + prop builders. exec after lib_bl
def hand_frame(Lr):
    """rest-pose grip frame of a hand: origin = fist centre, X = lateral (pinky->index), Y = finger dir, Z = palm normal (out of palm)."""
    h=bonesH[S+Lr+'Hand']; m1=bonesH[S+Lr+'HandMiddle1']; i1=bonesH[S+Lr+'HandIndex1']; p1=bonesH[S+Lr+'HandPinky1']; t2=bonesH[S+Lr+'HandThumb2']
    f=(m1-h).normalized(); lat=(i1-p1); lat=(lat-f*lat.dot(f)).normalized()
    n=f.cross(lat).normalized()
    if n.dot(t2-m1)<0: n=-n
    lat=n.cross(f).normalized()*(1 if lat.dot(n.cross(f))>0 else -1)
    o=h+(m1-h)*0.78+n*0.028
    M=Matrix.Identity(4)
    for i in range(3): M[i][0]=lat[i]; M[i][1]=f[i]; M[i][2]=n[i]; M[i][3]=o[i]
    return M
def place(o,M):
    o.data.transform(M); o.data.update(); return o
def cyl(r,dep,loc,axis='X',v=10):
    rot={'X':(0,D(90),0),'Y':(D(90),0,0),'Z':(0,0,0)}[axis]
    return prim('cylinder',loc=loc,rot=rot,vertices=v,radius=r,depth=dep)
def make_hammer(name,handle=0.36,head=0.12,grip_frac=0.25,face_r=0.018,wmat='wood_handle',imat='iron_tool'):
    """canonical: shaft along +X (head end at +X), grip at origin, hammer face toward -Z... face points along +Y? we use face dir = +Z."""
    x0=-handle*grip_frac; x1=x0+handle
    sh=cyl(0.0135,handle,((x0+x1)/2,0,0),'X',8)
    for v in sh.data.vertices: v.co.y*=0.8 if True else 1
    hd=prim('cube',loc=(x1-0.018,0,0.010),scale=(0.034,0.030,head))
    bm=bmesh.new(); bm.from_mesh(hd.data)
    for v in bm.verts:
        if v.co.z<0: v.co.x=(x1-0.018)+(v.co.x-(x1-0.018))*0.2; v.co.y*=1.0   # cross peen wedge (toward -Z)
        else: v.co.x=(x1-0.018)+(v.co.x-(x1-0.018))*1.12; v.co.y*=1.12
    bm.to_mesh(hd.data); bm.free()
    fc=cyl(face_r,0.016,(x1-0.018,0,0.010+head/2+0.004),'Z',10)
    w=join([sh],name+'_w'); i=join([hd,fc],name+'_i')
    return w,i
def make_tongs(name,length=0.46):
    parts=[]
    for s_ in (1,-1):
        pts=[Vector((-0.12,0.006*s_,0)),Vector((0.10,0.005*s_,0)),Vector((0.20,0.0,0)),Vector((0.28,0.010*s_,0.0)),Vector((0.34,0.010*s_,0.0))]
        parts.append(rope('tongarm',pts,0.0055,1))
    bar=prim('cube',loc=(0.40,0,0),scale=(0.16,0.022,0.022))
    piv=cyl(0.009,0.03,(0.20,0,0),'Y',8)
    return join(parts+[piv],name+'_i'),bar
