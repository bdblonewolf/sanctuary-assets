"""exits_v3 top-downs for the mirrored zones. Left = exits_v2 (5e55a62), right = exits_v3. Red box = exit (label = destination),
cyan dot = where you arrive (from the other zone's exit sx/sy), white dots = props, dark = solid. North up, west left."""
import json, copy, os
from PIL import Image, ImageDraw
import topdown
OUT = '/workspace/sanctuary_env/world_v1/exits/v3/topdown/'; os.makedirs(OUT, exist_ok=True)
WF = json.load(open('world_full.json'))['worlds']; V2 = json.load(open('v2in/worlds_v2.json')); V3 = json.load(open('v3in/worlds_v3.json'))
A3 = json.load(open('v3in/after_v3.json'))
def arrivals(G, z): return [(o, e['sx'], e['sy']) for o in G for e in G[o].get('exits', []) if e['to'] == z and e.get('sx') is not None]
def label(im, t):
    d = ImageDraw.Draw(im); H = im.height; d.rectangle([0, H - 16, 8 * len(t) + 8, H], fill=(0, 0, 0)); d.text((4, H - 13), t, fill=(255, 255, 255)); return im
for z in ['briarE', 'duneW', 'desert']:
    v2w = json.load(open('after_%s.json' % z)) if os.path.exists('after_%s.json' % z) else dict(copy.deepcopy(WF[z]), exits=V2[z]['exits'])
    S = 10; ims = []
    for w, G in ((v2w, V2), (A3[z], V3)):
        topdown.W[z] = w; im = topdown.draw(z, S); d = ImageDraw.Draw(im)
        for o, x, y in arrivals(G, z):
            d.ellipse([x * S - 5, y * S - 5, x * S + 5, y * S + 5], outline=(0, 255, 255), width=2); d.text((x * S + 6, y * S + 2), 'from ' + o, fill=(0, 255, 255))
        ims.append(im)
    b, a = ims; c = Image.new('RGB', (b.width + a.width + 12, max(b.height, a.height) + 22), (20, 20, 20)); d = ImageDraw.Draw(c)
    d.text((4, 4), '%s  exits_v2 -> exits_v3 (mirrored; N up, W left; wild is EAST)' % z, fill=(255, 255, 0))
    c.paste(label(b, 'exits_v2 (5e55a62)'), (0, 22)); c.paste(label(a, 'exits_v3'), (b.width + 12, 22)); c.save(OUT + '%s_exits_v2_v3.png' % z); print(z, c.size)
