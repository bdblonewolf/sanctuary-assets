"""exits_v3 step 2 (after build_v3.py): add points_move to the v3 patches of the mirrored zones. Applies each patch (without
points_move) to the full generated world (world_rich.json, dumped from the live bundle copy by dump_rich.mjs), then
pick_moves_v3.py picks a new open, reachable tile for every enemy spawn / nest / route point / critter on a blocked one."""
import json, subprocess
ZS = ['wild', 'briarE', 'duneW', 'desert', 'lut']
js = """const fs=require('fs');const {applyExitsPatch}=require('./out/apply_exits_patch.js');const W=JSON.parse(fs.readFileSync('world_rich.json')).worlds;const o={};
for(const z of %s){const w=JSON.parse(JSON.stringify(W[z]));const p=JSON.parse(fs.readFileSync('out_v3/'+z+'_exits_patch_v3.json'));delete p.points_move;applyExitsPatch(w,p);o[z]=w;}
fs.writeFileSync('v3in/v3rich_nomoves.json',JSON.stringify(o));""" % json.dumps(ZS)
subprocess.run(['node', '-e', js], check=True)
subprocess.run(['python3', 'pick_moves_v3.py', 'v3in/v3rich_nomoves.json', 'v3in/moves_v3.json'], check=True)
M = json.load(open('v3in/moves_v3.json'))
for z in ZS:
    f = 'out_v3/%s_exits_patch_v3.json' % z; p = json.load(open(f)); p.pop('points_move', None)
    if M.get(z): p['points_move'] = M[z]
    json.dump(p, open(f, 'w'), indent=1); print(z, len(M.get(z, [])), 'moves')
