# gen_check.py - builds dungeon_rooms_v2.json from v1 data, then runs the reference generator on 200 seeds/area.
import json,random,os
H=os.path.dirname(os.path.abspath(__file__))
V1=json.load(open(os.path.join(H,'../world_v1_coast_dungeons/coast_dungeons_v1.json')))
N=10;D=['N','E','S','W'];OPP={'N':'S','S':'N','E':'W','W':'E'};DV={'N':(0,-1),'E':(1,0),'S':(0,1),'W':(-1,0)}
STY={'wrecks':(10,2,8,(6,9)),'sewer_coast':(5,14,8,(7,10)),'church_coast':(5,13,None,(4,6)),'tidecave':(12,3,8,(5,8))}
DOOR={'N':[(4,0),(5,0)],'S':[(4,9),(5,9)],'W':[(0,4),(0,5)],'E':[(9,4),(9,5)]}
def room(rid,kind,sock,seed,floor,alt,water,extra={}):
  r=random.Random(seed);g=[[11]*N for _ in range(N)]
  for y in range(1,N-1):
    for x in range(1,N-1): g[y][x]=floor if r.random()>.2 else alt
  for _ in range(3):  # ragged wall bites in corners (no straight seams)
    g[r.choice([1,2,7,8])][r.choice([1,8])]=11
  if water and kind in('corridor','junction'):
    for x in range(1,3): g[1][x]=water; g[8][9-x]=water
  for s in sock:
    x0,y0=DOOR[s][0]
    for t in range(6):
      xx=x0-DV[s][0]*t; yy=y0-DV[s][1]*t
      for dx,dy in(((0,0),(1,0)) if s in'NS' else((0,0),(0,1))): g[yy+dy][xx+dx]=floor
  enc=[''.join('0123456789abcde'[v] for v in row) for row in g]
  return dict(id=rid,kind=kind,sockets=sock,tiles=enc,solid=[''.join('1' if c in'b8' else '0' for c in row) for row in enc],**extra)
pools={}
for i0,a in enumerate(V1['areas']):
  aid=a['id'];fl,al,wt,cnt=STY[aid];base=100*i0
  ex=a['exits'][0]
  R=[room(aid+'_entrance','entrance',['N'],base,fl,al,wt,dict(spawn=[4.5,6.5],exit=dict(x=4.5,y=8.0,to='coast',sx=ex['sx'],sy=ex['sy'],label=ex['label'])))]
  for i,(n,k,s) in enumerate([('dead','dead_end',['N']),('cor','corridor',['N','S']),('cor2','corridor',['N','S']),('crn','corner',['N','E']),('crn2','corner',['N','E']),('tee','junction',['N','E','S']),('x','junction',['N','E','S','W'])]):
    R.append(room(f'{aid}_{n}',k,s,base+i+1,fl,al,wt,dict(spawns=[[3.5,3.5]] if k!='dead_end' else [],loot=[[6.5,6.5]] if k=='dead_end' else [])))
  last={}
  if 'boss' in a: last['boss']=dict(a['boss'],pos=[4.5,3.5])
  if 'quest' in a: last['quest']=dict(a['quest'],pos=[4.5,2.5] if 'boss' not in a else [6.5,5.5])
  R.append(room(aid+('_boss' if 'boss' in a else '_quest'),'boss' if 'boss' in a else 'quest',['S'],base+20,fl,al,wt,dict(last,loot=[[2.5,2.5]],spawns=[[6.5,6.5]])))
  pools[aid]=dict(name=a['name'],wall_style=a['wall_style'],count=list(cnt),max_cells=6,packs=[e['pack'] for e in a['enemies']],props=[p['glb'] for p in a['props']],entrance_coast=a['entrance'],rooms=R)
out=dict(patch_id='dungeon_rooms_v2',applies_after='PROMPT_WP1 (live); replaces DNG1 (never pasted)',room_size=N,
 tile_enum=V1['tile_enum'],wall_glbs=V1['wall_glbs'],wall_rule=V1['wall_rule'],
 sockets='door = 2 tiles mid-edge: N (4,0)(5,0), S (4,9)(5,9), W (0,4)(0,5), E (9,4)(9,5). Rooms stored unrotated.',
 rotate='one 90deg CW step: tile new[y][x]=old[9-x][y]; point (x,y)->(10-y,x); sockets N->E->S->W->N. Rotate tiles+solid+points BEFORE building meshes and blocking.',
 seal='after growth, each socket without a matching neighbour: set its 2 door tiles to Wall b, solid 1.',
 wall_caps='solid tiles touching a walkable tile get a wall GLB; solid tiles with no walkable neighbour get nothing; map outer ring is always solid.',
 spawns='each spawns[] point gets one random pack from area.packs; boss/quest room as given; loot -> chest/urn; 1-2 random area props per non-entrance room on a walkable tile.',
 areas=pools)
