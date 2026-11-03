# exits_v2 (pt101u) text copy of terrain/gen_terrain.py: same algorithm, inputs = worlds after the exits_v2 patches; outputs *_v2 in a separate dir. Originals untouched.
"""world_v1 terrain generator (planning data only; nothing live reads it yet).
python3 gen_terrain.py  -> terrain/<zone>.json + terrain/elevation_table.json + previews/<zone>.png
Height model (Skyrim-like, data-driven):
  * every zone has a base elevation from the continent elevation table; each seam has ONE shared height
    (mean of both zones' bases) so both sides of an exit meet exactly.
  * road tiles: height = geodesic (along-road) blend between exit seam heights, then slope-limited to
    ROAD_MAX_DEG by iterative relaxation; if a zone's climb is longer than its roads allow it is flagged
    'needs_switchback' with the extra road length required.
  * off-road: harmonic fill from roads + terraced low-frequency noise -> plateaus (flat steps) and cliff
    edges (corner delta > CLIFF_DH over 1 m). Terraces are only applied >= ROAD_CLEAR tiles from any road, so
    terrain can never cut or block a road; a 2-tile shoulder around roads copies road height.
  * water tiles: surface -0.4 (engine ocean), bed -1.2.
  * corner heights (w+1)x(h+1) = mean of the 4 touching tile-centre heights => engine samples bilinearly.
"""
import json, math, os, sys, collections, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))  # outputs <zone>.json here; staged as <zone>_v2.json
AUD = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/worlds_v2.json'))
EXT = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/world_extract_v2.json'))['worlds']
COAST = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/coast_world_after_v2.json'))
ROAD_MAX_DEG = 14.0      # design target for roads/ramps (walkable limit is 30)
WALK_MAX_DEG = 30.0
CLIFF_DH = 1.2           # corner delta per 1 m above this = cliff/drop edge (~50 deg)
ROAD_CLEAR = 3
# base elevation (m) - hub Martsirt kept flat at 0 (no building offsets); west road climbs to The Narrow then drops to the desert basin;
# coast road climbs into the mountains.
BASE = dict(town=0.0, coast=0.0, flotsam=0.6, hollow=0.4, wild=6, briarE=12, duneW=6, desert=1.5, lut=2, market=2.5,
            waste=7, bastion=8, bluffs=17, mires=25, sink=19, ridge=38, ascent=52, crypts=47, chasm=36, iron=60,
            gaol=67, weald=72, isle=2)
RELIEF = dict(town=0.0, coast=0.0, flotsam=1.0, hollow=1.0, wild=5, briarE=7, duneW=4, desert=3, lut=2, market=1.5,
              waste=6, bastion=4, bluffs=7, mires=2, sink=5, ridge=9, ascent=9, crypts=6, chasm=8, iron=6,
              gaol=6, weald=6, isle=6)
ROLE = dict(town='hub', coast='coast', flotsam='coast', hollow='cove', wild='forest', briarE='forest ridge (approach to The Narrow)',
            duneW='The Narrow (pass, drops into the basin)', desert='basin', lut='basin', market='basin town', waste='ash country',
            bastion='coast climb', bluffs='switchbacks', mires='high marsh plateau', sink='sinkhole', ridge='ridge switchbacks',
            ascent='mountain plateau', crypts='cliff shelf', chasm='gorge', iron='mountain pass', gaol='high pass',
            weald='high forest plateau', isle='island')
Q = dict(water={8}, road={6, 9, 10, 7}, path={2})       # live enum (coast_world_after)
U = dict(water={4}, road={3, 5, 13, 12}, path={2})      # extract enum (U)

# seams that must not lift the A0 coast: the higher zone does the whole climb inside its own bounds
SEAM_OVERRIDE = {frozenset(('town', 'wild')): 0.0, frozenset(('coast', 'town')): 0.0, frozenset(('coast', 'bastion')): 0.0, frozenset(('coast', 'flotsam')): 0.0}
def seam_h(a, b): return SEAM_OVERRIDE.get(frozenset((a, b)), round((BASE[a] + BASE[b]) / 2, 2))
def water_level(z): return -0.4 if BASE[z] <= 2 else BASE[z] - 0.4

def zone_tiles(z):
    if z == 'coast': return COAST['w'], COAST['h'], COAST['tiles'], Q, COAST['exits']
    e = EXT[z]; return e['w'], e['h'], e['tiles'], U, AUD[z]['exits']

