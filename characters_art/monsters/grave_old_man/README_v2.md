# grave_old_man_v2.glb

A copy of `grave_old_man.glb` with new clips added. The original file is unchanged, and the v2 file keeps
all of its original clips (idle, walk, attack, hit, death) with the same frame counts.
30 fps, in place, lowercase clip names.

| clip | frames | seconds | key frames (0-based, 30 fps) |
|---|---|---|---|
| spit | 37 | 1.20 | head rears back and chest heaves 4–18 (head furthest back about 14–18), lurches forward with the head thrust out, **release frame 21** (spawn the spit/vomit VFX here), spew held 21–29 with a small head shake, recover to idle pose 29–36 |

Mouth / VFX
- This rig has **no jaw bone**. The spew is carried by the **mixamorig:Head** bone, with Neck and Spine1/Spine2 lurching.
- A new empty node named **`mouth`** is parented to mixamorig:Head at the front of the lips. Its rest position is about
  (0, 1.614, 0.156) m in glTF space (Y-up, +Z forward). Attach the spit VFX to it at frame 21 and aim it along the head's forward axis.
- loin_F/loin_B cloth bones are baked with the same damped follow as the live clips (follow 0.85, damp 0.45).
- The layers sit on the live idle, so the first frame matches idle frame 0 and the clip ends back near idle.

Source / licence
- Hand-keyed by script; no free spit/vomit clip was found in Mixamo, Quaternius UAL1/UAL2 or KayKit. It is original work, free to use in this project.
