# Blender-side helpers for props_gothic_v1. Model in Blender Z-up (exporter converts to glTF Y-up; Blender -Y => glTF +Z).
import bpy, bmesh, math, os, json, struct, random
import numpy as np
from mathutils import Vector, Matrix, noise
TEX='/workspace/gothwork/tex'
ROOT='/workspace/sanctuary_env/props_new'
RES='1k'   # '1k' or '512' (albedo); normals follow NRES
NRES='512'
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for c in (bpy.data.meshes,bpy.data.materials,bpy.data.images,bpy.data.objects): pass
# ---------------- materials
MATS={}
PROPS={ # rough, metal
 'wood_planks':(0.85,0),'wood_rough':(0.9,0),'wood_rot':(0.95,0),'wood_dark':(0.8,0),'wood_peel':(0.9,0),
 'stone_carved':(0.9,0),'stone_mossy':(0.92,0),'stone_block':(0.92,0),'rock':(0.93,0),'rock_dark':(0.9,0),'cliff':(0.93,0),'lichen':(0.93,0),
 'iron':(0.72,0.55),'iron_plate':(0.65,0.6),'cloth_hessian':(0.97,0),'cloth_linen':(0.95,0),'velvet':(0.9,0),'leather':(0.75,0),
 'bone':(0.8,0),'clay':(0.9,0),'sail_striped':(0.97,0),'tapestry_heraldic':(0.92,0),'book_pages':(0.9,0)}
def _img(path):
    for im in bpy.data.images:
        if im.filepath==path: return im
    im=bpy.data.images.load(path); return im
def mat(key,tint=(1,1,1),name=None,rough=None,metal=None,normal=True,res=None):
    """textured PBR material from prepped Poly Haven set; tint multiplies albedo (baseColorFactor)"""
    name=name or ('m_'+key if tint==(1,1,1) else f'm_{key}_{"%02x%02x%02x"%tuple(int(c*255) for c in tint)}')
    if name in MATS: return MATS[name]
    r,mt=PROPS.get(key,(0.9,0)); r=rough if rough is not None else r; mt=metal if metal is not None else mt
    res=res or RES
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    a=f'{TEX}/{key}_a.jpg' if res=='1k' else f'{TEX}/{key}_a_512.jpg'
    ti=nt.nodes.new('ShaderNodeTexImage'); ti.image=_img(a)
    if tint!=(1,1,1):
        mx=nt.nodes.new('ShaderNodeMix'); mx.data_type='RGBA'; mx.blend_type='MULTIPLY'; mx.inputs[0].default_value=1.0
        mx.inputs[7].default_value=(*tint,1); nt.links.new(ti.outputs[0],mx.inputs[6]); nt.links.new(mx.outputs[2],b.inputs['Base Color'])
    else: nt.links.new(ti.outputs[0],b.inputs['Base Color'])
    b.inputs['Roughness'].default_value=r; b.inputs['Metallic'].default_value=mt
    npath=f'{TEX}/{key}_n.jpg' if NRES=='1k' else f'{TEX}/{key}_n_512.jpg'
    if normal and os.path.exists(npath):
        tn=nt.nodes.new('ShaderNodeTexImage'); tn.image=_img(npath); tn.image.colorspace_settings.name='Non-Color'
        nm=nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(tn.outputs[0],nm.inputs['Color']); nt.links.new(nm.outputs[0],b.inputs['Normal'])
    m.use_backface_culling=True; MATS[name]=m; return m
