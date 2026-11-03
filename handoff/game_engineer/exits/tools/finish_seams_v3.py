"""exits_v3: annotate the regenerated seams for the pairs the mirror touches; write <pair>_v3.json + seams_index_v3.json
(= seams_index_v2.json with those pairs pointing at the _v3 files)."""
import json, os
V2 = '/workspace/sanctuary_env/world_v1/exits/v2/seams/'
WHY = {
 'briarE__wild': 'v2 had wild W edge <-> briarE W edge (rot 180): you left wild westward and walked in on briarE\'s WEST side. v3 mirrors briarE: wild W edge <-> briarE E edge, opposite edges, pure translation.',
 'briarE__duneW': 'briarE and duneW both mirrored: briarE W edge <-> duneW E edge (was briarE E <-> duneW W). Same road, same offsets mirrored.',
 'desert__duneW': 'duneW and desert both mirrored: duneW W edge <-> desert E edge (was duneW E <-> desert W).',
 'desert__lut': 'desert mirrored: its N-edge cut to Qadren moves from x 27.4 to x 8.6 (still N edge). lut unchanged (S gate).',
}
idx = json.load(open(V2 + 'seams_index_v2.json')); new = {e['file'][:-5]: e for e in json.load(open('seams_index.json'))}
out = []
for p, why in WHY.items():
    r = json.load(open(p + '.json')); v2f = p + ('_v2' if os.path.exists(V2 + p + '_v2.json') else '') + '.json'; v2 = json.load(open(V2 + v2f))
    r['exits_v3'] = dict(version='exits_v3', supersedes='seams/' + v2f, why=why,
                         was=dict(edges='%s|%s' % (v2['zone_a']['edge'], v2['zone_b']['edge']), rot_deg=v2['transform']['b_to_a']['rot_deg']),
                         now=dict(edges='%s|%s' % (r['zone_a']['edge'], r['zone_b']['edge']), rot_deg=r['transform']['b_to_a']['rot_deg']),
                         apply='inert until the matching handoff/game_engineer/exits/*_exits_patch_v3.json are applied (briarE, duneW, desert mirror + wild, lut arrivals)')
    for s in 'ab':
        if 'proposal_note' in r['zone_' + s]:
            r['zone_' + s]['proposal_note'] = 'SUPERSEDED: exits are placed on purpose (exits_v2/v3)'; r['zone_' + s]['proposed_offset_m'] = None
    json.dump(r, open(p + '_v3.json', 'w'), indent=1)
    print(p, r['exits_v3']['was'], '->', r['exits_v3']['now'], 'mismatch', r['transform']['orientation_mismatch'])
for e in idx:
    k = e['file'][:-5].replace('_v2', '')
    if k in WHY: e = dict(new[k]); e['file'] = k + '_v3.json'; e['exits_v3'] = 'regenerated (mirror)'
    out.append(e)
json.dump(out, open('seams_index_v3.json', 'w'), indent=1)
print(len(out), [e['file'] for e in out if 'exits_v3' in e])
