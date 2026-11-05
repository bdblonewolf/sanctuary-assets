#!/usr/bin/env python3
"""Builds coast_v3_grow.json (90x180 grow recipe for the Ashen Coast) and old_coast_recon.json.
Old 42x112 map: rows 0-15 = live dump (/workspace/npcdbg/coast_tiles.json, copied into old_coast_recon.json),
rows 16-111 = reconstructed from the bundle generator (Xc + Jc + Yc in live3.js); noise Sand/Sand2 is approximated.
Deterministic: python3 build_coast_v3.py"""
import json, math, random, os
from collections import deque
HERE=os.path.dirname(os.path.abspath(__file__))
G,G2,DI,SA,S2,ST,RD,PL,WA,BR=0,1,2,3,4,5,6,7,8,9
OW,OH=42,112; W,H=90,180; OX,OY=24,0
rng=random.Random(90180)
# ---------- old map reconstruction ----------
def recon():
    w,h=42,56; t=[[SA]*w for _ in range(h)]; s=[[0]*w for _ in range(h)]
    r=random.Random(789079)
    for y in range(h):
        for x in range(w):
            if r.random()<.45: t[y][x]=S2
    def Y(x0,y0,x1,y1,v,sol):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                if 0<=x<w and 0<=y<h: t[y][x]=v; s[y][x]=1 if sol else 0
    Y(0,0,7,29,WA,1);Y(0,24,41,29,WA,1);Y(0,30,41,55,WA,1);Y(19,24,22,29,BR,0);Y(19,0,21,18,RD,0);Y(21,13,41,15,RD,0)
    Y(14,16,24,20,PL,0);Y(26,8,34,12,DI,0);Y(11,16,13,17,SA,1);Y(36,19,37,20,DI,0)
    for (x,y) in [(31.5,20.6),(33.4,22.4),(34.2,18.2),(38.6,18.2),(39.2,21.4),(30.6,22.4),(38.4,22.6),(32.4,17.4),(39.4,17.2),(30.4,18.6)]:
        xi,yi=int(x),int(y)
        if t[yi][xi] not in (WA,RD,BR,PL) and not(35<=xi<=37 and 16<=yi<=22): s[yi][xi]=1
    # Jc
    Y(8,22,16,50,SA,0)
    for yy in range(24,51):
        for xx in range(8,17):
            if (xx*3+yy*5)%7<3: t[yy][xx]=S2
    Y(11,22,13,48,DI,0);Y(10,43,14,48,DI,0);Y(8,49,16,55,ST,1)
    for yy in range(20,24):
        for xx in range(11,22):
            v=t[yy][xx]
            if v not in (WA,BR): 
                if v not in (RD,PL): t[yy][xx]=DI
                s[yy][xx]=0
    e=26.4
    while e<=49.2:
        s[int(e)][8]=1; s[int(e+1.15)][16]=1; e+=3.25
    for (x,y) in [(9.6,51.4),(12.6,52.2),(15.2,51.2)]: s[int(y)][int(x)]=1
    # Yc mirror (180 deg rotation into the south half)
    T=[[SA]*w for _ in range(2*h)]; S=[[0]*w for _ in range(2*h)]
    for y in range(h):
        for x in range(w):
            T[y][x]=t[y][x];S[y][x]=s[y][x]; T[2*h-1-y][w-1-x]=t[y][x]; S[2*h-1-y][w-1-x]=s[y][x]
    for y in range(h-2,h+2):
        for x in range(w): T[y][x]=WA;S[y][x]=1
    for y in range(49,68):
        for x in range(10,15): T[y][x]=DI;S[y][x]=0
    for y in range(62,68):
        for x in range(10,35): T[y][x]=SA;S[y][x]=0
    # top 16 rows: live dump (verified); their mirrored rows too
    d=json.load(open('/workspace/npcdbg/coast_tiles.json'))
    for y,row in enumerate(d['rows']):
        for x,c in enumerate(row):
            v=int(c,36); T[y][x]=v; T[2*h-1-y][w-1-x]=v
    return T,S,len(d['rows'])
