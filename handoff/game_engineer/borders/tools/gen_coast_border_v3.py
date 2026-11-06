#!/usr/bin/env python3
"""Ashen Coast border v3: props-only fake scenery fitted to the live 90x180 coast (after WP1).

Writes handoff/game_engineer/borders/ashen/layout_coast_v3.json (add-only; layout_coast_v2.json is untouched).
Run from the sanctuary-assets repo root:  python3 handoff/game_engineer/borders/tools/gen_coast_border_v3.py

Frame: tile metres, three.js x east / z south, map [0,90]x[0,180]. Coordinates are FINAL (no ox/oy offset, no skip).
Rules:
- Rim only: every prop sits OUTSIDE the map rectangle (x<0, x>90, z<0, z>180). Nothing on walkable tiles, no tiles changed.
- Land edges (N, E rows 0..158) get the dead-season land look the coast border already shows in game
  (winter gtrees, bare spires, crag stacks, stumps, dead grass). Sea edges (W, S, E below the shoreline)
  get shore rocks + sea stacks standing in the sea (pos y = -0.4, the sea plane, same as placeShore).
- Only assets the live border loader (GD) actually draws. GD drops every models/outdoor/v5_maps/border/* asset
  (border_peak/shelf/dune), so v3 uses none of them.
- Exits stay open: Martsirt N gate x=36.5 (clear |x-36.5|<6.5), Bastion E exit z=81 (clear |z-81|<6.5).
- Old v2 N-edge props near the Martsirt gate are carried over (+24 x) when they are drawable, outside the gate
  corridor, and pushed off walkable tiles, so the familiar north ridge stays. All other v2 props are dropped
  (their W/E/S edges are now interior sea or land).
- No colliders (blocks_walk false everywhere): the props are outside the map; the edge clamp follows world.w/world.h.
- Perf: spires capped at 6 (22.5k tris each), gtrees capped at 32 (~3.5k each).
"""
import json, math, os, random, hashlib

ROOT = os.getcwd()
H = 'handoff/game_engineer/'
W_, H_ = 90, 180
OX, OY = 24, 0
A = 'models/ashen_v1/'; C = 'models/env_extra/cliffkit_v2/'
GT = [A + 'gtree_twisted_winter_lod0.glb', A + 'gtree_crooked_winter_lod0.glb', A + 'gtree_weeping_winter_lod0.glb']
SPIRE = C + 'rock_spire_bare_16m_dead.glb'
STUMP = C + 'dead_stump_blighted_dead.glb'
GRASS = C + 'sway_dead_grass_patch_2m.glb'
ROCK_S = [A + 'shore_rock_a_boulder.glb', A + 'shore_rock_d_cluster.glb', A + 'shore_rock_b_slab.glb']
STACK = A + 'shore_rock_c_stack.glb'; SEASTACK = A + 'shore_rock_e_seastack.glb'
GATE_N = (36.5, 1.2); EXIT_E = (89.4, 81.0); FLOTSAM = (44.6, 28.2)
CLEAR = 6.5
SEA_Y = -0.4

def rng(*k):
    return random.Random(int(hashlib.md5('|'.join(map(str, k)).encode()).hexdigest()[:12], 16))

# ---- live map (old recon + WP1 recipe) ----
R = json.load(open(H + 'world_v1_coast/coast_v3_grow.json'))
O = json.load(open(H + 'world_v1_coast/old_coast_recon.json'))
T = [[None] * W_ for _ in range(H_)]; S = [[0] * W_ for _ in range(H_)]
for y in range(112):
    for x in range(42):
        T[y][x + OX] = int(O['rows'][y][x], 36); S[y][x + OX] = int(O['solid'][y][x])
for y in range(H_):
    for x in range(W_):
        c = R['tiles'][y][x]; s = R['solid'][y][x]
        if c != '.': T[y][x] = int(c, 36)
        if s != '.': S[y][x] = int(s)
def tile(x, y):
    xi = min(W_ - 1, max(0, int(math.floor(x)))); yi = min(H_ - 1, max(0, int(math.floor(y))))
    return T[yi][xi]
def water_edge(x, y): return tile(x, y) == 8

# east shoreline: first row (from the top) where the E edge column is water for good
E_SHORE = next(y for y in range(H_) if all(T[yy][W_ - 1] == 8 for yy in range(y, H_)))
N_SEA_END = next(x for x in range(W_) if T[0][x] != 8)   # N edge x < this is water (NW corner)

