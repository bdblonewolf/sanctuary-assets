"""Write ../MANIFEST.json from work/<n>/meta.json + the final GLBs. usage: python3 manifest.py wolcen quill"""
import json,struct,sys,os
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(D)
HEIGHT={'wolcen':1.98,'quill':1.76}
PROF={'wolcen':'work_hammer','quill':'work_write'}
out={'format':'glTF 2.0 binary, KHR_mesh_quantization + EXT_texture_webp, Y-up, feet at y=0, facing +Z, metres',
     'skeleton':'mixamorig (single armature / single skin per GLB)','npcs':{}}
for n in sys.argv[1:]:
    M=json.load(open(f'{D}/work/{n}/meta.json'))
    b=open(f'{R}/glb/{n}.glb','rb').read(); L=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+L])
    clips=[a['name'] for a in j['animations']]
    hides={f'{n}_outfit_{s}':[f'{n}_body_{r}' for r in rs] for s,rs in M['hides'].items() if f'{n}_outfit_{s}' in M['nodes']}
    hidden={r for rs in hides.values() for r in rs}
    vis=sum(t for k,t in M['nodes'].items() if k not in hidden)+M['props'][f'{n}_keepsake']['tris']
    meshes=[{'node':k,'type':('body_region' if '_body_' in k else 'outfit' if '_outfit_' in k else 'hair'),'skinned':True,'tris':t} for k,t in M['nodes'].items()]
    meshes+=[{'node':k,'type':('keepsake' if k.endswith('_keepsake') else 'prop'),'skinned':False,'parent_bone':v['bone'],'tris':v['tris'],
              **({'mesh_child':k+'_mesh'} if '_prop_' in k else {})} for k,v in M['props'].items()]
    out['npcs'][n]={
     'glb':f'glb/{n}.glb','bytes':len(b),'MB':round(len(b)/1e6,3),'height_m':HEIGHT[n],
     'tris_total':sum(m['tris'] for m in meshes),'tris_visible_default':vis,
     'textures':{'basecolor':'1024 webp','normal':'1024 webp','orm':'1024 webp'},
     'materials':[f'{n}_mat',f'{n}_mat_cards'],
     'body_regions':[f'{n}_body_{r}' for r in ['head','torso','arms','hands','legs','feet']],
     'slots':{s:f'{n}_outfit_{s}' for s in M['slots']},
     'slot_hides':hides,
     'default_hidden_regions':sorted(hidden),
     'hair':f'{n}_hair',
     'props':{k:{'bone':v['bone'],'mesh_child':k+'_mesh','visible_in':[PROF[n]]} for k,v in M['props'].items() if '_prop_' in k},
     'keepsake':{'node':f'{n}_keepsake','bone':M['props'][f'{n}_keepsake']['bone'],'always_visible':True},
     'clips':clips,'profession_clip':PROF[n],
     'meshes':meshes,
     'previews':{v:f'previews/{n}_{v}.png' for v in ['front','q','side','back','face','bare_front']}|{'clips':f'previews/{n}_clips.jpg'}}
json.dump(out,open(f'{R}/MANIFEST.json','w'),indent=1)
for n,v in out['npcs'].items(): print(n,v['MB'],v['tris_total'],v['tris_visible_default'],v['clips'],v['slot_hides'])
