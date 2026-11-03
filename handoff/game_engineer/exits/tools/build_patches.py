import json
V=json.load(open('validate_tiles.json')); W0=json.load(open('world_full.json'))['worlds']
TN={0:'Grass',1:'Grass2',2:'Dirt',3:'Sand',4:'Sand2',5:'Stone',6:'Road',7:'Plaza',8:'Water',9:'Bridge',10:'Plank',11:'Wall',12:'Cave',13:'Rug',14:'Blood'}
def collapse(moves):
    out=[]
    for m in moves:
        for o in out:
            t=o['to']
            if o['match']['kind']==m['match']['kind'] and abs(t['x']-m['match']['x'])<.01 and abs(t['y']-m['match']['y'])<.01:
                o['to']=dict(t,x=m['to']['x'],y=m['to']['y']); o['why']+=' ; then '+m['why']; break
        else: out.append(json.loads(json.dumps(m)))
    for o in out:
        o['match']={k:(round(v,4) if isinstance(v,float) else v) for k,v in o['match'].items()}
    return out
SCHEMA=('live generated world object (sc(zone) in the routes bundle): w,h, tiles[] (row-major, i=y*w+x, enum Grass0 Grass2 1 Dirt2 Sand3 Sand2 4 Stone5 Road6 Plaza7 '
        'Water8 Bridge9 Plank10 Wall11 Cave12 Rug13 Blood14), solid[] (0/1), exits[{x,y,to,sx,sy}], props[{kind,x,y,style?,w?,...}]. tiles_set/solid_set rows = [x,y,old,new]: '
        'apply only if the current value == old (else warn and skip).')
APPLY=('applyExitsPatch(world, patch) from apply_exits_patch.js on the generated %s world, after the scene is built%s and before it is cached. Idempotent (world.exitsPatch marker).')
partner_arr={}
for z,extra in (('coast',' and AFTER applyAshenPatch (prop matches use post-Ashen positions)'),('wild',''),('desert',''),('mires','')):
    L=json.load(open('log_%s.json'%z)); ex=L['exits'][0]; rp=L['road_path'][0]
    partner_arr[ex['to']]=(z,ex)
    p=dict(patch_id='exits_v2_%s'%z,target_world=z,name=W0[z]['name'],apply=APPLY%(z,extra),schema=SCHEMA,
      match_rule='exits by "to"; props by {kind,x,y[,style]} with |dx|,|dy|<0.01; tiles/solid by [x,y] with old-value check',
      exits_set=[dict(match=dict(to=ex['to']),old=dict(x=ex['old']['x'],y=ex['old']['y']),new=dict(x=ex['new']['x'],y=ex['new']['y']),
                      sx_sy='unchanged (%s,%s)'%(ex['sx'],ex['sy']),edge=ex['edge'],why=ex['why'])],
      partner_arrival_in_this_zone=ex['partner_arrival_in_this_zone'],
      tiles_set=L['tiles_set'],solid_set=L['solid_set'],props_move=collapse(L['props_move']),props_add=L['props_add'],
      road_path=dict(to=rp['to'],centerline=rp['centerline'],gap=rp['gap'],old_gap_closed=rp['old_gap_closed'],road_tiles=rp['road_tiles'],pruned_stub_tiles=rp['pruned']),
      tile_names=TN,checks=V[z])
    if z=='coast':
        p['exits_set'][0]['sx_sy']='unchanged (19.8,31.6): legacy 2D-town value; the live Martsirt scene places arrivals from martsirt_world.json arrive.coast (see martsirt_exits_patch.json)'
        p['requires']=['martsirt_exits_patch.json (same release: the Martsirt side moves to its SW corner, x=49.6)']
        p['note_P4']='coast->bastion (E edge, 40.4,14.2) stays: the E side below y~20 is open sea on the current 42x112 coast; revisit when the coast grid grows (P4 deferred)'
    if z=='wild':
        p['note']='E branch x 37-71 on rows 25-29 reverts to grass (no longer leads anywhere) and the E ring gap at x 70-71 is closed with the ring tile + cloned mountains. Water tiles on rows 26-28 x 0-11 become Bridge (9, walkable): a 3-wide causeway. The body decor at (30,27) on the road has no collider (unchanged).'
    json.dump(p,open('out/%s_exits_patch.json'%z,'w'),indent=1)
# partners: sx/sy only
for b,(a,ex) in partner_arr.items():
    if b=='town': continue
    e=next(q for q in W0[b]['exits'] if q['to']==a); arr=ex['partner_arrival_in_this_zone']
    p=dict(patch_id='exits_v2_%s'%b,target_world=b,name=W0[b]['name'],apply=APPLY%(b,''),schema=SCHEMA,match_rule='exits by "to"',
      exits_set=[dict(match=dict(to=a),old=dict(x=e['x'],y=e['y'],sx=e['sx'],sy=e['sy']),new=dict(x=e['x'],y=e['y'],sx=arr['x'],sy=arr['y']),
                      why='%s moved its %s exit to (%s,%s); arrivals from here now land just inside it at (%s,%s). This zone\'s own exit tile, tiles and props are unchanged.'%(a,b,ex['new']['x'],ex['new']['y'],arr['x'],arr['y']))],
      tiles_set=[],solid_set=[],props_move=[],props_add=[])
    json.dump(p,open('out/%s_exits_patch.json'%b,'w'),indent=1)
print('ok')