def martsirt_tiles():
    w, h = 162, 154
    hdr = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/martsirt_world_v2.json'))
    ox, oz = hdr['origin']; T = np.zeros((h, w), int)
    roads = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/placements_v2.json'))['header']['v2']['roads']
    for r in roads:
        pts = r['points']; wd = r['width_m'] / 2
        for (a, b) in zip(pts, pts[1:]):
            ax, az = a[0] + ox, a[1] + oz; bx, bz = b[0] + ox, b[1] + oz
            n = int(max(abs(bx - ax), abs(bz - az)) * 2) + 1
            for i in range(n + 1):
                x = ax + (bx - ax) * i / n; zz = az + (bz - az) * i / n
                for yy in range(int(zz - wd), int(zz + wd) + 1):
                    for xx in range(int(x - wd), int(x + wd) + 1):
                        if 0 <= xx < w and 0 <= yy < h: T[yy, xx] = 3
    return w, h, T.ravel().tolist(), U, AUD['town']['exits']

def vnoise(w, h, seed, cell):
    rng = np.random.default_rng(seed); gw, gh = w // cell + 3, h // cell + 3; G = rng.random((gh, gw))
    ys, xs = np.mgrid[0:h, 0:w] / cell; x0, y0 = xs.astype(int), ys.astype(int); fx, fy = xs - x0, ys - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    return (G[y0, x0] * (1 - fx) * (1 - fy) + G[y0, x0 + 1] * fx * (1 - fy) + G[y0 + 1, x0] * (1 - fx) * fy + G[y0 + 1, x0 + 1] * fx * fy)

