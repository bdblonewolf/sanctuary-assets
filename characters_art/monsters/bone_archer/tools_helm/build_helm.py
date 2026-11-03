import bpy,bmesh,sys,math,json,struct
import numpy as np
from mathutils import Vector,Matrix
SRC,OUT,OUT_SOLO=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene; sc.render.fps=30
bpy.ops.import_scene.gltf(filepath=SRC)
for o in list(bpy.data.objects):
    if o.name.startswith('Icosphere'): bpy.data.objects.remove(o,do_unlink=True)
arm=bpy.data.objects['Armature']
clips_before=sorted(t.name for t in arm.animation_data.nla_tracks)
for t in arm.animation_data.nla_tracks: t.mute=True
arm.animation_data.action=None
for pb in arm.pose.bones: pb.matrix_basis.identity()
bpy.context.view_layer.update()
for n in ('helmet','helmet_band','helmet_nasal'): bpy.data.objects.remove(bpy.data.objects[n],do_unlink=True)
CX,CY,Z0=0.0,0.02,1.70   # brim plane (old band level), centre of old helmet
SY=1.12                  # skull is deeper front-back
# lathe profile (r,z) from brim lip, over the brim, up the dome
prof=[(0.236,-0.062),(0.242,-0.050),(0.232,-0.030),(0.19,-0.010),(0.150,0.008),(0.132,0.012),
      (0.134,0.030),(0.134,0.046),(0.126,0.050),(0.124,0.090),(0.114,0.125),(0.096,0.152),(0.070,0.172),(0.040,0.183),(0.0,0.187)]
# underside of the brim (so it has thickness) back to the inner rim
under=[(0.118,0.004),(0.150,-0.016),(0.19,-0.026),(0.222,-0.056)]
SEG=28
bm=bmesh.new()
rings=[]
pts=prof[::-1][:-0]  # top -> lip
pts=list(reversed(prof))+list(reversed(under))
for (r,z) in pts:
    ring=[]
    for k in range(SEG):
        a=2*math.pi*k/SEG
        ring.append(bm.verts.new((CX+r*math.sin(a),CY+SY*r*-math.cos(a),Z0+z)) if r>0 else None)
    rings.append(ring)
top=bm.verts.new((CX,CY,Z0+0.187)); rings[0]=[top]*SEG
for i in range(len(rings)-1):
    A,Bv=rings[i],rings[i+1]
    for k in range(SEG):
        k2=(k+1)%SEG
        vs=[A[k],A[k2],Bv[k2],Bv[k]]
        vs2=[]
        for v in vs:
            if v not in vs2: vs2.append(v)
        bm.faces.new(vs2)
# spike (8-sided cone) + small collar
def cone(z0,h,r0,r1,seg=8):
    b=[bm.verts.new((CX+r0*math.cos(2*math.pi*k/seg),CY+r0*math.sin(2*math.pi*k/seg),z0)) for k in range(seg)]
    if r1>0:
        t=[bm.verts.new((CX+r1*math.cos(2*math.pi*k/seg),CY+r1*math.sin(2*math.pi*k/seg),z0+h)) for k in range(seg)]
        for k in range(seg): bm.faces.new([b[k],b[(k+1)%seg],t[(k+1)%seg],t[k]])
        return t
    tip=bm.verts.new((CX,CY,z0+h))
    for k in range(seg): bm.faces.new([b[k],b[(k+1)%seg],tip])
cone(Z0+0.175,0.03,0.034,0.026); t=cone(Z0+0.205,0.012,0.026,0.024); cone(Z0+0.217,0.115,0.024,0)
# raised crest/comb strip front-to-back over the dome (thin fin) for silhouette from the side/top
fin=[]
for i in range(9):
    a=math.radians(-62+124*i/8)
    r=0.128; y=CY-SY*r*math.sin(a)*0.98; z=Z0+0.05+0.135*math.cos(a)
    fin.append((y,z))
