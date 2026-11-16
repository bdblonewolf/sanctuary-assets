# Knell Aura FX v2. NOT TESTED in game.

Persistent aura hook for the Guard-school rite **Knell** (the Ninth Bell). Built
as **ground decals at the hero's feet** for the game's **isometric** camera.
The live game currently only plays a one-off 0.3 s ring plus 8 burst particles
on toggle and then shows nothing on the character.

v2 drops the ghost bell (Brian t497u: "Get rid of the bell lets just keep what
bottom part. The dark blue is enough indicator for now."). The Ninth Peal is a
short **dark-blue shockwave** plus a **ground flash** at the feet. There is no
bell-rune ring.

The persistent look is a compact **Diablo 2 Fanaticism-inspired** pulse in
**light blue**: a slowly spinning ground ring, a softened pool at the feet
(not a solid ball), a low ground flicker, idle pulse waves, and **9 small
rigid dark-blue marks sitting on top of the ring**, lighting one per hit.

Runtime mesh is a horizontal `PlaneGeometry` at `y ≈ 0.02–0.05 m`,
`depthWrite: false`, with `renderOrder` / `polygonOffset` so the marks draw
above the ring and nothing z-fights or sinks under the floor. No new GLB.
Recolor uses a luma / channel-mask shader (premultiplied `tint * a`). Keep
blacks: do not switch to raw Additive blending.

## Reused (load from the live library; do not copy into this folder)

| Key | Live path | Role | Runtime tint |
|-----|-----------|------|----------------|
| `shock` | `characters_art/fx_rites/fireball/fireball_shockwave_ring.png` | Persistent slowly spinning ground ring, idle pulse waves, Ninth Peal shockwave | Aura: `#4A9AD0`. Peal: `#1A3A80` |
| `glow` | `characters_art/fx_rites/campfire_flame/campfire_flame_base_glow.png` | Soft pool at the feet. A wide gaussian falloff in the shader plus a lower peak opacity stops the solid "blue ball" the v1 billboard made. Laid flat, 1.28 m. | `#8EC8F0`, peak opacity 0.28 |
| `wisps` | `characters_art/fx_rites/behest_banspere/swirl_wisps_4x4.png` | Low **ground** flicker, 4×4 at 12 fps. Not a rising column. | `#4A9AD0`, peak 0.22 |
| `glint` | `characters_art/fx_rites/heavens_shrapnel/heavens_shrapnel_ground_glint.png` | Faint spark, spread to 0.55 m and shader-softened so the sharp star does not read as a center dot. | `#8EC8F0`, peak 0.12 |
| `burst` | `characters_art/fx_rites/heavens_shrapnel/heavens_shrapnel_impact_burst_4x4.png` | Brief **ground** flash on the Ninth Peal (no body billboard). | `#1A3A80` |

## New in this folder

| Key | File | Role |
|-----|------|------|
| `marks` | `characters_art/fx_rites/knell/knell_aura_v2/knell_marks_2x1.png` | 512×256, two 256×256 cells: **unlit** (left) and **lit** (right). R = fill mask, G = outline mask, A = coverage. Empty rgb is 0. Original, small and rigid, with a darker navy outline so they read on the light-blue ring. |

v1's `knell_ghost_bell.png` is **not** in this pack.

## Credits

**Marks.** Original Sanctuary art (small rigid diamond pips, unlit + lit, with outline).

**Reused rites textures.** Already in the library under the licences recorded
with those packs; this hook only tints them at runtime and does not copy them.

No downloaded bell is used in v2, so the Lamoot CC0 credit from v1 does not apply here.

## Hook (engineer)

```js
const fx = KnellAuraFX.create(THREE, scene, {
  shock: texShock, glow: texGlow, wisps: texWisps, glint: texGlint, burst: texBurst,
  marks: texMarks,   // characters_art/fx_rites/knell/knell_aura_v2/knell_marks_2x1.png
});
fx.attach(heroObject3D);          // centered under the character root; follows world position, does not inherit rotation
fx.setOn((player.auraOn || []).includes('knell'));
fx.setCount(game.peal);           // 0–8; lights that many marks (0 = all unlit)
if (justTolledNinthPeal) fx.ninth();  // shockwave + ground flash; all 9 marks light for the toll
fx.update(dt);                    // dt in seconds
fx.dispose();
```

`setCount(n)` clamps to 0–8 to match live `game.peal`. During `ninth()` all
nine marks light, then they restore to the last `setCount` when the peal ends
(call `setCount(0)` after the toll if the game has already reset `peal`).

## Centered under the character root

The aura is **centered under the character root**. Every ground layer (ring,
pulses, glow, glint, wisps, shockwave, flash) sits at local offset `(0, y, 0)`
— no forward or side offset. The 9 marks are equally spaced (every 40°) around
that same center, at radius 0.50 m.

`attach(heroObject3D)` plus `update(dt)` copy the hero's **world position**
(x, y, and z) each frame so the ring stays under him on raised ground. They
do **not** copy rotation or scale, so the planes stay world-flat when he turns
or tilts. Do not parent the FX root to the hero mesh; leave it on the scene
and let `attach` follow.

The current hero body (`characters_art/players/player_warrior.glb`) has its
origin at the feet (Y ≈ 0 to 1.87 m) and is centered on X. The mesh extends a
bit farther in +Z than −Z (visual center is about 0.15 m forward of the root).
The aura is still locked to the **root**, not the visual midpoint. If you
attach a node whose world position is not at the feet (for example a hip
root), the ring will sit at that node instead — pass an object whose world
position is at the feet.

Flipbook UV: 4×4 wisps/burst and the 2×1 marks atlas use the same
`_cellOffset` helper as ritefx2 (`flipY`-aware, cells from the top-left).

## Sizes (metres) and timing

- Ground ring plane: **1.40 m**, slow spin **18 s/rev**, chaotic pulse ~0.52–1.00. `y = 0.030`.
- Soft foot glow: **1.28 m** ground decal, `y = 0.022`, peak opacity **0.28**, wide gaussian falloff.
- Ground wisps: **0.72 m**, `y = 0.026`, 12 fps, peak opacity **0.22**.
- Ground glint: **0.55 m**, `y = 0.024`, peak opacity **0.12**, shader-softened.
- Count marks: **0.17 m**, 9 pips on the bright ring band at radius **0.50 m**
  (`0.7125 × 0.70 m`), starting at +Z, every 40°. `y = 0.048`, `renderOrder = 10`.
  Unlit fill `#1A3A80`, lit fill `#2E5AC0`, outline `#0C1A40`.
- Idle pulse wave: **0.50 → 1.56 m** over **0.85 s**, every ~1.0 s, `y = 0.032`.
- Ninth Peal shockwave: **0.56 → 2.10 m** over **0.40 s**, dark blue, `y = 0.036`.
- Ninth Peal flash: **0.35 s**, ground decal, `y = 0.038`.
- Fade in **0.18 s**, fade out **0.25 s**.

## Colours (runtime tints, hex)

- Light blue (aura, ring, wisps, idle waves): `#4A9AD0` mid, `#8EC8F0` core/glow.
- Dark blue (Ninth Peal shockwave + flash, unlit marks): `#1A3A80`.
- Lit marks: `#2E5AC0` (still dark blue, brighter so the count reads).
- Mark outline: `#0C1A40`.

Keep blacks: the shader writes premultiplied `tint * a`. Do not switch to raw
Additive blending or raise the glow/glint peaks without a visual check — that
is what made the v1 "blue ball."

## Files in this folder

| File | Notes |
|------|--------|
| `knell_aura_fx.js` | `KnellAuraFX.create` as above. `node --check` only. |
| `knell_marks_2x1.png` | New. 2×1 unlit/lit mark atlas (R fill, G outline). |
| `USAGE.md` | This note. |

Library path: `characters_art/fx_rites/knell/knell_aura_v2/`. Do not copy the
reused `fx_rites` textures into this folder (library rule: one copy of each
file). v1 was left untouched and was not pushed.

## Runtime status

**NOT TESTED** in three.js or in the game. Only `node --check` was run on the JS.

Previews (Python/headless isometric mimic, **not** the game renderer) were made
locally and are not part of this pack.
