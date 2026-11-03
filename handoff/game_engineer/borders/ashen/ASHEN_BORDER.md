# Ashen Coast border at 42x112 (world_v1, PROPOSAL, not live)

Status: new files only. No placements, world/interior JSONs, colliders, asset_version or live code were touched. Nothing was committed or pushed.
It matches sanctuary-assets `3907d8e`: same 42x112 tile bounds and the same A0 props. **World props moved: 0.**

## What it is
- Layout: `border_kit/out/layout_coast.json`. 33 kit pieces + 49 border props (crag 9, grass 11, gtree 3, seastack 7, shore_rock 13, spire 6). Kit is 25,860 tris.
- Runs:
  - N: land 0–42.
  - E: land 0–24, then sea 24–112.
  - S: land 0–42.
  - W: land 0–24, then sea 24–112.
- Seam spans (ring skipped; pass12 only as a fallback):
  - N 14.2–26.2 ↔ Martsirt;
  - E 8.2–20.2 ↔ Bastion. The E land→sea endcap was shifted to 20.2–32.2 so the exit road wins.
- Kit GLBs: `border_kit/glb/bk_coast_land_dead.glb`, `bk_sea_dead.glb`. The node name is the piece name. Pivot is on the edge line, the piece runs along +X, and it rises toward −Z.
- Border props: lip_outer layer, collidable where `blocks_walk` is set. They never sit on road, path, bridge or plank tiles, exit ±4 m, seam spans, or within 1.2 m of a world prop.

## Correct without placeRing
The live game hides the gap with a workaround. It places the rect ring `backdrop_near_rect_coast_{season}.glb` at (w/2, 0, 28), built for 42x56, and shifts near_sea_S by z += h − 56. The layout here is built for the true 42x112 bounds, so it needs none of that.

**Loader changes (engineer):**
1. For `coast`, stop calling placeRing (delete the rect ring and the near_sea_S shift). Instead, read `layout_coast.json`:
   - for each piece, clone node `piece` from `bk_<style>_<season>.glb`, set position `pos`, rotation.y = `rotY`, scale.x = `scaleX`;
   - for each prop, instance `asset` at `pos` / `rotY` / `scale`, and add a cylinder collider when `blocks_walk`.
   - Merge pieces per material (≤5 draws) and instance props per asset (≤8 draws).
2. Keep placeOcean (520x520 at y −0.4). The sea kit adds the seabed, stacks and sloped sea face on top.
3. On seam spans, copy neighbour scenery from `seams/coast__martsirt.json` and `seams/bastion__coast.json`. Fall back to pass12 if the neighbour isn't loaded.
4. FLAG: the 3D code tests water as CT=4 (old enum U), but the live tile enum has Water=8 (q). Check this before trusting any water test on the new tiles.
5. A cheaper minimum if (1) is too much: rebuild the rect ring at 42x112, place it at (w/2, 0, h/2), and drop the z-shift. The proofs here use the kit layout.

## Proof (real camera: FOV 38, pitch 50, dist 14 and 40, portrait 300x650 and landscape 650x300, hero at 4 corners inset 1 m + 4 edge mids + E_south (41,84) + W_south (1,100))
- `proof/before_*.png` and `proof/after_*.png`. Contact sheets: `proof/contact_portrait_d40.png`, `proof/contact_landscape_d40.png`. Numbers are in `proof/proof_results.json`.
- Magenta marks the gap: open ocean visible where land border should be, or black void.

| | views | mean gap | max gap | void |
|---|---|---|---|---|
| before (live placeRing rules) | 40 | 15.1 % | 71.6 % (SW / W_south) | 0 % |
| after (kit layout) | 40 | 0.004 % | 0.10 % (NE d40 landscape, sliver at the seam) | 0 % |

- Generator: `border_kit/gen_border.py`. Renderer: `border_kit/proof_render.py` (`blender -b -P proof_render.py -- coast <outdir>`).

## Terrain
`terrain/coast.json` keeps the coast at 0 m. Sea bed is −1.2 under the 0 sea at −0.4; the higher neighbour does the climbing. Of the 381 A0 props, **0** need a y-offset; the 8 sea rocks outside the bounds stand on the ocean plane.
