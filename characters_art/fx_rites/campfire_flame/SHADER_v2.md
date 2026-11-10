# Campfire fire shader / particle script — v2

For the environment bot. **LOCAL handoff, not pushed. GLSL is NOT COMPILED. The
shader and the particle script are NOT TESTED in three.js or in the game.**
The JS was syntax-checked with `node --check` only.

Companion files:

- `campfire_fire_shader_v2.js` — `ShaderMaterial` (additive, `depthWrite: false`) plus a small particle / rig script
- `campfire_flame_flipbook_v2.png` and `campfire_flame_flipbook_b_v2.png` — 1024×1024, 4×4, 16 frames, 16 fps, additive, premultiplied, true-black edges
- `smoke_shader_v2.js` / `SMOKE_v2.md` / `campfire_smoke_flipbook_v2.png` — the smoke stack that sits above this fire

The looping flame billboard already has a grit-dissolve baked into the **tips**
of the v2 sheet. Leave `uDissolveStrength` at `0` on that billboard so the
shader does not double-eat the tips. Raise it only for short-lived flame
*particles* that should break apart at the end of their life.

## 1. Alpha contrast (no linear fade)

Do **not** fade the particle with a linear `alpha *= (1.0 - age)` or a linear
texture-alpha multiply.

The fragment shader compresses the authored texture alpha with a tight
smoothstep, uniforms `uLo` / `uHi` (defaults **0.25** / **0.45**, matching
Brian's example):

```
alpha = smoothstep(uLo, uHi, texAlpha);
```

That tightens residual blurry edges into distinct flame tendrils. Sample the
flipbook with **linear** filtering (`LinearFilter`, no mipmaps). A nearest
lookup would look pixelated; a binary `step()` cut would look geometric. The
smoothstep is a contrast curve, not a hard rim.

The PNG is **premultiplied** (RGB already × alpha; RGB is 0 where alpha is 0).
The shader un-premultiplies to apply the clamp, then re-premultiplies for
`THREE.AdditiveBlending` (One, One).

`toneMapped: false` on the material so the engine tone-map / bloom does not
lift the true-black edges. Do not multiply the material by a gray tint. Cap
intensity (`uIntensityCap`, default 1.35).

## 2. Soft-particle depth fade (0.1 world units)

To stop the tightened flames from drawing a hard geometric clip line where
the billboard intersects a log, a stone, or the ground, the fragment shader
multiplies alpha by:

```
alpha *= smoothstep(0.0, uSoftDistance, sceneViewDist - fragViewDist);
```

with `uSoftDistance = 0.1` (metres). When the flame is within 0.1 units of
any solid in the depth pre-pass, it fades to 0.

### Recommended setup: linear view-distance color pre-pass

This path is the reliable one. It does not depend on whether
`logarithmicDepthBuffer` is on, and it does not need an unpack of
window-depth.

1. Allocate a float (or half-float) color target of the drawing-buffer size,
   with a depth buffer. See `createFireDepthTarget(THREE, renderer, w, h, true)`
   and `createLinearDepthMaterial(THREE)` in the JS file.
2. Each frame, before drawing the fire:
   - `renderer.setRenderTarget(depthTarget)`
   - render **solids only** (logs, stones, ground, buildings — no fire, no
     smoke, no other additive FX) with the linear-depth override material.
     That material writes `-viewPos.z` (positive view distance) into the red
     channel.
   - `renderer.setRenderTarget(null)`
3. Bind that color texture as `uDepth`, set `uUseDepth = 1`,
   `uDepthIsLinear = 1`, and pass `uCameraNear` / `uCameraFar` / the target
   size. The fire rig's `update(dt, depthSetup)` helper does the bind.

Resize the target when the drawing buffer changes (`renderer.getSize()` ×
`getPixelRatio()`).

### Alternative: a `DepthTexture` on a `WebGLRenderTarget`

Attach a `THREE.DepthTexture` (DepthFormat, UnsignedIntType) and render the
solid scene with its real materials. Bind `target.depthTexture` as `uDepth`
and set `uDepthIsLinear = 0`. The shader then unpacks with a standard
perspective conversion:

```
// window depth in [0, 1] → NDC z in [-1, 1]
zNdc = depth * 2.0 - 1.0
// three.js view Z is NEGATIVE in front of the camera
viewZ = (2.0 * near * far) / (zNdc * (far - near) - far - near)
sceneViewDist = -viewZ
```

**This alternative is only correct when `logarithmicDepthBuffer` is false.**

### Logarithmic depth

When `renderer.logarithmicDepthBuffer === true`, the value in a stock
`DepthTexture` is not the standard perspective window depth, so the unpack
above is wrong. three.js writes something of the form

```
gl_FragDepth = log2(max(1e-6, 1.0 + clip.w)) * logDepthBufFC * 0.5
```

with `logDepthBufFC = 2.0 / log2(camera.far + 1.0)`. Recovering a linear
view distance from that is easy to get slightly wrong across revisions, and
this file does **not** claim to have a tested unpack for it.

**Use the linear view-distance color pre-pass instead** whenever log-depth
is on (and, honestly, even when it is not — it is the simpler contract).

Do not render the fire or the smoke into the pre-pass, or the soft fade
will try to fade them against themselves.

## 3. Grit-dissolve at the apex of lifetime

For short-lived flame particles (not the looping campfire billboard), the
shader compares a fine hash / value-noise mask to a rising threshold driven
by normalized `uAge` (and, secondarily, by `uv.y` so tips break apart):

- Threshold starts low and rises toward 1 as age passes `uDissolveStart`
  (default 0.65) and as `uv.y` approaches the top of the quad.
- A *narrow* smoothstep, not a blur, decides which pixels survive. The tips
  break into sharp flickering micro-embers, not a muddy mist.
- A small amber (not red) colour boost is added on the dissolve *edge*.

The noise is hashed in UV + time so the fragments flicker. Looping campfire
billboards should keep `uDissolveStrength = 0`; the v2 flipbook already
bakes this at the tips.

## 4. Dark gothic palette, and light on the cobblestones

- `uTint` defaults to white so the authored colour (hint of blue-violet at
  the base, white-yellow heart, orange to dark amber tips) is preserved.
- `uIntensity` is capped (`uIntensityCap`). No bloom wash, no gray lift,
  keep blacks.
- The rig creates a **small, warm, decaying point light** at about 0.35 of
  the flame height: colour `0xffa24a` (warm orange, not red, not white),
  low intensity (default 1.6), distance about 6 m, decay 2. That is meant
  to throw a high-contrast, tight pool of light onto the surrounding
  cobblestones — not to flood the scene.
- Flicker is a cheap CPU hash **quantized to the same 16 fps as the
  flipbook**, so the light and the flame read as one fire, not two clocks.
- Shadow-casting is **off** by default (cost, and it can Peter-pan against
  the soft particles). If you turn it on, use a tight shadow camera (near
  ~0.15, far = light distance, 512 map, a small negative bias) and look at
  it in the game before leaving it on. That path is NOT TESTED.

## Particle / rig script (in the same JS file)

`createCampfireFireRig(THREE, opts)` builds:

- Two crossed upright planes (world XY and ZY), **not** both camera-facing,
  so the fire keeps volume from more than one angle. Billboard B uses
  `campfire_flame_flipbook_b_v2.png` (a different seed, not a copy) at 92 %
  scale, with a **different random frame offset**.
- Pivot at the **bottom center**. Put the group origin at the top-center of
  the log pile, inside the teepee, not in front of the near logs.
- Quad size: **1.20 m wide × 1.30 m tall**, 16 fps, 4×4 UV math (frame 0 is
  the top-left cell; see USAGE_v2.md).
- The flickering point light described above.
- `createEmberParticles` — a handful of short-lived additive sprites using
  the existing Fireball sheet `characters_art/fx_rites/fireball/fireball_sparks_embers.png`.
- Smoke is a separate rig: `createCampfireSmokeRig` in `smoke_shader_v2.js`,
  using `campfire_smoke_flipbook_v2.png` (preferred) or the softer
  `fireball_smoke_flipbook.png` as a fallback. Spawn it just above the
  flame apex (1.0–1.3 m). See `SMOKE_v2.md`.

`update(dt, depthSetup)` advances frames, flicker, and (if you pass it) the
depth-fade uniforms.

## What this file does not claim

- The GLSL has **not** been compiled.
- The material, the depth pre-pass, the light, and the particle motion have
  **not** been run in three.js or in the game. **NOT TESTED.**
- `texture2D` / `varying` is written in a WebGL1-style dialect; `uMapSize`
  is a uniform so it does not need `textureSize()` (ES3). If your engine
  forces WebGL2/`in`/`out`/`texture()`, adapt accordingly — that conversion
  is also NOT TESTED.
