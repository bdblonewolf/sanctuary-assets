# Grave Burst — cast clip (`grave_burst_slam`)

Hero mixamorig, meter scale. Kneel + **both hands slam into the ground**.

Brian direction (t437u): "graveburst both hands slam into ground".

## Files

| File | What |
|------|------|
| `grave_burst_slam.glb` | Clip `grave_burst_slam`, 1.40 s, 30 fps, in place |
| `grave_burst_slam_male.glb` | Byte-identical copy (same mixamorig names) |
| `grave_burst_slam_female.glb` | Byte-identical copy |
| `clip_meta.json` | Duration, impact frame, source, floor-contact check |
| `previews/preview_clip_strip.png` | 8-frame stick-figure strip; impact marked gold |
| `build_clip.py` / `compose_preview.py` | Rebuild scripts (local handoff only) |

## Clip timing

- **Name:** `grave_burst_slam`
- **Duration:** 1.40 s @ 30 fps (43 samples, inclusive)
- **Impact:** **frame 19 / 0.633 s** (~45%) — both hands at floor contact
- **Phases:** wind-up (hands overhead) → drop to kneel → dual-hand slam → brief hold → rise / loop-out
- **In place:** hips XZ locked; no root drift

## Source

- Mesh2Motion CC0: `m2m_attack_ground_pound` from `models/3d_rigs/m2m_human_anims_mixamo.glb`
- Window ~0.00–1.05 s of source (overhead peak ~0.25 s, source slam ~0.75 s), retimed onto 1.40 s
- Hand / finger / wrist channels: **time-resampled only, never value-edited**
- Floor reach: mild hips Y dip + Arm / ForeArm / Shoulder / Spine extras at impact so palms meet the floor plane; toes stay ≥ 0

## Engineer wiring (when Brian says send)

Suggested path once approved: `characters_art/fx_rites/grave_burst/` (or the path you name).

1. Play `grave_burst_slam` on the hero mixamorig skeleton.
2. Fire the Grave Burst ground FX (stone cross / soil burst) at **impact frame 19 / 0.633 s**.
3. Male and female both use the same clip file (joint names match).

## Floor contact (validated on this build)

At impact (t=0.633 s):

- Left hand wrist Y ≈ 0.129 m (palm ~floor)
- Right hand wrist Y ≈ 0.051 m (palm on floor)
- Neither hand goes below Y=0.02 across the clip
- Toe min Y ≈ 0.013 m (no foot sink)

## Honest weaknesses

- Stick-figure preview only (not the knight mesh).
- Source is a Mixamo/M2M ground pound, retimed — not a filmed kneel-slam take.
- Left wrist sits a bit higher than the right at impact (~0.13 vs ~0.05); palms still read as ground contact.
- Rise at the end returns toward a standing recovery from the source clip, not a held kneel forever.
- No Grave Burst VFX in this package (stone cross already lives under `rites/grave_burst/`).

## Not pushed

Local handoff only. Do not push or message Build until Brian says "send it".
