#!/usr/bin/env python3
"""Reference border generator (pure python, no deps beyond stdlib+json).
Lays the border kit + collidable border props around a rectangular zone from its
bounds, per-metre land/sea class, style map and seam/exit spans.

  v2 (exits_v2): same generator, inputs patched to the new exits (border_styles_v2.json seams; coast + Martsirt worlds/roads after the exits patches)
  python3 gen_border_v2.py coast    -> out/layout_coast_v2.json
  python3 gen_border_v2.py martsirt -> out/layout_martsirt_v2.json

Frame: tile metres. three.js world: x east, z south. Map = [0,w]x[0,h].
(The live coast loader already puts tile (x,y) at world (x,0,y). For Martsirt the
town group is at (origin.x,0,origin.z) and placements are town-local, so the
layout here is in tile metres: subtract origin to get town-local.)
Kit piece frame (see build_kit.py): pivot on the edge line, runs along local +X,
border rises to local -Z (outward). Clockwise walk N->E->S->W; outward is left.
"""
import json, math, os, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STY = json.load(open(os.path.join(HERE, 'border_styles_v2.json')))
MAN = json.load(open(os.path.join(HERE, 'kit_manifest.json')))
ENDCAP = 12.0; PASS = 12.0; EXIT_CLEAR = 4.0; PROP_CLEAR = 1.2

EDGES = {  # start, dir, rotY(deg) for clockwise walk
 'N': lambda w, h: ((0, 0), (1, 0), 0.0, w),
 'E': lambda w, h: ((w, 0), (0, 1), -90.0, h),
 'S': lambda w, h: ((w, h), (-1, 0), 180.0, w),
 'W': lambda w, h: ((0, h), (0, -1), 90.0, h)}
ORDER = ['N', 'E', 'S', 'W']

def rnd(*k):
    return int(hashlib.md5('|'.join(map(str, k)).encode()).hexdigest()[:8], 16) / 0xffffffff

def edge_tile(edge, t, w, h):
    i = int(math.floor(t))
    return {'N': (i, 0), 'E': (w - 1, i), 'S': (w - 1 - i, h - 1), 'W': (0, h - 1 - i)}[edge]

def at(edge, t, w, h, out=0.0):
    (sx, sz), (dx, dz), _, _ = EDGES[edge](w, h)
    ox, oz = dz, -dx  # outward = left of walk (north up): N->(0,-1)
    return sx + dx * t + ox * out, sz + dz * t + oz * out

def classify(zone, w, h, tilefn):
    """per edge: list of runs (cls, a, b); short runs (<12 m) are merged."""
    runs = {}
    for e in ORDER:
        L = EDGES[e](w, h)[3]
        cl = ['sea' if tilefn and tilefn(*edge_tile(e, t + .5, w, h)) == 'sea' else 'land' for t in range(int(L))]
        r = []
        for t, c in enumerate(cl):
            if r and r[-1][0] == c: r[-1][2] = t + 1
            else: r.append([c, t, t + 1])
        changed = True
        while changed and len(r) > 1:
            changed = False
            for i, q in enumerate(r):
                if q[2] - q[1] < 12:
                    j = i - 1 if i > 0 else i + 1
                    lo, hi = min(r[i][1], r[j][1]), max(r[i][2], r[j][2])
                    r[j][1], r[j][2] = lo, hi; r.pop(i); changed = True; break
        r[-1][2] = L
        runs[e] = r
    return runs

