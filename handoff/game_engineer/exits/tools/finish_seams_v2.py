"""exits_v2: annotate the regenerated seams for the pairs the exits re-plan touches and write <pair>_v2.json + seams_index_v2.json."""
import json, os
R = {
 'town':   ('moved', [81, 152], 'S gate stays the way out; a 4 m dirt trail bears W under the palisade to the SW corner (49.6,152.4). Off-centre so the town road and the coast A0 path meet at the same t~0.30, and the S gate approach is no longer a straight shot down the middle.'),
 'coast':  ('moved', [20.2, 1.2], 'Ashen A0 dirt path already climbs to the NW; the trigger now sits at its top (12.5,1.2) instead of a bare edge-centre stub.'),
 'wild':   ('moved', [70.4, 27.2], 'P1: The Narrow (briarE) lies WEST of Briarwood on the continent; the existing E-W highway on rows 26-28 now runs west over a 3-wide bridge causeway to the W edge. Near-centre is natural here: it is where the highway already is.'),
 'briarE': ('kept', None, "briarE's W-edge exit (1.4,20.2) already sits where its ridge road starts and lines up with Briarwood's W exit under the 180 deg placement; only the arrival sx/sy changed (3.4,27.5)."),
 'desert': ('moved', [27.4, 5.6], 'P2: Qadren (lut) is flush N of the basin; the trigger moved from 5 tiles inside the N wall to the edge through a cut in the ridge.'),
 'lut':    ('kept', None, "Qadren's S gate (14.2,22.4) stays on its main street axis; only the arrival sx/sy changed (27.4,3.4)."),
 'mires':  ('moved', [9.2, 15.2], 'P3: the Sink sits flush against the mires W edge; a plank boardwalk now runs over the black water to the W edge.'),
 'sink':   ('kept', None, 'The Sink exit (14.2,21.2) is the climb out of the sinkhole; only the arrival sx/sy changed (3.4,15.5).'),
 'bastion': ('kept', None, 'Unchanged exit; only the scenery copied in from the coast N/NW ring changed (coast layout v2).'),
}
PAIRS = ['coast__martsirt', 'briarE__wild', 'desert__lut', 'mires__sink', 'bastion__coast']
idx = json.load(open('seams_index.json')); out = []
for p in PAIRS:
    r = json.load(open(p + '.json')); v1 = json.load(open('/workspace/sanctuary_env/world_v1/seams/' + p + '.json'))
    rev = {}
    for s in 'ab':
        zz = r['zone_' + s]; st, old, why = R[zz['id']]
        rev[zz['id']] = dict(status=st, old_exit_tile=old or zz['exit_tile'], new_exit_tile=zz['exit_tile'], why=why)
        if 'proposal_note' in zz:
            zz['proposal_note'] = 'SUPERSEDED by exits_v2 (pt101u): %s at this position on purpose - %s' % (st, why); zz['proposed_offset_m'] = None
    r['exits_v2'] = dict(version='exits_v2', source_owner_msg='pt101u: exits/entrances can be anywhere; whatever is more natural and flowing',
                         v1_file='seams/%s.json (kept, not overwritten)' % p, v1_kind=v1.get('kind'), review=rev,
                         inputs='worlds_v2 / world_extract_v2 / coast_world_after_v2 / martsirt_world_v2 / layout_{coast,martsirt}_v2 / terrain *_v2',
                         apply='inert until the matching handoff/game_engineer/exits/*_exits_patch.json is applied')
    json.dump(r, open(p + '_v2.json', 'w'), indent=1)
for e in idx:
    k = e['file'][:-5]
    e = dict(e)
    if k in PAIRS: e['file'] = k + '_v2.json'; e['exits_v2'] = 'regenerated'
    out.append(e)
json.dump(out, open('seams_index_v2.json', 'w'), indent=1)
print([e['file'] for e in out if 'exits_v2' in e])
