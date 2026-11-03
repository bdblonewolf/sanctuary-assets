# add two glowing eye spheres skinned to the head bone. cfg: eye_bone, eye_frac (along head from nose), eye_r (fraction of head length), eye_zf, eye_xf
import bpy,mathutils,bmesh
hb=cfg.get('eye_bone',cfg['head_bone'])
src=[o for o in meshes if o.type=='MESH'][0]
vg=src.vertex_groups.get(hb)
P=[]
for v in src.data.vertices:
    for g in v.groups:
        if g.group==vg.index and g.weight>0.5: P.append(src.matrix_world@v.co)
ymin=min(p.y for p in P); ymax=max(p.y for p in P); Lh=ymax-ymin
ye=ymin+cfg.get('eye_frac',0.35)*Lh
sl=[p for p in P if abs(p.y-ye)<0.06*Lh] or P
xm=max(abs(p.x) for p in sl); z0=min(p.z for p in sl); z1=max(p.z for p in sl)
ze=z0+cfg.get('eye_zf',0.68)*(z1-z0); r=cfg.get('eye_r',0.07)*Lh
print('EYES Lh',Lh,'y',ye,'x',xm,'z',ze,'r',r)
mat=bpy.data.materials.new('Eye')
for sx in (-1,1):
    me=bpy.data.meshes.new('eye'); bm=bmesh.new(); bmesh.ops.create_uvsphere(bm,u_segments=10,v_segments=6,radius=r); bm.to_mesh(me); bm.free()
    o=bpy.data.objects.new('eye',me); bpy.context.scene.collection.objects.link(o)
    o.location=(sx*xm*cfg.get('eye_xf',0.82),ye,ze)
    me.materials.append(mat)
    o.vertex_groups.new(name=hb).add(list(range(len(me.vertices))),1.0,'REPLACE')
    md=o.modifiers.new('Armature','ARMATURE'); md.object=arm; o.parent=arm
    bpy.context.view_layer.update()
    mw=o.matrix_world.copy(); me.transform(o.matrix_basis); o.matrix_basis.identity()
    meshes.append(o)