props = []; occ = []
def free(x, z, r):
    return all(math.hypot(x - a, z - b) >= r + c for a, b, c in occ)
def blocked_exit(x, z):
    if math.hypot(x - GATE_N[0], z - GATE_N[1]) < CLEAR + 4 and abs(x - GATE_N[0]) < CLEAR: return True
    if abs(z - EXIT_E[1]) < CLEAR and x > 84: return True
    if math.hypot(x - FLOTSAM[0], z - FLOTSAM[1]) < 6: return True
    return False
def inside(x, z): return 0 <= x <= W_ and 0 <= z <= H_
def add(pid, asset, layer, edge, x, z, sc, rot, rad, y=0.0, src='v3'):
    if inside(x, z) or blocked_exit(x, z) or not free(x, z, rad): return False
    props.append(dict(id=pid, asset=asset, layer=layer, edge=edge, pos=[round(x, 3), y, round(z, 3)],
                      rotY=round(rot, 4), scale=round(sc, 3), ground=('sea' if y < 0 else 'land'),
                      collider='none (outside map)', blocks_walk=False, src=src))
    occ.append((x, z, rad)); return True

# ---- 1. carry the v2 north ridge (offset +24) ----
V2 = json.load(open(H + 'borders/ashen/layout_coast_v2.json'))
carried = 0
for p in V2['props']:
    if p['edge'] != 'N' or 'v5_maps/border' in p['asset']: continue
    x = p['pos'][0] + OX; z = p['pos'][2] + OY
    if z > -0.4: z = -0.4 - (z + 0.4) * 0.5 - 0.3      # was on walkable row 0/1 -> just outside the edge
    pid = p['id']
    if add(pid, p['asset'], p['layer'], 'N', x, z, p['scale'], p['rotY'], 0.6 if 'grass' in p['asset'] else 1.0, src='v2_carry'):
        carried += 1
CARRY_X = (min(p['pos'][0] for p in props), max(p['pos'][0] for p in props)) if props else (0, 0)

# ---- 2. generated land rim (N and E) ----
caps = {'spire': 6, 'gtree': 32}
count = {'spire': sum('spire' in p['asset'] for p in props), 'gtree': sum('gtree' in p['asset'] for p in props)}
def pick(r, layer):
    u = r.random()
    if layer == 'lip':
        if u < .45: return 'grass', GRASS, r.uniform(.8, 1.3), .6
        if u < .72: return 'stump', STUMP, r.uniform(.9, 1.3), .9
        return 'rock', r.choice(ROCK_S[:2]), r.uniform(.8, 1.3), .9
    if layer == 'outer':
        if u < .50 and count['gtree'] < caps['gtree']: return 'gtree', r.choice(GT), r.uniform(.85, 1.25), 1.6
        if u < .80: return 'crag', STACK, r.uniform(1.2, 1.8), 1.3
        return 'rock', r.choice(ROCK_S), r.uniform(1.1, 1.6), 1.1
    # far
    if u < .14 and count['spire'] < caps['spire']: return 'spire', SPIRE, r.uniform(.34, .5), 2.4
    if u < .45 and count['gtree'] < caps['gtree']: return 'gtree', r.choice(GT), r.uniform(1.1, 1.5), 2.0
    if u < .80: return 'crag', SEASTACK, r.uniform(1.5, 2.3), 1.8
    return 'crag', STACK, r.uniform(1.6, 2.4), 1.6

LAYERS = [('far', (6.0, 11.0), (3.4, 5.4)), ('outer', (1.8, 5.0), (2.6, 4.0)), ('lip', (0.3, 1.5), (1.8, 3.2))]
def run_land(edge, t0, t1, skip=None):
    for layer, off, sp in LAYERS:
        r = rng('cb3', edge, layer, t0)
        t = t0 + r.uniform(0, sp[0])
        while t < t1:
            o = r.uniform(*off)
            if edge == 'N': x, z = t, -o
            else: x, z = W_ + o, t
            if not (skip and skip(t)):
                kind, asset, sc, rad = pick(r, layer)
                if add(kind, asset, layer, edge, x + r.uniform(-.4, .4), z + r.uniform(-.4, .4), sc, r.uniform(0, 2 * math.pi), rad * max(1, sc * .6)):
                    if kind in count: count[kind] += 1
            t += r.uniform(*sp)

# N: whole edge from the NW sea corner to past the NE corner, skipping the carried v2 span (it is already dressed)
run_land('N', N_SEA_END - 2, W_ + 11, skip=lambda t: CARRY_X[0] - 1 <= t <= CARRY_X[1] + 1)
# E: from above the NE corner down to the shoreline (+ a short land endcap into the sea corner)
run_land('E', -11, E_SHORE + 2)