def fill(a, b, style, seed):
    """straights covering [a,b] exactly: 12/6/3 then stretch."""
    E = b - a
    if E <= 1e-6: return []
    n12 = int(E // 12); r = E - 12 * n12; n6 = int(r // 6); r -= 6 * n6; n3 = int(r // 3); r -= 3 * n3
    names = []
    for i in range(n12): names.append('straight12_' + 'abc'[int(rnd(seed, i) * 3)])
    names += ['straight6'] * n6 + ['straight3'] * n3
    if not names: names = ['straight3']
    # interleave short ones so stretching stays uniform
    names = [n for _, n in sorted(enumerate(names), key=lambda q: rnd(seed, q[1], q[0]))]
    lens = [float(n[8:10]) if n.startswith('straight12') else float(n[8:]) for n in names]
    k = E / sum(lens); out = []; t = a
    for n, l in zip(names, lens):
        out.append((n, t, l * k, k)); t += l * k
    return out

def layout(zone):
    Z = STY['zones'][zone]; w, h = Z['size']; land_style = Z['style']
    sea_style = STY['styles'].get(land_style, {}).get('sea_style', 'sea')
    tilefn, props_existing, blocked = None, [], set()
    if zone == 'coast':
        cw = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/coast_world_after_v2.json'))
        T = cw['tiles']
        tilefn = lambda x, y: 'sea' if T[y * w + x] == 8 else T[y * w + x]
        props_existing = [(p['x'], p['y']) for p in cw['props']]
        for y in range(h):
            for x in range(w):
                if T[y * w + x] in (2, 6, 7, 9): blocked.add((x, y))
    elif zone == 'martsirt':
        ms = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/martsirt_world_v2.json'))
        ox, oz = ms['origin']
        pl = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/placements_v2.json'))['placements']
        props_existing = [(p['pos'][0] + ox, p['pos'][2] + oz) for p in pl if p['kind'] in ('prop', 'building', 'interactable')]
        for rd in pl and json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/placements_v2.json'))['header']['v2']['roads']:
            pts = rd['points']; hw = rd['width_m'] / 2 + 1
            for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
                n = int(math.hypot(x1 - x0, z1 - z0)) + 1
                for i in range(n + 1):
                    cx, cz = x0 + (x1 - x0) * i / n + ox, z0 + (z1 - z0) * i / n + oz
                    if rd.get('tight_clear'):   # v2: edge-hugging trail blocks only its own width (the S border keeps its props)
                        r2 = rd['width_m'] / 2
                        for k in range(-int(2 * r2), int(2 * r2) + 1):
                            for m in range(-int(2 * r2), int(2 * r2) + 1):
                                if (k * .5) ** 2 + (m * .5) ** 2 <= r2 * r2: blocked.add((int(cx + k * .5), int(cz + m * .5)))
                        continue
                    for dx in range(-int(hw) - 1, int(hw) + 2):
                        for dz in range(-int(hw) - 1, int(hw) + 2):
                            blocked.add((int(cx + dx), int(cz + dz)))
    runs = classify(zone, w, h, tilefn)
    pieces, notes = [], []
    seams = Z.get('seams', [])
    for e in ORDER:
        (sx, sz), (dx, dz), rot, L = EDGES[e](w, h)
        # spans reserved on this edge: endcaps + passes (in walk param t)
        reserved = []
        r = runs[e]
        for i in range(1, len(r)):
            t0 = r[i][1]
            if r[i - 1][0] == 'land': reserved.append((t0 - ENDCAP, t0, 'endcap_land_to_sea', land_style))
            else: reserved.append((t0, t0 + ENDCAP, 'endcap_sea_to_land', land_style))
        # corner transitions
        nxt = ORDER[(ORDER.index(e) + 1) % 4]; prv = ORDER[(ORDER.index(e) - 1) % 4]
        if r[-1][0] == 'land' and runs[nxt][0][0] == 'sea': reserved.append((L - ENDCAP, L, 'endcap_land_to_sea', land_style))
        if r[0][0] == 'land' and runs[prv][-1][0] == 'sea': reserved.append((0, ENDCAP, 'endcap_sea_to_land', land_style))
        for s in seams:
            if s['edge'] != e: continue
            ex, ey = s['exit']
            # exit position along walk param
            tc = {'N': ex, 'E': ey, 'S': w - ex, 'W': h - ey}[e]
            a = max(0, min(L - PASS, tc - PASS / 2)); reserved.append((a, a + PASS, 'pass12', land_style))
            notes.append({'seam': s['neighbour'], 'edge': e, 'walk_t': [a, a + PASS], 'note': 'pass12 = fallback; engine replaces with neighbour scenery copy (seams/)'})
        reserved.sort()
        # passes (roads) win: push endcaps off a pass, into the neighbouring run (sea face over water is fine)
        passes = [q for q in reserved if q[2] == 'pass12']
        fixed = []
        for q in reserved:
            if q[2] != 'pass12':
                a, b = q[0], q[1]
                for pa, pb, _, _ in passes:
                    if a < pb and b > pa:
                        if q[2] == 'endcap_land_to_sea': a, b = pb, pb + ENDCAP
                        else: a, b = pa - ENDCAP, pa
                        notes.append({'edge': e, 'moved_endcap': q[2], 'from': [q[0], q[1]], 'to': [a, b], 'why': 'exit road wins; endcap shifted next to pass12'})
                q = (max(0, a), min(L, b), q[2], q[3])
            fixed.append(q)
        reserved = sorted(fixed)
        t = 0.0; segs = []
        for a, b, name, st in reserved:
            if a > t + 1e-6: segs.append(('fill', t, a))
            segs.append((name, a, b, st)); t = b
        if t < L - 1e-6: segs.append(('fill', t, L))
        for sg in segs:
            if sg[0] == 'fill':
                a, b = sg[1], sg[2]
                # split by run class
                for cls, ra, rb in runs[e]:
                    lo, hi = max(a, ra), min(b, rb)
                    if hi - lo <= 1e-6: continue
                    st = land_style if cls == 'land' else sea_style
                    for n, tt, l, k in fill(lo, hi, st, (zone, e, lo)):
                        pieces.append(dict(style=st, piece=n, edge=e, walk_t=round(tt, 3), length_m=round(l, 3), scaleX=round(k, 4)))
            else:
                name, a, b, st = sg
                k = round((b - a) / ENDCAP, 4) if name.startswith('endcap') and b - a < ENDCAP - 1e-6 else 1.0   # v2: endcap squeezed between a corner and a pass is scaled to fit (no overlap into the pass)
                pieces.append(dict(style=st, piece=name, edge=e, walk_t=round(a, 3), length_m=round(b - a, 3), scaleX=k))
                if k != 1.0: notes.append({'edge': e, 'scaled_endcap': name, 'walk_t': [round(a, 3), round(b, 3)], 'scaleX': k, 'why': 'exit sits near the corner; endcap fitted between the corner and the pass'})
        # corner at end of this edge
        endcls = r[-1][0]; nextcls = runs[nxt][0][0]
        cst = land_style if (endcls == 'land' and nextcls == 'land') else sea_style
        pieces.append(dict(style=cst, piece='corner_outer', edge=e, walk_t=L, length_m=0, scaleX=1.0, corner=e + nxt))
    for p in pieces:
        x, z = at(p['edge'], p['walk_t'], w, h); _, _, rot, _ = EDGES[p['edge']](w, h)
        p['pos'] = [round(x, 3), 0.0, round(z, 3)]; p['rotY_deg'] = rot; p['rotY'] = round(math.radians(rot), 5)
    # collidable border props
    props = []
    def ok(x, z):
        ti = (int(math.floor(x)), int(math.floor(z)))
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if (ti[0] + dx, ti[1] + dz) in blocked and -0.5 <= x <= w + .5 and -0.5 <= z <= h + .5: return False
        for px, pz in props_existing:
            if (px - x) ** 2 + (pz - z) ** 2 < PROP_CLEAR ** 2 + 1.0: return False
        for s in seams:
            ex, ey = s['exit']
            if abs(ex - x) < PASS / 2 + EXIT_CLEAR and abs(ey - z) < PASS / 2 + EXIT_CLEAR: return False
        return True
    for e in ORDER:
        L = EDGES[e](w, h)[3]
        for cls, ra, rb in runs[e]:
            st = land_style if cls == 'land' else sea_style
            S = STY['styles'][st]; rules = S.get('props') or STY['styles'][S['props_like']]['props']
            dens = S.get('density_x', 1.0)
            for ru in rules:
                t = ra + rnd(zone, e, ru['id'], ra) * ru['min_spacing_m']; i = 0
                while t < rb:
                    j = rnd(zone, e, ru['id'], i, 'j'); k = rnd(zone, e, ru['id'], i, 'k')
                    off = ru['offset_m'][0] + (ru['offset_m'][1] - ru['offset_m'][0]) * k
                    tt = t + (j - .5) * 2 * ru['jitter_m']
                    x, z = at(e, tt, w, h, off)
                    if 0 <= tt <= L and ok(x, z):
                        opts = ru['asset'][ru['asset'].find('{') + 1:ru['asset'].find('}')].split('|') if '{' in ru['asset'] and '|' in ru['asset'] else ['']
                        pick = opts[int(rnd(zone, e, ru['id'], i, 'v') * len(opts)) % len(opts)]
                        asset = ru['asset'].replace('{' + '|'.join(opts) + '}', pick) if pick else ru['asset']
                        asset = asset.replace('{season}', Z.get('season', 'dead' if zone == 'coast' else 'autumn'))
                        sc = ru['scale'][0] + (ru['scale'][1] - ru['scale'][0]) * rnd(zone, e, ru['id'], i, 's')
                        props.append(dict(id=ru['id'], asset=asset, layer=ru['layer'], edge=e, pos=[round(x, 3), 0.0, round(z, 3)],
                                          rotY=round(rnd(zone, e, ru['id'], i, 'r') * 2 * math.pi, 4), scale=round(sc, 3),
                                          collider=ru.get('collider', 'none'), blocks_walk=bool(ru.get('blocks_walk'))))
                    sp = ru['min_spacing_m'] + (ru['max_spacing_m'] - ru['min_spacing_m']) * rnd(zone, e, ru['id'], i, 'sp')
                    t += sp / dens; i += 1
    tris = sum(MAN['bk_%s_%s.glb' % (p['style'], 'autumn')]['pieces'][p['piece']]['tris'] for p in pieces)
    out = dict(zone=zone, size=[w, h], frame='tile metres; three.js x east z south; map [0,w]x[0,h]',
               glb='world_v1/border_kit/glb/bk_<style>_<season>.glb (node name = piece)',
               runs={e: runs[e] for e in ORDER}, seams=notes, pieces=pieces, props=props,
               stats=dict(pieces=len(pieces), props=len(props), kit_tris=tris,
                          prop_by_id={k: sum(1 for p in props if p['id'] == k) for k in sorted({p['id'] for p in props})},
                          moved_world_props=0))
    return out

if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    for z in sys.argv[1:] or ['coast', 'martsirt']:
        o = layout(z)
        json.dump(o, open(os.path.join(HERE, 'out', 'layout_%s_v2.json' % z), 'w'), indent=1)
        print(z, o['stats'], o['runs'])
