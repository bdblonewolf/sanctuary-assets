import json,copy,math,numpy as np
from PIL import Image
from mts_exit import TRAIL,CTRL,WIDTH,NEW_EXIT,ARRIVE,checks,M,OX,OY
MD='/workspace/sanctuary_env/martsirt_v2_2/'
SPLAT='/workspace/sanctuary-assets/models/town/ground_v1/martsirt_splat.png'
old=next(e for e in M['exits'] if e['to']=='coast')
NEW_SX,NEW_SY=12.5,4.0
local=[[round(x-OX,2),round(y-OY,2)] for x,y in CTRL]
road=dict(label='coast trail: south gate - SW to the coast road',width_m=WIDTH,points=local,surface='dirt trail',
          note='exits_v2: leaves the gatehouse mouth, bears west under the palisade (3+ m off the wall, 3+ m off the map edge) and meets the S edge at x=49.6 where the coast road arrives')
# ---- splat v2 (r = dirt trail), only outside cobble
im=np.array(Image.open(SPLAT).convert('RGB')).astype(float)/255; Hp,Wp,_=im.shape; ppm=4
P=np.array(TRAIL); ys,xs=np.mgrid[0:Hp,0:Wp]; wx=(xs+.5)/ppm; wy=(ys+.5)/ppm
box=(wx>P[:,0].min()-4)&(wx<P[:,0].max()+4)&(wy>P[:,1].min()-4)
d=np.full((Hp,Wp),99.)
for (ax,ay),(bx,by) in zip(P,P[1:]):
    vx,vy=bx-ax,by-ay;L2=vx*vx+vy*vy or 1e-9
    t=np.clip(((wx-ax)*vx+(wy-ay)*vy)/L2,0,1);dd=np.hypot(wx-(ax+t*vx),wy-(ay+t*vy));d=np.minimum(d,np.where(box,dd,99))
rng=np.random.default_rng(7);noise=rng.random((Hp,Wp))*.35
core=WIDTH/2-.4; v=np.clip((WIDTH/2+.5-d-noise*(d>core))/(.9),0,1)*.92
r,g,b=im[...,0],im[...,1],im[...,2]
paint=(v>0)&(g<.5)
nr=np.where(paint,np.maximum(r,v),r); s=nr+g+b; over=paint&(s>1)
k=np.where(over,np.clip((1-nr)/np.maximum(g+b,1e-6),0,1),1); g2=g*k; b2=b*k
out=np.stack([nr,g2,b2],-1)
Image.fromarray((out*255+.5).astype(np.uint8)).save('out/martsirt_splat_v2.png')
changed=int(((np.abs(out-im)*255)>1).any(-1).sum())
chk=checks()
patch=dict(patch_id='exits_v2_martsirt',target_world='martsirt_world.json (Martsirt v2.2, 162x154, origin [81,76])',
 name='Martsirt: coast exit moves off the centre line to the SW trail',
 apply='Edit martsirt_world.json exits[to=coast] and arrive.coast as below; append roads_add to placements.json header.v2.roads; '
       'add the road class to models/town/ground_v1/manifest.json road_classes; swap martsirt_splat.png for martsirt_splat_v2.png (same size/format, r channel = trail). '
       'Border: use borders/martsirt/layout_martsirt_v2.json (pass12 moved to the new exit). Seam: seams/coast__martsirt_v2.json. Idempotent: match exits by to=="coast".',
 schema='live martsirt_world.json exits:[{x,y,to,sx,sy,label}], arrive:{zone:[x,y]} (tile metres = town-local + origin)',
 requires=['coast_exits_patch.json (the coast side moves to x=12.5 on its N edge in the same release)'],
 match_rule=dict(exits='to == "coast"',arrive='key "coast"'),
 exits_set=[dict(match=dict(to='coast'),old=dict(x=old['x'],y=old['y'],sx=old['sx'],sy=old['sy'],label=old.get('label')),
   new=dict(x=NEW_EXIT['x'],y=NEW_EXIT['y'],sx=NEW_SX,sy=NEW_SY,label=old.get('label')),
   why='Leaving town you still walk out through the south gatehouse (the "ACT I" gate keeps its label and its camp), but the road no longer runs dead-straight '
       'down the centre line to the map edge: a dirt trail bears west under the palisade to the SW corner, which is where the coast road climbs in '
       '(continent: the coast lies south-west). The gate camp east of the gate stays a stop on the way, not a wall in the way.')],
 arrive_set=dict(coast=dict(old=M['arrive']['coast'],new=ARRIVE,why='arrive on the trail 4 m inside the exit, facing east along the palisade toward the gate (Ilyra stays at the gate, 84,136)')),
 roads_add=[road],
 manifest_road_classes_add={road['label']:['dirt trail',WIDTH]},
 splat=dict(file='exits/martsirt/martsirt_splat_v2.png',replaces='models/town/ground_v1/martsirt_splat.png',size_px=[Wp,Hp],changed_px=changed,
            rule='r = max(r, trail); g,b scaled down only where r+g+b>1; cobble (g>=0.5, the gate mouth) untouched'),
 solid_set=[],solid_note='trail runs on open ground; no solid or water bit changes',
 props_move=[],props_note='no placements move. dressLife gate camp (campfire 84.2,150.6, fence 86,150.8, crates/barrels) is east of the trail; nearest 3.6 m',
 north_exit=dict(to='wild',kept=True,why='north gap west of the watch-house already sits off-centre (76.2 of 162) and the north high road bends into it; it reads naturally'),
 alternative_B=dict(status='NOT the default; flagged only',idea='a west postern at the end of the mill lane (local -50.9,27.4), out through the west palisade, then a trail south to the SW corner',
   cost='needs one palisade segment removed/turned into a postern (placements change) and a 50 m trail; the gate story ("ACT I") would move off the gatehouse',
   why_not='more invasive than needed; the south gate is the town\'s front door'),
 checks=chk,
 continent_note='continent_layout places coast flush S of Martsirt with exits coinciding: coast x0 shifts from 60.8 to 37.1 (Martsirt frame); still clear of all other rects (see EXITS.md)')
json.dump(patch,open('out/martsirt_exits_patch.json','w'),indent=1)
# ---- v2 inputs for generators
mw=copy.deepcopy(json.load(open(MD+'martsirt_world.json')))
e=next(e for e in mw['exits'] if e['to']=='coast'); e['x'],e['y'],e['sx'],e['sy']=NEW_EXIT['x'],NEW_EXIT['y'],NEW_SX,NEW_SY
mw['arrive']['coast']=ARRIVE; json.dump(mw,open('v2in/martsirt_world_v2.json','w'))
pl=json.load(open(MD+'placements.json')); pl['header']['v2']['roads'].append(dict(road,tight_clear=True)); json.dump(pl,open('v2in/placements_v2.json','w'))
print(json.dumps(chk),changed)
