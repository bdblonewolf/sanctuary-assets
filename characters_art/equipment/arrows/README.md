# Arrows, stuck arrows, quiver

| Mobile copy (load this) | Master | Contents |
|---|---|---|
| `arrows_kit.glb` (194 KB) | `masters/arrows_kit.glb` | **Phone: load this one.** All 5 meshes as named nodes, 1 material, 1 atlas embedded once |
| `arrow.glb` | `masters/arrow.glb` | flying arrow, 312 tris |
| `arrow_stuck_deep.glb` | `masters/…` | stuck, 0.43 m visible, 252 tris |
| `arrow_stuck_short.glb` | `masters/…` | stuck, 0.30 m visible, 236 tris |
| `arrow_stuck_snapped.glb` | `masters/…` | snapped splintered stub, 0.19 m, 94 tris |
| `quiver.glb` | `masters/…` | leather quiver + 7 arrow tails, 1,882 tris |

The single-file GLBs embed the same atlas each, so don't load several of them on phone (they would duplicate textures). Use the kit and clone nodes by name.
Mobile copies were made with `tools/mobile_compress.sh` (prune and dedup only for static meshes; no meshopt or Draco). Masters are the raw Blender exports.

Shared material `arrows_atlas`: `textures/arrows_atlas_{bc,n,orm}.png`, 512 px. In the GLBs they're JPEG q88. ORM = R occlusion 1, G roughness, B metal. The atlas is baked from the earlier wood/forged-iron arrow materials plus Poly Haven `brown_leather` (CC0) for the quiver.

## Axes (glTF, Y up, metres)
- `arrow`: nock at the origin, **tip at +Z 0.78 m** (child node `tip`). Point +Z along the velocity. There's also a child node `nock` at the origin, for attaching to the bow hand or string.
- `arrow_stuck_*`: **origin = entry point on the surface**, and the shaft extends along **-Z**, back toward the shooter. On hit, place the node at the hit point with +Z = the arrow's flight direction, then parent it to the hit bone. Child nodes `*_embed` sit at the origin.
- `quiver`: origin at the bottom centre, open end up at +Y. Body 0.56 m tall, 0.79 m with the arrow tails. The strap side faces glTF +Z. Suggested mount: parent to `mixamorig:Spine2`, about 0.12 m behind the spine, tilted about 20° so the tails sit over the right shoulder.

Sound: `audio/sfx/weapon/arrow_whiz_0[1-2].ogg` (flight), `audio/sfx/impact/arrow_thunk_0[1-3].ogg` (at the frame where you spawn the stuck arrow).
Source: `src/build_kit.py` (`blender -b arrows_work.blend --python build_kit.py`). All original work, plus the CC0 leather texture.
