# build_dungeons.py - generates coast_dungeons_v1.json (add-only). python3 build_dungeons.py
import json,random,os
H=os.path.dirname(os.path.abspath(__file__))
C=json.load(open(os.path.join(H,'../world_v1_coast/coast_v3_grow.json')))
T=C['tiles'];S=C['solid']
def ok(x,y):
  return 0<=y<180 and 0<=x<90 and T[y][x] in '0126' and S[y][x]=='0'
def pick_church():
  best=None
  for y in range(50,110):
    for x in range(30,80):
      if all(ok(x+i,y+j) for i in range(-2,3) for j in range(-2,3)):
        d=abs(x-55)+abs(y-75)
        if best is None or d<best[0]: best=(d,x,y)
  return best[1]+.5,best[2]+.5
W,WA,CV,ST,PL,WT,DR,SA,BL,RG,RD=11,11,12,5,10,8,2,3,14,13,6
def make(w,h,seed,floor,alt,carve,wall_pal):
  r=random.Random(seed);g=[[W]*w for _ in range(h)]
  for (x0,y0,x1,y1) in carve:
    for y in range(y0,y1):
      for x in range(x0,x1): g[y][x]=floor if r.random()>.18 else alt
  # ragged edges: bite random wall tiles back in so no straight seams
  for y in range(1,h-1):
    for x in range(1,w-1):
      if g[y][x]==W and sum(g[y+dy][x+dx]!=W for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))>=2 and r.random()<.35: g[y][x]=alt
      elif g[y][x]!=W and sum(g[y+dy][x+dx]==W for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))>=2 and r.random()<.25: g[y][x]=W
  return g
def enc(g): return [''.join('0123456789abcde'[v] for v in row) for row in g]
def solid(g): return [''.join('1' if v in(W,WT) else '0' for v in row) for row in g]
def walk(g,x,y):
  g[int(y)][int(x)]=g[int(y)][int(x)] if g[int(y)][int(x)] not in(W,WT) else 2
cx,cy=pick_church()
areas=[]
# 1 wrecks: three hulls joined by plank gangways over water
g=make(30,22,1,PL,DR,[(2,15,10,21),(3,3,12,13),(12,7,19,10),(17,2,27,12),(19,12,23,17),(16,16,28,21)],'hull')
for y in range(22):
  for x in range(30):
    if g[y][x]==W and 10<=x<=19 and 9<=y<=20 and (x+y)%3: g[y][x]=WT
for x0,y0,x1,y1 in((5,11,7,17),(9,17,18,19),(11,7,19,9),(20,11,22,18)):
  for y in range(y0,y1):
    for x in range(x0,x1): g[y][x]=PL  # plank gangways
areas.append(dict(id='wrecks',name='The Broken Hulls',kind='dungeon',size=[30,22],
 entrance=dict(coast=[45.8,29.4],note='beside the flotsam dock exit (44.6,28.2); separate trigger, flotsam exit untouched',label='Climb into the wrecks'),
 spawn=[5.5,19.5],exits=[dict(x=5.5,y=20.5,to='coast',sx=45.8,sy=30.6,label='Back to the strand')],
 wall_style='wrecked hulls + rubble',enemies=[dict(id='wk_s1',pack=['zombie','zombie','corpse'],pos=[7.5,7.5]),dict(id='wk_s2',pack=['imp','imp'],pos=[21.5,6.5]),dict(id='wk_s3',pack=['corpse','zombie','imp'],pos=[21.5,18.5])],
 boss=dict(id='wk_boss',kind='zombie',elite=True,name='The Drowned Bosun',pos=[24.5,5.5],drop='chest'),
 loot=[[4.5,4.5],[25.5,19.5]],
 props=[dict(glb='models/town/martsirt_v2_2/props/prop_crate_stack_lite.glb',x=10.5,y=4.5),dict(glb='models/town/martsirt_v2_2/props/prop_barrel_group_lite.glb',x=18.5,y=10.5),dict(glb='models/town/martsirt_v2_2/props/prop_barrel_group_lite.glb',x=26.5,y=17.5),dict(glb='models/border_kit_v1/bk_sea_dead.glb',x=14.5,y=15.5,note='wall dressing at water edge')],
 tiles=enc(g),solid=solid(g)))