def build(z):
    if z == 'town': w, h, tiles, E, exits = martsirt_tiles()
    else: w, h, tiles, E, exits = zone_tiles(z)
    T = np.array(tiles).reshape(h, w)
    water = np.isin(T, list(E['water'])); road = np.isin(T, list(E['road'] | E['path'])) & ~water
    outdoor_exits = [x for x in exits if x['to'] in BASE]
    # seeds: exit tiles get the seam height
    seeds = []
    for x in outdoor_exits:
        tx, ty = min(w - 1, int(x['x'])), min(h - 1, int(x['y']))
        seeds.append((tx, ty, seam_h(z, x['to']), x['to']))
        road[max(0, ty - 1):ty + 2, max(0, tx - 1):tx + 2] |= ~water[max(0, ty - 1):ty + 2, max(0, tx - 1):tx + 2]
    base = BASE[z]
    # geodesic distances along road from each seed
    INF = 1e9; D = []
    for (sx, sy, sh, _) in seeds:
        d = np.full((h, w), INF); dq = collections.deque()
        # nearest road tile to seed
        d[sy, sx] = 0; dq.append((sx, sy))
        while dq:
            cx, cy = dq.popleft()
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < w and 0 <= ny < h and not water[ny, nx] and d[ny, nx] > d[cy, cx] + (1 if road[ny, nx] else 2.5):
                    d[ny, nx] = d[cy, cx] + (1 if road[ny, nx] else 2.5); dq.append((nx, ny))
        D.append(d)
    Hr = np.full((h, w), float(base))
    if seeds:
        num = np.zeros((h, w)); den = np.zeros((h, w))
        for (sx, sy, sh, _), d in zip(seeds, D):
            wgt = np.where(d < INF, 1.0 / (d + 0.5), 0); num += wgt * sh; den += wgt
        # zone base pulls the middle of long roads (plateau / valley floor)
        far = np.min(np.stack(D), 0); wb = np.where(far < INF, 0.15 * np.clip(far / 60.0, 0, 1) / (far + 0.5), 0)
        num += wb * base; den += wb
        Hr = np.where(den > 0, num / np.maximum(den, 1e-9), base)
    # road heights: harmonic on the road graph (=> linear grade along each road), seams + one core point fixed
    fixed = np.zeros((h, w), bool); FV = np.zeros((h, w))
    for (sx, sy, sh, _) in seeds:
        fixed[sy, sx] = True; FV[sy, sx] = sh
    if seeds:
        far = np.min(np.stack(D), 0); far = np.where(road & (far < INF), far, -1)
        cy, cx = np.unravel_index(np.argmax(far), far.shape)
        if far[cy, cx] >= 15:
            fixed[max(0, cy - 1):cy + 2, max(0, cx - 1):cx + 2] |= road[max(0, cy - 1):cy + 2, max(0, cx - 1):cx + 2]
            gg = math.tan(math.radians(ROAD_MAX_DEG)); lo_, hi_ = -1e9, 1e9
            for (sx, sy, sh, _), d in zip(seeds, D): lo_ = max(lo_, sh - gg * d[cy, cx]); hi_ = min(hi_, sh + gg * d[cy, cx])
            cb = min(max(base, lo_), hi_) if lo_ <= hi_ else base
            FV[max(0, cy - 1):cy + 2, max(0, cx - 1):cx + 2] = cb; core = [int(cx), int(cy), round(cb, 2)]
        else: core = None
    else: core = None
    Hr = np.where(fixed, FV, Hr)
    Rf = road.astype(float)
    for _ in range(3000):
        P = np.pad(Hr * Rf, 1); PR = np.pad(Rf, 1)
        s_ = P[:-2, 1:-1] + P[2:, 1:-1] + P[1:-1, :-2] + P[1:-1, 2:]; n_ = PR[:-2, 1:-1] + PR[2:, 1:-1] + PR[1:-1, :-2] + PR[1:-1, 2:]
        Hr = np.where(fixed, FV, np.where(road & (n_ > 0), s_ / np.maximum(n_, 1), Hr))
    # harmonic fill off-road (Jacobi), roads fixed
    H = np.where(road, Hr, base).astype(float)
    for _ in range(400):
        P = np.pad(H, 1, mode='edge'); avg = (P[:-2, 1:-1] + P[2:, 1:-1] + P[1:-1, :-2] + P[1:-1, 2:]) / 4
        H = np.where(road, Hr, avg * .7 + base * .3 * 0 + avg * .3)
    # distance from road (chebyshev, tiles)
    dr = np.full((h, w), 99); dr[road] = 0
    for _ in range(12):
        P = np.pad(dr, 1, constant_values=99); dr = np.minimum(dr, np.minimum.reduce([P[:-2, 1:-1], P[2:, 1:-1], P[1:-1, :-2], P[1:-1, 2:], P[:-2, :-2], P[2:, 2:], P[:-2, 2:], P[2:, :-2]]) + 1)
    rel = RELIEF[z]
    if rel > 0:
        n = vnoise(w, h, zlib.crc32(z.encode()) & 0xffff, 14) * .7 + vnoise(w, h, (zlib.crc32(z.encode()) >> 8) & 0xffff, 6) * .3
        step = 3.0 if rel >= 5 else 1.5
        terr = np.round((n - .45) * rel * 2 / step) * step          # terraces -> plateaus + cliffs
        fade = np.clip((dr - ROAD_CLEAR) / 3.0, 0, 1)                 # never near roads
        H = H + terr * fade
    # coast: keep A0 prop area flat (only the N ramp to the Martsirt seam and E ramp to bastion lift)
    # water: coastal zones use the engine sea (-0.4); inland water bodies sit 0.4 below their lowest shore
    if BASE[z] <= 2: H[water] = -1.2
    else:
        lab_ = -np.ones((h, w), int); k = 0
        for y0 in range(h):
            for x0 in range(w):
                if water[y0, x0] and lab_[y0, x0] < 0:
                    st = [(x0, y0)]; lab_[y0, x0] = k; cells = []; shore = []
                    while st:
                        cx_, cy_ = st.pop(); cells.append((cx_, cy_))
                        for nx, ny in ((cx_ + 1, cy_), (cx_ - 1, cy_), (cx_, cy_ + 1), (cx_, cy_ - 1)):
                            if 0 <= nx < w and 0 <= ny < h:
                                if water[ny, nx] and lab_[ny, nx] < 0: lab_[ny, nx] = k; st.append((nx, ny))
                                elif not water[ny, nx]: shore.append(H[ny, nx])
                    lvl = (min(shore) if shore else base) - 0.4
                    for a_, b_ in cells: H[b_, a_] = lvl - 0.8
                    k += 1
    g = math.tan(math.radians(ROAD_MAX_DEG))
    # corners (w+1)x(h+1)
    # corners: road tiles dominate (a road corner never averages with water/terrain), then land over water
    P = np.pad(H, 1, mode='edge'); PR = np.pad(road, 1, mode='edge').astype(float); PL = np.pad(~water, 1, mode='edge').astype(float)
    def nb(A): return np.stack([A[:-1, :-1], A[1:, :-1], A[:-1, 1:], A[1:, 1:]])
    HH, RR, LL = nb(P), nb(PR), nb(PL)
    wR = RR * 100 + LL * 1 + 0.01
    C = (HH * wR).sum(0) / wR.sum(0)
    for (sx, sy, sh, _) in seeds:  # seam corners exact
        C[sy:sy + 2, sx:sx + 2] = sh
    # per-tile slope from corners
    dzx = ((C[:-1, 1:] - C[:-1, :-1]) + (C[1:, 1:] - C[1:, :-1])) / 2; dzy = ((C[1:, :-1] - C[:-1, :-1]) + (C[1:, 1:] - C[:-1, 1:])) / 2
    slope = np.degrees(np.arctan(np.hypot(dzx, dzy)))
    maxd = np.maximum.reduce([np.abs(C[:-1, :-1] - C[1:, 1:]), np.abs(C[:-1, 1:] - C[1:, :-1]), np.abs(dzx), np.abs(dzy)])
    cliff = (maxd > CLIFF_DH) & ~road & ~water
    road_bad = road & (slope > WALK_MAX_DEG)
    ramp = road & (slope > 4)
    # plateaus = connected flat (<5deg) off-road non-water areas >= 30 tiles at similar height
    flat = (slope < 5) & ~water & ~cliff
    lab = -np.ones((h, w), int); plats = []; nid = 0
    for y in range(h):
        for x in range(w):
            if flat[y, x] and lab[y, x] < 0:
                st = [(x, y)]; lab[y, x] = nid; cells = []
                while st:
                    cx, cy = st.pop(); cells.append((cx, cy))
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < w and 0 <= ny < h and flat[ny, nx] and lab[ny, nx] < 0 and abs(H[ny, nx] - H[cy, cx]) < .5:
                            lab[ny, nx] = nid; st.append((nx, ny))
                if len(cells) >= 30:
                    xs, ys = zip(*cells); plats.append(dict(id='%s_pl%02d' % (z, len(plats)), tiles=len(cells), y=round(float(np.mean([H[b, a] for a, b in cells])), 2),
                                                          bbox=[min(xs), min(ys), max(xs) + 1, max(ys) + 1], kind='open_area' if len(cells) > 200 else 'plateau'))
                nid += 1
    # road length / required length
    climb = (max(s[2] for s in seeds) - min(s[2] for s in seeds)) if len(seeds) > 1 else 0
    road_len = int(road.sum() / 3)  # ~3-wide roads
    pairs = []
    for i, (ax, ay, ah, at) in enumerate(seeds):
        for j, (bx, by, bh, bt) in enumerate(seeds):
            if j <= i: continue
            dd = float(D[i][by, bx]); req = abs(ah - bh) / g
            pairs.append(dict(a=at, b=bt, dh=round(abs(ah - bh), 2), path_m=round(dd, 1), grade_deg=round(math.degrees(math.atan(abs(ah - bh) / max(dd, 1))), 1),
                              switchback_extra_m=round(max(0.0, req - dd), 1), switchback_legs=int(math.ceil(max(0.0, req - dd) / 16.0))))
    need_extra = max([p_['switchback_extra_m'] for p_ in pairs] + [0])
    # cliff edge segments (tile edges between cliff tile and lower neighbour)
    cl = [[int(x), int(y)] for y, x in zip(*np.nonzero(cliff))]
    out = dict(zone=z, name=AUD[z]['name'], size=[w, h], role=ROLE[z], enum='live q' if E is Q else 'extract U (verify against live)',
               format=dict(corners='(w+1)*(h+1) row-major, corner (x,y) index y*(w+1)+x, metres, sample bilinearly in tile', tiles_y_down=True),
               height_range=[round(float(C.min()), 2), round(float(C.max()), 2)], base=BASE[z],
               road=dict(width_m=3 if z != 'town' else 4, max_slope_deg_target=ROAD_MAX_DEG, max_slope_deg_walkable=WALK_MAX_DEG,
                         max_slope_deg_actual=round(float(slope[road].max()), 1) if road.any() else 0, violations=int(road_bad.sum()), violation_tiles=[[int(x), int(y), round(float(slope[y, x]), 1)] for y, x in zip(*np.nonzero(road_bad))],
                         climb_m=round(climb, 2), road_len_m_approx=road_len, needs_switchback=bool(need_extra > 0), extra_switchback_m=need_extra, seam_pairs=pairs,
                         switchback_rule='if needs_switchback: replace the straight run with N legs of <=16 m at <=14 deg joined by 4x4 flat landings (Skyrim hairpins), cliffs between legs'),
               seams=[dict(to=t, tile=[sx, sy], height=sh) for (sx, sy, sh, t) in seeds], core_road_point=core,
               ramp_tiles=[[int(x), int(y)] for y, x in zip(*np.nonzero(ramp))],
               cliff_tiles=cl, plateaus=plats,
               rules=['terrain never blocks a road: terraces/cliffs only >= %d tiles from road tiles; shoulder copies road height' % ROAD_CLEAR,
                      'only monsters/events may block roads', 'water surface -0.4 (engine ocean), bed -1.2'],
               phone_cost=dict(ground_tris=2 * w * h, pathing='height per corner, no navmesh change; nav stays tile-based, cliffs -> solid edges list',
                               camera_occlusion='cliff steps >3 m within 8 m south of the camera path fade (dither) - flag %d cliff tiles' % len(cl),
                               fog_height='fog stays distance-based; optional height fog band at base-2 m for basins/gorges'),
               corners=[round(float(v), 2) for v in C.ravel()])
    if z == 'coast':
        offs = []
        for p in COAST['props']:
            x, y = p['x'], p['y']
            if not (0 <= x < w and 0 <= y < h): continue  # out-of-bounds sea rocks sit on the ocean plane, no terrain under them
            cx, cy = min(w - 1e-3, max(0, x)), min(h - 1e-3, max(0, y)); i, j = int(cx), int(cy); fx, fy = cx - i, cy - j
            hv = (C[j, i] * (1 - fx) * (1 - fy) + C[j, i + 1] * fx * (1 - fy) + C[j + 1, i] * (1 - fx) * fy + C[j + 1, i + 1] * fx * fy)
            if COAST['tiles'][min(h - 1, int(y)) * w + min(w - 1, int(x))] in E['water']: continue
            if abs(hv) > .05: offs.append(dict(kind=p['kind'], x=x, y=y, y_offset=round(float(hv), 2)))
        out['a0_prop_y_offsets'] = offs
        out['a0_note'] = 'land interior kept at 0 m except the seam ramps; %d of %d A0 props need y_offset (listed); props outside the 42x112 bounds stand on the ocean plane and are skipped. Water props (boats) are excluded if on water.' % (len(offs), len(COAST['props']))
    return out, H, C, road, water, cliff

