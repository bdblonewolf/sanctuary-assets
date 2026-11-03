# exits_v3 copy of gen_seams_v2.py: same algorithm; inputs = worlds after the exits_v3 patches (briarE, duneW, desert mirrored). Outputs in v3/seams.
"""One seam JSON per outdoor zone pair (from the live exit graph in design/audit/worlds.json).
Frame per zone: tile coords x right, y down (three x,z). Edge outward normals N(0,-1) E(1,0) S(0,1) W(-1,0).
B is placed beyond A's edge so that B.exit == A.exit and B's outward normal == -A's outward normal:
    pA = exitA + R(theta) (pB - exitB)          theta = rotation taking nB to -nA (multiples of 90)
Scenery copy: every border piece / border prop / world prop of B within COPY_DEPTH of B's seam edge and
within COPY_HALF of the exit along the edge is transformed into A; it is kept only if it lands OUTSIDE A's
bounds (no clipping into A's playable tiles), at least 1.2 m from A's own border props, and not on the 6 m
pass corridor (road stays open). Same the other way round. Terrain: both sides share one seam height.
"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
AUD = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v3in/worlds_v3.json'))
EXT = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v3in/world_extract_v3.json'))['worlds']
TER = '/workspace/sanctuary_env/world_v1/exits/v3/terrain/'
LAYD = '/workspace/sanctuary_env/world_v1/border_kit/out/'
OUTDOOR = ['town', 'coast', 'flotsam', 'hollow', 'bastion', 'bluffs', 'mires', 'sink', 'ridge', 'ascent', 'crypts', 'chasm', 'iron',
           'gaol', 'weald', 'wild', 'briarE', 'duneW', 'desert', 'lut', 'market', 'waste']
FILE = {'town': 'martsirt'}
NRM = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
COPY_DEPTH, COPY_HALF, PASS_HALF = 16.0, 22.0, 3.0
def size(z):
    if z == 'coast': return 42, 112
    return AUD[z]['w'], AUD[z]['h']
def edge_of(z, x, y):
    w, h = size(z); d = {'N': y, 'S': h - y, 'W': x, 'E': w - x}; return min(d, key=d.get)
def along(e, x, y, w, h):  # offset along the clockwise walk of that edge
    return {'N': x, 'E': y, 'S': w - x, 'W': h - y}[e]
def rot_between(nb, target):
    a = math.atan2(target[1], target[0]) - math.atan2(nb[1], nb[0]); k = round(a / (math.pi / 2)) % 4; return k * 90
def R(deg, v):
    c, s = round(math.cos(math.radians(deg))), round(math.sin(math.radians(deg))); return (c * v[0] - s * v[1], s * v[0] + c * v[1])
def scenery(z):
    """border kit + border props from the layout if generated, plus the zone's own world props"""
    out = []; fn = LAYD + ('layout_%s_v2.json' if FILE.get(z, z) in ('coast', 'martsirt') else 'layout_%s.json') % FILE.get(z, z)
    if os.path.exists(fn):
        L = json.load(open(fn))
        for p in L['pieces']: out.append(dict(src='kit', id=p['piece'], style=p['style'], x=p['pos'][0], y=p['pos'][2], rotY=p['rotY'], scaleX=p['scaleX']))
        for p in L['props']: out.append(dict(src='border_prop', id=p['id'], asset=p['asset'], x=p['pos'][0], y=p['pos'][2], rotY=p['rotY'], scale=p['scale'], collider=p.get('collider')))
    if z == 'coast':
        for p in json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/coast_world_after_v2.json'))['props']:
            out.append(dict(src='world_prop', id=p['kind'], x=p['x'], y=p['y'], style=p.get('style')))
    elif z == 'town':
        ms = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/martsirt_world_v2.json')); ox, oz = ms['origin']
        for p in json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/placements_v2.json'))['placements']:
            if p['kind'] == 'interactable': continue
            out.append(dict(src='world_prop', id=os.path.basename(p['piece']).replace('.glb', ''), asset=p['piece'], x=p['pos'][0] + ox, y=p['pos'][2] + oz, rotY=p.get('rotY', 0), kind=p['kind']))
    elif z in EXT:
        for p in EXT[z].get('props', []):
            if p['kind'] in ('building', 'arch', 'npc', 'chest'): continue
            out.append(dict(src='world_prop', id=p['kind'], x=p['x'], y=p['y'], style=p.get('style')))
    return out
