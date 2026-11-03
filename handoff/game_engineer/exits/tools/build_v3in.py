"""exits_v3 inputs for the seam/terrain/layout generators: worlds_v2 + world_extract_v2 with briarE, duneW, desert mirrored
left<->right and the v3 exits (out_v3/*_exits_patch_v3.json exits_final)."""
import json, copy
A = json.load(open('v2in/worlds_v2.json')); E = json.load(open('v2in/world_extract_v2.json'))
MIR = ['briarE', 'duneW', 'desert']
for z in ['briarE', 'duneW', 'desert', 'wild', 'lut']:
    p = json.load(open('out_v3/%s_exits_patch_v3.json' % z))
    for f in p['exits_final']:
        e = next(q for q in A[z]['exits'] if q['to'] == f['to']); e.update({k: f[k] for k in ('x', 'y', 'sx', 'sy')})
for z in MIR:
    e = E['worlds'][z]; w, h = e['w'], e['h']
    e['tiles'] = [e['tiles'][y * w + (w - 1 - x)] for y in range(h) for x in range(w)]
    for k in ('props', 'npcs'):
        for p in e.get(k, []) or []:
            p['x'] = round(w - p['x'], 4)
            if p.get('style') in ('face-e', 'face-w'): p['style'] = {'face-e': 'face-w', 'face-w': 'face-e'}[p['style']]
    e['exits'] = copy.deepcopy(A[z]['exits'])
    for k in ('spawn',):
        if isinstance(e.get(k), dict): e[k]['x'] = round(w - e[k]['x'], 4)
json.dump(A, open('v3in/worlds_v3.json', 'w')); json.dump(E, open('v3in/world_extract_v3.json', 'w'))
print({z: [(q['to'], q['x'], q['y'], q.get('sx'), q.get('sy')) for q in A[z]['exits']] for z in ['wild', 'briarE', 'duneW', 'desert', 'lut']})
print({z: list(E['worlds'][z].keys()) for z in MIR})
