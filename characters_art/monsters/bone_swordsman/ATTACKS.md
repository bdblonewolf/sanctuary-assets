# bone_swordsman — light / heavy attacks (add-only)

File: `bone_swordsman_v2_attacks.glb` — a copy of `bone_swordsman_v2.glb` with **2 clips appended**. The existing 10 clips are untouched, the rig is unchanged (no re-rig, no finger/wrist patches). `bone_swordsman.glb`, `bone_swordsman_v2.glb`, `README.md`, `README_v2.md` are not modified.

Metadata: `clip_meta_attacks.json` (full numbers + checks).

| Clip | Duration | Frames | Impact frame | Impact time | Source |
|------|----------|--------|--------------|-------------|--------|
| `skeleton_attack_light` | 0.90 s | 28 | **14** | 0.467 s | Mesh2Motion CC0 `m2m_sword_regular_a` (+ `_rec`), as downloaded, retargeted |
| `skeleton_attack_heavy` | 1.80 s | 55 | **24** | 0.80 s | Mesh2Motion CC0 `m2m_two_handed_overhead_slam`, as downloaded, retargeted |

- 30 fps, lowercase clip names, **in place** (no root motion).
- Light: one-hand right-hand sword swing.
- Heavy: both hands on the grip, sword up overhead, chops all the way down onto the target (blade lowest at f24), recovers to idle.
- Both clips start and end on idle frame 0; feet are locked on their idle spots (0.0 cm first-vs-last).
- Licence: Mesh2Motion animations are CC0.

Gameplay numbers Brian asked for (engineer wires these; not in the glb): level 1 Skeleton 100 HP, light attack 1–3 dmg, heavy attack 2–9 dmg, 10 defense, always hits.

**Runtime: NOT TESTED** — not played in the game or loaded in three.js.
