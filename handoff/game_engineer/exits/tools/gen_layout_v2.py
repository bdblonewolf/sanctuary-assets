# exits_v2 (pt101u) text copy of continent/gen_layout.py
"""Continent layout v1 (PLAN). Places every outdoor zone at its LATER size (<=400 m) on a 4.5 x 4.5 km sheet by
walking the live exit graph: each seam puts the neighbour flush against the shared edge with the exit offset kept
proportional, so the layout and seams/ agree. x = east, y = south (same as tile frames), metres, 1 tile = 1 m."""
import json, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, '/workspace/sanctuary_env/world_v1/continent')
AUD = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/worlds_v2.json'))
ELEV = json.load(open('/workspace/sanctuary_env/world_v1/exits/v2/terrain/elevation_table.json'))
SHEET = 4500
# now = live tile grid, later = planned tile grid (1 m tiles), style = border style
Z = {  # id: (later w, h, style, role)
 'town':   (240, 220, 'town', 'hub town (Martsirt)'),
 'coast':  (180, 360, 'coast_land', 'coast road, sea W/S'),
 'flotsam':(180, 140, 'coast_land', 'wreck shore across the bay (boat)'),
 'hollow': (140, 110, 'coast_land', 'smuggler cove'),
 'bastion':(220, 180, 'mountain', 'coast road climbs (switchbacks)'),
 'bluffs': (320, 260, 'mountain', 'cliff plateaus'),
 'mires':  (300, 260, 'forest', 'high bog shelf'),
 'sink':   (150, 130, 'mountain', 'sinkhole (stair down)'),
 'ridge':  (260, 360, 'mountain', 'switchback ridge'),
 'ascent': (240, 260, 'mountain', 'hairpin climb'),
 'crypts': (220, 200, 'mountain', 'sunken crypt shelf'),
 'chasm':  (180, 220, 'mountain', 'flooded gorge'),
 'iron':   (340, 180, 'mountain', 'Iron Bastion pass'),
 'gaol':   (220, 300, 'mountain', 'Inquisitor plateau'),
 'weald':  (380, 340, 'mountain', 'Obsidian Spires summit plateau'),
 'wild':   (400, 320, 'forest', 'Briarwood'),
 'briarE': (360, 260, 'forest', 'Briarwood East (falls toward The Narrow)'),
 'duneW':  (260, 120, 'desert', 'The Narrow (pass, drop into the basin)'),
 'desert': (400, 380, 'desert', 'desert basin'),
 'lut':    (240, 220, 'desert', 'Qadren'),
 'market': (320, 260, 'desert', 'Highmarket'),
 'waste':  (400, 360, 'desert', 'Cinder Barrens'),
 'isle':   (400, 340, 'coast_land', 'Blackwater (island, boat only)'),
}
NRM = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
SIDE_OF = {(0, -1): 'N', (1, 0): 'E', (0, 1): 'S', (-1, 0): 'W'}
def R(k, v):
    for _ in range(k % 4): v = (-v[1], v[0])   # +90 (x east, y south: clockwise on the map)
    return v
def edge_and_t(z, x, y):
    w, h = AUD[z]['w'], AUD[z]['h']
    if z == 'coast': h = 112
    d = {'N': y, 'S': h - y, 'W': x, 'E': w - x}; e = min(d, key=d.get)
    t = {'N': x / w, 'S': x / w, 'E': y / h, 'W': y / h}[e]
    return e, t, d[e]
# graph edges (zone, exit-to, edge, t); proposals override live edges
EDGES = {}
for z in Z:
    if z not in AUD: continue
    for ex in AUD[z]['exits']:
        if ex['to'] in Z: EDGES[(z, ex['to'])] = edge_and_t(z, ex['x'], ex['y'])