OT,OS,DUMPROWS=recon()
# ---------- noise ----------
def h2(i,j,sd): 
    n=(i*374761393+j*668265263+sd*1442695041)&0xffffffff; n=((n^(n>>13))*1274126177)&0xffffffff; return ((n^(n>>16))&0xffffffff)/4294967296
def vn(x,y,sd):
    i,j=math.floor(x),math.floor(y); fx,fy=x-i,y-j; fx=fx*fx*(3-2*fx); fy=fy*fy*(3-2*fy)
    a,b,c,d=h2(i,j,sd),h2(i+1,j,sd),h2(i,j+1,sd),h2(i+1,j+1,sd)
    return a+(b-a)*fx+(c-a)*fy+(a-b-c+d)*fx*fy
def fbm(x,y,sd): return .6*vn(x,y,sd)+.3*vn(2*x,2*y,sd+7)+.1*vn(4*x,4*y,sd+13)
def inold(x,y): return OX<=x<OX+OW and OY<=y<OY+OH
# ---------- full grid: None = keep old ----------
T=[[None]*W for _ in range(H)]; S=[[None]*W for _ in range(H)]
def oldv(x,y): return OT[y-OY][x-OX]
# ---- override (a): north entrance -> grass (old x0-41, y0..~16, noisy south boundary)
north_grass=0
for x in range(OW):
    by=13+int(4*fbm(x/6,0.5,11))+ (3 if x<=8 else 0)   # 13..19 under the old water block, 13..16 elsewhere
    for y in range(0,by+1):
        if y>=DUMPROWS and x>7: continue        # only touch verified dump rows, or the known water strip x0-7
        v=oldv(x+OX,y)
        if v in (RD,PL,BR,DI): continue
        n=fbm((x+OX)/3.1,y/3.1,23)
        nv= G if n<.42 else (G2 if n<.78 else DI)
        if v in (WA,SA,S2,ST): T[y][x+OX]=nv; S[y][x+OX]=0; north_grass+=1
