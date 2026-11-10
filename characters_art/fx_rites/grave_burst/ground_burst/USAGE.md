# Grave Burst — ground burst FX (add-only, CC0, procedural/original)

Files (4x4 sheets, 256 px cells, 1024x1024, premultiplied alpha, true-black edges):

| File | Blend | Use |
|------|-------|-----|
| `ground_crack_decal_flipbook.png` | NORMAL, flat ground decal | cracks race out, soil heaves, ends in a dark crater (16 fps, holds last frame, then fades) |
| `dirt_burst_spray_flipbook.png` | NORMAL, camera-facing | dirt clods + fine soil thrown up and falling (16 fps) |
| `dust_puff_flipbook.png` | NORMAL (not additive), camera-facing | low dark soot-brown dust wisps, soft (12 fps). Polished 2026-11-10: darker/thinner, keep-blacks |
| `rock_debris_atlas.png` | NORMAL, 16 single sprites | very small rocks / chips / pebble clusters, crisp silhouettes |
| `ground_burst_fx.js` | — | `GraveGroundBurst.create(THREE, scene, {crack, spray, dust, rocks}, opts)` → `burst(pos, {small})`, `update(dt)`, `dispose()` |

## When to spawn
- `burst(pos, { small: true })` at the **slam impact, frame 19 (0.633 s)** of `grave_burst_slam_v2` (also `_male_v2` / `_female_v2`).
- `burst(pos)` (full burst) **when the stone cross breaks the ground** (engine's existing ~1 s delay).

Rocks: 34 very small rocks (≈2–6.5 cm, a few 9 cm chips), thrown radially + upward 1.6–4.2 m/s, gravity 9.8, up to 2 bounces, fade at 1.25–1.6 s.

Keep blacks: do not lift the darks of the crater/cracks/dust.

**Runtime: NOT TESTED** — only `node --check` was run on the JS; not played in the game.
