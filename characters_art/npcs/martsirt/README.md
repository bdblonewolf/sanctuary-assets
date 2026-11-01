# Martsirt town NPCs — batch 1 (Wolcen, Quill)

Realistic, battle-worn gothic-medieval townsfolk for *Sanctuary* (three.js). Built only on the approved bodies, which were copied from
`/workspace/sanctuary_npc/approved/` into `src/bodies/`. The originals were never modified.

| NPC | GLB | size | height | tris visible (default outfit) | tris total | clips |
|---|---|---|---|---|---|---|
| Wolcen (smith) | glb/wolcen.glb | 1.386 MB | 1.98 m | 21,469 | 24,147 | idle, walk, talk, sit, sit_talk, work_hammer, sleep |
| Quill (scribe) | glb/quill.glb | 1.243 MB | 1.76 m | 19,948 | 22,948 | idle, walk, talk, sit, sit_talk, work_write, sleep |

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
- Wolcen: torso→[body_torso], legs→[body_legs], feet→[body_feet], hands→[] (the bracers leave the forearms and hands bare).
- Quill: torso→[body_torso, body_arms], legs→[body_legs], feet→[body_feet], hands→[].

Coverage is computed per face by casting rays from the skin against each slot's garments. A slot hides a region when it covers more than 50 % of the region's faces.
Uncovered faces inside a hidden region (the neck/collar and the wrists) were moved into the neighbouring visible region (torso→head, arms→hands),
so hiding never opens a hole. If a garment is swapped for a shorter one, show the region again.

## Textures
Each NPC has one 1024² atlas set in WebP (basecolor, normal and ORM), shared by every node in the GLB.

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
- Body decimation is set per region in `lib_fin.finalize(region_budget=…)`. Head and hands get the most because they are always visible.

## Known issues
- Heels sit about 1 cm below y=0 in the standing clips.
- Wolcen's hair and beard cards have fairly hard edges at the hairline.
- From behind, Quill's hair reads a little boxy, like a hood.
- Bodies under the clothes are reduced (torso about 1.3–1.5k, legs about 0.8k, feet about 0.4k tris). They are fine for swaps, but they are lower detail than the head and hands.
- Overlapping garments, such as the shirt under the apron and the hose under the coat, are no longer trimmed, so outfits stay swappable. This costs a few hundred hidden tris.

## Later batches (not built)
Ysara, Ilyra, Bram (about 1.90 m), Mira, Orrin, Ness and Ayla. Ayla is not a hireling and stays in the stable yard; include her spear prop only if it is easy.