# 2 sewer: winding brick channels, water down the middle
g=make(34,20,2,ST,BL,[(2,2,8,8),(6,4,26,7),(22,2,31,10),(26,9,30,17),(8,13,30,17),(3,8,9,18)],'brick')
for x in range(7,26): g[5][x]=WT
for x in range(9,27): g[15][x]=WT
for y in (5,15):
  for x in (12,20): g[y][x]=9
areas.append(dict(id='sewer_coast',name='Ashen Drains',kind='dungeon',size=[34,20],
 entrance=dict(coast=[60.6,19.8],note='WP1 sewer_stairs; if the live sewer world already exists, reuse its id and only add this layout as sewer_coast'),
 spawn=[4.5,3.5],exits=[dict(x=4.5,y=2.5,to='coast',sx=60.6,sy=21.0,label='Up the stairs')],
 wall_style='brick + collapsed rubble',enemies=[dict(id='sw_s1',pack=['zombie','corpse'],pos=[16.5,4.5]),dict(id='sw_s2',pack=['imp','imp','imp'],pos=[27.5,6.5]),dict(id='sw_s3',pack=['zombie','zombie','corpse'],pos=[16.5,14.5])],
 boss=dict(id='sw_boss',kind='corpse',elite=True,name='The Drain Mother',pos=[5.5,15.5],drop='chest'),
 loot=[[29.5,15.5],[4.5,10.5]],
 props=[dict(glb='models/town/martsirt_v2_2/dressing/dress_rocks_lite.glb',x=24.5,y=8.5),dict(glb='models/town/martsirt_v2_2/props/prop_crate_stack_lite.glb',x=28.5,y=3.5),dict(glb='models/env_extra/props_gothic_v1/props/chains_shackles_v1_lite.glb',x=6.5,y=14.5)],
 tiles=enc(g),solid=solid(g)))
# 3 church: ruined nave + crypt room
g=make(20,16,3,ST,RG,[(3,3,17,10),(6,10,14,14),(8,1,12,3)],'ruin')
for x in range(5,16): g[6][x]=RG
areas.append(dict(id='church_coast',name='Salt Chapel (ruin)',kind='quest',size=[20,16],
 entrance=dict(coast=[cx,cy-1.5],note='plan has no coast church slot: chosen open land tile nearest map centre on coast_v3 (5x5 walkable)',exterior_glb='models/town/martsirt_v2_2/buildings/chapel_st_noll/bld_chapel_st_noll_shared_lite.glb',exterior_pos=[cx,cy]),
 spawn=[10.5,12.5],exits=[dict(x=10.5,y=13.5,to='coast',sx=cx,sy=cy+1.5,label='Out to the strand')],
 wall_style='broken stone ruin',enemies=[dict(id='ch_s1',pack=['corpse','corpse'],pos=[5.5,4.5]),dict(id='ch_s2',pack=['zombie','imp'],pos=[15.5,8.5])],
 quest=dict(id='dng1_church',pos=[10.5,2.5],kind='altar',note='quest point at altar; hook to the quest Brian names (none assigned in plan)'),
 loot=[[15.5,4.5]],
 props=[dict(glb='models/env_extra/props_gothic_v1/props/church_pew_v1_lite.glb',x=6.5,y=7.5),dict(glb='models/env_extra/props_gothic_v1/props/church_pew_v1_lite.glb',x=13.5,y=7.5),dict(glb='models/env_extra/props_gothic_v1/props/candelabra_tall_v1_lite.glb',x=9.0,y=2.5),dict(glb='models/env_extra/props_gothic_v1/props/altar_cloth_v1_lite.glb',x=10.5,y=2.0),dict(glb='models/env_extra/props_gothic_v1/props/cobweb_cards_v1_lite.glb',x=4.5,y=9.0)],
 tiles=enc(g),solid=solid(g)))
