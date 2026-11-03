import json
o = json.load(open('../../v2/continent/continent_layout_core_v2.json')); d = json.load(open('continent_layout_core_v3.json'))
t2, t3 = o['zones']['town']['center'], d['zones']['town']['center']; zm = {}
for k in d['zones']:
    a, b = o['zones'][k], d['zones'][k]
    s = [round((b['center'][0] - t3[0]) - (a['center'][0] - t2[0]), 1), round((b['center'][1] - t3[1]) - (a['center'][1] - t2[1]), 1)]
    if max(map(abs, s)) > 0.5 or a['rot'] != b['rot']: zm[k] = dict(shift_m_rel_martsirt=s, rot=[a['rot'], b['rot']])
out = dict(note='exits_v3 continent check: gen_layout_v3 on worlds_v3 (briarE, duneW, desert mirrored). Same algorithm as v2. HOLD plan file itself is NOT rewritten.',
  west_road='Plan and game now agree: Martsirt -> wild -> (wild W edge) -> briarE -> duneW -> desert, each WEST of the last, all rot 0 (v2 needed rot 2 = 180deg, which the game cannot represent).',
  qadren_branch_divergence='lut, market, waste are towns and were NOT changed. Their live exits run lut E-> market E-> waste, so with the west road un-rotated the branch now runs EAST from lut, back over the west road. The HOLD plan (rot 2) had it running WEST. At later-grid sizes this gives the overlaps below. In-game chart is fine (row above the west road, no bump). Resolving it is a plan decision: (a) re-place the HOLD plan nodes (n_*) / pull the branch north, or (b) move lut/market/waste exits to the W side (contradicts Hesta: "East of the lamps, the Barrens begin"). Not done here.',
  overlaps=d['overlaps'], zones_moved=zm)
json.dump(out, open('continent_delta_v3.json', 'w'), indent=1); print(len(zm), out['overlaps'])