def flat(name,color,rough=0.9,metal=0.0,emit=None):
    if name in MATS: return MATS[name]
    m=bpy.data.materials.new(name); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(*color,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal
    if emit: b.inputs['Emission Color'].default_value=(*emit,1); b.inputs['Emission Strength'].default_value=1.0
    m.use_backface_culling=True; MATS[name]=m; return m
def cutout(name,png,rough=0.95,emissive=False,tint=(1,1,1)):
    """alpha-MASK card material (post-export patch sets alphaMode MASK). name must start with cut_"""
    if name in MATS: return MATS[name]
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    ti=nt.nodes.new('ShaderNodeTexImage'); ti.image=_img(f'{TEX}/{png}')
    nt.links.new(ti.outputs[0],b.inputs['Base Color']); nt.links.new(ti.outputs[1],b.inputs['Alpha'])
    b.inputs['Roughness'].default_value=rough
    if tint!=(1,1,1): pass
    if emissive:
        nt.links.new(ti.outputs[0],b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=1.0
    try: m.blend_method='CLIP'; m.alpha_threshold=0.5
    except Exception: pass
    m.use_backface_culling=False
    MATS[name]=m; return m
# ---------------- mesh building
def obj_from(name,V,F,m=None,smooth_angle=None,mats=None,fmat=None,uv=None):
    me=bpy.data.meshes.new(name); me.from_pydata([tuple(map(float,v)) for v in V],[],[tuple(int(i) for i in f) for f in F]); me.validate(); me.update()
    o=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(o)
    if mats:
        for mm in mats: me.materials.append(mm)
        if fmat is not None:
            for p,k in zip(me.polygons,fmat): p.material_index=int(k)
    elif m is not None: me.materials.append(m)
    if uv is not None: set_uv(o,uv)
    if smooth_angle is not None: smooth(o,smooth_angle)
    return o
def obj_uvv(name,V,F,UV,m=None,angle=40,mats=None,fmat=None):
    """mesh with per-vertex UV list"""
    o=obj_from(name,V,F,m,mats=mats,fmat=fmat); me=o.data; me.uv_layers.new(name='UVMap'); uvl=me.uv_layers[0].data
    for li,l in enumerate(me.loops): uvl[li].uv=UV[l.vertex_index]
    weld(o); smooth(o,angle); return o
def weld(o,d=1e-4):
    bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=d); bm.to_mesh(o.data); bm.free(); o.data.update()
def smooth(o,angle=40):
    me=o.data
    for p in me.polygons: p.use_smooth=True
    if angle<180:
        bm=bmesh.new(); bm.from_mesh(me)
        for e in bm.edges:
            if len(e.link_faces)==2 and e.calc_face_angle(0)>math.radians(angle): e.smooth=False
        bm.to_mesh(me); bm.free()
    me.update()
def set_uv(o,fn):
    """fn(world_co, normal, poly_center) -> (u,v) per loop"""
    me=o.data
    if not me.uv_layers: me.uv_layers.new(name='UVMap')
    uvl=me.uv_layers[0].data; M=o.matrix_world
    for p in me.polygons:
        n=(M.to_3x3()@p.normal).normalized(); c=M@p.center
        for li in p.loop_indices:
            co=M@me.vertices[me.loops[li].vertex_index].co; uvl[li].uv=fn(co,n,c)
def box_uv(o,scale=1.0,grain='z',off=(0,0)):
    """triplanar-by-face box map in metres/scale. grain axis maps to V (texture planks/grain run along V)."""
    ax={'x':0,'y':1,'z':2}[grain]
    def fn(co,n,c):
        d=max(range(3),key=lambda i:abs(n[i])); o=[i for i in range(3) if i!=d]
        if ax in o: vv=ax; uu=[i for i in o if i!=ax][0]
        else: uu,vv=o
        return ((co[uu]/scale+off[0]),(co[vv]/scale+off[1]))
    set_uv(o,fn)
def cyl_uv(o,scale=1.0,axis='z',center=(0,0)):
    """cylindrical map around axis: U=angle*perimeter-ish, V=along axis (grain)"""
    ax={'x':0,'y':1,'z':2}[axis]; oth=[i for i in range(3) if i!=ax]
    me=o.data
    if not me.uv_layers: me.uv_layers.new(name='UVMap')
    uvl=me.uv_layers[0].data; M=o.matrix_world
    for p in me.polygons:
        cs=[M@me.vertices[me.loops[li].vertex_index].co for li in p.loop_indices]
        angs=[math.atan2(c[oth[1]]-center[1],c[oth[0]]-center[0]) for c in cs]
        a0=angs[0]; angs=[a if abs(a-a0)<math.pi else a-2*math.pi*math.copysign(1,a-a0) for a in angs]
        for li,c,a in zip(p.loop_indices,cs,angs): uvl[li].uv=(a*0.5/scale,c[ax]/scale)
def join(objs,name):
    objs=[o for o in objs if o is not None]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]
    if len(objs)>1: bpy.ops.object.join()
    o=bpy.context.view_layer.objects.active; o.name=name; o.data.name=name
    return o
