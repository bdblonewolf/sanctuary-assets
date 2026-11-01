# Finishing: hide/decimate body, weights, join, UV atlas, bake, final materials, export (raw, no animation).
def hide_inner(inner,outers,maxd=0.03,zmin=-9.0):
    tr=tree_of(outers); me=inner.data; cov=[]
    for v in me.vertices:
        n=v.normal; h=tr.ray_cast(v.co+n*0.001,n,maxd); cov.append(h[0] is not None and v.co.z>zmin)
    bm=bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    dl=[f for f in bm.faces if all(cov[v.index] for v in f.verts)]
    bmesh.ops.delete(bm,geom=dl,context='FACES'); bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(me); bm.free(); print('HIDE_INNER',inner.name,len(dl))
def sel_only(objs,active=None):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=active or objs[0]
HEAD_BOOST=float(os.environ.get('HEAD_BOOST','2.6'))
TEXRES=int(os.environ.get('TEXRES','2048'))
def bake_img(name,cs='Non-Color',res=None):
    res=res or TEXRES
    im=bpy.data.images.new(name,res,res,alpha=True,float_buffer=False); im.colorspace_settings.name=cs; return im
def smooth_sharp(o,ang):
    me=o.data; bm=bmesh.new(); bm.from_mesh(me)
    sh=[ (len(e.link_faces)==2 and e.calc_face_angle(0.0)>math.radians(ang)) for e in bm.edges]; bm.free()
    for p in me.polygons: p.use_smooth=True
    a=me.attributes.get('sharp_edge') or me.attributes.new('sharp_edge','BOOLEAN','EDGE')
    a.data.foreach_set('value',np.array(sh,bool))
def seam_attr(o,ang=72.0,step=0.003):
    """per-vertex distance (m) to the nearest garment edge: open boundary or sharp crease (solidify rims, panel borders)"""
    from mathutils import kdtree
    me=o.data; bm=bmesh.new(); bm.from_mesh(me); pts=[]
    for e in bm.edges:
        sharp=len(e.link_faces)!=2 or (e.calc_face_angle(0.0)>math.radians(ang))
        if not sharp: continue
        a,b=e.verts[0].co,e.verts[1].co; n=max(1,int((b-a).length/step))
        pts+= [a.lerp(b,t/n) for t in range(n+1)]
    bm.free()
    if not pts: set_attr(o,'seam',lambda c:np.ones(len(c))); return
    kd=kdtree.KDTree(len(pts))
    for i,p_ in enumerate(pts): kd.insert(p_,i)
    kd.balance(); d=np.array([kd.find(v.co)[2] for v in me.vertices])
    set_attr(o,'seam',lambda c:d)
REGIONS=['head','torso','arms','hands','legs','feet']
SLOTS=['head','torso','legs','feet','hands','back']
def region_of(gn):
    if 'Hand' in gn: return 'hands'
    if 'Foot' in gn or 'Toe' in gn: return 'feet'
    if 'Leg' in gn: return 'legs'
    if 'Arm' in gn: return 'arms'
    if 'Head' in gn or 'Neck' in gn: return 'head'
    return 'torso'
def set_part(o,code):
    a=o.data.attributes.get('part') or o.data.attributes.new('part','INT','FACE')
    a.data.foreach_set('value',np.full(len(o.data.polygons),code,np.int32))