json.dump(out,open(os.path.join(H,'dungeon_rooms_v2.json'),'w'),indent=1)
# ---- reference generator ----
def rot(rm,k):
  t=[list(r) for r in rm['tiles']];s=list(rm['sockets'])
  for _ in range(k): t=[[t[9-x][y] for x in range(N)] for y in range(N)]; s=[D[(D.index(q)+1)%4] for q in s]
  return t,s
def gen(p,seed):
  r=random.Random(seed);lo,hi=p['count'];mx=p['max_cells']
  by={}
  for x in p['rooms']: by.setdefault(x['kind'],[]).append(x)
  t,s=rot(by['entrance'][0],r.randrange(4));cells={(0,0):(t,s)};op=[((0,0),q) for q in s]
  target=r.randint(lo,hi)-1;mids=by['corridor']+by['corner']+by['junction']
  def fits(n):
    xs=[c[0] for c in cells]+[n[0]];ys=[c[1] for c in cells]+[n[1]];return max(xs)-min(xs)<mx and max(ys)-min(ys)<mx
  for _ in range(300):
    if not op or len(cells)>=target: break
    c,q=op.pop(r.randrange(len(op)));n=(c[0]+DV[q][0],c[1]+DV[q][1])
    if n in cells or not fits(n): continue
    pool=mids+(by['dead_end'] if len(op)>2 else [])
    rm=r.choice(pool);done=False
    for k in r.sample(range(4),4):
      t,s=rot(rm,k)
      if OPP[q] in s and all((n[0]+DV[z][0],n[1]+DV[z][1]) not in cells or z==OPP[q] for z in s): done=True;break
    if not done: op.append((c,q));continue
    cells[n]=(t,s);op+=[(n,z) for z in s if z!=OPP[q]]
  dist={(0,0):0};fr=[(0,0)]
  while fr:
    c=fr.pop(0)
    for z in cells[c][1]:
      n=(c[0]+DV[z][0],c[1]+DV[z][1])
      if n in cells and n not in dist and OPP[z] in cells[n][1]: dist[n]=dist[c]+1;fr.append(n)
  cand=[(dist[c],c,q) for c,q in op if c in dist and (c[0]+DV[q][0],c[1]+DV[q][1]) not in cells and fits((c[0]+DV[q][0],c[1]+DV[q][1]))]
  if not cand: return None
  _,c,q=max(cand);n=(c[0]+DV[q][0],c[1]+DV[q][1]);b=(by.get('boss') or by['quest'])[0]
  for k in range(4):
    t,s=rot(b,k)
    if s==[OPP[q]]: break
  cells[n]=(t,s)
  if not(lo<=len(cells)<=hi): return None
  xs=[c[0] for c in cells];ys=[c[1] for c in cells];W=(max(xs)-min(xs)+1)*N;Hh=(max(ys)-min(ys)+1)*N
  G=[['b']*W for _ in range(Hh)]
  for (cx,cy),(t,s) in cells.items():
    for z in s:
      nb=(cx+DV[z][0],cy+DV[z][1])
      if not(nb in cells and OPP[z] in cells[nb][1]):
        for x,y in DOOR[z]: t[y][x]='b'
    ox=(cx-min(xs))*N;oy=(cy-min(ys))*N
    for y in range(N):
      for x in range(N): G[oy+y][ox+x]=t[y][x]
  return G,cells,(min(xs),min(ys)),n
def check(G,cells,o,bc):
  sol=lambda x,y:G[y][x] in 'b8';ctr=lambda c:((c[0]-o[0])*N+4,(c[1]-o[1])*N+4)
  s0=ctr((0,0));seen={s0};st=[s0]
  while st:
    x,y=st.pop()
    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
      n=(x+dx,y+dy)
      if 0<=n[1]<len(G) and 0<=n[0]<len(G[0]) and n not in seen and not sol(*n): seen.add(n);st.append(n)
  allc=all(ctr(c) in seen for c in cells)
  edge=all(G[0][x]=='b' and G[-1][x]=='b' for x in range(len(G[0]))) and all(r[0]=='b' and r[-1]=='b' for r in G)
  return ctr(bc) in seen and allc and edge and len(G)<=60 and len(G[0])<=60
res={}
for aid,p in pools.items():
  ok=0;retr=0;sz=[];ks=[]
  for seed in range(200):
    g=None
    for att in range(10):
      g=gen(p,seed*97+att)
      if g: break
      retr+=1
    if g and check(*g): ok+=1;sz.append((len(g[0][0]),len(g[0])));ks.append(len(g[1]))
  res[aid]=dict(passed=f'{ok}/200',retries_total=retr,rooms=[min(ks),max(ks)] if ks else None,max_tiles_wh=[max(a for a,b in sz),max(b for a,b in sz)] if sz else None)
  print(aid,res[aid])
json.dump(res,open(os.path.join(H,'check_result.json'),'w'),indent=1)
