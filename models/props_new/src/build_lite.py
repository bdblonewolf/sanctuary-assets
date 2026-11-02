# _lite decimations of existing GLBs -> props_new/lite/. Originals are read only (imported, never written).
import sys,os,math,json; sys.path.insert(0,os.path.dirname(__file__))
import bpy
from mathutils import Vector,Matrix
import lib
OUT=lib.ROOT+'/lite'
RA='/workspace/repos/sanctuary-assets/models'; PH='/workspace/sanctuary/assets3d/overworld/polyhaven'
JOBS={ # name: (src, target total tris, max tex px, variants)
 'iron_chest_lite':(f'{RA}/env_extra/interactables/chest.glb',3000,1024,['closed','opened']),
 'bookshelf_worn_lite':(f'{PH}/wooden_bookshelf_worn.glb',2600,512,[None]),
 'shrine_basic_lite':(f'{RA}/shrines/shrine_basic.glb',4800,1024,[None]),
 'shrine_weeping_angel_lite':(f'{RA}/shrines/shrine_weeping_angel.glb',4800,1024,[None]),
 'pier_lite':(f'{PH}/modular_wooden_pier.glb',9000,512,[None]),
}
def tri(o): return sum(len(p.vertices)-2 for p in o.data.polygons)
def run(name,src,target,px,var):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    ms=[o for o in bpy.context.scene.objects if o.type=='MESH' and not o.name.startswith('col_')]
    tot=sum(tri(o) for o in ms); keep_small=[o for o in ms if tri(o)<=200]
    big=[o for o in ms if tri(o)>200]; budget=target-sum(tri(o) for o in keep_small); bt=sum(tri(o) for o in big)
    for o in big:
        r=min(1.0,budget/bt)
        if r<0.999:
            md=o.modifiers.new('d','DECIMATE'); md.ratio=r; md.use_collapse_triangulate=True
            bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
            bpy.ops.object.modifier_apply(modifier='d')
    for im in bpy.data.images:
        if im.size[0]>px: im.scale(px,int(im.size[1]*px/im.size[0]))
    out=name if var is None else f'{name}_{var}'
    if var=='opened':
        lid=bpy.data.objects['lid']; lid.rotation_mode='XYZ'; lid.rotation_euler.x+=math.radians(-105)
        lid['anim']='hinge pivot = node origin; opened state rotated -105 deg about local X'
    elif name.startswith('iron_chest'):
        lid=bpy.data.objects['lid']; lid['anim']='hinge pivot = node origin (back edge); rotate about local X to open (opened file = -105 deg)'
    fn=f'{OUT}/{out}.glb'
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=fn,export_format='GLB',use_selection=True,export_image_format='JPEG',export_jpeg_quality=80,
        export_draco_mesh_compression_enable=False,export_cameras=False,export_lights=False,export_apply=True,export_yup=True,export_extras=True,export_tangents=True)
    J,b=lib.glb_json(fn)
    for m in J.get('materials',[]):
        m.pop('extensions',None)
        if 'emissiveFactor' in m: m['emissiveFactor']=[min(1,x) for x in m['emissiveFactor']]
    for k in ('extensionsUsed','extensionsRequired'): J.pop(k,None)
    lib.glb_write(fn,J,b)
    st=lib.stats(fn); bb=lib.bbox(list(bpy.context.scene.objects)); st.update(bb)
    st.update(path=os.path.relpath(fn,lib.ROOT),category='lite',source=src,source_tris=tot,notes=f'decimated (collapse) from {tot} tris; textures <= {px}px; nodes/extras kept')
    lib.record(out,st); print('EXPORTED',out,st['bytes'],st['tris'],st['size_m'])
sel=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(JOBS)
for n in sel:
    s,t,p,vs=JOBS[n]
    for v in vs: run(n,s,t,p,v)
