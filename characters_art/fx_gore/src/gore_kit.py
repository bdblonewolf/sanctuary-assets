# Blender: procedural gore cap kit. Up axis = +Z (glTF +Y). Nominal radius R0 = 0.05 m. Origin = centre of the cut plane.
import bpy, bmesh, math, random, sys, os
from mathutils import Vector, noise
OUT=sys.argv[sys.argv.index('--')+1]
bpy.ops.wm.read_factory_settings(use_empty=True)
T='/workspace/dmg/gore/textures/'
mat=bpy.data.materials.new('gore_flesh'); mat.use_nodes=True; nt=mat.node_tree; P=nt.nodes['Principled BSDF']
def img(n,non=False):
    i=bpy.data.images.load(T+n); 
    if non: i.colorspace_settings.name='Non-Color'
    t=nt.nodes.new('ShaderNodeTexImage'); t.image=i; return t
b=img('gore_atlas_bc.png'); nt.links.new(b.outputs[0],P.inputs['Base Color'])
o=img('gore_atlas_orm.png',True); sp=nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(o.outputs[0],sp.inputs[0]); nt.links.new(sp.outputs[1],P.inputs['Roughness']); nt.links.new(sp.outputs[2],P.inputs['Metallic'])
n=img('gore_atlas_n.png',True); nm=nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(n.outputs[0],nm.inputs[1]); nt.links.new(nm.outputs[0],P.inputs['Normal'])
R0=0.05
def fuv(x,y): return (0.375+0.36*x*0.92, 0.5-0.48*y*0.92)   # flesh disc uv (v flipped for blender)
def buv(a,h): return (0.75+0.25*(a/(2*math.pi)), 1-(0.2+0.8*h))
def make(name,seed,bone=True,bone_off=(0,0),bone_h=0.45,bone_r=0.24,split=False,rag=0.15,tatters=4,oval=(1,1),seg=24,
         dome=0.12,vert=False,trachea=False,guts=0,concave=False):
    rnd=random.Random(seed); bm=bmesh.new(); uvl=bm.loops.layers.uv.new('UVMap')
    rings=[0.0,0.18,0.32,0.5,0.68,0.85,1.0]
    if bone: rings=[r for r in rings if r==0 or r>bone_r+0.06]
    ph=rnd.random()*10
    def rad(a,r):
        if r<0.99: return r
        return r*(1+rag*(noise.noise(Vector((math.cos(a)*2+ph,math.sin(a)*2,seed)))*1.6)+rag*0.5*(rnd.random()-0.5))
    V=[]
    for ri,r in enumerate(rings):
        row=[]
        n=1 if r==0 else seg
        for k in range(n):
            a=2*math.pi*k/seg; rr=rad(a,r)
            x=math.cos(a)*rr*oval[0]; y=math.sin(a)*rr*oval[1]
            z=(dome*(1-r*r) if not concave else -0.05*(1-r*r))+0.04*noise.noise(Vector((x*3+ph,y*3,1)))
            if bone and r>0 and r<0.5: z+=0.04
            if r==1.0: z=-0.02+0.05*(rnd.random()-0.5)
            row.append(bm.verts.new((x,y,z)))
        V.append(row)
    # skirt ring going down (covers ragged openings)
    sk=[]
    for k in range(seg):
        v=V[-1][k].co; sk.append(bm.verts.new((v.x*0.93,v.y*0.93,-0.32-0.1*rnd.random())))
    V.append(sk)
    faces=[]
    def F(vs,uvs):
        try: f=bm.faces.new(vs)
        except ValueError: return
        for l,uv in zip(f.loops,uvs): l[uvl].uv=uv
    def duv(v): return fuv(v.co.x/max(oval[0],1e-3)/1.18,v.co.y/max(oval[1],1e-3)/1.18)
    start=0
    if bone:
        # bone ring at bone_r around offset, connect flesh inner ring to bone base ring
        bx,by=bone_off; nb=10
        base=[bm.verts.new((bx+math.cos(2*math.pi*k/nb)*bone_r,by+math.sin(2*math.pi*k/nb)*bone_r,0.04)) for k in range(nb)]
        tops=[]
        for k in range(nb):
            a=2*math.pi*k/nb; hh=bone_h*(0.75+0.5*rnd.random())
            if split and k in (2,3,7): hh*=1.6
            tops.append(bm.verts.new((bx+math.cos(a)*bone_r*0.92,by+math.sin(a)*bone_r*0.92,hh)))
        for k in range(nb):
            k2=(k+1)%nb; a1=2*math.pi*k/nb; a2=2*math.pi*(k+1)/nb
            F([base[k],base[k2],tops[k2],tops[k]],[buv(a1,0),buv(a2 if k2 else 2*math.pi,0),buv(a2 if k2 else 2*math.pi,0.95),buv(a1,0.95)])
        # marrow top, recessed centre
        c=bm.verts.new((bx,by,min(t.co.z for t in tops)*0.7))
        for k in range(nb):
            k2=(k+1)%nb; F([tops[k],tops[k2],c],[(0.8,0.95),(0.95,0.95),(0.875,0.85)])
        # bridge flesh first ring to bone base: nearest-angle fan
        ring=V[1]
        for k in range(seg):
            k2=(k+1)%seg; a=2*math.pi*(k+0.5)/seg; j=int(round(a/(2*math.pi)*nb))%nb
            F([ring[k2],ring[k],base[j]],[duv(ring[k2]),duv(ring[k]),duv(base[j])])
        for j in range(nb):
            j2=(j+1)%nb; a=2*math.pi*(j+1)/nb; k=int(round(a/(2*math.pi)*seg))%seg
            F([base[j],base[j2],ring[k]],[duv(base[j]),duv(base[j2]),duv(ring[k])])
        start=1
    else:
        c=V[0][0]; r1=V[1]
        for k in range(seg):
            k2=(k+1)%seg; F([c,r1[k],r1[k2]],[duv(c),duv(r1[k]),duv(r1[k2])])
        start=1
    for i in range(start,len(V)-1):
        A,B=V[i],V[i+1]
        for k in range(seg):
            k2=(k+1)%seg
            uvB=[duv(B[k2]),duv(B[k])] if i<len(V)-2 else [fuv(math.cos(2*math.pi*k2/seg)*0.99,math.sin(2*math.pi*k2/seg)*0.99),fuv(math.cos(2*math.pi*k/seg)*0.99,math.sin(2*math.pi*k/seg)*0.99)]
            F([A[k],A[k2],B[k2],B[k]],[duv(A[k]),duv(A[k2])]+uvB)
    # torn flaps hanging off the rim
    rim=V[-2]
    for t in range(tatters):
        k=rnd.randrange(seg); k2=(k+1+rnd.randrange(2))%seg; a=2*math.pi*k/seg
        L=0.25+0.3*rnd.random(); out=Vector((math.cos(a),math.sin(a),0))
        p1=rim[k].co+out*L*0.6+Vector((0,0,-L*0.6)); p2=rim[k2].co+out*L*0.5+Vector((0,0,-L*0.8))
        tip=(p1+p2)/2+out*L*0.3+Vector((0,0,-L*0.5))
        v1=bm.verts.new(p1); v2=bm.verts.new(p2); vt=bm.verts.new(tip)
        F([rim[k],rim[k2],v2,v1],[(0.07,0.5),(0.07,0.55),(0.02,0.55),(0.02,0.5)]); F([v1,v2,vt],[(0.02,0.5),(0.02,0.55),(0.01,0.52)])
        F([v1,rim[k],rim[k2],v2][::-1],[(0.02,0.5),(0.07,0.55),(0.07,0.5),(0.02,0.55)][::-1]) if False else None
    if vert:  # vertebra flange around the bone
        bx,by=bone_off; nb=8; inner=[];outer=[]
        for k in range(nb):
            a=2*math.pi*k/nb; ro=bone_r*(1.9 if k in (2,6) else 1.5)*(1.25 if k==4 else 1)
            inner.append(bm.verts.new((bx+math.cos(a)*bone_r*1.02,by+math.sin(a)*bone_r*1.02,bone_h*0.55)))
            outer.append(bm.verts.new((bx+math.cos(a)*ro,by+math.sin(a)*ro,bone_h*0.45)))
        for k in range(nb):
            k2=(k+1)%nb; F([inner[k],inner[k2],outer[k2],outer[k]],[(0.8,0.4),(0.9,0.4),(0.9,0.5),(0.8,0.5)])
    if trachea:  # dark tube hole toward front (-Y)
        nb=8; cx,cy=0,-0.5; top=[];bot=[]
        for k in range(nb):
            a=2*math.pi*k/nb
            top.append(bm.verts.new((cx+math.cos(a)*0.14,cy+math.sin(a)*0.11,0.16)))
            bot.append(bm.verts.new((cx+math.cos(a)*0.10,cy+math.sin(a)*0.08,-0.15)))
        for k in range(nb):
            k2=(k+1)%nb; F([top[k],top[k2],bot[k2],bot[k]],[(0.77,0.05),(0.8,0.05),(0.8,0.15),(0.77,0.15)])
    bm.normal_update()
    for g in range(guts):  # low-poly gut lumps
        a=rnd.uniform(-2.4,-0.7); rr=rnd.uniform(0.25,0.6)
        c=Vector((math.cos(a)*rr*oval[0],math.sin(a)*rr*oval[1],dome*0.8+0.05))
        s=rnd.uniform(0.14,0.22)
        res=bmesh.ops.create_icosphere(bm,subdivisions=1,radius=s)
        for v in res['verts']:
            v.co=c+Vector((v.co.x*1.4,v.co.y,v.co.z*0.8))
        for f in {f for v in res['verts'] for f in v.link_faces}:
            for l in f.loops: l[uvl].uv=fuv(0.1+0.3*(l.vert.co.x-c.x)/s,0.1+0.3*(l.vert.co.y-c.y)/s)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for v in me.vertices: v.co*=R0
    ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob); me.materials.append(mat)
    for p in me.polygons: p.use_smooth=True
    return ob
