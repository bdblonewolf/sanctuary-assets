# wolf — corrupted wolf (white / grey / black coats)

All three coats share **one mesh and one skeleton**. Each coat is a separate GLB, and the only difference between them is the baked texture set:

| file | coat |
|---|---|
| `wolf_white.glb` | pale/ash white, mangy, dark dorsal saddle |
| `wolf_grey.glb`  | grey timber wolf |
| `wolf_black.glb` | black wolf |

Look: realistic fur-strand texture with mange patches and open sores, faint dark-red corruption veins with only a weak glow, and smouldering ember-red eyes.
Materials: one PBR material per file (baked baseColor, roughness, normal and emissive at 1024²). Backface culling is on.

## Specs
- Tris: **11,772**, as one skinned mesh
- Height: **0.99 m** at the shoulders/ears. Length is about 2.06 m including the tail.
- Forward axis is glTF **+Z**. The model is Y-up, with its feet on y=0.
- Clips run at 30 fps and are **in place**, with no root motion.
- Walk speed at 1x: **0.50 m/s**
- Run speed at 1x: **1.61 m/s**
- Speeds are measured from the foot-bone stride divided by the cycle time.

## Clips
| clip | frames | loop | impact frame | notes |
|---|---|---|---|---|
| idle | 101 | yes | – | |
| walk | 32 | yes | – | |
| run | 17 | yes | – | gallop |
| attack | 41 | no | **11** | bite |
| attack2 | 41 | no | **28** | pounce/leap: front paws land on f28, then it settles back to stance |
| hit | 21 | no | – | flinch |
| death | 32 | no | – | collapses to the ground around f20 |

There is no howl clip. The source pack doesn't include one, and the rig has no jaw bone.

## Source / licence
- Base mesh and animations: **Quaternius – Ultimate Animated Animal Pack, "Wolf"**, licensed **CC0 1.0** (https://quaternius.com, also on poly.pizza).
- Work done here:
  - Clips renamed and retimed from 24 to 30 fps.
  - Mesh merged, subdivided once and reshaped (narrower head).
  - New realistic corrupted texturing, procedurally baked.
  - Units flattened to metres.
- `preview_wolf.png` shows the 3/4 view of each coat plus keyframes from walk, attack, attack2 and death.


## Master vs mobile copy (2026-11-03)
Each GLB at its usual path is now the **mobile copy**, with the same filename, clip names and frame counts at 30 fps. Use it in the live and mobile game.
The **master** is the uncompressed full-rate original, now kept in `masters/` with the same name. Keep it for an HTML or PC build, and for re-authoring.

| file (mobile) | master | MB | keyframes | max joint drift (mm) |
|---|---|---|---|---|
| `wolf_white.glb` | `masters/wolf_white.glb` | 3.07 → 2.87 | 11,093 → 6,521 | 1.53 |
| `wolf_grey.glb` | `masters/wolf_grey.glb` | 2.98 → 2.78 | 11,093 → 6,521 | 1.53 |
| `wolf_black.glb` | `masters/wolf_black.glb` | 2.91 → 2.71 | 11,093 → 6,521 | 1.53 |

Pipeline (`/workspace/sanctuary_art/tools/mobile_compress.sh`):
1. resample at tolerance 1e-4
2. prune, keeping all nodes and skins
3. dedup
4. drop scale tracks that never change
5. drop translation tracks, except on mixamorig:Hips, the root bones, animated pieces and the empties (mouth, javelin)

**No meshopt or Draco** is used, so the loader needs no decoder. The release and impact frames listed above are unchanged: they were checked frame by frame against the master.