# ---- 3. sea rim (W, S, E below the shoreline, NW corner) ----
def run_sea(edge, t0, t1):
    r = rng('cb3sea', edge, t0)
    for layer, off, sp in [('sea_far', (10, 26), (16, 30)), ('sea_lip', (1.0, 6.0), (6.0, 13.0))]:
        t = t0 + r.uniform(0, sp[0])
        while t < t1:
            o = r.uniform(*off)
            x, z = {'W': (-o, t), 'S': (t, H_ + o), 'E': (W_ + o, t), 'N': (t, -o)}[edge]
            if layer == 'sea_far': kind, asset, sc, rad = 'seastack', r.choice([SEASTACK, SEASTACK, STACK]), r.uniform(1.3, 2.2), 2.0
            else: kind, asset, sc, rad = 'shore_rock', r.choice(ROCK_S + [STACK]), r.uniform(.8, 1.6), 1.0
            add(kind, asset, layer, edge, x, z, sc, r.uniform(0, 2 * math.pi), rad, y=SEA_Y)
            t += r.uniform(*sp)
run_sea('W', -12, H_ + 12)
run_sea('S', -12, W_ + 12)
run_sea('E', E_SHORE + 3, H_ + 12)
run_sea('N', -12, N_SEA_END - 1)

# ---- checks ----
assert all(not inside(p['pos'][0], p['pos'][2]) for p in props), 'prop inside map'
assert all('v5_maps/border' not in p['asset'] for p in props)
for p in props: assert os.path.exists(p['asset']), p['asset']
def near(pt, d): return [p for p in props if math.hypot(p['pos'][0] - pt[0], p['pos'][2] - pt[1]) < d]
tris = {GT[0]: 3242, GT[1]: 3528, GT[2]: 3748, SPIRE: 22524, STUMP: 442, GRASS: 78, ROCK_S[0]: 576, ROCK_S[1]: 864, ROCK_S[2]: 576, STACK: 576, SEASTACK: 576}
by_asset = {}
for p in props: by_asset[p['asset'].split('/')[-1]] = by_asset.get(p['asset'].split('/')[-1], 0) + 1
by_edge = {}
for p in props: by_edge[p['edge']] = by_edge.get(p['edge'], 0) + 1
v2_drawn = [p for p in V2['props'] if 'v5_maps/border' not in p['asset']]
out = dict(
    zone='coast', size=[W_, H_], version=3,
    frame='tile metres; three.js x east, z south; map [0,90]x[0,180]. FINAL coordinates for the 90x180 coast: do NOT add ox/oy and do NOT skip by tile.',
    replaces='layout_coast_v2.json (42x112) for the coast once world.coastV3 is set. v2 stays in the repo for the old 42x112 path.',
    glb='props only (no kit pieces)',
    runs={'N': [['sea', 0, N_SEA_END], ['land', N_SEA_END, W_]], 'E': [['land', 0, E_SHORE], ['sea', E_SHORE, H_]], 'S': [['sea', 0, W_]], 'W': [['sea', 0, H_]]},
    exits_open={'town_N': list(GATE_N), 'bastion_E': list(EXIT_E), 'flotsam': list(FLOTSAM), 'clear_m': CLEAR},
    ground={'land': 'pos y 0 = ground; loader snaps to ground height minus a small bury', 'sea': 'pos y -0.4 = sea plane (placeShore uses the same)'},
    pieces=[], props=props,
    stats=dict(pieces=0, props=len(props), by_edge=by_edge, by_asset=by_asset, carried_from_v2_N=carried,
               v2_props_total=len(V2['props']), v2_props_drawn_by_GD=len(v2_drawn),
               tris_v3=sum(tris[p['asset']] for p in props), tris_v2_drawn=sum(tris.get(p['asset'], 600) for p in v2_drawn),
               spires=count['spire'], gtrees=count['gtree'], east_shoreline_row=E_SHORE, inside_map=0,
               props_within_6_5m_of_N_gate=len(near(GATE_N, CLEAR)), props_within_6_5m_of_E_exit=len(near(EXIT_E, CLEAR)),
               collider_changes=0, moved_world_props=0, tile_changes=0))
json.dump(out, open(H + 'borders/ashen/layout_coast_v3.json', 'w'), indent=1)
print(json.dumps(out['stats'], indent=1)); print('runs', out['runs'])
