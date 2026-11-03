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