# ---- water mask: old water + west/south sea + blend blobs
wet=[[False]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if inold(x,y): wet[y][x]=(T[y][x] if T[y][x] is not None else oldv(x,y))==WA
def _ss(a,b,v):
    u=min(1,max(0,(v-a)/(b-a))); return u*u*(3-2*u)
def xw(y):  # west shoreline: ~3..17 m, but the W sea floods to the old map between y~20 and ~88 (old W water strip)
    base=3+(y/180)*7+7*fbm(y/16,1.7,31)+1.5*vn(y/4,3.3,37)
    k=_ss(15+4*vn(1,2,33),26,y)*(1-_ss(82,94+3*vn(3,4,35),y))
    return base+k*30
def ys(x): return 156+ 9*fbm(x/14,4.1,41)+2*vn(x/4,9.2,43) - (6 if x<30 else 0)  # south shoreline ~150..167
border_wet=[(x,y) for y in range(OY,OY+OH) for x in (OX,OX+OW-1) if wet[y][x]]+[(x,OY+OH-1) for x in range(OX,OX+OW) if wet[OY+OH-1][x]]
for y in range(H):
    for x in range(W):
        if inold(x,y): continue
        if x<xw(y) or y>ys(x): wet[y][x]=True; continue
        best=99
        for (bx,by) in border_wet:
            d=math.hypot(x-bx,y-by)
            if d<best: best=d
        side_w = x<OX
        r=(9+9*fbm(x/7,y/7,51)) if side_w else (3+5*fbm(x/6,y/6,53))
        if y>=OY+OH and x<OX+OW: r=3+6*fbm(x/6,y/6,57)
        if best<r: wet[y][x]=True
# ---- road skeleton (never straight; 4-6 m wide)
def poly(pts,step=.25):
    out=[]
    for (a,b) in zip(pts,pts[1:]):
        n=int(math.hypot(b[0]-a[0],b[1]-a[1])/step)+1
        for i in range(n):
            u=i/n; out.append((a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u))
    out.append(pts[-1]); return out
def jit(pts,amp,sd):
    o=[pts[0]]
    for i,(x,y) in enumerate(pts[1:-1]): o.append((x+(vn(i*1.7,0,sd)-.5)*amp,y+(vn(0,i*1.3,sd)-.5)*amp))
    o.append(pts[-1]); return o
BAST=(89.4,81.0)
road_e=poly(jit([(64.5,14.0),(68.5,15.2),(73.0,19.5),(78.5,26.0),(80.0,34.0),(77.5,43.0),(79.5,52.0),(83.0,60.0),(82.0,68.5),(85.5,76.0),(89.4,81.0)],2.0,61))
road_s=poly(jit([(45.5,111.0),(46.5,116.0),(43.0,122.5),(37.5,128.0),(33.5,135.0),(27.0,140.5),(21.0,146.0),(17.5,150.0)],1.6,63))
road_w=poly(jit([(37.5,129.5),(31.0,124.0),(24.0,118.5),(18.0,112.0),(14.5,104.0),(13.5,99.5)],1.4,65))
road=[[False]*W for _ in range(H)]
roadpts=[]
for pts,sd in ((road_e,71),(road_s,73),(road_w,75)):
    for k,(px,py) in enumerate(pts):
        rad=2.0+1.0*vn(k/40,0,sd)          # 2..3 -> 4..6 m wide
        roadpts.append((px,py))
        for y in range(int(py-rad)-1,int(py+rad)+2):
            for x in range(int(px-rad)-1,int(px+rad)+2):
                if 0<=x<W and 0<=y<H and not inold(x,y) and math.hypot(x+.5-px,y+.5-py)<=rad:
                    road[y][x]=True; wet[y][x]=False
# ---- distance to water (BFS, 8-neigh)
INF=999; dist=[[INF]*W for _ in range(H)]; q=deque()
for y in range(H):
    for x in range(W):
        if wet[y][x]: dist[y][x]=0; q.append((x,y))
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
        a,b=x+dx,y+dy
        if 0<=a<W and 0<=b<H and dist[b][a]>dist[y][x]+1: dist[b][a]=dist[y][x]+1; q.append((a,b))
# ---- plateaus off the road (raised shelves; rim = solid dirt + rocks, one ramp facing the road)
plateaus=[dict(id="P1",cx=73.0,cy=46.0,r=4.6,ramp=(77.0,45.0),height_m=1.6),
          dict(id="P2",cx=86.0,cy=40.5,r=3.4,ramp=(82.5,39.0),height_m=1.2),
          dict(id="P3",cx=13.5,cy=99.5,r=5.4,ramp=(16.0,103.5),height_m=2.2,poi="E01"),
          dict(id="P4",cx=57.5,cy=133.0,r=4.8,ramp=(52.5,130.5),height_m=1.4)]
plat_tag=[[None]*W for _ in range(H)]
for p in plateaus:
    for y in range(int(p['cy']-p['r'])-3,int(p['cy']+p['r'])+4):
        for x in range(int(p['cx']-p['r'])-3,int(p['cx']+p['r'])+4):
            if not(0<=x<W and 0<=y<H) or inold(x,y): continue
            ang=math.atan2(y+.5-p['cy'],x+.5-p['cx'])
            rr=p['r']*(0.82+0.36*vn(math.cos(ang)*2+5,math.sin(ang)*2+5,81))
            d=math.hypot(x+.5-p['cx'],y+.5-p['cy'])
            if d<=rr+.5:
                wet[y][x]=False
                plat_tag[y][x]='rim' if d>rr-.8 else 'top'
    # ramp: clear rim between ramp point and centre
    for k in range(30):
        u=k/29; px=p['ramp'][0]+(p['cx']-p['ramp'][0])*u*.7; py=p['ramp'][1]+(p['cy']-p['ramp'][1])*u*.7
        for y in range(int(py)-1,int(py)+2):
            for x in range(int(px)-1,int(px)+2):
                if 0<=x<W and 0<=y<H and plat_tag[y][x]=='rim': plat_tag[y][x]='ramp'
# ---- paint new tiles
for y in range(H):
    for x in range(W):
        if inold(x,y): continue
        n=fbm(x/3.3,y/3.3,91); m=fbm(x/9,y/9,93)
        if wet[y][x]: T[y][x]=WA; S[y][x]=1; continue
        S[y][x]=0
        if road[y][x]: T[y][x]=RD; continue
        pt=plat_tag[y][x]
        if pt=='rim': T[y][x]=DI; S[y][x]=1; continue
        if pt=='top': T[y][x]=G2 if n<.6 else DI; continue
        if pt=='ramp': T[y][x]=DI; continue
        d=dist[y][x]+2.2*(n-.5)
        if d<1.6: T[y][x]=SA if n<.5 else S2
        elif d<3.6+1.5*m: T[y][x]=S2 if n<.65 else SA
        elif d<6.5+2*m: T[y][x]=DI if n<.55 else S2
        else: T[y][x]=(DI if m>.68 else (G if n<.45 else G2))
# soft road shoulders (dirt), never straight
for y in range(H):
    for x in range(W):
        if inold(x,y) or T[y][x] in (RD,WA) or S[y][x]: continue
        if any(0<=x+dx<W and 0<=y+dy<H and road[y+dy][x+dx] for dx in (-1,0,1) for dy in (-1,0,1)) and fbm(x/2,y/2,97)<.55: T[y][x]=DI
# ---- override (b): blend old E-edge road end so the road continues (old road x41 y13-15 is already Road; nothing to change)
# ---- props
ASSET=dict(twisted="models/ashen_v1/gtree_twisted_winter_lod0.glb",crooked="models/ashen_v1/gtree_crooked_winter_lod0.glb",
  weeping="models/ashen_v1/gtree_weeping_winter_lod0.glb",stump="models/env_extra/cliffkit_v2/dead_stump_blighted_dead.glb",
  rockA="models/ashen_v1/shore_rock_a_boulder.glb",rockB="models/ashen_v1/shore_rock_b_slab.glb",rockC="models/ashen_v1/shore_rock_c_stack.glb",
  rockD="models/ashen_v1/shore_rock_d_cluster.glb",stack="models/ashen_v1/shore_rock_e_seastack.glb",
  grass="models/env_extra/cliffkit_v2/sway_dead_grass_patch_2m.glb",bonfire="models/town/martsirt_v2_2/portable/props/prop_bonfire_main_tex.glb",
  camp="models/town/martsirt_v2_2/portable/props/prop_campfire_tex.glb",log="models/town/martsirt_v2_2/portable/props/prop_seat_log_tex.glb",
  barrels="models/town/martsirt_v2_2/portable/props/prop_barrel_group_tex.glb",crates="models/town/martsirt_v2_2/portable/props/prop_crate_stack_tex.glb",
  bench="models/town/martsirt_v2_2/portable/props/prop_seat_stone_bench_tex.glb")
props=[]; occ=[]
def near_road(x,y,m):
    for yy in range(int(y-m)-1,int(y+m)+2):
        for xx in range(int(x-m)-1,int(x+m)+2):
            if 0<=xx<W and 0<=yy<H and road[yy][xx] and math.hypot(xx+.5-x,yy+.5-y)<m: return True
    return False
def free(x,y,r): return all(math.hypot(x-a,y-b)>=r+c for a,b,c in occ)
def add(pid,key,x,y,sc,layer,rad,solid=False):
    if road[int(y)][int(x)]: return
    props.append(dict(id=pid,asset=ASSET[key],layer=layer,pos=[round(x,3),0.0,round(y,3)],rotY=round(rng.uniform(0,6.2832),4),scale=round(sc,3),**({"solid_tile":[int(x),int(y)]} if solid else {})))
    occ.append((x,y,rad))
    if solid: S[int(y)][int(x)]=1
CAMPS=[(76.0,30.5),(30.5,141.5),(13.0,8.5)]
camps_out=[]
for (cx,cy) in CAMPS:
    xi,yi=int(cx),int(cy)
    if wet[yi][xi] or inold(xi,yi): continue
    add("bonfire","bonfire",cx,cy,1.0,"camp",1.6); camps_out.append([cx,cy])
    add("seat_log","log",cx+1.7,cy+.6,1.0,"camp",.8); add("seat_log","log",cx-1.4,cy+1.3,.95,"camp",.8)
    add("barrels","barrels",cx+.9,cy-2.0,.9,"camp",.8); add("crates","crates",cx-2.1,cy-1.1,.9,"camp",.8)
cand=[(x+rng.uniform(.15,.85),y+rng.uniform(.15,.85)) for y in range(H) for x in range(W)]
rng.shuffle(cand)
cnt=dict(tree=0,stump=0,shore=0,grass=0,stack=0)
for (x,y) in cand:
    xi,yi=int(x),int(y)
    if inold(xi,yi) or not(1<=xi<W-1 and 1<=yi<H-1): continue
    v=T[yi][xi]
    if v==WA: continue
    if road[yi][xi] or near_road(x,y,1.8) or plat_tag[yi][xi]=='ramp': continue
    d=dist[yi][xi]
    if plat_tag[yi][xi]=='rim':
        if cnt['shore']<200 and free(x,y,1.0): add("shore_rock",rng.choice(["rockA","rockB","rockD"]),x,y,rng.uniform(.8,1.3),"plateau_rim",1.0); cnt['shore']+=1
        continue
    if d<=2 and S[yi][xi]==0:
        if rng.random()<.18 and free(x,y,2.2): add("shore_rock",rng.choice(["rockA","rockB","rockC","rockD"]),x,y,rng.uniform(.7,1.35),"shore",1.6,solid=rng.random()<.5); cnt['shore']+=1
        continue
    if d>=4 and rng.random()<.055 and free(x,y,2.6):
        k=rng.choice(["twisted","twisted","crooked","weeping"]); add("gtree",k,x,y,rng.uniform(.75,1.2),"scatter",2.2,solid=True); cnt['tree']+=1; continue
    if d>=3 and rng.random()<.03 and free(x,y,1.6): add("stump","stump",x,y,rng.uniform(.8,1.25),"scatter",1.1); cnt['stump']+=1; continue
    if d>=3 and rng.random()<.03 and free(x,y,1.4): add("grass","grass",x,y,rng.uniform(.5,.9),"scatter",.9); cnt['grass']+=1
# a few sea stacks just off the new W/S shore
for (x,y) in cand:
    xi,yi=int(x),int(y)
    if cnt['stack']>=9: break
    if inold(xi,yi) or T[yi][xi]!=WA: continue
    # water tile 2-4 tiles from land
    land=any(0<=xi+dx<W and 0<=yi+dy<H and not wet[yi+dy][xi+dx] for dx in range(-4,5) for dy in range(-4,5))
    close=any(0<=xi+dx<W and 0<=yi+dy<H and not wet[yi+dy][xi+dx] for dx in range(-1,2) for dy in range(-1,2))
    if land and not close and (xi<OX or yi>=OH) and free(x,y,6): add("seastack","stack",x,y,rng.uniform(.8,1.3),"sea",3); cnt['stack']+=1
# ---------- exits / points (old coords + offset) ----------
def off(p): return [round(p[0]+OX,2),round(p[1]+OY,2)]
exits=[
 dict(to="town",old=[12.5,1.2],new=off([12.5,1.2]),edge="N",rule="offset only; live exit x is 12.5 if exits_v2_coast is live (tile dump: road x10-13 at y0), else 20.2 -> 44.2. Apply x+ox to whatever is live.",alt_if_live_20_2=off([20.2,1.2])),
 dict(to="bastion",old=[40.4,14.2],new=[BAST[0],BAST[1]],edge="E",t=0.45,rule="MOVED to the new E edge at t=0.45 (P4). sx,sy (arrival in Bastion) unchanged."),
 dict(to="flotsam",old=[20.6,28.2],new=off([20.6,28.2]),rule="offset only (dock on the bridge)"),
]
sewer=dict(old=[36.6,19.8],new=off([36.6,19.8]))
intro=dict(old=[12.5,46.4],new=off([12.5,46.4]))
# enemy spawns (kinds from Xc: fu(...,[zombie,zombie,corpse,imp]) and qc(...,[zombie,corpse,imp]))
def snap(x,y):
    best=None
    for yy in range(H):
        for xx in range(W):
            if S[yy][xx]==0 and T[yy][xx] not in (WA,) and not inold(xx,yy) and not road[yy][xx]:
                d=math.hypot(xx+.5-x,yy+.5-y)
                if best is None or d<best[0]: best=(d,xx+.5,yy+.5)
    return [round(best[1],2),round(best[2],2)]
spawns=[dict(id="cv3_s1",kind="zombie",pack=["zombie","zombie","corpse"],pos=snap(81.0,22.0)),
        dict(id="cv3_s2",kind="imp",pack=["imp","imp","zombie"],pos=snap(84.5,64.0)),
        dict(id="cv3_s3",kind="corpse",pack=["corpse","zombie","zombie"],pos=snap(24.5,128.0)),
        dict(id="cv3_s4",kind="zombie",pack=["zombie","imp","corpse"],pos=snap(48.0,145.0))]
def snapany(x,y):
    best=None
    for yy in range(H):
        for xx in range(W):
            v=T[yy][xx] if T[yy][xx] is not None else oldv(xx,yy); s=S[yy][xx] if S[yy][xx] is not None else OS[yy-OY][xx-OX]
            if s==0 and v!=WA:
                d=math.hypot(xx+.5-x,yy+.5-y)
                if best is None or d<best[0]: best=(d,xx+.5,yy+.5)
    return [round(best[1],2),round(best[2],2)]
pois=[dict(id="E01",name="Cliff overlook above the sea",uv=[0.15,0.55],uv_point=[13.5,99.0],pos=[13.5,99.5],on="plateau P3 (W sea cliff)",kind="marker"),
      dict(id="SQ01_v2",name="Parish wells - variation 2",uv=[0.5,0.2],uv_point=[45.0,36.0],pos=snapany(45.0,36.0),kind="marker",note="uv point is old-map water; snapped to the nearest walkable tile (old Jc dirt corridor)"),
      dict(id="SQ14_v3",name="Tidebound coves & cairns - variation 3",uv=[0.2,0.85],uv_point=[18.0,153.0],pos=snapany(18.0,153.0),kind="marker",note="end of the south road at the SW cove")]
# ---------- encode ----------
B36="0123456789abcdefghijklmnopqrstuvwxyz"
rows=[''.join('.' if T[y][x] is None else B36[T[y][x]] for x in range(W)) for y in range(H)]
srows=[''.join('.' if S[y][x] is None else str(S[y][x]) for x in range(W)) for y in range(H)]
NAMES=["Grass","Grass2","Dirt","Sand","Sand2","Stone","Road","Plaza","Water","Bridge","Plank","Wall","Cave","Rug","Blood"]
from collections import Counter
cnew=Counter(T[y][x] for y in range(H) for x in range(W) if T[y][x] is not None and not inold(x,y))
cov=Counter(T[y][x] for y in range(H) for x in range(W) if T[y][x] is not None and inold(x,y))
# full merged (for checks/png)
MT=[[T[y][x] if T[y][x] is not None else oldv(x,y) for x in range(W)] for y in range(H)]
MS=[[S[y][x] if S[y][x] is not None else OS[y-OY][x-OX] for x in range(W)] for y in range(H)]
cfull=Counter(v for r in MT for v in r)
recipe=dict(
 patch_id="coast_v3_grow", target_world="coast", version=1,
 apply="AFTER the coast world is fully built (Xc carve+mirror+dress, applyAshenPatch, applyExitsPatch, NPCs, quests, spawns). Idempotent: world.coastV3 marker.",
 size=dict(old=[OW,OH],new=[W,H]), offset=dict(ox=OX,oy=OY,why="oy=0 keeps the Martsirt exit on the N edge. ox=24 puts 24 m of new land/sea W of the old map (new W sea + bays where the old W water strip meets it) and 24 m E (new road to the bastion exit on the new E edge). New S band y112-179 ends in the S sea."),
 encoding=dict(rows="H strings of W chars, row y, char x. Base-36 tile id: 0 Grass,1 Grass2,2 Dirt,3 Sand,4 Sand2,5 Stone,6 Road,7 Plaza,8 Water,9 Bridge,a Plank,b Wall,c Cave,d Rug,e Blood. '.' = KEEP the old tile copied from old (x-ox,y-oy). Only appears inside the old rect.",
   solid_rows="same layout, '0' walkable, '1' solid, '.' keep old solid", old_rect=[OX,OY,OX+OW-1,OY+OH-1],
   overrides="Any non-'.' char inside old_rect is an override and is written over the copied old tile."),
 tiles=rows, solid=srows,
 overrides=dict(north_entrance=dict(desc="Old N water block (Water x0-7 y0..~17) and Sand/Sand2/Stone in the north ~16 m converted to Grass/Grass2/Dirt with a noisy (non-straight) south edge. Roads, Plaza, Dirt and Bridge kept.",tiles=north_grass,region_old="x0-41, y0..13-19 (noisy)"),
   west_east_blend="No old tiles changed: every old W/E/S water tile on the old rect border is continued by new Water in a noisy blob (W: 9-18 m, merges with the new W sea; E: 3-8 m lagoon; S: 3-9 m), so there is no straight seam."),
 exits=exits, martsirt=dict(arrive_coast="Martsirt arrive.coast (martsirt_world.json) is the spot IN MARTSIRT; it is unchanged by this recipe ([53.8,150.9] per the bundle). What must change is the Martsirt->coast exit arrival in the coast: sx,sy = (12.5+ox, 4.0) = [36.5, 4.0] (was [12.5,4.0]); if the live coast town exit is still at x 20.2 use [44.2, 4.2].", coast_arrival_from_martsirt=[36.5,4.0]),
 bastion=dict(coast_exit=[BAST[0],BAST[1]],bastion_to_coast_arrival_new=[87.4,81.0],note="Bastion's exit {to:'coast'} sx,sy must be set to [87.4,81.0] (was [37.4,14.2]); move the BASTION arch prop from (40.4+ox,14.2) to the new exit."),
 sewer_stairs=sewer, intro_spawn=intro,
 road=dict(width_m=[4,6],polylines=dict(east=[[round(a,2),round(b,2)] for a,b in road_e[::12]],south=[[round(a,2),round(b,2)] for a,b in road_s[::12]],west=[[round(a,2),round(b,2)] for a,b in road_w[::12]]),note="Road tiles (6) are already in tiles[]; polylines are for minimap/AI hints only. East road starts at the old road end (old x41,y13-15)."),
 plateaus=[dict(p, ramp=list(p['ramp'])) for p in plateaus],
 plateau_note="Plateau rim tiles are solid Dirt dressed with shore rocks; height_m is optional (raise ground inside the rim if cheap, else flat).",
 props=props, camps=camps_out,
 spawns=spawns, spawn_kinds_source="Xc in the bundle: fu(e,t,7,[zombie,zombie,corpse,imp],...), qc(...,[zombie,corpse,imp])",
 pois=pois,
 stats=dict(tiles_new_area={NAMES[k]:v for k,v in sorted(cnew.items())}, overrides_in_old={NAMES[k]:v for k,v in sorted(cov.items())}, tiles_full_estimate={NAMES[k]:v for k,v in sorted(cfull.items())},
   props={k:v for k,v in cnt.items()}|{"camp_props":5*len(camps_out),"total":len(props)}, north_entrance_grass_tiles=north_grass),
 caveats=["Old rows 16-111 of the coast are reconstructed from the older live3.js generator; Sand/Sand2 noise is approximate, so tiles_full_estimate is an estimate. The recipe only writes over old tiles in rows 0-19 (rows 0-15 = verified dump; rows 16-19 only the Water strip x0-7 that Xc paints).",
   "The coast border layout (layout_coast_v2.json) is fitted to the 42x112 edge; see PROMPT_WP1 step for how to treat it."])
json.dump(recipe,open(os.path.join(HERE,'coast_v3_grow.json'),'w'),separators=(',',':'))
json.dump(dict(note="old 42x112 coast: rows 0-15 live dump, rest reconstructed",w=OW,h=OH,dump_rows=DUMPROWS,rows=[''.join(B36[v] for v in r) for r in OT],solid=[''.join(map(str,r)) for r in OS]),open(os.path.join(HERE,'old_coast_recon.json'),'w'))
print("ok props",len(props),cnt,"north_grass",north_grass,"spawns",[s['pos'] for s in spawns],"pois",[p['pos'] for p in pois])
