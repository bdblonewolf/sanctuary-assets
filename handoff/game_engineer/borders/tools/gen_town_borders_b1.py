# Fast b1 border layouts for ringless outdoor zones (bastion, lut, market). Props only, outside map or on edge-ring solid tiles.
import json, math, random, os
R='handoff/game_engineer/'
W=json.load(open(R+'exits/tools/world_rich.json'))['worlds']
B='models/outdoor/v5_maps/border/'; C='models/env_extra/cliffkit_v2/'; A='models/ashen_v1/'; T=R+'borders/martsirt/trees_v2_1/'
P='models/outdoor/v5/plants/'
S={
 'bastion':dict(outer=[(B+'border_peak_a_v5_dead.glb',3,(2.6,4.2)),(B+'border_peak_b_v5_dead.glb',3,(2.6,4.2)),(B+'border_peak_c_v5_dead.glb',3,(2.6,4.2)),(B+'border_shelf_a_v5_dead.glb',2,(2.2,3.2)),(B+'border_shelf_b_v5_dead.glb',2,(2.2,3.2)),(C+'rock_spire_bare_16m_dead.glb',1,(0.35,0.6))],
   inner=[(A+'gtree_crooked_winter_lod0.glb',3,(0.8,1.2)),(A+'gtree_twisted_winter_lod0.glb',3,(0.8,1.2)),(C+'dead_stump_blighted_dead.glb',2,(0.9,1.3)),(C+'sway_dead_grass_patch_2m.glb',3,(0.9,1.4)),(A+'shore_rock_a_boulder.glb',2,(0.7,1.1)),(A+'shore_rock_d_cluster.glb',2,(0.7,1.1))]),
 'lut':dict(outer=[(B+'border_dune_a_v5_summer.glb',3,(2.4,3.8)),(B+'border_dune_b_v5_summer.glb',3,(2.4,3.8)),(B+'border_dune_c_v5_summer.glb',3,(2.4,3.8)),(B+'border_peak_a_v5_summer.glb',2,(2.4,3.6)),(B+'border_peak_b_v5_summer.glb',2,(2.4,3.6)),(B+'border_shelf_c_v5_summer.glb',1,(2.2,3.0))],
   inner=[(P+'plant_cactus_column_a_v5.glb',2,(0.9,1.3)),(P+'plant_cactus_cluster_b_v5.glb',2,(0.9,1.3)),(C+'dead_stump_blighted.glb',1,(0.9,1.3)),(A+'shore_rock_a_boulder.glb',2,(0.7,1.1)),(A+'shore_rock_d_cluster.glb',2,(0.7,1.1))]),
 'market':dict(outer=[(B+'border_peak_a_v5_autumn.glb',3,(2.6,4.2)),(B+'border_peak_b_v5_autumn.glb',3,(2.6,4.2)),(B+'border_peak_c_v5_autumn.glb',3,(2.6,4.2)),(B+'border_shelf_a_v5_autumn.glb',2,(2.2,3.2)),(B+'border_shelf_b_v5_autumn.glb',2,(2.2,3.2)),(C+'rock_spire_bare_16m.glb',1,(0.35,0.6))],
   inner=[(T+'btree_gothic_tall_autumn.glb',3,(0.45,0.65)),(T+'btree_gothic_twisted_autumn.glb',3,(0.45,0.65)),(T+'btree_oak_autumn.glb',2,(0.45,0.65)),(C+'dead_stump_blighted.glb',2,(0.9,1.3)),(A+'shore_rock_a_boulder.glb',2,(0.7,1.1)),(A+'shore_rock_d_cluster.glb',2,(0.7,1.1))]),
}
def pick(rng,lst):
    t=sum(w for _,w,_ in lst); r=rng.random()*t
    for a,w,s in lst:
        r-=w
        if r<=0: return a,s
    return lst[-1][0],lst[-1][2]
out={}
for z,st in S.items():
    for lst in st.values():
        for a,_,_ in lst: assert os.path.exists(a), a
    v=W[z]; w,h=v['w'],v['h']; sol=v['solid']; rng=random.Random(sum(map(ord,z))*7919)
    solid=lambda x,y: x<0 or y<0 or x>=w or y>=h or bool(sol[int(y)*w+int(x)])
    # exit gaps: edge tiles that are walkable
    gaps=[]
    for x in range(w):
        for y in (0,h-1):
            if not solid(x,y): gaps.append((x+.5,y+.5))
    for y in range(h):
        for x in (0,w-1):
            if not solid(x,y): gaps.append((x+.5,y+.5))
    def neargap(px,pz,d): return any(math.hypot(px-gx,pz-gy)<d for gx,gy in gaps)
    props=[]
    edges={'N':((0,0),(1,0),(0,-1),w),'S':((0,h),(1,0),(0,1),w),'W':((0,0),(0,1),(-1,0),h),'E':((w,0),(0,1),(1,0),h)}
    for e,((ox,oz),(dx,dz),(nx,nz),L) in edges.items():
        for layer,off,sp,lst in (('outer_far',(5.5,9.0),(3.2,5.2),'outer'),('outer',(1.2,4.0),(2.4,4.0),'outer'),('lip_inner',(-1.6,-0.4),(1.8,3.4),'inner')):
            t=-4.0 if layer!='lip_inner' else 0.6
            end=L+4.0 if layer!='lip_inner' else L-0.6
            while t<end:
                t+=rng.uniform(*sp); o=rng.uniform(*off)
                px=ox+dx*t+nx*o+rng.uniform(-.6,.6)*abs(nz); pz=oz+dz*t+nz*o+rng.uniform(-.6,.6)*abs(nx)
                if layer=='lip_inner':
                    if not (solid(px,pz) and solid(px-.45,pz-.45) and solid(px+.45,pz+.45) and solid(px-.45,pz+.45) and solid(px+.45,pz-.45)): continue
                    if neargap(px,pz,2.6): continue
                else:
                    if neargap(px,pz,2.2+0.6*(layer=='outer')) and layer=='outer': continue
                a,s=pick(rng,st[lst]); sc=round(rng.uniform(*s),3)
                if layer=='outer_far': sc=round(sc*1.25,3)
                inside=layer=='lip_inner'
                props.append(dict(id=os.path.basename(a).replace('.glb',''),asset=a,layer=layer,edge=e,pos=[round(px,3),0.0,round(pz,3)],rotY=round(rng.uniform(0,6.2832),4),scale=sc,
                    collider='none (edge-ring tile already solid)' if inside else 'none (outside map)',blocks_walk=False))
    by={}
    for p in props: by[p['id']]=by.get(p['id'],0)+1
    L=dict(zone=z,size=1,frame='tile metres; three.js x east z south; map [0,w]x[0,h]',glb='props only (no kit pieces)',runs={},seams=0,pieces=[],props=props,
           stats=dict(pieces=0,props=len(props),prop_by_id=by,moved_world_props=0,collider_changes=0))
    json.dump(L,open(R+f'borders/{z}/layout_{z}.json','w'),indent=1)
    out[z]=(0,len(props))
print(out)