def apply_tf(o):
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
def place(o,loc=(0,0,0),rot=(0,0,0),scale=None):
    o.location=loc; o.rotation_euler=rot
    if scale is not None: o.scale=scale if hasattr(scale,'__len__') else (scale,)*3
    bpy.context.view_layer.update(); return o
# primitives (return objects; geometry in local coords)
def box(name,size,loc=(0,0,0),m=None,rot=(0,0,0),bevel=0.0,seg=1,uvscale=1.0,grain='z'):
    sx,sy,sz=[s/2 for s in size]
    V=[(-sx,-sy,-sz),(sx,-sy,-sz),(sx,sy,-sz),(-sx,sy,-sz),(-sx,-sy,sz),(sx,-sy,sz),(sx,sy,sz),(-sx,sy,sz)]
    F=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    o=obj_from(name,V,F,m); place(o,loc,rot)
    if bevel>0:
        bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.bevel(bm,geom=bm.edges[:],offset=bevel,segments=seg,affect='EDGES',profile=0.5); bm.to_mesh(o.data); bm.free()
    if m is not None: box_uv(o,uvscale,grain)
    smooth(o,35)
    return o
def lathe(name,prof,seg=16,m=None,loc=(0,0,0),rot=(0,0,0),cap_top=True,cap_bot=True,uvscale=1.0,angle=40,phase=0.0,squash=(1,1)):
    """prof: list of (r,z) bottom->top"""
    V=[];F=[]; n=len(prof)
    for i,(r,z) in enumerate(prof):
        for k in range(seg):
            a=2*math.pi*k/seg+phase; V.append((r*math.cos(a)*squash[0],r*math.sin(a)*squash[1],z))
    for i in range(n-1):
        for k in range(seg):
            a=i*seg+k;b=i*seg+(k+1)%seg; F.append((a,b,b+seg,a+seg))
    if cap_bot and prof[0][0]>1e-4: F.append(tuple(reversed(range(seg))))
    if cap_top and prof[-1][0]>1e-4: F.append(tuple(range((n-1)*seg,n*seg)))
    o=obj_from(name,V,F,m); place(o,loc,rot)
    if m is not None: cyl_uv(o,uvscale,'z',(loc[0],loc[1])) if rot==(0,0,0) else box_uv(o,uvscale)
    smooth(o,angle); return o
def tube(name,path,radii,sides=6,m=None,cap=True,uvscale=1.0,angle=50,squash=None,twist=0.0):
    path=[Vector(p) for p in path]; n=len(path)
    radii=[float(r) for r in radii] if hasattr(radii,"__len__") else [float(radii)]*n
    T=[]
    for i in range(n):
        t=(path[min(i+1,n-1)]-path[max(i-1,0)]).normalized(); T.append(t)
    a=Vector((0,0,1)) if abs(T[0].z)<0.9 else Vector((1,0,0))
    N=[(a-T[0]*a.dot(T[0])).normalized()]
    for i in range(1,n): v=N[-1]-T[i]*N[-1].dot(T[i]); N.append(v.normalized())
    V=[];F=[]; L=0; Ls=[0]
    for i in range(1,n): L+=(path[i]-path[i-1]).length; Ls.append(L)
    for i in range(n):
        B=T[i].cross(N[i])
        for k in range(sides):
            ang=2*math.pi*k/sides+twist*i; sx,sy=(squash[i] if squash else (1,1))
            V.append(path[i]+radii[i]*(math.cos(ang)*sx*N[i]+math.sin(ang)*sy*B))
    for i in range(n-1):
        for k in range(sides): a=i*sides+k;b=i*sides+(k+1)%sides; F.append((a,b,b+sides,a+sides))
    if cap:
        if radii[0]>1e-4: F.append(tuple(reversed(range(sides))))
        if radii[-1]>1e-4: F.append(tuple(range((n-1)*sides,n*sides)))
    o=obj_from(name,V,F,m)
    if m is not None:
        # uv: u around, v along length
        me=o.data; me.uv_layers.new(name='UVMap'); uvl=me.uv_layers[0].data
        for p in me.polygons:
            for li in p.loop_indices:
                vi=me.loops[li].vertex_index; i,k=divmod(vi,sides)
                kk=k
                if p.loop_indices and k==0 and any((me.loops[l2].vertex_index%sides)==sides-1 for l2 in p.loop_indices): kk=sides
                uvl[li].uv=(kk/sides*2*math.pi*max(radii)/uvscale*1.0+0.0, Ls[i]/uvscale)
    smooth(o,angle); return o
