#!/usr/bin/env python3
"""Reachability check + proof PNG for coast_v3_grow.json. Merges the recipe over old_coast_recon.json.
Walkable = solid 0 (Bridge counts, Water is solid). Every exit, sewer stairs, intro spawn, new spawn, POI and camp must sit in
the same 4-connected walkable component as the intro spawn. Writes coast_v3_proof.png (4 px per tile) and check_result.json."""
import json, os, sys
from collections import deque
from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__))
R=json.load(open(os.path.join(D,'coast_v3_grow.json'))); O=json.load(open(os.path.join(D,'old_coast_recon.json')))
W,H=R['size']['new']; ox,oy=R['offset']['ox'],R['offset']['oy']; OW,OH=R['size']['old']
assert len(R['tiles'])==H and all(len(r)==W for r in R['tiles']), "tile rows"
assert len(R['solid'])==H and all(len(r)==W for r in R['solid']), "solid rows"
def inold(x,y): return ox<=x<ox+OW and oy<=y<oy+OH
T=[[0]*W for _ in range(H)]; S=[[0]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        c=R['tiles'][y][x]; s=R['solid'][y][x]
        if c=='.': assert inold(x,y),("keep outside old rect",x,y); c=O['rows'][y-oy][x-ox]
        if s=='.': assert inold(x,y); s=O['solid'][y-oy][x-ox]
        T[y][x]=int(c,36); S[y][x]=int(s)
start=tuple(int(v) for v in R['intro_spawn']['new'])
seen=[[False]*W for _ in range(H)]; q=deque([start]); seen[start[1]][start[0]]=True
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        a,b=x+dx,y+dy
        if 0<=a<W and 0<=b<H and not seen[b][a] and S[b][a]==0: seen[b][a]=True; q.append((a,b))
pts=[("exit:"+e['to'],e['new']) for e in R['exits']]+[("sewer",R['sewer_stairs']['new']),("intro",R['intro_spawn']['new']),("martsirt_arrival",R['martsirt']['coast_arrival_from_martsirt']),("bastion_arrival",R['bastion']['bastion_to_coast_arrival_new'])]
pts+=[("spawn:"+s['id'],s['pos']) for s in R['spawns']]+[("poi:"+p['id'],p['pos']) for p in R['pois']]+[("camp",c) for c in R['camps']]
res=[]; ok=True
for n,p in pts:
    x,y=int(p[0]),int(p[1]); r=seen[y][x] and S[y][x]==0
    res.append(dict(name=n,pos=p,tile=T[y][x],walkable=S[y][x]==0,reachable=r)); ok&=r
walk=sum(1 for y in range(H) for x in range(W) if S[y][x]==0); reach=sum(1 for y in range(H) for x in range(W) if seen[y][x])
# props must not sit on Water/Road
badp=[p for p in R['props'] if T[int(p['pos'][2])][int(p['pos'][0])] in (6,) ]
out=dict(pass_=ok,walkable_tiles=walk,reachable_from_intro=reach,unreached_walkable=walk-reach,points=res,props_on_road=len(badp))
json.dump(out,open(os.path.join(D,'check_result.json'),'w'),indent=1)
for r in res: print(("OK  " if r['reachable'] else "FAIL"),r['name'],r['pos'],'tile',r['tile'])
print("walkable",walk,"reachable",reach,"unreached pockets",walk-reach,"props_on_road",len(badp))
# ---- PNG
C={0:(78,86,62),1:(96,100,74),2:(104,90,70),3:(150,140,118),4:(128,120,100),5:(110,110,112),6:(70,62,56),7:(120,112,100),8:(34,48,62),9:(120,90,60),10:(110,85,60),11:(40,40,40),12:(30,30,30),13:(90,30,30),14:(110,20,20)}
K=4; im=Image.new('RGB',(W*K,H*K)); d=ImageDraw.Draw(im)
for y in range(H):
    for x in range(W):
        c=C[T[y][x]]
        if S[y][x] and T[y][x]!=8: c=tuple(int(v*.6) for v in c)
        if S[y][x]==0 and not seen[y][x]: c=(c[0]//2+80,c[1]//2,c[2]//2)
        d.rectangle([x*K,y*K,x*K+K-1,y*K+K-1],fill=c)
d.rectangle([ox*K,oy*K,(ox+OW)*K-1,(oy+OH)*K-1],outline=(255,255,255))
for poly in R['road']['polylines'].values():
    d.line([(a*K,b*K) for a,b in poly],fill=(230,200,90),width=1)
col={'gtree':(20,30,15),'stump':(60,40,25),'shore_rock':(170,170,175),'seastack':(200,200,205),'grass':(140,140,90)}
for p in R['props']:
    x,y=p['pos'][0]*K,p['pos'][2]*K; c=col.get(p['id'],(255,120,0))
    d.ellipse([x-1.5,y-1.5,x+1.5,y+1.5],fill=c)
for n,p in pts:
    x,y=p[0]*K,p[1]*K
    c=(255,60,60) if n.startswith('exit') else (60,160,255) if n.startswith('spawn') else (255,0,255) if n.startswith('poi') else (255,140,0) if n=='camp' else (255,255,0)
    d.ellipse([x-4,y-4,x+4,y+4],outline=c,width=2)
im.save(os.path.join(D,'coast_v3_proof.png'))
sys.exit(0 if ok else 1)
