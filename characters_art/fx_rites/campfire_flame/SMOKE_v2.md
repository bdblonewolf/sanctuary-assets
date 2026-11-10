# Campfire smoke shader / particle script — v2

For the environment bot. **LOCAL handoff, not pushed. GLSL is NOT COMPILED.
The shader and the particle script are NOT TESTED in three.js or in the game.**
The JS was syntax-checked with `node --check` only.

The existing Fireball puff `characters_art/fx_rites/fireball/fireball_smoke_flipbook.png`
is a soft brown cloud — too soft, and too gray-brown, for a dark-fantasy
bonfire sitting in fog. A new sheet is in this folder:

- `campfire_smoke_flipbook_v2.png` — 1024×1024, 4×4, 16 frames, **normal
  blend (NOT additive)**, premultiplied, deep matte soot (not gray),
  true-black / zero-alpha edges, KEEP BLACKS
- `smoke_shader_v2.js` — `ShaderMaterial` + a rising-card particle script
- `preview_campfire_smoke_composite_v2.png`, `preview_campfire_smoke_contact_v2.png`,
  `preview_campfire_smoke_loop_v2.gif` — 2D previews over a dark foggy
  cobblestone / log-pile scene (so the black soot has something to read
  against). **NOT TESTED in the game.**

Play the sheet at **12–16 fps**. The preview GIF is at 12 fps.

## Rules, as implemented

### 1. BASE — born almost invisible

Where the smoke is born (just above the flame apex) it is **highly
transparent**: only a subtle, faint heat-tint over the fire, no cloud
clutter and no screen blockage.

The fragment shader eases alpha with a smoothstep on normalized age
(`uInvisibleUntil`, default **0.25**). The first 25 % of the particle's
life / vertical ascent stays near-invisible, then it eases in. There is
no pop.

The texture itself is also thinner at the bottom of each cell, so even a
static card does not drop a solid puff onto the flames.

### 2. SOOT INVERSION — deep matte black at the tips, not gray

In the upper **50–75 %** of lifetime (`uSootStart` 0.50, `uSootEnd` 0.75)
the colour ramps from a faint warm heat-tint `(0.16, 0.07, 0.03)` to a
**deep matte soot black** `(0.025, 0.016, 0.012)`. That is a warm near-black,
not a mid-gray, and not a flat geometric fill — the shape comes from the
tendril texture plus a tight, tunable alpha smoothstep (`uLo` / `uHi`,
defaults 0.18 / 0.42).

`toneMapped: false` and `premultipliedAlpha: true` on a
`THREE.NormalBlending` material (One, OneMinusSrcAlpha). Do not lift the
soot toward gray. Do not switch this material to additive — additive black
smoke vanishes, and additive gray smoke washes the scene.

Against a dark foggy environment the soot reads as a *darker-than-fog*
tendril. The 2D previews composite over a slightly lifted dark fog so you
can see that; a pure-black backdrop would hide it.

### 3. TRAIL — upward velocity, small wind, grit dissipation

Motion is in the **particle script**, not the fragment shader:

- Strictly **upward** velocity. Over a default life of 2.8 s a card rises
  about **2.2 m**.
- Subtle wind-driven horizontal turbulence: a small-amplitude, noise-driven
  sway (default 0.16 m). It is not a sideways drift that would shear the
  column into a smear.
- Spawn just above the flame apex. The flames themselves are 1.0–1.3 m
  tall in a 1.2 m pit; default `spawnY` is **1.25 m** above the log-pile
  pivot, with 0.18 m of jitter.

At the end of life, the fragment shader replaces any blur-out with a
**high-frequency noise dissolve**: a fine hash / value-noise mask compared
to a threshold that rises with normalized age (`uDissolveStart` 0.78 → 1.0).
The black soot fragments and dithers away into sharp microscopic wisps
until it is gone. No muddy mist.

## Soft-particle depth fade

The same **0.1 world-unit** contract as the fire shader. Reuse the **same
linear view-distance pre-pass** (`createLinearDepthMaterial` /
`createFireDepthTarget` in `campfire_fire_shader_v2.js`). Bind it through
`update(dt, depthSetup)`. See `SHADER_v2.md` §2 for the near/far unpack,
why a `DepthTexture` is only safe with log-depth **off**, and why the
linear color pre-pass is the recommended path either way.

Do not render the smoke (or the fire) into that pre-pass.

## Particle script

`createCampfireSmokeRig(THREE, opts)`:

- Builds `count` (default 6) upright cards, staggered in age so the column
  is always populated.
- Per-particle **age**, a **random flipbook frame offset**, and a slight
  yaw so stacked cards do not z-fight as one plane.
- Pivot at the bottom center. Scale eases up slightly as a card rises
  (thin at birth, a wider soot head later).
- `depthWrite: false`, normal blend, renderOrder under the additive fire
  and over the solids.
- `update(dt, depthSetup)` advances age, position (up + wind), frame, and
  the depth-fade uniforms.

## What this file does not claim

- The GLSL has **not** been compiled.
- The material, the depth fade, and the particle motion have **not** been
  run in three.js or in the game. **NOT TESTED.**
- The 2D previews apply a CPU stand-in of the age / soot / dissolve curve
  over a flat stack of cards. They are not a 3D simulation of the rig.