def blob(name,r,loc=(0,0,0),m=None,sub=2,amp=0.25,freq=1.5,seed=0,scale=(1,1,1),flatten_bottom=None,uvscale=1.0,rot=(0,0,0)):
    """organic lump (no flat faces): icosphere + fractal noise along normal; optional soft sink below z=flatten_bottom (rounded, not cut)"""
    bm=bmesh.new(); bmesh.ops.create_icosphere(bm,subdivisions=sub,radius=1.0)
    off=Vector((seed*7.31,seed*3.17,seed*5.71))
    for v in bm.verts:
        p=v.co.copy(); d=noise.fractal(p*freq+off,0.6,2.0,4,noise_basis='PERLIN_ORIGINAL')
        v.co=p*(1+amp*d)
        v.co.x*=scale[0]*r; v.co.y*=scale[1]*r; v.co.z*=scale[2]*r
        if flatten_bottom is not None and v.co.z<flatten_bottom:  # squash (not planar) below threshold
            v.co.z=flatten_bottom+(v.co.z-flatten_bottom)*0.35
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(o)
    if m is not None: me.materials.append(m)
    place(o,loc,rot); 
    if m is not None: box_uv(o,uvscale)
    smooth(o,180); return o
def displace(o,amp,freq,seed=0,axis_mask=(1,1,1)):
    off=Vector((seed*1.7,seed*2.3,seed*0.9))
    for v in o.data.vertices:
        d=noise.noise_vector(v.co*freq+off); v.co+=Vector((d.x*axis_mask[0],d.y*axis_mask[1],d.z*axis_mask[2]))*amp
    o.data.update()
def decimate(o,ratio):
    md=o.modifiers.new('dec','DECIMATE'); md.ratio=ratio
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
    bpy.ops.object.modifier_apply(modifier=md.name)
def subsurf(o,lv=1):
    md=o.modifiers.new('ss','SUBSURF'); md.levels=lv; md.render_levels=lv
    bpy.context.view_layer.objects.active=o; bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.ops.object.modifier_apply(modifier=md.name)
def tris(o):
    return sum(len(p.vertices)-2 for p in o.data.polygons)
# ---------------- nodes
def collider(name,size,center,rot=(0,0,0),parent=None,extras=None):
    sx,sy,sz=[s/2 for s in size]
    V=[(-sx,-sy,-sz),(sx,-sy,-sz),(sx,sy,-sz),(-sx,sy,-sz),(-sx,-sy,sz),(sx,-sy,sz),(sx,sy,sz),(-sx,sy,sz)]
    F=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    o=obj_from(name,V,F,None); place(o,center,rot)
    o['collider']='box'; o['size_m']=[round(s,3) for s in size]
    if extras:
        for k,v in extras.items(): o[k]=v
    o.display_type='WIRE'; o.hide_render=True
    if parent: o.parent=parent
    return o
def empty(name,loc,rot=(0,0,0),parent=None,**props):
    o=bpy.data.objects.new(name,None); bpy.context.scene.collection.objects.link(o); o.location=loc; o.rotation_euler=rot; o.empty_display_size=0.3
    for k,v in props.items(): o[k]=v
    if parent: o.parent=parent
    return o
# ---------------- export + post
def glb_json(fn):
    b=open(fn,'rb').read(); n=struct.unpack('<I',b[12:16])[0]; return json.loads(b[20:20+n]),b
def glb_write(fn,J,b):
    n=struct.unpack('<I',b[12:16])[0]; rest=b[20+n:]
    js=json.dumps(J,separators=(',',':')).encode()
    while len(js)%4: js+=b' '
    out=struct.pack('<III',0x46546C67,2,12+8+len(js)+len(rest))+struct.pack('<II',len(js),0x4E4F534A)+js+rest
    open(fn,'wb').write(out)
