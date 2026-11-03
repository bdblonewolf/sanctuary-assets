"""exits_v3: pick new spots for enemy spawns / nests that sit on blocked or unreachable tiles (final, mirrored frame).
Nearest open tile reachable from the player spawn; nests prefer off-road, next to cover (solid tile or a prop within 1.5);
spawns prefer off-road; both keep >= 4 tiles from exits/arrivals/player spawn and >= 2 from other spawns/nests."""
import json, math, sys
W = json.load(open(sys.argv[1]))
ROAD = {6, 2}  # Road, Dirt (trail)
def reach(w):
    R = set(); s = (int(w['spawn']['x']), int(w['spawn']['y'])); st = [s]; R.add(s)
    while st:
        x, y = st.pop()
        for a, b in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= a < w['w'] and 0 <= b < w['h'] and (a, b) not in R and not w['solid'][b*w['w']+a]: R.add((a, b)); st.append((a, b))
    return R
def blocked(w, R, p): return (int(p['x']), int(p['y'])) not in R
out = {}
for z, w in W.items():
    R = reach(w); W_ = w['w']; moves = []
    avoid = [(e['x'], e['y']) for e in w['exits']] + [(w['spawn']['x'], w['spawn']['y'])]
    others = lambda: [(q['x'], q['y']) for q in w['spawns'] + w['nests']]
    for lst, role in (('spawns', 'spawn'), ('nests', 'nest')):
        for i, p in enumerate(w[lst]):
            if not blocked(w, R, p): continue
            best = None
            for (tx, ty) in R:
                if tx < 1 or ty < 1 or tx > W_-2 or ty > w['h']-2: continue
                cx, cy = tx + .5, ty + .5; d = math.hypot(cx - p['x'], cy - p['y'])
                if d > 8: continue
                tile = w['tiles'][ty*W_+tx]; sc = d
                if tile in ROAD: sc += 4 if role == 'nest' else 1.5
                if min(math.hypot(cx-a, cy-b) for a, b in avoid) < 4: sc += 6
                if any(math.hypot(cx-a, cy-b) < 2 for a, b in others() if (a, b) != (p['x'], p['y'])): sc += 3
                # every 4-neighbour open keeps the mob from spawning wedged in a 1-tile slot
                op = sum((tx+a, ty+b) in R for a, b in ((1,0),(-1,0),(0,1),(0,-1))); sc += (4-op) * .6
                cover = any(w['solid'][(ty+b)*W_+tx+a] for a in (-1,0,1) for b in (-1,0,1)) or any(math.hypot(q['x']-cx, q['y']-cy) < 1.5 for q in w['props'])
                if role == 'nest' and not cover: sc += 2
                if best is None or sc < best[0]: best = (sc, cx, cy, tile, cover, d)
            sc, cx, cy, tile, cover, d = best
            m = dict(list=lst, old=dict(x=round(p['x'], 4), y=round(p['y'], 4)), new=dict(x=cx, y=cy),
                     why='%s was on %s tile %d (%s); nearest open tile reachable from the player spawn%s, %.1f tiles away, tile %d%s' % (
                        role, 'a SOLID' if w['solid'][int(p['y'])*W_+int(p['x'])] else 'an UNREACHABLE', w['tiles'][int(p['y'])*W_+int(p['x'])],
                        'predates v3; also blocked on the live world', ', off the road' if tile not in ROAD else '', d, tile, ', next to cover' if cover else ''))
            if 'kind' in p: m['kind'] = p['kind']
            p['x'], p['y'] = cx, cy; moves.append(m)
    # patrol route points (route[0] follows its spawn in movePoints): nearest open reachable tile whose legs to the
    # previous and next route points are walkable in a straight line (sampled every 0.25 tile)
    def leg_ok(a, b):
        L = math.hypot(b[0]-a[0], b[1]-a[1]); n = max(1, int(L / .25))
        return all(not w['solid'][int(a[1]+(b[1]-a[1])*t/n)*W_+int(a[0]+(b[0]-a[0])*t/n)] for t in range(n+1))
    for i, sp in enumerate(w['spawns']):
        r = sp.get('route') or []
        for k in range(1, len(r)):
            p = r[k]
            if not blocked(w, R, p): continue
            pr, nx = r[k-1], r[(k+1) % len(r)]; best = None
            for (tx, ty) in R:
                if tx < 1 or ty < 1 or tx > W_-2 or ty > w['h']-2: continue
                cx, cy = tx + .5, ty + .5; d = math.hypot(cx - p['x'], cy - p['y'])
                if d > 6: continue
                sc = d + (0 if leg_ok((pr['x'], pr['y']), (cx, cy)) else 5) + (0 if leg_ok((cx, cy), (nx['x'], nx['y'])) else 5)
                if best is None or sc < best[0]: best = (sc, cx, cy, d)
            sc, cx, cy, d = best
            moves.append(dict(list='spawns', route_i=k, old=dict(x=round(p['x'], 4), y=round(p['y'], 4)), new=dict(x=cx, y=cy),
                why='%s patrol route point %d was on %s tile %d (predates v3; also blocked on the live world); nearest open tile reachable from the player spawn with walkable legs to its neighbours, %.1f tiles away' % (
                    sp['kind'], k, 'a SOLID' if w['solid'][int(p['y'])*W_+int(p['x'])] else 'an UNREACHABLE', w['tiles'][int(p['y'])*W_+int(p['x'])], d)))
            p['x'], p['y'] = cx, cy
            print(z, 'route', sp['kind'], k, moves[-1]['old'], '->', moves[-1]['new'], 'legs ok' if sc - d < 1 else 'LEG BLOCKED')
    out[z] = moves
    for m in moves: print(z, m['list'], m.get('kind', ''), m['old'], '->', m['new'], '|', m['why'])
json.dump(out, open(sys.argv[2], 'w'), indent=1)
