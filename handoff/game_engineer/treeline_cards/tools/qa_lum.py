import sys,glob,json; sys.path.insert(0,'/tmp')
from gl import *
from PIL import Image
def s2l(x): x=x/255.0; return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)
def lum(c): return 0.2126*c[...,0]+0.7152*c[...,1]+0.0722*c[...,2]
orig={}
import os
if os.path.exists('/tmp/orig_lum2.json'): orig=json.load(open('/tmp/orig_lum2.json'))
else:
    from collections import defaultdict
    S=defaultdict(list)
    for f in sorted(glob.glob('/workspace/sanctuary-assets/models/border_kit_v1/bk_*.glb')+glob.glob('/workspace/sanctuary-assets/models/outdoor/v5_maps/rect/*.glb')):
        g=pygltflib.GLTF2().load(f); season=f.rsplit('_',1)[1][:-4]; kind='kit' if '/bk_' in f else 'ring'
        key=kind+'_'+season
        for n in g.nodes:
            if n.name.startswith('trees') and n.mesh is not None:
                for p in g.meshes[n.mesh].primitives: S[key].append(lum(acc(g,p.attributes.COLOR_0)[:,:3]))
    for k,v in S.items():
        L=np.concatenate(v); orig[k]=dict(mean=float(L.mean()),p5=float(np.percentile(L,5)),p50=float(np.median(L)))
    json.dump(orig,open('/tmp/orig_lum2.json','w'))
for k in ['kit_summer','ring_summer','kit_autumn','ring_autumn','kit_winter','ring_winter','kit_dead']:
    a=np.asarray(Image.open(f'atlas_{k}.png').convert('RGBA')).astype(float)
    m=a[...,3]>127; L=lum(s2l(a[...,:3][m]))*0.93  # x mean vertex jitter
    o=orig[k]; 
    print(f"{k:12s} card mean {L.mean():.4f} p5 {np.percentile(L,5):.4f} p50 {np.median(L):.4f} | orig mean {o['mean']:.4f} p5 {o['p5']:.4f} p50 {o['p50']:.4f} | ratio mean {L.mean()/o['mean']:.2f} p5 {np.percentile(L,5)/max(o['p5'],1e-6):.2f}")
