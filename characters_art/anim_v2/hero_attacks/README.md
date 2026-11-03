# hero_attacks: throw_1h (one-hand overarm javelin throw)

New clip only. The bow, sword, axe, greatsword, dagger and magic hero clips were **not** remade; they already exist in `models/knight_anim_v10b.glb`.

## Files
Each file holds just the armature and the one clip `throw_1h`. There is no mesh, so merge the clip into the hero mixer the same way hero_extra.glb clips are merged.

| file | rig | use |
|---|---|---|
| throw_1h_knight.glb | 27-joint knight subset of mixamorig (same joints as knight_anim_v10b) | the live hero (`heroAnimUrl` skeleton) |
| throw_1h_male_regular.glb | mixamorig 52 | warrior / necromancer class bodies |
| throw_1h_female_skinny.glb | mixamorig 52 | archer body |
| throw_1h_female_medium.glb, throw_1h_female_curvy.glb | mixamorig 52 | elementalist body blend |

Each skeleton has its own bake (local quaternion tracks plus absolute Hips translation), so use the file that matches the skeleton.

## Clip `throw_1h`: 31 frames @ 30 fps (1.0 s), in place

| frame | phase |
|---|---|
| 0-3 | idle, side-on (left shoulder toward the target) |
| 4-12 | wind-up: right hand back and high (about 0.5 m behind the hips, at head height); left arm points at the target; weight on the back foot |
| 12-14 | whip forward: hips and shoulders square up to face the target (-Z in glTF, which is the hero's forward) |
| **14** | **RELEASE**: right hand forward and above the head (about 1.6 m high on male_regular). Peak hand speed is f13-14. Spawn the javelin projectile here. |
| 15-22 | follow-through across the body, leaning forward |
| 23-30 | recover to idle |

- **Release frame: 14** (t = 0.467 s). The javelin is held in **mixamorig:RightHand**. Hide the held javelin and spawn the projectile at f14.
- Sound: whoosh/release around f12-14.
- `throw_1h_report.json` has the per-frame right-hand speed for each rig.
- Source: hand-keyed. There is no free throw or javelin clip in the Mixamo packs on disk. It was built over the Mixamo "sword and shield idle" pose (already in the repo's Mixamo set) with the addclip framework. The scripts are in tools/ (`blender -b --python addclip_h.py -- body.glb out.glb r_throw.py`).

## Audit: clip names the game code requests vs knight_anim_v10b
I checked every clip name in live routes JS (`playHero(...)`, the weapon clip-set table, deaths, peace, bow draw/release, and the sit clips from hero_extra). **All of them exist** in knight_anim_v10b or hero_extra.

The strings `spear_*`, `shield_*` and `staff_twirl` turned up in the search but are skill or rite ids, not clip names. There is no javelin/spear weapon clip set in the code yet. When one is added, map its attack to `throw_1h`.

No other clips were added.

## Previews
- previews/throw_1h_knight_side.png
- previews/throw_1h_knight_top.png
- previews/throw_1h_female_skinny_side.png

Frames shown: 0, 6, 10, 12, 13, 14, 16, 19, 24, 30.


## Master vs mobile copy (2026-11-03)
Each GLB at its usual path is now the **mobile copy**, with the same filename, clip names and frame counts at 30 fps. Use it in the live and mobile game.
The **master** is the uncompressed full-rate original, now kept in `masters/` with the same name. Keep it for an HTML or PC build, and for re-authoring.

| file (mobile) | master | MB | keyframes | max joint drift (mm) |
|---|---|---|---|---|
| `throw_1h_knight.glb` | `masters/throw_1h_knight.glb` | 0.06 → 0.02 | 2,511 → 313 | 0.16 |
| `throw_1h_male_regular.glb` | `masters/throw_1h_male_regular.glb` | 0.12 → 0.03 | 4,836 → 363 | 0.2 |
| `throw_1h_female_skinny.glb` | `masters/throw_1h_female_skinny.glb` | 0.12 → 0.03 | 4,836 → 363 | 0.16 |
| `throw_1h_female_medium.glb` | `masters/throw_1h_female_medium.glb` | 0.12 → 0.03 | 4,836 → 363 | 0.17 |
| `throw_1h_female_curvy.glb` | `masters/throw_1h_female_curvy.glb` | 0.12 → 0.03 | 4,836 → 363 | 0.17 |

Pipeline (`/workspace/sanctuary_art/tools/mobile_compress.sh`):
1. resample at tolerance 1e-4
2. prune, keeping all nodes and skins
3. dedup
4. drop scale tracks that never change
5. drop translation tracks, except on mixamorig:Hips, the root bones, animated pieces and the empties (mouth, javelin)

**No meshopt or Draco** is used, so the loader needs no decoder. The release and impact frames listed above are unchanged: they were checked frame by frame against the master.