def export(name,root,outdir,extras=None):
    os.makedirs(outdir,exist_ok=True)
    for o in bpy.context.scene.objects: o.hide_render=False
    bpy.ops.object.select_all(action='DESELECT')
    def sel(o):
        o.select_set(True)
        for c in o.children: sel(c)
    sel(root)
    if extras:
        for k,v in extras.items(): root[k]=v if not isinstance(v,(dict,list)) else json.dumps(v)
    fn=f'{outdir}/{name}.glb'
    kw=dict(filepath=fn,export_format='GLB',use_selection=True,export_image_format='AUTO',export_jpeg_quality=82,
        export_draco_mesh_compression_enable=False,export_cameras=False,export_lights=False,export_apply=True,export_yup=True,
        export_materials='EXPORT',export_extras=True,export_texcoords=True,export_normals=True,export_tangents=False,export_attributes=False)
    try: bpy.ops.export_scene.gltf(**kw,export_vertex_color='NONE')
    except TypeError: bpy.ops.export_scene.gltf(**kw)
    J,b=glb_json(fn); ch=False
    for m in J.get('materials',[]):
        if m.get('name','').startswith('ds_'): m['doubleSided']=True; ch=True
        elif not m.get('name','').startswith('cut_') and m.get('doubleSided'): m.pop('doubleSided'); ch=True
        if m.get('name','').startswith('cut_'):
            m['alphaMode']='MASK'; m['alphaCutoff']=0.5; m['doubleSided']=True; ch=True
        if 'emissiveFactor' in m: m['emissiveFactor']=[min(1.0,x) for x in m['emissiveFactor']]; ch=True
        if 'extensions' in m: m.pop('extensions'); ch=True
    for k in ('extensionsUsed','extensionsRequired'):
        if k in J: J.pop(k); ch=True
    for nd in J['nodes']:
        if 'extras' in nd:
            for k,v in list(nd['extras'].items()):
                if isinstance(v,str) and v[:1] in '[{':
                    try: nd['extras'][k]=json.loads(v); ch=True
                    except Exception: pass
    if ch: glb_write(fn,J,b)
    return fn
def stats(fn):
    J,b=glb_json(fn); acc=J['accessors']; tri=0; ctri=0
    for nd in J['nodes']:
        if 'mesh' not in nd: continue
        t=sum(acc[p['indices']]['count']//3 for p in J['meshes'][nd['mesh']]['primitives'])
        if nd.get('name','').startswith('col_'): ctri+=t
        else: tri+=t
    names=[nd.get('name') for nd in J['nodes']]
    return {'bytes':os.path.getsize(fn),'tris':tri,'collider_tris':ctri,'nodes':names,'materials':[m['name'] for m in J.get('materials',[])],
            'images':len(J.get('images',[]))}
def bbox(objs):
    pts=[]
    for o in objs:
        if o.type!='MESH' or o.name.startswith('col_'): continue
        for c in o.bound_box: pts.append(o.matrix_world@Vector(c))
    P=np.array(pts); mn=P.min(0); mx=P.max(0)
    # report in glTF axes: X, Y(up)=blender Z, Z=-blender Y
    return {'size_m':[round(float(mx[0]-mn[0]),2),round(float(mx[2]-mn[2]),2),round(float(mx[1]-mn[1]),2)],
            'min_y':round(float(mn[2]),2),'max_y':round(float(mx[2]),2)}
REPORT_FN=ROOT+'/src/_report.json'
def record(key,info):
    R=json.load(open(REPORT_FN)) if os.path.exists(REPORT_FN) else {}
    R[key]=info; json.dump(R,open(REPORT_FN,'w'),indent=1)
def finish(name,root,outdir,extras=None,notes='',category='',interactable=None,envs=None):
    objs=[root]+list(root.children_recursive)
    bb=bbox(objs)
    fn=export(name,root,outdir,extras)
    st=stats(fn); st.update(bb); st['path']=os.path.relpath(fn,ROOT); st['notes']=notes; st['category']=category
    if interactable: st['interactable']=interactable
    if envs: st['environments']=envs
    record(name,st); print('EXPORTED',name,st['bytes'],st['tris'],st['size_m'])
    return st
def root_empty(name):
    return empty(name,(0,0,0))
def parent_all(root,objs):
    for o in objs:
        if o.parent is None and o is not root: o.parent=root