PROPOSALS = [
 dict(id='P1', change="wild: move the briarE exit from the E edge (70.4,27.2) to the W edge (1.4,27.2) so the west road runs west into The Narrow and the desert basin (mountains stay east). briarE..waste chain is placed rotated 180 deg; their own exits do not move.",
      edge=('wild', 'briarE'), new=('W', 27.2 / 56)),
 dict(id='P2', change="desert->lut exit (27.4,5.6) is 5.6 m inside the N edge; treated as an N-edge seam (move to y=1.2 when the zone is rebuilt).", edge=('desert', 'lut'), new=('N', 27.4 / 36)),
 dict(id='P4', change="coast later grid: the bastion exit sits at t=0.45 of the E edge (live 14.2/112 = 0.13 would push Bastion into Martsirt once both grow).", edge=('coast', 'bastion'), new=('E', 0.45)),
 dict(id='P3', change="mires->sink is a stair/drop inside mires (9.2,15.2); sink is laid flush to the mires W edge 6 m below (cliff), no road seam.", edge=('mires', 'sink'), new=('W', 15.2 / 34)),
]
PROPOSALS = [p for p in PROPOSALS if p['id'] == 'P4']  # exits_v2: P1-P3 are now live exits (worlds_v2); P4 deferred
for p in PROPOSALS: EDGES[p['edge']] = (p['new'][0], p['new'][1], 0)
rot = {'town': 0}; pos = {'town': (2050, 1600)}
order = ['town']; done = {'town'}
SKIP = {('coast', 'flotsam'), ('flotsam', 'coast')}  # boat link, placed by hand
while order:
    a = order.pop(0)
    for (z, b), (ea, ta, _) in list(EDGES.items()):
        if z != a or b in done or (a, b) in SKIP: continue
        eb, tb = (EDGES[(b, a)][0], EDGES[(b, a)][1]) if (b, a) in EDGES else ({'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[ea], 0.5)
        if (a, b) == ('mires', 'sink'): eb, tb = 'E', 0.5
        na = R(rot[a], NRM[ea]); nb_local = NRM[eb]
        k = next(k for k in range(4) if R(k, nb_local) == (-na[0], -na[1]))
        rot[b] = k
        # exit point of a in continent coords
        def world_pt(z, e, t, rz, pz):
            w, h = Z[z][0], Z[z][1]
            lp = {'N': (t * w, 0), 'S': (t * w, h), 'W': (0, t * h), 'E': (w, t * h)}[e]
            c = (w / 2, h / 2); v = R(rz, (lp[0] - c[0], lp[1] - c[1]))
            return pz[0] + v[0], pz[1] + v[1]
        pa = world_pt(a, ea, ta, rot[a], pos[a])
        w, h = Z[b][0], Z[b][1]
        lp = {'N': (tb * w, 0), 'S': (tb * w, h), 'W': (0, tb * h), 'E': (w, tb * h)}[eb]
        v = R(k, (lp[0] - w / 2, lp[1] - h / 2))
        pos[b] = (pa[0] - v[0], pa[1] - v[1]); done.add(b); order.append(b)
# boat links / island
pos['flotsam'] = (pos['coast'][0] - 620, pos['coast'][1] + 40); rot['flotsam'] = 0
# hollow follows flotsam S
pos['hollow'] = (pos['flotsam'][0] + 0, pos['flotsam'][1] + 140 / 2 + 110 / 2); rot['hollow'] = 0
pos['isle'] = (pos['coast'][0] - 900, pos['coast'][1] + 900); rot['isle'] = 0
def rect(z):
    w, h = Z[z][0], Z[z][1]
    if rot[z] % 2: w, h = h, w
    cx, cy = pos[z]; return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
NEW = {
 'n_tidecoves': ('coast', 'W', 0.78, 240, 200, 'coast_land', 'Tidebound leeward coves + tidal caves (night coves)', 0.3),
 'n_hollowridge': ('hollow', 'S', 0.5, 220, 140, 'coast_land', 'Hollow smuggler ridge path + cove', 3),
 'n_tollgorge': ('bluffs', 'N', 0.35, 300, 200, 'mountain', 'Toll bridges + undercrofts (gorge on the bluffs road)', 18),
 'n_manor_bluffs': ('mires', 'S', 0.25, 220, 180, 'mountain', 'Gothic manor (Mourning Bluffs) explore-only', 22),
 'n_quarantine': ('gaol', 'W', 0.5, 240, 220, 'mountain', 'Inquisition quarantine village', 64),
 'n_citadel': ('iron', 'E', 0.5, 340, 320, 'mountain', 'Open Eye citadel outer wards + drainage grates', 62),
 'n_ruin': ('weald', 'E', 0.3, 180, 180, 'mountain', 'Single untouched-cache ruin (far off-road)', 80),
 'n_sinkholes': ('wild', 'N', 0.3, 300, 240, 'forest', 'Survivor sinkhole shrines', 10),
 'n_manor_briar': ('briarE', 'N', 0.5, 220, 180, 'forest', 'Gothic manor (Briarwood) explore-only', 13),
 'n_burn': ('waste', 'N', 0.5, 320, 260, 'desert', 'Ashen Covenant burn-circles', 8),
 'n_ashcamp': ('market', 'S', 0.5, 280, 220, 'desert', 'Ash-camp of the Touched', 3),
 'n_oasis': ('desert', 'N', 0.6, 160, 160, 'desert', 'Hidden oasis - NO road, secret quest', -2),
 'n_manor_coast': ('town', 'W', 0.7, 200, 180, 'coast_land', 'Gothic manor (sea cliff W of Martsirt) explore-only', 6),
}
GAP = {'n_oasis': 140, 'n_ruin': 160}
for n, (anc, side, t, w, h, st, role, base) in NEW.items():
    r = rect(anc); g = GAP.get(n, 0)
    if side == 'W': c = (r[0] - w / 2 - g, r[1] + t * (r[3] - r[1]))
    if side == 'E': c = (r[2] + w / 2 + g, r[1] + t * (r[3] - r[1]))
    if side == 'N': c = (r[0] + t * (r[2] - r[0]), r[1] - h / 2 - g)
    if side == 'S': c = (r[0] + t * (r[2] - r[0]), r[3] + h / 2 + g)
    Z[n] = (w, h, st, role); pos[n] = c; rot[n] = 0
def overlap(r1, r2):
    return max(0, min(r1[2], r2[2]) - max(r1[0], r2[0])) * max(0, min(r1[3], r2[3]) - max(r1[1], r2[1]))
over = []
names = list(pos)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        o = overlap(rect(names[i]), rect(names[j]))
        if o > 1: over.append((names[i], names[j], round(o)))
# shift whole map to fit sheet with 500 m margin
xs = [rect(z) for z in pos]; minx = min(r[0] for r in xs); miny = min(r[1] for r in xs); maxx = max(r[2] for r in xs); maxy = max(r[3] for r in xs)
dx = (SHEET - (maxx - minx)) / 2 - minx; dy = (SHEET - (maxy - miny)) / 2 - miny
for z in pos: pos[z] = (pos[z][0] + dx, pos[z][1] + dy)
now_area = sum((112 * 42 if z == 'coast' else AUD[z]['w'] * AUD[z]['h']) for z in Z if z in AUD)
later_area = sum(Z[z][0] * Z[z][1] for z in Z)
AUD_OUT = [z for z in Z if z in AUD]
out = dict(version='continent_layout_v1+exits_v2', status='PLAN - nothing built; HOLD for Brian', sheet_m=[SHEET, SHEET], total_km2=SHEET * SHEET / 1e6,
           frame='x east, y south, metres; zone rect = [x0,y0,x1,y1]; rot = quarter turns clockwise of the zone tile frame',
           proposals=PROPOSALS, overlaps=over,
           zones={z: dict(name=AUD[z]['name'] if z in AUD else Z[z][3].split(' (')[0], status='live' if z in AUD else 'NEW - HOLD for Brian', style=Z[z][2], role=Z[z][3], now_grid=([AUD[z]['w'], 112 if z == 'coast' else AUD[z]['h']] if z in AUD else None), later_grid=[Z[z][0], Z[z][1]],
                          rot=rot[z], center=[round(pos[z][0], 1), round(pos[z][1], 1)], rect=[round(v, 1) for v in rect(z)],
                          base_m=ELEV['base_m'].get(z, NEW.get(z, [0]*8)[7]), relief_m=ELEV['relief_m'].get(z)) for z in Z},
           area=dict(now_walkable_km2=round(now_area / 1e6, 3), later_walkable_km2=round(later_area / 1e6, 3), zones_now=len(AUD_OUT), zones_later=len(Z)))
json.dump(out, open(os.path.join(HERE, 'continent_layout_core_v2.json'), 'w'), indent=1)
print('overlaps', over); print(out['area'])
for z in Z: print(z, out['zones'][z]['rect'], rot[z])