def seam_h(z, to):
    fn = TER + FILE.get(z, z) + '.json'
    if not os.path.exists(fn): return None
    for s in json.load(open(fn))['seams']:
        if s['to'] == to: return s['height']
pairs = {}
for a in OUTDOOR:
    for ex in AUD[a]['exits']:
        b = ex['to']
        if b not in OUTDOOR: continue
        key = tuple(sorted((a, b)))
        if key in pairs: continue
        back = [q for q in AUD[b]['exits'] if q['to'] == a]
        if not back: continue
        pairs[key] = (a, ex, b, back[0])
index = []
for key, (a, ea, b, eb) in sorted(pairs.items()):
    wa, ha = size(a); wb, hb = size(b)
    xa, ya, xb, yb = ea['x'], ea['y'], eb['x'], eb['y']
    sa, sb = edge_of(a, xa, ya), edge_of(b, xb, yb)
    def edist(z, x, y): w, h = size(z); return min(x, y, w - x, h - y)
    if edist(a, xa, ya) > 4 or edist(b, xb, yb) > 4:
        rec = dict(id='%s__%s' % key, kind='interior_exit', zone_a=dict(id=a, exit_tile=[xa, ya], edge_dist=round(edist(a, xa, ya), 1)),
                   zone_b=dict(id=b, exit_tile=[xb, yb], edge_dist=round(edist(b, xb, yb), 1)),
                   rule='exit is inside a zone (dock/boat/sinkhole/stair), not on an edge: no ring skip, no scenery copy; the continent layout places the zones apart (by water or a drop); terrain heights still match at the trigger tiles.',
                   terrain=dict(seam_height_a=seam_h(a, b), seam_height_b=seam_h(b, a)))
        fn = '%s__%s.json' % (FILE.get(key[0], key[0]), FILE.get(key[1], key[1])); json.dump(rec, open(os.path.join(HERE, fn), 'w'), indent=1)
        index.append(dict(file=fn, a=a, b=b, kind='interior_exit')); print(index[-1]); continue
    th = rot_between(NRM[sb], (-NRM[sa][0], -NRM[sa][1]))       # B -> A
    thi = (-th) % 360                                            # A -> B
    def BtoA(x, y): v = R(th, (x - xb, y - yb)); return xa + v[0], ya + v[1]
    def AtoB(x, y): v = R(thi, (x - xa, y - ya)); return xb + v[0], yb + v[1]
    def copy(src_zone, dst_zone, T, src_edge, src_exit, dst_w, dst_h, dst_props):
        res, dropped = [], collections_counter()
        sw, sh_ = size(src_zone); ex, ey = src_exit; nx, ny = NRM[src_edge]
        for it in scenery(src_zone):
            # depth inward from the source seam edge, and offset along it from the exit
            dx, dy = it['x'] - ex, it['y'] - ey
            depth_in = -(dx * nx + dy * ny); off = dx * (-ny) + dy * nx
            if depth_in > COPY_DEPTH or depth_in < -12 or abs(off) > COPY_HALF: continue
            if it['src'] == 'kit' and abs(off) < PASS_HALF + 6 and it['id'] == 'pass12':
                dropped['pass_piece'] += 1; continue
            px, py = T(it['x'], it['y'])
            inside = (-0.5 < px < dst_w + 0.5) and (-0.5 < py < dst_h + 0.5)
            if inside: dropped['would_clip_inside'] += 1; continue
            if abs(off) < PASS_HALF and it['src'] != 'kit': dropped['on_pass_corridor'] += 1; continue
            if any((px - q[0]) ** 2 + (py - q[1]) ** 2 < 1.44 for q in dst_props): dropped['too_close_to_dst_prop'] += 1; continue
            r = dict(it); r['src_xy'] = [round(it['x'], 2), round(it['y'], 2)]; r['x'], r['y'] = round(px, 2), round(py, 2)
            if 'rotY' in r: r['rotY'] = round(r['rotY'] - math.radians(T is BtoA and th or thi), 4)
            res.append(r)
        return res, dict(dropped)
    import collections
    def collections_counter(): return collections.Counter()
    def own_props(z):
        return [(s['x'], s['y']) for s in scenery(z) if s['src'] != 'kit']
    copyBA, dBA = copy(b, a, BtoA, sb, (xb, yb), wa, ha, own_props(a))
    copyAB, dAB = copy(a, b, AtoB, sa, (xa, ya), wb, hb, own_props(b))
    ha_, hb_ = seam_h(a, b), seam_h(b, a)
    rec = dict(id='%s__%s' % key, zone_a=dict(id=a, name=AUD[a]['name'], size=[wa, ha], edge=sa, exit_tile=[xa, ya], arrive=[ea.get('sx'), ea.get('sy')],
                                             offset_along_edge_m=round(along(sa, xa, ya, wa, ha), 2), edge_len_m={'N': wa, 'S': wa, 'E': ha, 'W': ha}[sa]),
               zone_b=dict(id=b, name=AUD[b]['name'], size=[wb, hb], edge=sb, exit_tile=[xb, yb], arrive=[eb.get('sx'), eb.get('sy')],
                           offset_along_edge_m=round(along(sb, xb, yb, wb, hb), 2), edge_len_m={'N': wb, 'S': wb, 'E': hb, 'W': hb}[sb]),
               transform=dict(b_to_a=dict(rot_deg=th, formula='pA = exitA + R(rot)(pB - exitB)'), a_to_b=dict(rot_deg=thi, formula='pB = exitB + R(rot)(pA - exitA)'),
                              orientation_mismatch=bool(th != 0), note=('edges are not opposite (%s vs %s): the copy is rotated %d deg; continent layout places B rotated' % (sa, sb, th)) if th else 'opposite edges, pure translation'),
               pass_span=dict(a=[round(along(sa, xa, ya, wa, ha) - 6, 2), round(along(sa, xa, ya, wa, ha) + 6, 2)], b=[round(along(sb, xb, yb, wb, hb) - 6, 2), round(along(sb, xb, yb, wb, hb) + 6, 2)],
                              corridor_open_m=2 * PASS_HALF, rule='ring skips this span on both sides; road corridor stays open'),
               terrain=dict(seam_height_a=ha_, seam_height_b=hb_, consistent=(ha_ is not None and hb_ is not None and abs(ha_ - hb_) < 1e-6)),
               copy_into_a=dict(count=len(copyBA), dropped=dBA, items=copyBA), copy_into_b=dict(count=len(copyAB), dropped=dAB, items=copyAB),
               exits_offset=dict(a=abs(along(sa, xa, ya, wa, ha) - {'N': wa, 'S': wa, 'E': ha, 'W': ha}[sa] / 2) > 2, b=abs(along(sb, xb, yb, wb, hb) - {'N': wb, 'S': wb, 'E': hb, 'W': hb}[sb] / 2) > 2))
    for side, z, e, x, y in (('a', a, sa, xa, ya), ('b', b, sb, xb, yb)):
        if not rec['exits_offset'][side]:
            L = rec['zone_' + side]['edge_len_m']; t = rec['zone_' + side]['offset_along_edge_m']
            rec['zone_' + side]['proposed_offset_m'] = round(L * (0.35 if (len(z) % 2) else 0.65), 1)
            rec['zone_' + side]['proposal_note'] = 'exit sits at the edge centre; PROPOSAL ONLY (needs a world-JSON change by the engineer, not done): move to the proposed offset and bend the road; the other side follows via the transform'
    rec['kind'] = 'edge_seam'
    fn = '%s__%s.json' % (FILE.get(key[0], key[0]), FILE.get(key[1], key[1]))
    json.dump(rec, open(os.path.join(HERE, fn), 'w'), indent=1)
    index.append(dict(file=fn, a=a, b=b, edges='%s|%s' % (sa, sb), rot=th, off_a=rec['zone_a']['offset_along_edge_m'], off_b=rec['zone_b']['offset_along_edge_m'],
                      h=[ha_, hb_], into_a=len(copyBA), into_b=len(copyAB), offset_exits=rec['exits_offset']))
    print(index[-1])
json.dump(index, open(os.path.join(HERE, 'seams_index.json'), 'w'), indent=1)
