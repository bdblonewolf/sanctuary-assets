import json,struct,glob,os,subprocess
R='/workspace/sanctuary_env/props_new'
def rd(p):
    b=open(p,'rb').read(); L=struct.unpack('<I',b[12:16])[0]; return json.loads(b[20:20+L])
val={}
out=subprocess.run(['node',R+'/src/validate.js']+sorted(glob.glob(R+'/*.glb')+glob.glob(R+'/breakables/*.glb')+glob.glob(R+'/lite/*.glb')),capture_output=True,text=True).stdout
for l in out.splitlines():
    if l.split('\t')[0].endswith('.glb'): p=l.split(); val[p[0]]=int(p[p.index('tris')+1])
def bbox(j):
    import numpy as np
    def M(n):
        import math
        T=np.eye(4)
        if 'matrix' in n: return np.array(n['matrix']).reshape(4,4).T
        t=n.get('translation',[0,0,0]); r=n.get('rotation',[0,0,0,1]); s=n.get('scale',[1,1,1])
        x,y,z,w=r; Rm=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
        T[:3,:3]=Rm*np.array(s); T[:3,3]=t; return T
    mn=np.full(3,1e9); mx=np.full(3,-1e9)
    def walk(i,P):
        n=j['nodes'][i]; W=P@M(n)
        if 'mesh' in n and not n.get('name','').startswith('col_'):
            for pr in j['meshes'][n['mesh']]['primitives']:
                a=j['accessors'][pr['attributes']['POSITION']]
                for cx in range(8):
                    c=[a['max'][k] if (cx>>k)&1 else a['min'][k] for k in range(3)]
                    v=(W@np.array([*c,1]))[:3]; mn[:]=np.minimum(mn,v); mx[:]=np.maximum(mx,v)
        for c in n.get('children',[]): walk(c,W)
    for r in j['scenes'][0]['nodes']: walk(r,np.eye(4))
    return mn,mx
ST={ # status, source
'map_board_known_roads':('NEW','nothing suitable existed (hanging_sign_v1 is a wall sign); textures painted from repo map names'),
'rowboat_ferry':('DERIVED','props_gothic_v1 longship: same hull.py clinker generator + m_hull_tarred/wood materials, scaled to a 4 m rowboat'),
'well_stone':('NEW + REUSED part','no well existed; bucket = decimated Poly Haven wooden_bucket_01 (CC0, local assets3d)'),
'well_stone_heal':('DERIVED','from well_stone + runes_e emissive band, glowing water'),
'trapdoor_ashen_coast':('DERIVED','inn bld_inn_salted_kettle_shared cellar_hatch footprint (col_cellar_hatch 1.2 x 1.0 m; inn has no hatch mesh) + inn soot stone'),
'cart':('DERIVED','footprint/scale from models/town/martsirt/props/prop_cart_broken.glb (bed ~2.0 x 1.4 m); rebuilt so both states match and wheels are pivot nodes'),
'wardrobe':('NEW','no wardrobe/cabinet in repo or workspace (KayKit only cartoon)'),
'nightstand':('NEW','none existed'),
'desk':('DERIVED','Poly Haven wooden_table_02 (CC0) rescaled + drawer/papers/ink/candle'),
'rug':('NEW','none existed; texture from Poly Haven fabric + painted medallion'),
'urn_a':('DERIVED','break method from props_gothic_v1 loot/burial_urn (jagged lathe, shards, ash)'),'urn_b':('DERIVED','as urn_a'),'urn_c':('DERIVED','as urn_a (amphora with handles)'),
'weapon_rack':('DERIVED + REUSED','layout from props_gothic_v1 weapon_rack_wreck; weapons = decimated copies of models/weapons/weapon_mourning_spear, weapon_briar_hatchet, characters_art/monsters/swordsman sword, characters_art/props/kite_shield_sanctuary (originals untouched)'),
'barrel':('NEW','replaces modular_dungeon_kit BarrelClosed_01/02/03 + BarrelBroken_01/02, and single uses of characters_art/props/wine_barrel_01_sanctuary.glb'),
'barrel_group':('DERIVED','layout of models/town/martsirt_v2_2/props/prop_barrel_group.glb (3 barrels, placements market_barrels, inn_barrels) -> replaces it'),
'crate':('NEW','single breakable crate (dungeons currently draw kit barrels as crates)'),
'crate_stack':('DERIVED','size of models/town/martsirt_v2_2/props/prop_crate_stack.glb (placement forge_crates, inn.json) -> replaces it'),
'sack':('NEW','single sack'),
'sack_pile':('DERIVED','props_gothic_v1 loot/sack_pile_closed/opened -> replaces them as a breakable pair'),
'iron_chest_lite':('DERIVED (lite)','decimated from props_gothic_v1 iron chest (24k -> 3k), opened = lid node rotated'),
'bookshelf_worn_lite':('DERIVED (lite)','decimated from props_gothic_v1 bookshelf_worn'),
'shrine_basic_lite':('DERIVED (lite)','decimated from batch1_interactables/v4/shrine_basic'),
'shrine_weeping_angel_lite':('DERIVED (lite)','decimated from batch1_interactables/v4/shrine_weeping_angel'),
'pier_lite':('DERIVED (lite)','decimated from local Poly Haven pier (not a repo file); modular sections kept in source layout'),
}
def key(f):
    b=os.path.basename(f)[:-4]
    for s in ('_closed','_opened','_intact','_broken'):
        if b.endswith(s): b=b[:-len(s)]
    return b
