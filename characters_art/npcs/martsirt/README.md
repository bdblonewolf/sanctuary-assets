# Martsirt town NPCs — batch 1 (Wolcen, Quill), quality pass 3

Realistic, battle-worn gothic-medieval townsfolk for *Sanctuary* (three.js). Built only on the approved bodies, which were copied from
`/workspace/sanctuary_npc/approved/` into `src/bodies/`. The originals were never modified.

| NPC | GLB | size | height | tris visible (default outfit) | tris total | clips |
|---|---|---|---|---|---|---|
| Wolcen (smith) | glb/wolcen.glb | 2.882 MB | 1.98 m | 22,323 | 24,914 | idle, walk, talk, sit, sit_talk, work_hammer, sleep |
| Quill (scribe) | glb/quill.glb | 2.715 MB | 1.76 m | 20,681 | 23,680 | idle, walk, talk, sit, sit_talk, work_write, sleep |

gltf-validator reports 0 errors for both files. The only warnings are MESH_PRIMITIVE_GENERATED_TANGENT_SPACE, which is expected because tangents
are not exported and three.js derives them, and NODE_SKINNED_MESH_NON_ROOT, which is the standard Blender layout where the meshes sit under the armature node.

## Node layout (one GLB per NPC, single armature + single skin)
- `<id>_body_head|torso|arms|hands|legs|feet`: the whole bare body as skinned region submeshes. Region borders were locked during
  decimation, and whole-body vertex normals were restored after the split, so the seams do not show when every region is visible (see previews/*_bare_front.png).
- `<id>_outfit_<slot>`: skinned garments. Wolcen and Quill use the torso, legs, feet and hands slots.
- `<id>_hair`: skinned hair and beard cards, using the alpha-blend/alpha-clip material `<id>_mat_cards`.
- `<id>_prop_<name>`: a rigid node parented to a bone. Its mesh is on the child `<id>_prop_<name>_mesh` (gltf-transform splits it this way because
  the prop node is animated). Props are scaled to 0 in every clip except the profession clip.
- `<id>_keepsake`: a rigid node parented to a bone and always visible. Wolcen's is Odder's small hammer on Hips (it hangs in the apron loop).
  Quill's is the inward-turned signet ring on RightHandRing1. His cold-iron wrist bands are in `quill_outfit_hands`.

The body under the clothes is never deleted. With the default outfit, the engine hides the regions that each slot lists in MANIFEST `slot_hides`:
- Wolcen: torso→[body_torso], legs→[], feet→[body_feet], hands→[] (the bracers leave the forearms and hands bare). The legs are covered jointly by trousers + boots (77 %), but no single slot covers >50 %, so body_legs (798 tris) stays rendered under the trousers.
- Quill: torso→[body_torso, body_arms], legs→[body_legs], feet→[body_feet], hands→[].

Coverage is computed per face by casting rays from the skin against each slot's garments. A slot hides a region when it covers more than 50 % of the region's faces.
Uncovered faces inside a hidden region (the neck/collar and the wrists) were moved into the neighbouring visible region (torso→head, arms→hands),
so hiding never opens a hole. If a garment is swapped for a shorter one, show the region again.

## Textures
Each NPC has one **2048²** atlas set in WebP (basecolor, normal and ORM), shared by every node in the GLB. Raised from 1024² in pass 2: at 1024 the
weave/leather grain, stitching, scorch marks and strong folds in the normal map turned to mush and the hair-card alpha edges went blocky.
Cost: about +1.2 MB per GLB (pass 3: Wolcen 2.88 MB, Quill 2.72 MB, both under the 3 MB ceiling). Downscaling to 1024 at load is safe if memory is tight.

## Placement notes (metres, glTF coordinates)
- Wolcen work_hammer: anvil top at y 0.88, centre (−0.02, 0.80, 0.53) relative to the NPC root. Seat height for sit/sit_talk/sleep is 0.50.
- Quill work_write: the lectern box centre is (0.02, 1.04, 0.40) and the page is about (0.02, 1.06, 0.36). Seat height is 0.44.
  He works in the scriptorium north of the square.
- Walk is in place. Root speed is about 2.0 m/s × height/1.98.

## Pipeline (src/)
```
B=/workspace/sanctuary_npc/tools/blender-4.2.3-linux-x64/blender
$B -b --python npc_<id>.py -- fit      # fit garments to the copied body (once)
$B -b --python npc_<id>.py -- build    # weights, region split, slot coverage, UV/bake, export work/<id>/raw.glb + meta.json
bash pipeline.sh <id>                  # anim.py (retargeted clips, foot_fix), resample/prune/quantize(scene)/prune, namefix, validate -> glb/<id>.glb
python3 manifest.py wolcen quill       # MANIFEST.json
HIDE=torso,legs,feet SAMPLES=48 $B -b --python preview.py -- ../glb/<id>.glb ../previews/<id> stills
HIDE=... ANVIL=1 BENCH=0.50 | LECTERN="0.02,1.04,0.40" BENCH=0.44  $B -b --python preview.py -- GLB /tmp/x/p clips ; python3 sheet.py /tmp/x/p ../previews/<id>_clips.jpg
```
- Clips are retargeted with pose.Retarget, which corrects for the rest pose; it is not a name copy. Fingers are relaxed, with a tool grip in the work clips.
- `foot_fix` applies a constant foot-pitch correction (about 21°) and a small hip lift on the standing clips, so the toes no longer go under the floor.
  `EXTRA_LIFT` in anim.py (measured, 0.011 m for both) lifts the boot heels to y≥0 (lowest vertex: idle/talk/work 0.000–0.001, walk −0.004…+0.002).
- Body decimation is set per region in `lib_fin.finalize(region_budget=…)`. Head and hands get the most because they are always visible.

## Quality pass 2 (Nov 1, 2026)
- Concept sheets: `concept/<id>_concept_sheet.jpg`; side-by-sides: `previews/<id>_vs_concept.jpg`.
- Garments rebuilt with silhouette and layering: fold rows, ragged hems, solidified edges, buckles/pouches, smooth shading with sharp creases (`lib_fin.smooth_sharp`).
- Wolcen: crew-neck shirt with rolled sleeves above the elbow, scorched apron front + back panel and crossed straps, belt kit, cuffed strapped boots, strand-card hair with back braid, beard cards with chin braid.
- Quill: face sculpt (cheekbones, hollow cheeks, temples, brow, sockets), coat = closed upper + split open skirt with inverted-V front and a back vent, ragged capelet, cowl + thrown-back hood, blue-ink cuffs, belt with buckle, pouch, ink horn and pen case, right-hip satchel with scrolls on a strap over the left shoulder, cuffed boots with soles, 230 swept-back strand cards.
- Heels fixed (see Pipeline).

## Quality pass 3 (Nov 1, 2026): concept sheets are the locked target
- **Albedo projected from the concept sheets** (`lib_proj.py`, `proj_ext.py`): the front, side and back views of `concept/<id>_concept_sheet.jpg` are
  registered onto the posed fit (TV-L1 flow on silhouette SDFs) and baked per vertex, then blended into the 2048² basecolor per material (`PJ_MIX`),
  with per-material tone correction (`PJ_COMP.tone`). Weave, leather grain, stitching, scorch and wear now come from the concept. Fine normal detail is derived from
  the projected luminance (`nstr`, `keepn`). Run it with `$B -b --python npc_<id>.py -- proj` (QA: `src/work/proj/<id>_qa.png`; it is also run inside `build`).
- Wolcen: shirt rebuilt as an offset shell of the body (exact body skin weights) for natural, slimmer shoulders, with thin sleeve rolls and an off-white/grey linen tone;
  knee-length dark scorched apron with a ragged hem, straps and belt; darker trousers and wrapped tall boots; hairline root cards, shorter cropped sides
  and a back braid; a fuller beard (more, wider cards with softer taper).
- Quill: older, gaunt face (deeper cheeks, under-eye hollows, nasolabial folds, heavier lids, weathered darker skin, stubble, dark eyes); long dark
  shoulder-length hair (340 layered cards that cover the crown, with temple strands routed behind the cheek); the hood now rises behind the head to ear level and frames it from the front;
  long single-breasted dark wool coat with belt and satchel strap; grey-blue cuffs; costume contrast raised for dim light; skirt re-weighted
  (back on Hips, front following the thighs and shins) so it no longer bunches in sit, sit_talk and sleep.

## Known issues
- Wolcen: neck/trapezius skin is still slightly faceted; the hair top still reads a little like a cap in close-up; the beard is fuller but still a bit blotchy; the face reads paler than the concept;
  the back of the shirt is darker than the front because the back concept view is darker.
- Quill: the face reads older, but less gaunt and sly than the concept; there is a lighter patch of skin at the hairline at his right temple; the coat is darker overall than the concept, which favours dim light
  but loses some mid-tone fold detail.
- Bodies under the clothes are reduced (torso about 1.3k, legs about 0.8k, feet about 0.4k tris). They are fine for swaps, but they are lower detail than the head and hands.
- Overlapping garments are not trimmed, so outfits stay swappable. This costs a few hundred hidden tris.

## Later batches (not built)
Ysara, Ilyra, Bram (about 1.90 m), Mira, Orrin, Ness and Ayla. Ayla is not a hireling and stays in the stable yard; include her spear prop only if it is easy.
