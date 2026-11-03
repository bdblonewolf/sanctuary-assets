# rag_zombie_v2.glb

A copy of `rag_zombie.glb` with new clips added. The original file is unchanged, and the v2 file keeps
all of its original clips (idle, walk, attack, hit, death) with the same frame counts.
30 fps, in place, lowercase clip names.

| clip | frames | seconds | key frames (0-based, 30 fps) |
|---|---|---|---|
| spit | 37 | 1.20 | head rears back and chest heaves 4–18 (head furthest back about 14–18), lurches forward with the head thrust out, **release frame 21** (spawn the spit/vomit VFX here), spew held 21–29 with a small head shake, recover to idle pose 29–36 |

Mouth / VFX
- This rig has **no jaw bone**. The spew is carried by the **mixamorig:Head** bone, with Neck and Spine1/Spine2 lurching.
- A new empty node named **`mouth`** is parented to mixamorig:Head at the front of the lips. Its rest position is about
  (0, 1.620, 0.156) m in glTF space (Y-up, +Z forward). Attach the spit VFX to it at frame 21 and aim it along the head's forward axis.
- skirt_F/skirt_B cloth bones are baked with the same damped follow as the live clips (follow 0.75, damp 0.4).
- The layers sit on the live idle, so the first frame matches idle frame 0 and the clip ends back near idle.

Source / licence
- Hand-keyed by script; no free spit/vomit clip was found in Mixamo, Quaternius UAL1/UAL2 or KayKit. It is original work, free to use in this project.

## Update 2026-11-03: slow deaths
Clips (30 fps): idle, walk, attack, hit, spit (release f21), **death_old** (the previous 133-frame "Dying" clip, kept), plus these two new deaths:
- **death** (82 f, 2.70 s): stagger then collapse. Lurching sway f0-30, drops to the knees at about f30, pitches forward. **Body impact f54**, then it lies still to f81. Base: Mixamo Pro Magic Pack "Standing React Death Forward", time-warped, plus a hand-keyed stagger sway (hips, Spine1, Head).
- **death2** (81 f, 2.67 s): knees hit the ground about f29, kneeling sway f30-56, falls forward. **Body impact f61** (chest f60). Base: Mixamo Pro Longbow Pack "standing death forward 01", slowed, plus a hand-keyed sway.
- Lowest vertex stays at or above z=0 the whole time, and ends at 0.
- Sounds: put a knee thud at the knee frame and the body thud at the impact frame (start the sound at the impact frame minus round(thud_s×30)).
- Previews (Cycles): previews_v2/death_side.png, death2_side.png
- Script: humanoid_v2/r_zombie_death.py, run through addclip.py.


## Master vs mobile copy (2026-11-03)
Each GLB at its usual path is now the **mobile copy**, with the same filename, clip names and frame counts at 30 fps. Use it in the live and mobile game.
The **master** is the uncompressed full-rate original, now kept in `masters/` with the same name. Keep it for an HTML or PC build, and for re-authoring.

| file (mobile) | master | MB | keyframes | max joint drift (mm) |
|---|---|---|---|---|
| `rag_zombie_v2.glb` | `masters/rag_zombie_v2.glb` | 3.70 → 2.65 | 89,100 → 17,514 | 0.69 |

Pipeline (`/workspace/sanctuary_art/tools/mobile_compress.sh`):
1. resample at tolerance 1e-4
2. prune, keeping all nodes and skins
3. dedup
4. drop scale tracks that never change
5. drop translation tracks, except on mixamorig:Hips, the root bones, animated pieces and the empties (mouth, javelin)

**No meshopt or Draco** is used, so the loader needs no decoder. The release and impact frames listed above are unchanged: they were checked frame by frame against the master.
