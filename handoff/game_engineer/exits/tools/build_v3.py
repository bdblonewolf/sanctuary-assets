"""exits_v3: mirror the west-road wilderness zones (briarE, duneW, desert) left<->right so the unrotated in-game chart
reads  wild <-W- briarE <-W- duneW <-W- desert, with every exit on the edge that faces its neighbour.
Writes out_v3/<zone>_exits_patch_v3.json for briarE, duneW, desert (mirror) and wild, lut (arrival sx/sy only).
v3 patches REPLACE the v2 patch of the same zone (they contain the v2 ops, then the mirror)."""
import json, copy
W = json.load(open('world_full.json'))['worlds']
MIR = ['briarE', 'duneW', 'desert']
r2 = lambda v: round(v + 0.0, 4)
def v2(z):
    try: return json.load(open('out/%s_exits_patch.json' % z))
    except FileNotFoundError: return None
# exits after the v2 patches (x,y,sx,sy), by zone and target
EX = {}
for z in ['wild', 'briarE', 'duneW', 'desert', 'lut']:
    ex = {e['to']: dict(e) for e in copy.deepcopy(W[z]['exits'])}
    p = v2(z)
    for s in (p or {}).get('exits_set', []):
        ex[s['match']['to']].update({k: v for k, v in s['new'].items() if k in ('x', 'y', 'sx', 'sy')})
    EX[z] = ex
def edge(z, x, y):
    w, h = W[z]['w'], W[z]['h']; d = {'N': y, 'S': h - y, 'W': x, 'E': w - x}; return min(d, key=d.get)
FINAL = {}
for z, ex in EX.items():
    fin = []
    for to, e in ex.items():
        x, y, sx, sy = e['x'], e['y'], e.get('sx'), e.get('sy')
        if z in MIR: x = r2(W[z]['w'] - x)
        if to in MIR and sx is not None: sx = r2(W[to]['w'] - sx)
        if (x, y, sx, sy) != (e['x'], e['y'], e.get('sx'), e.get('sy')) or z in MIR:
            fin.append(dict(to=to, x=x, y=y, sx=sx, sy=sy, edge=edge(z, x, y), was=dict(x=e['x'], y=e['y'], sx=e.get('sx'), sy=e.get('sy'), edge=edge(z, e['x'], e['y']))))
    FINAL[z] = fin
WHY = {
 'briarE': 'Mirrored left<->right. Briarwood (wild) is EAST of here: the BRIARWOOD arch and the wild exit are now on the E edge (50.6,20.2), and you arrive from wild just inside it at (48.6,20.4). The Narrow (duneW) exit and its arch are on the W edge (2.6,20.2). The ridge road, trees, tomb and bonfire are the same layout, mirrored.',
 'duneW': 'Mirrored left<->right. Briarwood East is EAST of here (exit E edge (26.8,8.2)); the desert is WEST (exit W edge (1.8,8.2)). Arches, shrine and dunes follow.',
 'desert': 'v2 ops (lut road cut through the N ridge) then mirrored left<->right. The Narrow (duneW) is EAST of here (exit E edge (34.8,14.2)); Qadren (lut) stays NORTH (exit N edge, now (8.6,0.6)). Lut is not mirrored: its S gate already faces the desert.',
 'wild': 'Same as exits_v2_wild (W-edge causeway exit to briarE) except the arrival: briarE is mirrored, so you land just inside its E edge (48.6,20.4).',
 'lut': "Same as exits_v2_lut except the arrival: the desert is mirrored, so leaving Qadren's S gate lands just inside the desert's N-edge cut at (8.6,3.4).",
}
for z in ['briarE', 'duneW', 'desert', 'wild', 'lut']:
    base = v2(z) or dict(patch_id=None, target_world=z, name=W[z]['name'], schema=v2('briarE')['schema'], tiles_set=[], solid_set=[], props_move=[], props_add=[], exits_set=[])
    p = copy.deepcopy(base)
    p['patch_id'] = 'exits_v3_' + z; p['replaces'] = base['patch_id'] or 'none (no v2 patch for this zone)'
    p['apply'] = ('applyExitsPatch(world, patch) from apply_exits_patch.js (v3: supports mirror_x + exits_final) on the generated %s world, after the scene is built and before it is cached. '
                  'Use INSTEAD of the v2 patch for this zone (v3 contains the v2 ops). Order inside the function: tiles_set, solid_set, exits_set, props_move, props_add (all in the original unmirrored frame), then mirror_x, then exits_final. Idempotent (world.exitsPatch marker).' % z)
    if z in MIR:
        p['mirror_x'] = dict(expect_w=W[z]['w'], expect_h=W[z]['h'], rule='x -> w - x for every point (props, npcs, spawn, lights, nests, exits ...); tile rows reversed; face-e <-> face-w; rotY -> -rotY')
        if z == 'briarE':  # v2 exits_set for briarE only changed the wild arrival, now carried by exits_final
            p['exits_set'] = []
    p['exits_final'] = FINAL[z]
    p['why_v3'] = WHY[z]
    p['chart'] = dict(rule='in-game chart (Od/cardinalExits: nearest edge of the exit, no rotation) places the target on the side the exit is on',
                      exits={e['to']: e['edge'] for e in FINAL[z]} if FINAL[z] else None)
    json.dump(p, open('out_v3/%s_exits_patch_v3.json' % z, 'w'), indent=1)
    print(z, [(e['to'], e['edge'], e['x'], e['y'], e['sx'], e['sy'], 'was', e['was']) for e in FINAL[z]])
