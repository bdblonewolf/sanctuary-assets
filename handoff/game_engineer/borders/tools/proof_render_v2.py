"""Proof renderer: game camera (FOV38 vertical, pitch 50, lookAt hero+1.15, dist 14/40,
portrait 9:19.5 + landscape 19.5:9), Cycles + three.js linear fog composite, void metric.
blender -b -P proof_render_v2.py -- <zone coast|martsirt> <outdir> [quick]   (exits_v2: v2 layouts + worlds after the exits patches; adds EXIT views at the moved exits)
void  = pixel whose ray reaches nothing (no geometry) while its ground-plane depth < 0.9*fog.far
gap   = (coast) pixel whose first hit is the bare ocean plane outside the map in front of a LAND border run
        (the dark-ocean 'black spot' look) with depth < 0.9*far.
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector, Euler
A = sys.argv[sys.argv.index('--') + 1:]
ZONE, OUT = A[0], A[1]; QUICK = len(A) > 2 and A[2] == 'quick'
os.makedirs(OUT, exist_ok=True)
HERE = '/workspace/sanctuary_env/world_v1/border_kit/'
REPO = '/workspace/repos/sanctuary-assets/'; ASH = '/workspace/sanctuary_env/ashen_cleanup/glb/'
LAY = json.load(open(HERE + 'out/layout_%s_v2.json' % ZONE))
W, H = LAY['size']
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
def mat(name, col, rough=.9, em=0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    if em: b.inputs['Emission Color'].default_value = (*col, 1); b.inputs['Emission Strength'].default_value = em
    return m
def coll(name):
    c = bpy.data.collections.new(name); sc.collection.children.link(c); return c
C_BASE, C_BEFORE, C_AFTER = coll('base'), coll('before'), coll('after')
SRC = bpy.data.collections.new('src')  # not linked to scene
cache = {}
def load(path, keep_names=False):
    if path in cache: return cache[path]
    if not os.path.exists(path): print('MISSING', path); cache[path] = None; return None
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    c = bpy.data.collections.new(os.path.basename(path))
    for o in new:
        for cc in list(o.users_collection): cc.objects.unlink(o)
        c.objects.link(o)
        if o.name.startswith(('col_', 'nav_', 'fx_', 'npc_spot')): o.hide_render = True
    cache[path] = c; return c
def inst(c, loc3, rotY, s, target, idx):
    """loc3 = three.js (x,y,z)"""
    if c is None: return
    e = bpy.data.objects.new('i', None); e.instance_type = 'COLLECTION'; e.instance_collection = c
    e.location = (loc3[0], -loc3[2], loc3[1]); e.rotation_euler = (0, 0, rotY)
    e.scale = s if isinstance(s, tuple) else (s, s, s); e.pass_index = idx; target.objects.link(e); return e
def resolve_asset(a):
    if a.startswith('models/ashen_v1/'): return ASH + a[len('models/ashen_v1/'):]
    return REPO + a
# ---------- ground ----------
import bmesh
if ZONE == 'coast':
    cw = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/coast_world_after_v2.json')); T = cw['tiles']
    TC = {0:(.10,.10,.075),1:(.09,.09,.07),2:(.13,.10,.075),3:(.21,.19,.155),4:(.18,.165,.135),5:(.14,.14,.145),6:(.12,.105,.09),7:(.15,.14,.13),8:(.025,.04,.05),9:(.20,.13,.07)}
    mats = {k: mat('t%d' % k, c, rough=(.25 if k == 8 else .95)) for k, c in TC.items()}
    me = bpy.data.meshes.new('ground'); ob = bpy.data.objects.new('ground', me); C_BASE.objects.link(ob); ob.pass_index = 2
    keys = sorted(mats); [me.materials.append(mats[k]) for k in keys]
    bm = bmesh.new()
    for ty in range(H):
        for tx in range(W):
            t = T[ty * W + tx]; z = -.18 if t == 8 else 0
            f = bm.faces.new([bm.verts.new((tx + dx, -(ty + dy), z)) for dx, dy in ((0, 0), (1, 0), (1, 1), (0, 1))]); f.material_index = keys.index(t if t in TC else 1)
    bm.to_mesh(me); bm.free()
    # engine ocean: 520x520 plane centred on map at y=-0.4 (placeOcean)
    bpy.ops.mesh.primitive_plane_add(size=520, location=(W / 2, -H / 2, -.4)); oc = bpy.context.object
    for c in list(oc.users_collection): c.objects.unlink(oc)
    C_BASE.objects.link(oc); oc.data.materials.append(mat('ocean', (.012, .03, .036), rough=.25)); oc.pass_index = 1
    # A0 interior props are omitted: they do not change edge coverage.
    # BEFORE: live ring (42x56 rect ring, workaround: centred z=28, near_sea_S pushed +56)
    ring = load(REPO + 'models/outdoor/v5_maps/rect/backdrop_near_rect_coast_dead.glb')
    sea = set('EWS')
    for o in list(ring.objects):
        n = o.name.split('.')[0]; vis = None
        for s in 'ENWS':
            if n in ('near_land_' + s, 'apron_' + s): vis = (s not in sea)
            if n == 'near_sea_' + s: vis = (s in sea)
        if vis is False: o.hide_render = True
        if n == 'near_sea_S' and o.parent is None: o.location.y -= (H - 56)  # three z += 56
    inst(ring, (W / 2, 0, 28), 0, 1, C_BEFORE, 3)
    SEASON = 'dead'
else:
    ms = json.load(open('/workspace/sanctuary_env/world_v1/exits/work/v2in/martsirt_world_v2.json')); ox, oz = ms['origin']
    pl = json.load(open('/workspace/sanctuary_env/martsirt_v2_2/placements.json'))['placements']
    bpy.ops.mesh.primitive_plane_add(size=1, location=(W / 2, -H / 2, 0)); g = bpy.context.object; g.scale = (W, H, 1)
    for c in list(g.users_collection): c.objects.unlink(g)
    C_BASE.objects.link(g); g.data.materials.append(mat('townground', (.085, .075, .06))); g.pass_index = 2
    for p in pl:
        if p['kind'] == 'interactable': continue
        c = load(REPO + p['piece'])
        x, y, z = p['pos']; inst(c, (x + ox, y, z + oz), p.get('rotY', 0), 1, C_BASE, 2)
    SEASON = 'autumn'
# ---------- AFTER: kit + border props ----------
kits = {}
for p in LAY['pieces']:
    st = p['style']
    if st not in kits:
        c = load(HERE + 'glb/bk_%s_%s.glb' % (st, SEASON)); kits[st] = {}
        # split into per-piece collections (root nodes named after pieces)
        for o in list(c.objects):
            if o.parent is None:
                pc = bpy.data.collections.new('%s_%s' % (st, o.name.split('.')[0]))
                stack = [o]
                while stack:
                    q = stack.pop(); pc.objects.link(q); stack += list(q.children)
                o.location = (0, 0, 0); o.rotation_euler = (0, 0, 0) if o.rotation_mode == 'XYZ' else o.rotation_euler
                kits[st][o.name.split('.')[0]] = pc
    pc = kits[st].get(p['piece'])
    if pc is None: print('NO PIECE', st, p['piece']); continue
    inst(pc, p['pos'], p['rotY'], (p['scaleX'], 1, 1), C_AFTER, 3)
for q in LAY['props']:
    c = load(resolve_asset(q['asset']))
    inst(c, q['pos'], q['rotY'], q['scale'], C_AFTER, 4)
# ---------- light / render ----------
sun = bpy.data.lights.new('moon', 'SUN'); sun.energy = 1.2; sun.color = (.6, .66, .8)
so = bpy.data.objects.new('moon', sun); so.rotation_euler = (math.radians(45), 0, math.radians(-35)); sc.collection.objects.link(so)
wd = bpy.data.worlds.new('w'); sc.world = wd; wd.use_nodes = True
bg = wd.node_tree.nodes['Background']; bg.inputs[0].default_value = (.03, .033, .04, 1); bg.inputs[1].default_value = 1
# world must not count as a hit: use holdout via film transparent + alpha
sc.render.film_transparent = True
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 6 if QUICK else 10; sc.cycles.use_denoising = False
sc.cycles.max_bounces = 2
sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = 1.6
vl = sc.view_layers[0]; vl.use_pass_z = True; vl.use_pass_object_index = True; vl.use_pass_position = True
sc.use_nodes = True; nt = sc.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
rl = nt.nodes.new('CompositorNodeRLayers'); fo = nt.nodes.new('CompositorNodeOutputFile')
fo.format.file_format = 'OPEN_EXR'; fo.format.color_depth = '32'; fo.base_path = '/tmp/proof_exv2_%s/' % ZONE
fo.file_slots.clear()
for nm in ('Image', 'Depth', 'IndexOB', 'Position'):
    fo.file_slots.new(nm); nt.links.new(rl.outputs[nm], fo.inputs[nm])
comp = nt.nodes.new('CompositorNodeComposite'); nt.links.new(rl.outputs['Image'], comp.inputs['Image'])
def srgb2lin(c): c = c / 255.0; return ((c + .055) / 1.055) ** 2.4 if c > .04045 else c / 12.92
CLEAR = (7, 8, 12)
GAIN = float(os.environ.get('GAIN', '3.0'))
FOG = (7, 8, 12) if ZONE == 'coast' else (16, 19, 26)
runs = LAY['runs']
EDGE_PIECES = {e: [] for e in 'NESW'}; CORNER_LAND = {}
for p_ in LAY['pieces']:
    if p_['piece'].startswith('corner'):
        x_, z_ = p_['pos'][0], p_['pos'][2]
        CORNER_LAND[('N' if z_ < H / 2 else 'S') + ('W' if x_ < W / 2 else 'E')] = p_['style'] != 'sea'
    else: EDGE_PIECES[p_['edge']].append((p_['walk_t'], p_['walk_t'] + p_['length_m'], p_['style'], p_['piece']))
def land_required(x, z):
    """x,z three coords outside map -> True when the border piece in front of it is a full-height land piece.
    sea pieces, endcap transitions and the open 6 m of a pass (neighbour scenery fills it via the seam) are exempt."""
    inx, inz = 0 <= x <= W, 0 <= z <= H
    if not inx and not inz:
        return CORNER_LAND.get(('N' if z < 0 else 'S') + ('W' if x < 0 else 'E'), True)
    if inx: e, t = ('N', x) if z < 0 else ('S', W - x)
    else: e, t = ('W', H - z) if x < 0 else ('E', z)
    for a_, b_, st, pc in EDGE_PIECES[e]:
        if a_ - 1e-6 <= t <= b_ + 1e-6:
            if st == 'sea' or pc.startswith('endcap'): return False
            if pc == 'pass12' and abs(t - (a_ + b_) / 2) < 3: return False
            return True
    return True
def load_exr(path):
    im = bpy.data.images.load(path); a = np.array(im.pixels[:], dtype=np.float32).reshape(im.size[1], im.size[0], im.channels)[::-1]
    bpy.data.images.remove(im); return a
views = []
inset = 1.0
pts = {'NW': (inset, inset, (-1, -1)), 'N': (W / 2, inset, (0, -1)), 'NE': (W - inset, inset, (1, -1)), 'E': (W - inset, H / 2, (1, 0)),
       'SE': (W - inset, H - inset, (1, 1)), 'S': (W / 2, H - inset, (0, 1)), 'SW': (inset, H - inset, (-1, 1)), 'W': (inset, H / 2, (-1, 0))}
if ZONE == 'coast':  # also the south-half E/W edges the workaround leaves bare
    pts['E_south'] = (W - inset, 84, (1, 0)); pts['W_south'] = (inset, 100, (-1, 0))
# exits_v2: look straight out through each moved exit (pass12 fallback + ring either side)
if ZONE == 'coast': pts['EXIT_town'] = (12.5, 2.0, (0, -1))
else: pts['EXIT_coast'] = (49.6, H - 2.0, (0, 1))
for name, (hx, hz, u) in pts.items():
    for dist in (14, 40):
        for orient in ('portrait', 'landscape'):
            views.append((name, hx, hz, u, dist, orient))
cd = bpy.data.cameras.new('cam'); co = bpy.data.objects.new('cam', cd); sc.collection.objects.link(co); sc.camera = co
cd.sensor_fit = 'VERTICAL'; cd.angle = math.radians(38); cd.clip_start = 1.0; cd.clip_end = 400
results = []
LIMIT = int(os.environ.get('LIMIT', '0'))
if LIMIT: views = [v for v in views if v[0] in os.environ.get('ONLY', v[0]).split(',')][:LIMIT]
RES = {'portrait': (300, 650), 'landscape': (650, 300)}
for state in ('before', 'after'):
    C_BEFORE.hide_render = state != 'before'; C_AFTER.hide_render = state != 'after'
    for name, hx, hz, u, dist, orient in views:
        ux, uz = u; yaw = math.atan2(-ux, -uz)  # view dir = -(sin yaw, cos yaw) == outward
        o = dist * math.cos(math.radians(50)); s = dist * math.sin(math.radians(50))
        cam3 = (hx + math.sin(yaw) * o, s, hz + math.cos(yaw) * o)
        co.location = (cam3[0], -cam3[2], cam3[1])
        co.rotation_euler = (Vector((hx, -hz, 1.15)) - co.location).to_track_quat('-Z', 'Y').to_euler()
        if ZONE == 'coast': near, far = 16 + (dist - 14), 46 + (dist - 14)
        else: near, far = 30, 110
        rx, ry = RES[orient]; sc.render.resolution_x, sc.render.resolution_y = rx, ry
        tag = '%s_%s_d%d_%s' % (state, name, dist, orient)
        sc.render.filepath = '/tmp/proof_exv2_%s/_c.png' % ZONE
        for f in os.listdir(fo.base_path) if os.path.exists(fo.base_path) else []: os.remove(fo.base_path + f)
        bpy.ops.render.render(write_still=False)
        fl = {f[:f.rfind('0')].rstrip('0') if False else f.split('0')[0]: f for f in os.listdir(fo.base_path)}
        def get(k):
            f = [x for x in os.listdir(fo.base_path) if x.startswith(k)][0]; return load_exr(fo.base_path + f)
        img = get('Image'); dep = get('Depth')[..., 0]; idx = get('IndexOB')[..., 0]; pos = get('Position')[..., :3]
        alpha = img[..., 3]
        hit = alpha > 0.5
        # analytic ground-plane depth for every pixel
        M = co.matrix_world; fwd = -(M.to_3x3() @ Vector((0, 0, 1))); fwd.normalize()
        th = math.tan(math.radians(19)); aspect = rx / ry
        yy, xx = np.mgrid[0:ry, 0:rx]
        ndx = ((xx + .5) / rx * 2 - 1) * th * aspect; ndy = (1 - (yy + .5) / ry * 2) * th
        R3 = np.array(M.to_3x3()); dirs = (R3 @ np.stack([ndx, ndy, -np.ones_like(ndx)], -1)[..., None])[..., 0]
        camz = co.location.z; dz = dirs[..., 2]
        tg = np.where(dz < -1e-6, -camz / np.minimum(dz, -1e-6), np.inf)
        gdepth = tg * 1.0  # dirs built with z=-1 in camera space -> t is planar depth already
        void = (~hit) & (gdepth < 0.9 * far)
        gap = np.zeros_like(void)
        if ZONE == 'coast':
            cam = np.array(co.location)
            P = cam + dirs * dep[..., None]  # planar depth * (dir with cam-space z=-1)
            oc_hit = hit & (np.abs(P[..., 2] + 0.4) < 0.08) & (dep < 0.9 * far)
            px, pz = P[..., 0], -P[..., 1]
            outside = (px < -0.3) | (px > W + .3) | (pz < -0.3) | (pz > H + .3)
            cand = np.argwhere(oc_hit & outside)
            for (j, i) in cand[::1]:
                if land_required(px[j, i], pz[j, i]): gap[j, i] = True
        # composite three.js fog (linear in view depth); empty pixels = clear colour
        fogc = np.array([srgb2lin(c) for c in FOG], np.float32); clr = np.array([srgb2lin(c) for c in CLEAR], np.float32)
        f = np.clip((dep - near) / (far - near), 0, 1)[..., None]
        col = np.clip(img[..., :3] * GAIN, 0, 1) * (1 - f) + fogc * f
        col = np.where(hit[..., None], col, clr)
        out = col.copy()
        mk = void | gap
        out[mk] = out[mk] * .35 + np.array([1, 0, 1], np.float32) * .65
        out = np.clip(out, 0, 1); out = np.where(out <= .0031308, out * 12.92, 1.055 * np.power(out, 1 / 2.4) - .055)
        rgba = np.concatenate([out, np.ones_like(out[..., :1])], -1)[::-1]
        im = bpy.data.images.new(tag, rx, ry, alpha=True); im.pixels = rgba.ravel().tolist()
        im.filepath_raw = os.path.join(OUT, tag + '.png'); im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im)
        r = dict(state=state, view=name, dist=dist, orient=orient, yaw_deg=round(math.degrees(yaw), 1), fog=[near, far],
                 void_pct=round(100 * void.mean(), 2), dark_gap_pct=round(100 * gap.mean(), 2), file=tag + '.png')
        results.append(r); print('VIEW', r, flush=True)
json.dump(results, open(os.path.join(OUT, 'proof_results.json'), 'w'), indent=1)
print('DONE')
