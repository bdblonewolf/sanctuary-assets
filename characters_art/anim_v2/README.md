# anim_v2: baked per-body clips (no runtime retarget)

These are new files only. Nothing the live game loads now was changed.
Built 2026-11-01 with numpy retarget math and Blender 4.2.3 (headless import, mesh checks and preview renders). The scripts are in `tools/` and `build.py` rebuilds everything.

## Files
| file | for | clips |
|---|---|---|
| `clips_<body>.glb` (13 files, ~1.1 MB each) | `characters_art/bodies/<body>.glb` (12) and `npcs/ayla_phimn/ayla_phimn_body.glb` | idle, walk, walk_natural, talk, sit, sit_talk, sleep, sit_down, stand_up, sit_to_sleep, sleep_to_sit |
| `hero_extra.glb` (0.35 MB) | `models/knight_anim_v10b.glb` | axe_draw__up, axe_sheath__up, bow_draw__up, bow_equip__up, bow_sheath__up, gs_draw__up, ss_draw__up, ss_sheath__up, gs_sheath, gs_sheath__up, gs_walk, sit_down, sit, stand_up, sit_talk |
| `ANIM_V2.json` | | per-body durations, natural walk speed, stand offset, validation |
| `previews/*.png` | | contact sheets |

Wolcen uses the same skeleton as male_brute_heavy, so `clips_male_brute_heavy.glb` drives `wolcen.glb` directly. Quill matches male_skinny in the same way, so `clips_male_skinny.glb` drives `quill.glb`. Those two files add the transitions and the 1.2 m/s walk to Wolcen and Quill.

## Loading (game code)
```js
const clipsGltf = await loader.loadAsync('characters_art/anim_v2/clips_female_tiny.glb');
const mixer = new THREE.AnimationMixer(bodyGltf.scene);          // the body's own scene/SkinnedMesh root
const act = n => mixer.clipAction(THREE.AnimationClip.findByName(clipsGltf.animations, n));
act('idle').play();
```
- Do not retarget, and do not apply a hip-height scale or offset. The clips are baked for that body's own skeleton, rest pose and leg length. The track names are `mixamorigHips.quaternion` and so on, which three.js sanitises the same way as the body.
- Every joint gets a rotation track. The only translation track is Hips, which carries the absolute hip position in metres.
- Hero: `hero_extra.glb` animations go into the knight's existing mixer with `mixer.clipAction(clip)`.
  - `*__up` clips carry no Hips, leg or foot tracks. Play them on top of the run or walk action, either with a higher weight on a second action or by masking. They stop the draw/sheath glide.
  - gs_sheath is gs_draw played in reverse.
  - gs_walk uses the ss_walk legs with the gs_idle arms. Its natural speed matches ss_walk at about 1.29 m/s.

## Locomotion
- `walk` is retimed so its natural ground speed is **1.2 m/s** for every body. The stride is unchanged and only the cycle gets longer.
- `walk_natural` is the unretimed cycle. Its speed per body is in `ANIM_V2.json` under `bodies.<b>.walk_natural_speed_mps`, and ranges from 1.19 m/s for female_tiny to 1.96 m/s for brute.
- For tall males (1.96 m/s natural) the 1.2 m/s cycle is about 1.6x slower and reads as a stroll. If that looks floaty, set that NPC's move speed to its `walk_natural_speed_mps` and use `walk_natural`, or set `timeScale = moveSpeed / walk_natural_speed_mps`.

## Sitting (benches, seat 0.45 m)
- The thigh underside sits at 0.44–0.45 m, measured from each body's mesh. Feet are IK'd flat to the floor, and short bodies such as Ayla keep their feet on the floor too.
- Place the NPC or hero root at the seat point, at floor level and at the front-centre of the seat, facing away from the backrest.
- `sit_down` (1.0 s): starts as the idle pose standing `stand_offset_m` in front of the root along +Z. Ease plus forward lean (24° spine, 10° pelvis), hips back and down, a small settle bounce, ends in `sit`.
- `stand_up` (1.1 s): leans forward 34°, hands go to the knees with arm IK, pushes up, and ends in idle `stand_offset_m` in front. When it finishes, move the root forward by `stand_offset_m` and switch to idle. The value is per body in the JSON, for example ayla 0.288 and knight 0.373.
- `sleep` in the source is a **seated doze**, not lying down, so the transitions are `sit_to_sleep` (1.4 s) and `sleep_to_sit` (1.0 s). The source data has no lying pose.

## Method
- Retarget uses world-space rotation transfer with per-bone rest compensation: each target bone's rest direction is aligned to the source's. Shoulders use delta-from-rest, which keeps Ayla's sloped shoulders and avoids a shrug bump.
- Sources: Wolcen for the brute, regular and vshape males. Quill for male_skinny, all females and Ayla.
- Hips translation is scaled by leg length. Each standing frame is then re-grounded so the lowest foot or toe joint stays at rest height (feet on y=0).

## Validation
Results are in ANIM_V2.json under `verification` and per-clip `foot_contact_cm`.
- Track names: every track node name exists in the matching body. Rest TRS diff is 0.0 for all 14 files.
- Joint foot contact: standing clips stay within −0.7 to +1.0 cm. Sit, sit_talk, sleep and the transitions are at 0.0 cm (IK).
- Blender evaluated mesh, lowest vertex:
  - Ayla sit_down, sit and stand_up: −0.1 cm.
  - male_regular walk: −1.1 to +0.3 cm.
  - Knight sit: −5.8 cm, caused by the hanging sword/scabbard prop, not the feet. Hide or re-attach weapons when seated.