rows=[]
for sub in ('','breakables/','lite/'):
    for f in sorted(glob.glob(f'{R}/{sub}*.glb')):
        j=rd(f); mn,mx=bbox(j); d=mx-mn
        nodes=[n['name'] for n in j['nodes'] if 'name' in n]
        piv=[n for n in nodes if not n.startswith('col_') and n!=os.path.basename(f)[:-4]]
        cols=[n for n in nodes if n.startswith('col_')]
        st=ST.get(key(f),('?',''))[0]
        rows.append(f"| `{sub}{os.path.basename(f)}` | {val.get(os.path.basename(f),'?')} | {os.path.getsize(f)/1e6:.2f} | {d[0]:.2f} x {d[1]:.2f} x {d[2]:.2f} | {mn[1]:+.2f} | {', '.join(piv)} | {', '.join(cols)} | {st} |")
src='\n'.join(f'- **{k}**: {v[0]}: {v[1]}' for k,v in ST.items())
open(R+'/README.md','w').write(f'''# props_new: game-ready props (v1)

Plain GLB (no extensions), 1 unit = 1 m, Y up, front +Z, base y=0 (the well shaft, trapdoor shaft and ladder go below 0 on purpose). No lights or cameras; emissive <= 1.0.
Textures are Poly Haven CC0 (512 px, map/rug 1k). Validated with gltf-validator (0 errors; the only warnings are MESH_PRIMITIVE_GENERATED_TANGENT_SPACE) and loaded with three.js GLTFLoader (38/38 OK).
`col_*` nodes are invisible box colliders (hide or replace with physics boxes). `col_click` = pick volume. Stone and massing are rounded rubble; only crafted planks are flat.

Previews: `previews/props_new_lineup.png`, `previews/props_new_breakables_lineup.png`.

## Files
Size = W x H x D in m (glTF X, Y, Z, visual meshes only). Ymin < 0 = geometry below the floor (shafts).

| file | tris | MB | size m | Ymin | nodes (pivots/anchors) | colliders | status |
|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Pivots and anchors
- **trapdoor_ashen_coast**: node `lid` origin = hinge on the back edge (glTF -Z side). Open = rotate about local X by -112° (the `_opened` file is exactly that pose). Also `hinge` and `nav_down` (`dest=ashen_coast`) empties. Place the root on the inn node `cellar_hatch` (5.2, 0.06, 4.3); it covers the same 1.2 x 1.0 m as `col_cellar_hatch`. The inn has no hatch mesh, so this is the visual.
- **cart**: `wheel_L` (+X) and `wheel_R` (-X) origins = axle centre (y 0.5); spin about local X. `axle` and `hitch` (shaft tips) empties. Broken: `wheel_L` is detached and lying flat.
- **well_stone / well_stone_heal**: node `bucket` origin = rope top under the winch (y 1.68). Lower it by translating -Y (up to ~1.6 m into the shaft). Heal: the `fx_heal_glow` empty is for a point light or particles (#40d9b3).
- **rowboat_ferry**: `oar_L` and `oar_R` pivot at the oarlocks. `waterline` empty (y 0.2): sink the boat so it sits at the water surface. Also `seat_rower`, `seat_passenger` and `player_board`. Bow faces -Z.
- **map_board_known_roads**: `map_slot` is a separate 1.5 x 1.0 m quad with its own material `m_map_slot` (UV 0..1), so you can swap its texture at runtime. `interact` stand point.
- **wardrobe**: `door_L` and `door_R` origins on the outer hinge edges; rotate about Y. **nightstand**: `drawer` slides +Z. `fx_candle` on the nightstand and the desk.
- **weapon_rack**: each weapon is its own `loot_*` node (spear, hatchet, sword, shield), so you can hide it on pickup.
- **Breakables**: swap `_intact` for `_broken` at the same transform. `_broken` has no blocking collider, only `col_click`. glTF extras on the root: `state`, `pair`, `replaces`.

## Player room (inn north upstairs hall, upper floor y=3.5, about 15.4 x 5.3 m, ~2.8 m headroom)
wardrobe 1.26 x 2.11 x 0.71 | nightstand 0.54 x 0.6 (0.86 with candle) x 0.46 | desk 1.29 x 0.76 x 0.71 | rug 2.4 x 1.6 | plus the existing bed and `iron_chest_lite` as the stash. Everything fits between the north windows (z -6.42) and the corridor partition (z -1.0).

## Breakable replacements (originals untouched)
| pair | replaces |
|---|---|
| breakables/barrel_* | `models/modular_dungeon_kit.glb` BarrelClosed_01/02/03 + BarrelBroken_01/02; single uses of `characters_art/props/wine_barrel_01_sanctuary.glb` (inn.json) |
| breakables/barrel_group_* | `models/town/martsirt_v2_2/props/prop_barrel_group.glb` (+ martsirt, martsirt_v2 copies); placements market_barrels, inn_barrels |
| breakables/crate_* | crate stand-ins (dungeons draw kit barrels as crates) |
| breakables/crate_stack_* | `models/town/martsirt_v2_2/props/prop_crate_stack.glb`; placement forge_crates, inn.json |
| breakables/sack_* | new single sack |
| breakables/sack_pile_* | `models/env_extra/props_gothic_v1/loot/sack_pile_closed/opened.glb` |
| breakables/urn_a/b/c_* | new (method from loot/burial_urn) |
| breakables/weapon_rack_* | new (layout from loot/weapon_rack_wreck) |

## Reuse status (searched repo models/, characters_art/props/, wip_models/, /workspace/sanctuary_env, /workspace/sanctuary_art, local Poly Haven/KayKit)
{src}

KayKit Dungeon had barrels, crates, tables and shelves, but it is a cartoon style, so it was not used.
Build scripts: `src/build_new.py`, `src/build_lite.py` (Blender 4.2). Not wired into the game: no placements or JSONs were edited.
''')
print(len(rows))
