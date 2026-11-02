# Lootable corpses (Sanctuary)

Three static, unrigged corpse props, each with a NORMAL and a LOOTED variant. They are built **by reusing existing Sanctuary assets** (bodies, gear, props). Textures are the originals, downscaled 2048 to 1024 and re-saved as JPEG for size. The only new geometry is the stone wall block for `chained_prisoner`.

Conventions: glTF 2.0 binary, metres, Y up, ground at y = 0, facing +Z, origin at base centre. No animations or skins.

| File | Tris | Size | Dims W×D×H (m) | Reuses |
|---|---|---|---|---|
| `glb/fallen_adventurer.glb` | 2,580 | 0.64 MB | 1.60 × 1.80 × 0.61 | body, sword, closed sack |
| `glb/fallen_adventurer_looted.glb` | 2,479 | 0.72 MB | 1.48 × 1.80 × 0.57 | body, opened sack (sword removed) |
| `glb/gibbet_corpse.glb` | 2,968 (2,944 visual + 24 collider) | 0.86 MB | 1.95 × 0.67 × 3.68 | gibbet cage, body, coin purse |
| `glb/gibbet_corpse_looted.glb` | 2,878 (2,854 + 24) | 0.72 MB | 1.95 × 0.67 × 3.68 | gibbet cage, body (purse removed) |
| `glb/chained_prisoner.glb` | 2,904 | 0.82 MB | 1.73 × 1.65 × 1.46 | body, chains, new wall, closed bundle |
| `glb/chained_prisoner_looted.glb` | 2,993 | 0.93 MB | 1.81 × 1.65 × 1.46 | body, chains, new wall, opened bundle |

Previews (normal on the left, looted on the right, 3/4 view): `previews/<name>.png`.

## Mesh nodes (for the game code)
- fallen_adventurer: `corpse_body`, `gear_sword`, `loot_sack` / looted: `corpse_body`, `loot_sack_opened`
- gibbet_corpse: `gallows`, `cage`, `corpse_body`, `loot_coin_purse`, `col_cage`, `col_post` (simple box colliders kept from the cage asset, so hide or ignore them for rendering) / looted: the same nodes minus `loot_coin_purse`
- chained_prisoner: `stone_wall`, `wall_chains`, `corpse_body`, `loot_bundle` / looted: `loot_bundle` is swapped for `loot_bundle_opened`

## Reused assets (repo paths; copied, never modified)
- **fallen_adventurer**: body = `characters_art/monsters/grave_risen/grave_risen.glb`, posed lying on its back and decimated. Sword = the `swordsman_sword` mesh from `characters_art/monsters/swordsman/swordsman.glb`. Sack = `models/env_extra/props_gothic_v1/loot/sack_pile_closed.glb` scaled to 0.42. Looted uses `sack_pile_opened.glb` instead.
- **gibbet_corpse**: cage and gallows = `models/env_extra/props_gothic_v1/props/gibbet_cage_v1.glb`, with its built-in skeleton removed. Body = `characters_art/monsters/shambler/shambler.glb`, posed hanging and decimated. Coin purse = `sack_pile_closed.glb` scaled to 0.13.
- **chained_prisoner**: body = `grave_risen.glb`, posed seated and slumped. Chains = `models/env_extra/props_gothic_v1/props/chains_shackles_v1.glb`, scaled to fit the wall. Wall = a new beveled box that uses the `m_rock` material from `gibbet_cage_v1.glb`. Bundle = `sack_pile_closed.glb` scaled to 0.32. Looted uses `sack_pile_opened.glb` scaled to 0.30.

## Known caveats
- fallen_adventurer: the lying pose is a little crumpled, and the legs cross. The decimated sword is thin and reads small. The sack reads as a small cluster of sacks, and the opened version looks like flat discs.
- gibbet_corpse: looting only removes the purse, which is a tiny scaled sack pile. The "rags hang open" idea was not done.
- chained_prisoner: the grave_risen face texture reads as a pale grey band. The chains are scaled unevenly, so the links stretch a little, and only one chain shows clearly in the 3/4 view. The body sits slightly into the ground.
- The same grave_risen body is used for the adventurer and the prisoner. No mail coat was added.
- glTF validator: 0 errors. There are tangent-space warnings only (tangents are generated at runtime).

Pipeline: Blender 4.2 script (`build.py`, kept in the local work folder and not pushed).
