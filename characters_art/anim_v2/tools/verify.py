import pygltflib,os,json,numpy as np
A='/workspace/sanctuary-assets/'; O=A+'characters_art/anim_v2/'
pairs={f'clips_{n[:-4]}.glb':A+'characters_art/bodies/'+n for n in os.listdir(A+'characters_art/bodies')}
pairs['clips_ayla_phimn.glb']=A+'characters_art/npcs/ayla_phimn/ayla_phimn_body.glb'
pairs['hero_extra.glb']=A+'models/knight_anim_v10b.glb'
res={}
for f,b in sorted(pairs.items()):
    g=pygltflib.GLTF2().load(O+f); gb=pygltflib.GLTF2().load(b)
    bj={gb.nodes[j].name:gb.nodes[j] for j in gb.skins[0].joints}
    tn=set(g.nodes[c.target.node].name for a in g.animations for c in a.channels)
    miss=sorted(tn-set(bj)); 
    rest=max(max(np.abs(np.array(g.nodes[i].translation)-np.array(bj[g.nodes[i].name].translation or [0,0,0])).max(),
                  np.abs(np.array(g.nodes[i].rotation)-np.array(bj[g.nodes[i].name].rotation or [0,0,0,1])).max()) for i in range(1,len(g.nodes)))
    res[f]=dict(meshes=len(g.meshes),animations=len(g.animations),tracks_target_names=len(tn),missing_in_body=miss,rest_trs_maxdiff=float(rest),bytes=os.path.getsize(O+f))
    print(f,res[f])
json.dump(res,open('/workspace/animv2/verify.json','w'),indent=1)
