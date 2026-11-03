# crawler — rigged + animated

`crawler_anim.glb` (the original `crawler.glb` is unchanged)

- Mesh: decimated to 14,000 triangles from 18k. 25-bone procedural quadruped-crawl rig, with a jaw bone.
- Height is 0.90 m at rest, and the model is about 1.0 m long.
- 30 fps, in place: no root motion, and the root has no keys.

| clip | frames | seconds | loops |
|---|---|---|---|
| idle | 90 | 3.0 | yes |
| walk | 24 | 0.8 | yes |
| run | 14 | 0.467 | yes |
| attack | 30 | 1.0 | no (one-hand rake lunge) |
| attack2 | 42 | 1.4 | no (rears up, double slam, bite) |
| hit | 16 | 0.533 | no |
| death | 72 | 2.4 | no, holds the last frame (rolls onto its side) |

## Speeds and gait
- Walk is about 0.63 m/s, measured from hand travel. Run is about 2.46 m/s.
- The crawler pulls itself along with its hands. The hind legs drag behind with twitchy shoves.
- Its rhythm is jittery and skittering on purpose.

## Provenance
- The animation is project-made and procedural, keyframed with a Blender script.
- No suitable free crawl animation was found:
  - KayKit "Crawling" is a humanoid on a different rig and posture.
  - Quaternius' CC0 monster and animal packs have no crawler.


## Master vs mobile copy (2026-11-03)
Each GLB at its usual path is now the **mobile copy**, with the same filename, clip names and frame counts at 30 fps. Use it in the live and mobile game.
The **master** is the uncompressed full-rate original, now kept in `masters/` with the same name. Keep it for an HTML or PC build, and for re-authoring.

| file (mobile) | master | MB | keyframes | max joint drift (mm) |
|---|---|---|---|---|
| `crawler_anim.glb` | `masters/crawler_anim.glb` | 4.80 → 4.53 | 22,125 → 5,256 | 0.64 |

Pipeline (`/workspace/sanctuary_art/tools/mobile_compress.sh`):
1. resample at tolerance 1e-4
2. prune, keeping all nodes and skins
3. dedup
4. drop scale tracks that never change
5. drop translation tracks, except on mixamorig:Hips, the root bones, animated pieces and the empties (mouth, javelin)

**No meshopt or Draco** is used, so the loader needs no decoder. The release and impact frames listed above are unchanged: they were checked frame by frame against the master.