# 4 tidal cave at SQ14_v3 cove (NL2/F10 tidal caves)
g=make(26,18,4,CV,SA,[(2,12,8,17),(5,6,12,13),(10,3,20,8),(17,7,24,15),(11,12,19,16)],'cliff')
areas.append(dict(id='tidecave',name='Tidebound Cave',kind='dungeon',size=[26,18],
 entrance=dict(coast=[17.5,151.0],note='cave mouth by SQ14_v3 (17.5,152.5), SW cove; mouth piece = bk_sea_dead + dress_rocks'),
 spawn=[4.5,15.5],exits=[dict(x=4.5,y=16.5,to='coast',sx=17.5,sy=153.5,label='Out to the cove')],
 wall_style='sea cliffs + boulders',enemies=[dict(id='tc_s1',pack=['zombie','zombie'],pos=[8.5,9.5]),dict(id='tc_s2',pack=['imp','corpse','imp'],pos=[20.5,11.5])],
 boss=dict(id='tc_boss',kind='imp',elite=True,name='Cairn-Keeper',pos=[15.5,4.5],drop='chest'),
 quest=dict(id='SQ14_v3',pos=[14.5,14.5],kind='cairn',note='Tidebound cairn variation 3'),
 loot=[[22.5,13.5]],
 props=[dict(glb='models/town/martsirt_v2_2/dressing/dress_rocks_lite.glb',x=6.5,y=8.5),dict(glb='models/border_kit_v1/bk_sea_dead.glb',x=12.5,y=4.5),dict(glb='models/town/martsirt_v2_2/props/prop_barrel_group_lite.glb',x=21.5,y=8.5)],
 tiles=enc(g),solid=solid(g)))
for a in areas:
  for p in [a['spawn']]+[[e['x'],e['y']] for e in a['exits']]+[e['pos'] for e in a['enemies']]+a['loot']+[p2 for p2 in [a.get('boss',{}).get('pos'),a.get('quest',{}).get('pos')] if p2]+[[q['x'],q['y']] for q in a['props']]:
    x,y=int(p[0]),int(p[1]);row=list(a['tiles'][y]);sr=list(a['solid'][y])
    if sr[x]=='1': row[x]='2' if a['id']!='church_coast' else '5';sr[x]='0'
    a['tiles'][y]=''.join(row);a['solid'][y]=''.join(sr)
out=dict(patch_id='coast_dungeons_v1',applies_after='PROMPT_WP1 (coast_v3_grow)',tile_enum='0 Grass,1 Grass2,2 Dirt,3 Sand,4 Sand2,5 Stone,6 Road,7 Plaza,8 Water,9 Bridge,a Plank,b Wall,c Cave,d Rug,e Blood',
 encoding='tiles: H strings of W base-36 chars (row y). solid: 1 blocked. Blocking is by solid tiles only (col_* never blocks).',
 wall_glbs={'hull':'models/border_kit_v1/bk_sea_dead.glb','brick':'models/border_kit_v1/bk_town_dead.glb','ruin':'models/border_kit_v1/bk_town_autumn.glb','cliff':'models/border_kit_v1/bk_mountain_dead.glb'},
 wall_rule='instance the style GLB on solid tiles that touch walkable tiles; random rotY in 90deg steps + scale 0.85-1.15 + skip 1 in 4 for rubble gaps; mix dress_rocks_lite on corners. No straight seams.',
 areas=areas)
json.dump(out,open(os.path.join(H,'coast_dungeons_v1.json'),'w'),indent=1)
# check: every exit/spawn reachable from spawn
for a in areas:
  w,h=a['size'];sol=a['solid'];sx,sy=map(int,a['spawn']);seen={(sx,sy)};st=[(sx,sy)]
  while st:
    x,y=st.pop()
    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
      n=(x+dx,y+dy)
      if 0<=n[0]<w and 0<=n[1]<h and n not in seen and sol[n[1]][n[0]]=='0': seen.add(n);st.append(n)
  pts=[a.get('boss',{}).get('pos'),a.get('quest',{}).get('pos')]+[e['pos'] for e in a['enemies']]+a['loot']
  bad=[p for p in pts if p and (int(p[0]),int(p[1])) not in seen]
  print(a['id'],a['size'],'reach',len(seen),'unreachable',bad)
print('church coast tile',cx,cy)
