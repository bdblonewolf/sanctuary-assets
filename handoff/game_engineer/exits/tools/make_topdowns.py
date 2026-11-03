"""exits_v2 before/after top-downs. Red box = exit trigger (label = destination), cyan dot = where you arrive in this zone
(from the other zone's exit sx/sy), white dots = props, dark = solid, orange line = new road. Left BEFORE (live), right AFTER (exits_v2)."""
import json, copy, os
from PIL import Image, ImageDraw
import topdown, mts
OUT = '/workspace/sanctuary_env/world_v1/exits/v2/topdown/'; os.makedirs(OUT, exist_ok=True)
WF = json.load(open('world_full.json'))['worlds']; V2 = json.load(open('v2in/worlds_v2.json')); AUD = json.load(open('/workspace/sanctuary/design/audit/worlds.json'))
def arrivals(G, z):
    return [(o, e['sx'], e['sy']) for o in G for e in G[o].get('exits', []) if e['to'] == z and e.get('sx') is not None]
def label(im, t):
    d = ImageDraw.Draw(im); H = im.height; d.rectangle([0, H - 16, 8 * len(t) + 8, H], fill=(0, 0, 0)); d.text((4, H - 13), t, fill=(255, 255, 255)); return im
def pair(b, a, title, fn):
    W_ = b.width + a.width + 12; c = Image.new('RGB', (W_, max(b.height, a.height) + 22), (20, 20, 20)); d = ImageDraw.Draw(c)
    d.text((4, 4), title, fill=(255, 255, 0)); c.paste(label(b, 'BEFORE (live)'), (0, 22)); c.paste(label(a, 'AFTER exits_v2'), (b.width + 12, 22)); c.save(OUT + fn); print(fn, c.size)
def tile_zone(z, after, S):
    topdown.W[z] = after; im = topdown.draw(z, S); d = ImageDraw.Draw(im)
    return im
for z in ['coast', 'wild', 'desert', 'mires', 'briarE', 'lut', 'sink']:
    bw = WF[z]; aw = json.load(open('after_%s.json' % z)) if os.path.exists('after_%s.json' % z) else dict(copy.deepcopy(bw), exits=V2[z]['exits'])
    S = 6 if bw['w'] > 60 or bw['h'] > 60 else 10
    ims = []
    for w, G in ((bw, AUD), (aw, V2)):
        topdown.W[z] = w; im = topdown.draw(z, S); d = ImageDraw.Draw(im)
        for o, x, y in arrivals(G, z):
            d.ellipse([x * S - 5, y * S - 5, x * S + 5, y * S + 5], outline=(0, 255, 255), width=2); d.text((x * S + 6, y * S + 2), 'from ' + o, fill=(0, 255, 255))
        ims.append(im)
    if z == 'coast': ims = [i.crop((0, 0, i.width, 40 * S)) for i in ims]  # A0 north half (seam side)
    pair(ims[0], ims[1], '%s  exits_v2 before/after  (red=exit, cyan=arrival, white=props, dark=solid)' % z, '%s_exits_before_after.png' % z)
# Martsirt (uses the live 3D-town renderer: roads, buildings, gate-camp LIFE props in magenta, border props green, pass12 red)
LB = json.load(open('/workspace/sanctuary_env/world_v1/border_kit/out/layout_martsirt.json')); LA = json.load(open('/workspace/sanctuary_env/world_v1/border_kit/out/layout_martsirt_v2.json'))
P = json.load(open('out/martsirt_exits_patch.json')); MV = json.load(open('v2in/martsirt_world_v2.json'))
crop = (20, 104, 140, 156)
b = mts.draw(8, crop, border=LB)
a = mts.draw(8, crop, exits=MV['exits'], arrive=MV['arrive'], extra_roads=P['roads_add'], border=LA)
pair(b, a, 'martsirt S edge  exits_v2 before/after  (orange=new coast trail, red box=exit, cyan=arrivals, magenta=gate-camp props, green=border props, red sq=pass12)', 'martsirt_exits_before_after.png')
b = mts.draw(3, border=LB); a = mts.draw(3, exits=MV['exits'], arrive=MV['arrive'], extra_roads=P['roads_add'], border=LA)
pair(b, a, 'martsirt full', 'martsirt_full_before_after.png')