caps=[make('gore_cap_limb_a',1),
make('gore_cap_limb_b',2,bone_off=(0.12,-0.05),split=True,bone_h=0.6,rag=0.22,tatters=6),
make('gore_cap_limb_c',3,bone_h=0.22,bone_r=0.2,rag=0.1,tatters=3,dome=0.05),
make('gore_cap_neck',4,bone_off=(0,0.25),bone_h=0.4,bone_r=0.2,vert=True,trachea=True,tatters=5),
make('gore_cap_waist',5,bone_off=(0,0.5),bone_h=0.3,bone_r=0.18,vert=True,oval=(1.0,0.7),guts=4,tatters=6,seg=28),
make('gore_cap_flesh',6,bone=False,rag=0.2,tatters=4,dome=0.18),
make('gore_sev_a',7,bone_h=0.12,concave=True,tatters=3,rag=0.12),
make('gore_sev_b',8,bone_off=(0.1,0.05),bone_h=0.2,bone_r=0.2,concave=True,tatters=5,rag=0.2,split=True)]
for c in caps:
    me=c.data; me.calc_loop_triangles(); print('TRIS',c.name,len(me.loop_triangles))
    c['nominal_radius_m']=R0
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/gore_kit.blend')
for _n in mat.node_tree.nodes:
    if _n.type=='BSDF_PRINCIPLED': _n.inputs['Specular IOR Level'].default_value=0.5; _n.inputs['IOR'].default_value=1.5
bpy.ops.export_scene.gltf(filepath=OUT+'/gore_caps.glb',export_format='GLB',export_image_format='AUTO',export_extras=True)
print('DONE')
