# wild_boar — corrupted wild boar

`wild_boar.glb` is a single skinned mesh with one PBR material (baked baseColor, roughness, normal and emissive at 1024²). Backface culling is on.

**Look:** coarse dark bristle hide with a dorsal bristle mane, mange patches and open sores. It has faint dark-red corruption veins, blood-stained ivory tusks and ember-red eyes.

## Specs
- **Tris:** 10,945
- **Size:** 1.10 m tall including the mane (about 1.0 m at the shoulder) and about 1.75 m long
- **Orientation:** forward is glTF **+Z**, Y is up, feet sit on y=0
- **Clips:** 30 fps, **in place** (no root motion)
- **Walk speed at 1x:** **0.30 m/s**
- **Run speed at 1x:** **0.96 m/s**
- Speeds are measured as foot stride ÷ cycle time. The source walk cadence is slow, so raise the playback rate if the game moves the boar faster.

## Clips
| clip | frames | loop | impact frame | notes |
|---|---|---|---|---|
| idle | 101 | yes | – | |
| walk | 36 | yes | – | |
| run | 19 | yes | – | gallop |
| attack | 31 | no | **17** | tusk gore: head drops at f8 and hooks up and forward at f17 |
| attack2 | 60 | no | **46** | charge: 2 gallop cycles (f0–29), then a blend into the tusk gore (gore starts at f29, hit lands at f46) |
| hit | 21 | no | – | flinch |
| death | 31 | no | – | collapses onto its side by about f20 |

## Source / licence
- **Base mesh and animation:** Quaternius, *Ultimate Animated Animal Pack*, "Bull". Licence **CC0 1.0** (https://quaternius.com).
- **Changes made here, all original work:**
  - Removed the horns.
  - Reshaped the model into a boar: a long wedge snout, a thick hunched neck and shoulders, a lower rump and a short tail.
  - Added procedural curved tusks and a bristle mane, both skinned to the head and spine bones.
  - Subdivided the mesh and baked new realistic corrupted textures.
  - Retimed the clips from 24 to 30 fps and renamed them.
  - attack2 (charge) was built by blending the gallop into the gore.
- **Preview:** `preview_wild_boar.png`


## Master vs mobile copy (2026-11-03)
Each GLB at its usual path is now the **mobile copy**, with the same filename, clip names and frame counts at 30 fps. Use it in the live and mobile game.
The **master** is the uncompressed full-rate original, now kept in `masters/` with the same name. Keep it for an HTML or PC build, and for re-authoring.

| file (mobile) | master | MB | keyframes | max joint drift (mm) |
|---|---|---|---|---|
| `wild_boar.glb` | `masters/wild_boar.glb` | 3.00 → 2.84 | 10,328 → 6,216 | 1.1 |

Pipeline (`/workspace/sanctuary_art/tools/mobile_compress.sh`):
1. resample at tolerance 1e-4
2. prune, keeping all nodes and skins
3. dedup
4. drop scale tracks that never change
5. drop translation tracks, except on mixamorig:Hips, the root bones, animated pieces and the empties (mouth, javelin)

**No meshopt or Draco** is used, so the loader needs no decoder. The release and impact frames listed above are unchanged: they were checked frame by frame against the master.
