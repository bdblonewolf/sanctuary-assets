# feral_phimn_walk.glb: heavy four-legged walk for the feral phimn

- **Mobile file:** `characters_art/monsters/corrupted_phimn/feral_phimn_walk.glb` (1.44 MB). **Master:** `masters/feral_phimn_walk.glb` (1.45 MB).
- Both follow the `red_demon_spawnling_walk.glb` layout: the feral lod15k_v2 mesh + skin + materials, and a single clip named **`walk`**.
- These are new files. The existing feral GLBs and `monsters_3d.json` are unchanged; brute, bear and melakir still map `walk` to `run`.
- **Gait:** a lateral-sequence walk on all fours, on the phimn's own 52-joint rig. Left hind, then left fore, then right hind, then right fore.
  - Body hunched and low, with a heavy bob (22 mm at native scale) that drops at each hind plant.
  - Hips sway and roll, spine counter-yaw, a head nod at front plants, and the head stabilised.
  - Feet and hands stay flat in stance. The heel peels about the toes at push-off; the palm peels about the knuckles, with the fingers held flat.
- 30 fps, in place (Hips x/z = 0), loops seamlessly. **Left hind heel-down at normalized time 0.**

## Measurements (native rig scale; identical on corrupted_phimn_feral.glb, _lod15k.glb and _lod15k_v2.glb)

| clip | frames (keys) | sec | m / cycle | m/s native | LH down / off | LF down / off | RH down / off | RF down / off | duty | max slip |
|---|---|---|---|---|---|---|---|---|---|---|
| walk | 22 (23) | 0.733 | 0.716 | 0.976 | 0 / 14 | 6 / 20 | 11 / 3 | 17 / 9 | 0.64 | 0.0 mm feet, 0.1 mm hands |

Two or three limbs are always on the ground; there is no flight phase.

**In-game speed, which scales with `height`.** Set `walkNat` to these values if the walk clip is switched to `walk`:

| kind | height | scale | walk m/s (walkNat) | current walkNat (run clip) |
|---|---|---|---|---|
| melakir | 1.8 | ×1.173 | 1.145 | 1.04 |
| brute | 2.2 | ×1.434 | 1.400 | 1.27 |
| bear | 3.0 | ×1.956 | 1.909 | 1.73 |

## How to use

- The rest skeleton is identical to the three feral GLBs: same 52 `mixamorig:*` joints, rest offsets within 3e-7 m, root `corrupted_phimn` identity. The clip therefore plays on all three.
- To use it, either:
  - load the clip from this file onto the existing kind, or
  - point a kind at this file.
- Either way, map `clips.walk` → `walk` and set `walkNat` from the table above.

## Checks

- `verify_clips.mjs`, master vs mobile: 23 / 23 keys, worst 0.06 mm, 0.0001 rotation.
- The glTF validator gives 0 errors on both files. The 15 warnings (`NODE_SKINNED_MESH_NON_ROOT`) and 5 infos are identical to the live `corrupted_phimn_feral_lod15k*.glb`.
- Keyframes: 1,219 (master) → 561 (mobile). No meshopt or Draco.
- Preview: `art_2d/sanctuary_art/monsters/models3d/previews/feral_phimn_walk.png` (side view with world travel, plus the footfall chart).

## Pipeline

- The walk is generated procedurally from the rig's own idle pose at frame 0. No external motion data was used.
- Stance targets move at exactly −v. Swing uses min-jerk travel with sine lift: 85 mm hind, 72 mm fore.
- Limbs are solved with two-bone IK (UpLeg-Leg-Foot, Arm-ForeArm-Hand), using the idle knees and elbows as poles. The hips are lowered automatically where reach would exceed 97.5% (3 mm needed).
- Written with the add-clips writer (old clips and their accessors removed; mesh, skin and leaf nodes kept). Then `tools/mobile_compress.sh`.