w=0.009
for (y0,z0),(y1,z1) in zip(fin,fin[1:]):
    for (yy0,zz0,yy1,zz1,h) in [(y0,z0,y1,z1,0.035)]:
        v=[bm.verts.new((CX+s*w,yy,zz+dh)) for s in (-1,1) for (yy,zz,dh) in ((yy0,zz0,0),(yy1,zz1,0),(yy1,zz1,h),(yy0,zz0,h))]
        L=v[:4];R=v[4:]
        bm.faces.new(L[::-1]); bm.faces.new(R); bm.faces.new([L[2],L[3],R[3],R[2]])
bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
me=bpy.data.meshes.new('skeleton_helm'); bm.to_mesh(me); bm.free()
helm=bpy.data.objects.new('skeleton_helm',me); sc.collection.objects.link(helm)
# material: lighter rusted iron
mat=bpy.data.materials.new('mon_rust_light'); mat.use_nodes=True; nt=mat.node_tree; bs=nt.nodes['Principled BSDF']
im=bpy.data.images.load('/workspace/hero_atk/helm/helm_rust_light_c.jpg'); tx=nt.nodes.new('ShaderNodeTexImage'); tx.image=im
nt.links.new(tx.outputs['Color'],bs.inputs['Base Color']); bs.inputs['Metallic'].default_value=0.5; bs.inputs['Roughness'].default_value=0.6
me.materials.append(mat)
bpy.ops.object.select_all(action='DESELECT'); bpy.context.view_layer.objects.active=helm; helm.select_set(True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=0.01); bpy.ops.object.mode_set(mode='OBJECT')
for p in me.polygons: p.use_smooth=True
me.shade_smooth() if hasattr(me,'shade_smooth') else None
try:
    helm.modifiers.new('ws','WEIGHTED_NORMAL'); bpy.ops.object.modifier_apply(modifier='ws')
except Exception as e: print('wn',e)
tris=sum(len(p.vertices)-2 for p in me.polygons); print('HELM tris',tris,'dims',tuple(round(x,3) for x in helm.dimensions))
# solo copy (made before skinning)
solo=helm.copy(); solo.data=me.copy(); solo.name='skeleton_helm_solo'; sc.collection.objects.link(solo)
# skin to Head
vg=helm.vertex_groups.new(name='mixamorig:Head'); vg.add(list(range(len(me.vertices))),1.0,'REPLACE')
helm.parent=arm; md=helm.modifiers.new('Armature','ARMATURE'); md.object=arm
for t in arm.animation_data.nla_tracks: t.mute=False
arm.animation_data.action=None
def export(path,objs,anim):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]
    kw=dict(filepath=path,export_format='GLB',use_selection=True,export_morph=False,export_image_format='AUTO')
    if anim: kw.update(export_animations=True,export_animation_mode='NLA_TRACKS',export_force_sampling=True,export_optimize_animation_size=False,export_frame_range=False,export_anim_slide_to_zero=True,export_skins=True)
    else: kw.update(export_animations=False,export_skins=False)
    bpy.ops.export_scene.gltf(**kw)
export(OUT,[arm]+[o for o in arm.children if o.type=='MESH'],True)
# Head joint inverse bind matrix from the exported file -> solo helm in Head-joint local space
d=open(OUT,'rb').read(); n=struct.unpack('<I',d[12:16])[0]; j=json.loads(d[20:20+n]); binoff=20+n+8
sk=j['skins'][0]; hi=[i for i in sk['joints'] if j['nodes'][i]['name']=='mixamorig:Head'][0]; ji=sk['joints'].index(hi)
acc=j['accessors'][sk['inverseBindMatrices']]; bv=j['bufferViews'][acc['bufferView']]
off=binoff+bv.get('byteOffset',0)+acc.get('byteOffset',0)+ji*64
IBM=np.array(struct.unpack('<16f',d[off:off+64])).reshape(4,4).T
C=Matrix(((1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)))  # blender -> gltf
M=C.inverted()@Matrix(IBM.tolist())@C
solo.parent=None; solo.matrix_world=Matrix.Identity(4); solo.data.transform(M); solo.data.update()
export(OUT_SOLO,[solo],False)
print('IBM_head',IBM.round(4).tolist())
print('CLIPS',clips_before)
json.dump({'tris':tris,'clips':clips_before},open(OUT[:-4]+'_info.json','w'))
