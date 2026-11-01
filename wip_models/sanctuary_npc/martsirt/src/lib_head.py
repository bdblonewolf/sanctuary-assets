# hair / beard shells + face masks. exec after lib_bl (needs L landmarks)
def face_frame(co):
    hc=L['head_c']; x=co[:,0]; y=co[:,1]-hc[1]; z=co[:,2]
    phi=np.degrees(np.arctan2(np.abs(x),-y))   # 0 front, 90 side, 180 back
    return x,y,z,phi
def sm(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def hairline(phi,front=0.050,side=0.022,behind=-0.035,back=-0.085,temple=0.035):
    ez=L['eye_z']
    return ez+np.interp(phi,[0,35,62,100,125,180],[front,temple,side,side-0.004,behind,back])
def scalp_mask(co,**kw):
    x,y,z,phi=face_frame(co); h=hairline(phi,**kw)
    m=np.clip((z-h)/0.018+0.5,0,1)
    ez=L['eye_z']; rx=L['head_rx']
    return m*(1-sm(rx-0.03,rx-0.012,np.abs(x))*(1-sm(ez+0.045,ez+0.065,z)))   # keep ears bare
def beard_mask(co,full=1.0,mustache=True):
    x,y,z,phi=face_frame(co); ez=L['eye_z']; m=L['mouth']; n=L['nose']; ch=L['chin']; rx=L['head_rx']; hc=L['head_c']
    ax=np.abs(x)
    ztop=ez-0.034+0.050*sm(0.035,rx-0.012,ax)          # cheek line rising into sideburns
    v=sm(-0.012,0.012,ztop-z)
    v*=1-sm(-0.008,0.016,y+0.004)*(1-sm(0,0.03,ch[2]-z+0.005))   # stop at ear line / behind jaw
    v*=sm(ch[2]-0.075,ch[2]-0.035,z)                   # down onto the throat
    neck=(z<ch[2]-0.01); v=np.where(neck,v*(1-sm(-0.03,0.0,co[:,1]-(ch[1]+0.075))),v)
    lr=np.sqrt((x/0.026)**2+((z-m[2]+0.002)/0.0095)**2)
    v=v*sm(0.85,1.5,lr)
    if not mustache: v*=1-((ax<0.03)&(z>m[2]-0.004))
    v=v*(1-sm(n[2]-0.024,n[2]-0.012,z)*(1-sm(0.016,0.028,ax)))
    return np.clip(v*full,0,1)
def shell_from_body(name,mask_fn,off_fn,thresh=0.04,vgroups=None):
    """duplicate head faces where mask>thresh, push out along normal by off_fn(co, mask). stores 'hedge' attribute."""
    me=BM; mask=mask_fn(P); keep=mask>thresh
    bm=bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
    dl=[f for f in bm.faces if not all(keep[v.index] for v in f.verts) or PMAT[f.index]!=MATN.index('skin')]
    bmesh.ops.delete(bm,geom=dl,context='FACES'); bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    idx=bm.verts.layers.int.new('src')
    nm=bpy.data.meshes.new(name); bm.to_mesh(nm); bm.free()
    o=link(bpy.data.objects.new(name,nm))
    co=np.array([v.co[:] for v in nm.vertices]); nn=np.array([v.normal[:] for v in nm.vertices]); mk=mask_fn(co)
    off=off_fn(co,mk)
    for v,d,n in zip(nm.vertices,off,nn): v.co=Vector(v.co)+Vector(n)*d
    set_attr(o,'hedge',lambda c:mk)
    for p in nm.polygons: p.use_smooth=True
    return o