def preview(z, H, road, water, cliff, path):
    from PIL import Image
    h, w = H.shape; lo, hi = H[~water].min() if (~water).any() else 0, H.max()
    v = (H - lo) / max(1e-6, hi - lo)
    gy, gx = np.gradient(H); shade = np.clip(.75 + (-gx - gy) * .35, .3, 1.2)
    rgb = np.stack([.18 + .5 * v, .16 + .42 * v, .14 + .3 * v], -1) * shade[..., None]
    rgb[water] = (.03, .07, .1); rgb[road] = (.55, .45, .3); rgb[cliff] = (.08, .06, .06)
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).resize((w * 6, h * 6), Image.NEAREST); im.save(path)

if __name__ == '__main__':
    zones = sys.argv[1:] or ['coast', 'town', 'flotsam', 'hollow', 'bastion', 'bluffs', 'mires', 'sink', 'ridge', 'ascent', 'crypts', 'chasm',
                             'iron', 'gaol', 'weald', 'wild', 'briarE', 'duneW', 'desert', 'lut', 'market', 'waste', 'isle']
    os.makedirs(HERE + '/previews', exist_ok=True); summary = []
    for z in zones:
        o, H, C, road, water, cliff = build(z)
        fn = 'martsirt' if z == 'town' else z
        json.dump(o, open('%s/%s.json' % (HERE, fn), 'w'), separators=(',', ':'))
        preview(z, H, road, water, cliff, '%s/previews/%s.png' % (HERE, fn))
        s = dict(zone=fn, size=o['size'], range=o['height_range'], road_max=o['road']['max_slope_deg_actual'], viol=o['road']['violations'],
                 climb=o['road']['climb_m'], switch=o['road']['needs_switchback'], extra=o['road']['extra_switchback_m'],
                 plateaus=len(o['plateaus']), cliffs=len(o['cliff_tiles']), offs=len(o.get('a0_prop_y_offsets', [])))
        summary.append(s); print(s)
    json.dump(dict(base_m=BASE, relief_m=RELIEF, role=ROLE, seam_heights={'%s|%s' % (a, b): seam_h(a, b) for a in BASE for b in BASE if a < b and
               any(x['to'] == b for x in AUD[a]['exits'])}, summary=summary), open(HERE + '/elevation_table.json', 'w'), indent=1)