META={}
def finalize(NAME,body_budget,inner_hide=(),body_keep=None,body_cut=None,body_attrs={},strip=False,out=None,shell_names=('hair','beard'),bake_samples=64,region_budget=None,slot_fn=lambda o,m:'torso',fallback={'arms':'hands','torso':'head'}):
    sc=bpy.context.scene
    garments=[o for o,m,w,k in PIECES if k=='opaque']
    # 1) the bare body stays WHOLE (no face deletion); covered skin is split into region submeshes later.
    #    The approved body's linen undergarment is kept as part of the body (torso/legs regions), baked with the linen recipe.
    for ih in inner_hide: hide_inner(*ih)
    li=MATN.index('linen_undergarment')
    BM.materials[li]=bpy.data.materials.get('linen_shirt') or BM.materials[li]
    # per-region decimation (edit-mode decimate on each region's faces; region borders stay locked -> clean seams)
    RB=dict(head=3000,hands=1400,torso=1600,arms=700,legs=900,feet=400); RB.update(region_budget or {})
    vr=[]
    for v in BM.vertices:
        g=max(v.groups,key=lambda g:g.weight,default=None); vr.append(region_of(body.vertex_groups[g.group].name if g else ''))
    from collections import Counter as _C
    import bmesh as _bm
    m=body.modifiers.new('t','TRIANGULATE'); apply_mod(body,m)
    rl=body.data.attributes.new('rg','INT','POINT')
    for i,r in enumerate(vr): rl.data[i].value=REGIONS.index(r)
    print('DEC0',flush=True); sel_only([body]); bpy.ops.object.mode_set(mode='EDIT'); print('DEC1',flush=True); bpy.ops.mesh.select_mode(type='FACE')
    for r in REGIONS:
        bm=_bm.from_edit_mesh(body.data); lay=bm.verts.layers.int['rg']; ri=REGIONS.index(r)
        for f in bm.faces: f.select_set(False)
        n=0
        for f in bm.faces:
            if _C(v[lay] for v in f.verts).most_common(1)[0][0]==ri: f.select_set(True); n+=1
        bm.select_flush_mode(); _bm.update_edit_mesh(body.data); print('DECsel',r,n,flush=True)
        if n>RB[r]: bpy.ops.mesh.decimate(ratio=RB[r]/n,use_symmetry=True,symmetry_axis='X')
        bpy.ops.object.mode_set(mode='OBJECT'); bpy.ops.object.mode_set(mode='EDIT')
        bm=_bm.from_edit_mesh(body.data); print('DECIMATE',r,n,'->',sum(1 for f in bm.faces if f.select)); del bm
    bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT'); body.data.attributes.remove(body.data.attributes['rg'])
    # pull skin back behind decimated garments (no poke-through at necklines / armholes)
    gtr=tree_of(garments); nmov=0
    for v in BM.vertices:
        g=max(v.groups,key=lambda g:g.weight,default=None); gn=body.vertex_groups[g.group].name if g else ''
        if 'Head' in gn or 'Hand' in gn: continue
        h=gtr.find_nearest(v.co,0.025)
        if h[0] is None: continue
        n=h[1].normalized(); d=(v.co-h[0]).dot(n)
        if d>-0.004: v.co=v.co-n*(d+0.004); nmov+=1
    BM.update(); print('SKIN_PULLBACK',nmov)
    # 1b) body regions (dominant bone, face majority) and default-outfit coverage per slot
    gslot={o.name:slot_fn(o,m) for o,m,w,k in PIECES if k=='opaque'}
    trees={sl:tree_of([o for o,m,w,k in PIECES if k=='opaque' and gslot[o.name]==sl]) for sl in sorted(set(gslot.values()))}
    vreg=[];vcov=[]
    for v in BM.vertices:
        g=max(v.groups,key=lambda g:g.weight,default=None); vreg.append(region_of(body.vertex_groups[g.group].name if g else ''))
        n=v.normal; best=None
        for j,d in enumerate((n,(n+Vector((0,0,0.35))).normalized(),(n-Vector((0,0,0.35))).normalized())):
            hits=[(tr.ray_cast(v.co+n*0.0015,d,0.08),sl) for sl,tr in trees.items()]
            hits=[(h[3],sl) for h,sl in hits if h[0] is not None]
            if not hits: best=None; break
            if j==0: best=min(hits)[1]
        vcov.append(best)
    from collections import Counter
    freg=[];fcov=[]
    for f in BM.polygons:
        freg.append(Counter(vreg[i] for i in f.vertices).most_common(1)[0][0])
        cs=[vcov[i] for i in f.vertices]; fcov.append(Counter(cs).most_common(1)[0][0] if all(cs) else None)
    hides={sl:[] for sl in trees}; moved=Counter()
    for r in REGIONS:
        fi=[k for k,x in enumerate(freg) if x==r]
        if not fi: continue
        c=Counter(fcov[k] for k in fi if fcov[k]); sl,nc=(c.most_common(1)[0] if c else (None,0))
        print('REGION',r,len(fi),'covered',dict(c))
        if sl and nc/len(fi)>0.5: hides[sl].append(r)
    hidden={r for l in hides.values() for r in l}
    for k in range(len(freg)):   # skin of a hidden region left uncovered by its slot -> neighbouring visible region
        r=freg[k]
        if r in hidden and fcov[k] is None and fallback.get(r) and fallback[r] not in hidden: freg[k]=fallback[r]; moved[r+'->'+fallback[r]]+=1
    print('HIDES',hides,'MOVED',dict(moved))
    a=BM.attributes.get('part') or BM.attributes.new('part','INT','FACE'); a.data.foreach_set('value',np.array([REGIONS.index(r) for r in freg],np.int32))
    for o,m,w,k in PIECES:
        if k=='opaque': set_part(o,10+SLOTS.index(gslot[o.name]))
    META.update(hides=hides,slots=sorted(set(gslot.values()),key=SLOTS.index))
    print('PIECE body',tris(body)); [print('PIECE',o.name,tris(o)) for o,*_ in PIECES]
    if os.environ.get('TRIONLY'): raise SystemExit
    for k,fn in body_attrs.items(): set_attr(body,k,fn)
    # body materials -> recipes
    BM.materials[MATN.index('skin')]=bpy.data.materials['skin_'+NAME]; BM.materials[MATN.index('eye')]=bpy.data.materials['eye_'+NAME]
    # 2) weights, materials, parenting
    for o,mat,wfn,kind in PIECES:
        if isinstance(kind,tuple): pass
        else:
            assign(o,wfn); md=o.modifiers.new('arm','ARMATURE'); md.object=arm; o.parent=arm
        o.data.materials.clear(); o.data.materials.append(bpy.data.materials[mat])
        for p in o.data.polygons: p.use_smooth=True
        for k_ in [a.name for a in o.data.attributes if a.name not in ('position','.edge_verts','.corner_vert','.corner_edge','sharp_face','material_index','hedge','soot','ink','stubble') and not a.name.startswith('.') and a.domain=='POINT' and a.data_type=='FLOAT']: pass
    groups={'main':[body],'keepsake':[],'cards':[]}; props={}
    for o,mat,wfn,kind in PIECES:
        if kind=='opaque': groups['main'].append(o)
        elif kind=='cards': groups['cards'].append(o)
        elif kind=='keepsake': groups['keepsake'].append(o)
        else: props.setdefault(kind[2],(kind[1],[]))[1].append(o)
    # every mesh carries the attributes used by shaders (missing ones -> 0)
    allo=[o for g in groups.values() for o in g]+[o for b,l in props.values() for o in l]
    for o,m,w,k in PIECES:
        if k=='opaque' and 'seam' not in o.data.attributes: seam_attr(o)
    # smooth shading with real creases kept sharp (solidify rims, soles, buckles): grid/hull meshes are flat by default
    for o in allo:
        if o.name.startswith('body'): continue
        smooth_sharp(o,float(os.environ.get('SHARP_ANG','62')))
    for o in allo:
        if 'seam' not in o.data.attributes: set_attr(o,'seam',lambda c:np.ones(len(c)))
        if 'card' not in o.data.attributes: set_attr(o,'card',lambda c:np.zeros(len(c)))
        for k in ('hedge','soot','ink','stubble'):
            if k not in o.data.attributes: set_attr(o,k,lambda c:np.zeros(len(c)))
        if 'UVMap' not in o.data.uv_layers:
            if len(o.data.uv_layers): o.data.uv_layers[0].name='UVMap'
            else: o.data.uv_layers.new(name='UVMap')
    main=join(groups['main'],'npc_'+NAME)
    cards=join(groups['cards'],'cards_'+NAME) if groups['cards'] else None
    kp=join(groups['keepsake'],'keepsake_'+NAME) if groups['keepsake'] else None
    sel_only([main]); bpy.ops.object.material_slot_remove_unused()
    pro=[]
    for pn,(bone,l) in props.items():
        po=join(l,pn); pro.append((po,bone))
    shells=[o for o in ([cards] if cards else [])]
    # 3) atlas UVs
    uvobjs=[main]+([kp] if kp else [])+[p for p,b in pro]+([cards] if cards else [])
    for o in uvobjs:
        if 'atlas' not in o.data.uv_layers: o.data.uv_layers.new(name='atlas')
        o.data.uv_layers.active=o.data.uv_layers['atlas']
    strand_faces={}
    if cards is not None:   # strand cards (marked with attribute 'card'>0.5) go to the strip; shells get unique islands
        cm=cards.data; ca=cm.attributes.get('card')
        strand_faces={p.index for p in cm.polygons if ca and all(ca.data[v].value>0.5 for v in p.vertices)}
    sel_only(uvobjs); bpy.ops.object.mode_set(mode='EDIT')
    bodymat={i for i,m in enumerate(main.data.materials) if m and (m.name.startswith('skin_') or m.name.startswith('eye_'))}
    for o in uvobjs:
        bmx=bmesh.from_edit_mesh(o.data); al=bmx.loops.layers.uv['atlas']; sl=bmx.loops.layers.uv.get('UVMap')
        for f in bmx.faces:
            isbody=(o==main and f.material_index in bodymat)
            if isbody and sl is not None:
                for l in f.loops: l[al].uv=l[sl].uv
            f.select=not (o==cards and f.index in strand_faces) and not isbody
        bmesh.update_edit_mesh(o.data)
    bpy.ops.uv.smart_project(angle_limit=D(66),island_margin=0.002,area_weight=0.0,scale_to_bounds=False)
    for o in uvobjs:
        bmx=bmesh.from_edit_mesh(o.data)
        for f in bmx.faces: f.select=not (o==cards and f.index in strand_faces)
        bmesh.update_edit_mesh(o.data)
    bpy.ops.uv.select_all(action='SELECT'); bpy.ops.uv.average_islands_scale()
    # texel boost: head/face x2.2, hands x1.4
    for o in uvobjs:
        bmx=bmesh.from_edit_mesh(o.data); uvl=bmx.loops.layers.uv['atlas']
        vgi={g.name:g.index for g in o.vertex_groups}; dl_=bmx.verts.layers.deform.verify()
        def boost(f):
            if o.name.startswith('keepsake') or o in [p for p,b in pro]: return 1.0
            w=f.verts[0][dl_]
            hd=w.get(vgi.get(S+'Head',-1),0)+w.get(vgi.get(S+'Neck',-1),0)*0.5
            hn=sum(w.get(vgi.get(k,-1),0) for k in vgi if 'Hand' in k)
            if o==cards: return 2.0
            return HEAD_BOOST if hd>0.5 else (1.4 if hn>0.5 else 1.0)
        # islands: scale each face's uv around its own island centre ~ approximate by scaling about face-set centroid of connected uv islands
        isl=uv_islands(bmx,uvl)
        for faces in isl:
            if o==cards and faces[0].index in strand_faces: continue
            b=boost(faces[0])
            if b==1.0: continue
            c=sum((l[uvl].uv for f in faces for l in f.loops),Vector((0,0)))/sum(len(f.loops) for f in faces)
            for f in faces:
                for l in f.loops: l[uvl].uv=c+(l[uvl].uv-c)*b
        bmesh.update_edit_mesh(o.data)
    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(rotate=True,scale=True,margin=0.004,shape_method='CONCAVE')
    umax=0.8 if (strip or strand_faces) else 1.0; print('STRAND_FACES',len(strand_faces))
    for o in uvobjs:
        bmx=bmesh.from_edit_mesh(o.data); uvl=bmx.loops.layers.uv['atlas']; src=bmx.loops.layers.uv.get('UVMap')
        for f in bmx.faces:
            for l in f.loops:
                if o==cards and f.index in strand_faces:
                    u,v=l[src].uv; l[uvl].uv=(0.8+0.2*min(max(u,0.002),0.998),min(max(v,0.002),0.998))
                else: l[uvl].uv=(l[uvl].uv.x*umax,l[uvl].uv.y)
        bmesh.update_edit_mesh(o.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    # 4) bake
    sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=4
    sc.render.bake.margin=16; sc.render.bake.use_clear=True
    imgs={k:bake_img(NAME+'_'+k,'sRGB' if k=='base' else 'Non-Color') for k in ('base','alpha','rough','metal','ao','normal')}
    mats={m for o in uvobjs for m in o.data.materials if m and m.name in MATS}
    def set_target(k):
        for m in mats:
            nt=m.node_tree; n=nt.nodes.get('BAKE') or nt.nodes.new('ShaderNodeTexImage'); n.name='BAKE'; n.image=imgs[k]
            nt.nodes.active=n
    def emit_wire(key):
        for m in mats:
            info=MATS[m.name]; nt=m.node_tree; e=nt.nodes.get('EMIT') or nt.nodes.new('ShaderNodeEmission'); e.name='EMIT'
            s_=info[key]
            nt.links.new(s_,e.inputs[0]); nt.links.new(e.outputs[0],info['out'].inputs[0])
    def bsdf_wire():
        for m in mats: info=MATS[m.name]; m.node_tree.links.new(info['bsdf'].outputs[0],info['out'].inputs[0])
    sel_only(uvobjs,main)
    for k in ('base','alpha','rough','metal'):
        set_target(k); emit_wire(k); bpy.ops.object.bake(type='EMIT'); print('BAKED',k)
    set_target('normal'); bsdf_wire(); bpy.ops.object.bake(type='NORMAL',normal_space='TANGENT',uv_layer='atlas'); print('BAKED normal')
    # AO: props and shells baked in isolation (moved away) so they don't shadow the body
    away=[p for p,b in pro]+([cards] if cards else [])
    for i,o in enumerate(away): o.location.x+=3.0*(i+1)
    sc.cycles.samples=bake_samples; set_target('ao'); bpy.ops.object.bake(type='AO'); print('BAKED ao')
    for i,o in enumerate(away): o.location.x-=3.0*(i+1)
    tex=out+'/tex'; os.makedirs(tex,exist_ok=True)
    for k,im in imgs.items(): im.filepath_raw=f'{tex}/{NAME}_{k}.png'; im.file_format='PNG'; im.save()
    return main,cards,kp,pro,imgs,mats
def uv_islands(bmx,uvl):
    # connected faces sharing UV-coincident edges
    seen=set(); out=[]
    fl=[f for f in bmx.faces if f.select]
    key=lambda l:(round(l[uvl].uv.x,5),round(l[uvl].uv.y,5))
    for f0 in fl:
        if f0.index in seen: continue
        st=[f0]; seen.add(f0.index); isl=[]
        while st:
            f=st.pop(); isl.append(f)
            for l in f.loops:
                e=l.edge
                for lf in e.link_loops:
                    g=lf.face
                    if g.index in seen or not g.select: continue
                    # uv-connected if the shared edge has the same uv coords on both sides
                    a={key(l),key(l.link_loop_next)}; b={key(lf),key(lf.link_loop_next)}
                    if a==b: seen.add(g.index); st.append(g)
        out.append(isl)
    return out
def composite(NAME,out,ao_mix=0.35):
    t=out+'/tex'
    def ld(k):
        im=bpy.data.images.load(f'{t}/{NAME}_{k}.png',check_existing=False); im.colorspace_settings.name='Non-Color'
        a=np.empty(im.size[0]*im.size[1]*4,np.float32); im.pixels.foreach_get(a); w,h=im.size; bpy.data.images.remove(im); return a.reshape(h,w,4)
    base=ld('base'); ao=ld('ao')[...,0]; al=ld('alpha')[...,0]; ro=ld('rough')[...,0]; me=ld('metal')[...,0]
    lin=base[...,:3]**2.2*(1-ao_mix+ao_mix*ao)[...,None]; rgb=lin**(1/2.2)
    def sv(arr,nm):
        h,w,_=arr.shape; im=bpy.data.images.new(nm,w,h,alpha=True); im.colorspace_settings.name='Non-Color'
        im.pixels.foreach_set(arr.astype(np.float32).ravel()); im.filepath_raw=f'{t}/{nm}.png'; im.file_format='PNG'; im.save(); bpy.data.images.remove(im)
        return f'{t}/{nm}.png'
    one=np.ones_like(ao)
    pb=sv(np.dstack([rgb,al]),NAME+'_basecolor_final'); po=sv(np.dstack([ao,ro,me,one]),NAME+'_orm_final')
    return pb,po,f'{t}/{NAME}_normal.png'
def final_material(name,bc,orm,nrm,cards):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    o=nt.nodes.new('ShaderNodeOutputMaterial'); b=nt.nodes.new('ShaderNodeBsdfPrincipled'); nt.links.new(b.outputs[0],o.inputs[0])
    uv=nt.nodes.new('ShaderNodeUVMap'); uv.uv_map='UVMap'
    def img(path,cs):
        n=nt.nodes.new('ShaderNodeTexImage'); n.image=bpy.data.images.load(path,check_existing=True); n.image.colorspace_settings.name=cs; nt.links.new(uv.outputs[0],n.inputs[0]); return n
    ib=img(bc,'sRGB'); io=img(orm,'Non-Color'); inn=img(nrm,'Non-Color')
    nt.links.new(ib.outputs['Color'],b.inputs['Base Color'])
    sp=nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(io.outputs['Color'],sp.inputs[0])
    nt.links.new(sp.outputs['Green'],b.inputs['Roughness']); nt.links.new(sp.outputs['Blue'],b.inputs['Metallic'])
    nm=nt.nodes.new('ShaderNodeNormalMap'); nm.uv_map='UVMap'; nt.links.new(inn.outputs['Color'],nm.inputs['Color']); nt.links.new(nm.outputs[0],b.inputs['Normal'])
    # glTF occlusion via the exporter's custom group
    g=bpy.data.node_groups.get('glTF Material Output')
    if g is None:
        g=bpy.data.node_groups.new('glTF Material Output','ShaderNodeTree'); g.interface.new_socket('Occlusion',in_out='INPUT',socket_type='NodeSocketFloat')
    gn=nt.nodes.new('ShaderNodeGroup'); gn.node_tree=g; nt.links.new(sp.outputs['Red'],gn.inputs['Occlusion'])
    if cards:
        nt.links.new(ib.outputs['Alpha'],b.inputs['Alpha']); m.blend_method='CLIP'; m.alpha_threshold=0.5; m.use_backface_culling=False
    else:
        m.use_backface_culling=True
    return m
def split_by_part(o,names):
    pa=np.zeros(len(o.data.polygons),np.int32); o.data.attributes['part'].data.foreach_get('value',pa)
    vn={tuple(round(c,6) for c in v.co):v.normal.copy() for v in o.data.vertices}
    outs=[]
    for code,nm in names.items():
        if not (pa==code).any(): continue
        c=o.copy(); c.data=o.data.copy(); bpy.context.collection.objects.link(c); c.name=nm; c.data.name=nm
        bm=bmesh.new(); bm.from_mesh(c.data); lay=bm.faces.layers.int.get('part')
        bmesh.ops.delete(bm,geom=[f for f in bm.faces if f[lay]!=code],context='FACES')
        bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS'); bm.to_mesh(c.data); bm.free()
        c.data.attributes.remove(c.data.attributes['part'])
        sel_only([c]); bpy.ops.object.material_slot_remove_unused()
        if code<10:   # body regions: keep the whole-body vertex normals so the seams read as one skin
            c.data.normals_split_custom_set_from_vertices([vn.get(tuple(round(x,6) for x in v.co),v.normal) for v in c.data.vertices])
        outs.append(c)
    bpy.data.objects.remove(o); return outs
def finish_export(NAME,main,cards,kp,pro,out_glb,tex_out,cards_mats):
    bc,orm,nrm=composite(NAME,tex_out)
    mo=final_material(NAME+'_mat',bc,orm,nrm,False); mc=final_material(NAME+'_mat_cards',bc,orm,nrm,True)
    for o in [main]+([kp] if kp else [])+[p for p,b in pro]+([cards] if cards else []):
        me=o.data
        for i,m in enumerate(me.materials): me.materials[i]=mc if (m.name in cards_mats or (cards is not None and o==cards)) else mo
        for uvn in [u.name for u in me.uv_layers if u.name!='atlas']: me.uv_layers.remove(me.uv_layers[uvn])
        me.uv_layers['atlas'].name='UVMap'
        for an in [a.name for a in me.attributes if a.name in ('hedge','soot','ink','stubble','card','seam')]: me.attributes.remove(me.attributes[an])
        first={}; remap=[first.setdefault(m.name,i) for i,m in enumerate(me.materials)]
        if len(first)<len(me.materials):
            mi=[0]*len(me.polygons); me.polygons.foreach_get('material_index',mi); me.polygons.foreach_set('material_index',[remap[i] for i in mi])
            sel_only([o]); bpy.ops.object.material_slot_remove_unused()
    names={i:f'{NAME}_body_{r}' for i,r in enumerate(REGIONS)}; names.update({10+i:f'{NAME}_outfit_{s_}' for i,s_ in enumerate(SLOTS)})
    parts=split_by_part(main,names)
    if cards is not None:
        cards.name=cards.data.name=NAME+'_hair'
        if 'part' in cards.data.attributes: cards.data.attributes.remove(cards.data.attributes['part'])
        sel_only([cards]); bpy.ops.object.material_slot_remove_unused(); parts.append(cards)
    main=parts
    # props: rigid children of hand joints
    for p,bone in pro:
        p.parent=arm; p.parent_type='BONE'; p.parent_bone=S+bone
        mw=p.matrix_world.copy()
        bpy.context.view_layer.update()
        # keep rest-pose world placement: geometry is already in world coords, so set parent inverse
        pb=arm.pose.bones[S+bone]
        p.matrix_parent_inverse=(arm.matrix_world@Matrix.Translation(pb.tail-pb.head)@pb.matrix).inverted() if False else (arm.matrix_world@arm.data.bones[S+bone].matrix_local@Matrix.Translation((0,arm.data.bones[S+bone].length,0))).inverted()
        p.matrix_world=Matrix.Identity(4)@mw if False else p.matrix_world
    bpy.context.view_layer.update()
    sel_only([arm]+main+[p for p,b in pro],arm)
    bpy.ops.export_scene.gltf(filepath=out_glb,export_format='GLB',use_selection=True,export_image_format='WEBP',export_image_quality=int(os.environ.get('WEBPQ','80')),
        export_skins=True,export_influence_nb=4,export_yup=True,export_animations=False,export_tangents=False,export_apply=False,export_def_bones=False)
    return main
def write_meta(NAME,parts,pro,out):
    import json
    nodes={o.name:tris(o) for o in parts}
    props={p.name:{'bone':S+b,'tris':tris(p)} for p,b in pro}
    M=dict(name=NAME,nodes=nodes,props=props,hides=META.get('hides',{}),
           slots={s_:f'{NAME}_outfit_{s_}' for s_ in META.get('slots',[]) if f'{NAME}_outfit_{s_}' in nodes},
           body_regions=[n for n in nodes if n.startswith(NAME+'_body_')])
    hid={r for l in M['hides'].values() for r in l}
    M['visible_tris_default']=sum(t for n,t in nodes.items() if not (n.startswith(NAME+'_body_') and n[len(NAME)+6:] in hid))+sum(v['tris'] for k,v in props.items() if k.endswith('_keepsake'))
    json.dump(M,open(out+'/meta.json','w'),indent=1); print('META',json.dumps(M))
