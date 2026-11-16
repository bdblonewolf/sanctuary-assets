# Thrall spawn burst v1 (add-only, original work, CC0-compatible). NOT TESTED in game

Dark-red variant of Grave Burst's `ground_burst` pack
(`characters_art/fx_rites/grave_burst/ground_burst/`). Same compact scale, same
4×4 / 256 px cell / 1024×1024 layout, same frame counts, same premultiplied-alpha
+ true-black 2 px cell borders, and the same runtime mesh (a flat ground-plane
decal + camera-facing sprites) and physics as `GraveGroundBurst`. There is no
separate GLB mesh — the original pack also has none; the JS builds a
`PlaneGeometry` and sprites at runtime. No hero slam clip is included (that
belongs to the rite, not to monster spawn).

## Usage (Brian, 2026-11-16)

Use for ANY enemy that randomly spawns into the map (only random map spawns for
now): play the burst at the spawn point and the monster crawls/rises out of the
earth from it. Not for scripted/boss spawns.

- Call `burst(pos)` at the spawn point when the random spawn happens. `pos` is a
  `THREE.Vector3` on the ground.
- `burst(pos, { small: true })` if a smaller pop is wanted (0.45 scale, fewer
  rocks/dust), same hook as the original.
- This pack is FX only: it has no emerge clip and no emerge callback. Start the
  monster's crawl/rise from the same spawn point so it appears to come out of
  the opening earth. Suggested start (from flipbook inspection, NOT TESTED in
  game): at `burst()` or by ~0.125 s (decal frame 2 at 16 fps), when the crater
  hole is open. Cracks finish growing by ~0.688 s (frame 11).

## What changed vs Grave Burst

- Earth browns kept, with dark-red pigment (around `#4a0c0a`–`#6e1410`, not
  bright) mixed into the soil / crater chunks.
- Rocks and flying rubble (rock atlas + dirt-spray clods) are dark red. Fine
  soil mist in the spray stays earth with a slight red tint.
- Dust stays earth, with only a faint red tint.
- Crack pattern is simply different: 7 radial cracks (was 8), start angle
  rotated ~27°, new path / chunk seeds. Same growth timing.
- Keep-blacks: darks were checked equal-or-darker than the original
  (5th-percentile and mean unpremultiplied luma). Cracks and the crater hole
  stay near-black.

## Files

| File | Blend | Use |
|------|-------|-----|
| `ground_crack_decal_flipbook.png` | NORMAL, flat ground decal | new 7-ray cracks race out, rust-red soil heaves, ends in a dark crater (16 fps, holds last frame, then fades) |
| `dirt_burst_spray_flipbook.png` | NORMAL, camera-facing | earth soil mist + dark-red clods thrown up and falling (16 fps) |
| `dust_puff_flipbook.png` | NORMAL (not additive), camera-facing | low dark soot-brown dust wisps with a faint red tint, soft (12 fps) |
| `rock_debris_atlas.png` | NORMAL, 16 single sprites | same silhouettes as Grave Burst (same seeds), recolored to dark red stone |
| `thrall_spawn_burst_fx.js` | — | `ThrallSpawnBurst.create(THREE, scene, {crack, spray, dust, rocks}, opts)` → `burst(pos, {small})`, `update(dt)`, `dispose()`. Physics and defaults are the same as `GraveGroundBurst`. |

All four textures are new (none were identical to the original, so none are
referenced in place). The JS is a renamed copy of `ground_burst_fx.js` with
spawn-focused comments; the engineer can also keep using `GraveGroundBurst.create`
and just point it at these textures.

## Timing (from the JS defaults; NOT TESTED in game)

- Decal: 16 frames at 16 fps = 1.0 s play, then `decalHold` 2.5 s on the last
  frame, then `decalFade` 1.2 s.
- Dirt spray: 16 frames at 16 fps = 1.0 s.
- Dust: 16 frames at 12 fps = 1.333 s, with puff delays of 0 / 0.06 / 0.12 s.
- Rocks: 34 very small rocks (≈2–6.5 cm, a few 9 cm chips), thrown radially +
  upward 1.6–4.2 m/s, gravity 9.8, up to 2 bounces, fade at 1.25–1.6 s
  (`rockLife` 1.6, `rockFade` 0.35, launch delay up to 0.05 s).

Call `fx.update(dt)` every frame (`dt` in seconds). `fx.dispose()` when done.

Keep blacks: do not lift the darks of the crater / cracks / dust / rocks.

**Runtime: NOT TESTED** — only `node --check` was run on the JS; not played in
three.js or in the game. Previews used during review were a Python
re-implementation of the JS physics, not the game renderer, and were not pushed.
