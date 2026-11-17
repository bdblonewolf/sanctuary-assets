# Knell Aura FX v3. NOT TESTED in game.

Persistent aura hook for the Guard-school rite **Knell** (the Ninth Bell). Built
as **ground decals at the hero's feet** for the game's **isometric** camera.
v2 is live in the library (`characters_art/fx_rites/knell/knell_aura_v2/`,
commit `a08b43b`) and is left untouched.

The whole aura is scaled to **80%** (`opts.scale` default `0.8`) so the same
textures sit on a tighter footprint and read denser. The sigil mask's star
centroid is locked to the UV / plane center.

The fire is a **darker blue** (Brian t503u): deep `#1E4C8C` to medium `#3A78C0`,
with cores capped at `#6AA8E0`. Gold (`#D8A040`) is only a faint hint on a few
tips and streaks, at about 20% of the earlier gold peaks. Edges are **hazy and
feathered** like a Diablo 2 aura (soft kernel on the sigil, fire, tendrils,
embers, and peal, plus a soft outer haze glow). The 9 marks stay crisp so the
count still reads. The aura is **always animated** (flipbook fire, UV drift,
per-spike warp, pulse, slow haze / fork / ember spin, flickering tendrils).

v3 drops the **blue circle** (Brian t499u: "Lets make the blue circle no longer
a circle... a chaotic, jagged starburst sigil... sharp, irregular spikes of
flickering gold and blue fire... crackling flame tendrils shooting outward.
No smooth circles, no solid rings."). There is no spinning ring, no pulse
ring, no shockwave ring, and no ghost bell.

The persistent look is a compact **jagged starburst sigil** of flickering
**gold and light-blue fire**, projected flat under the feet. The Fanaticism-
style pulse is now the spikes growing and shrinking chaotically (uneven
per-spike lengths over time), not expanding rings. **9 small rigid dark-blue
marks** sit on the inner part of the star / the spike bases and light one per
hit. The Ninth Peal is a short **dark-blue jagged spike flare** (the sigil
plus the crackle forks, scaled out) — not a ring.

Runtime mesh is a horizontal `PlaneGeometry` at `y ≈ 0.02–0.05 m`,
`depthWrite: false`, with `renderOrder` / `polygonOffset` so the marks draw
on top and nothing z-fights or sinks under the floor. No new GLB. Recolor
uses a luma / channel-mask shader (premultiplied `tint * a`) with an optional
radial warp. Keep blacks: do not switch to raw Additive blending.

## Reused (load from the live library; do not copy into this folder)

| Key | Live path | Role | Runtime tint |
|-----|-----------|------|----------------|
| `flame` | `characters_art/fx_rites/fireball/fireball_explosion_flipbook.png` | 4×4 fire fill, **masked by the sigil** so the circular explosion never shows as a circle. Main layer is darker blue with a slow UV drift; a faint gold layer stays as a hint. Soft-edged. | Blue: `#3A78C0`. Gold hint: `#D8A040` |
| `fork` | `characters_art/fx_rites/arc_whip/arc_whip_impact_fork_4x4_v2.png` | Crackling tendrils laid flat, 4×4. The circular core is faded out so only the jagged forks show. Soft-edged, tinted darker blue. | `#3A78C0` / `#6AA8E0`. Peal: `#1A3A80` |
| `embers` | `characters_art/fx_rites/fireball/fireball_sparks_embers.png` | Scattered streaks around the sigil, soft-edged, slow spin | `#3A78C0` |
| `trail` | `characters_art/fx_rites/fireball/fireball_trail_strip.png` | Short tendrils at the nine spike tips, flickering and growing. Most are darker blue; two tips keep a faint gold hint. Soft-edged. | Blue: `#3A78C0`. Gold hint: `#D8A040` |
| `marks` | `characters_art/fx_rites/knell/knell_aura_v2/knell_marks_2x1.png` | 9 count marks. Reused in place (library rule: one copy). | Unlit `#1A3A80`, lit `#2E5AC0`, outline `#0C1A40` |

Intentionally unused: `fireball/fireball_shockwave_ring.png` (smooth solid ring)
and `campfire_flame/campfire_flame_base_glow.png` (soft circular pool).

## New in this folder

| Key | File | Role |
|-----|------|------|
| `sigil` | `characters_art/fx_rites/knell/knell_aura_v3/knell_sigil_starburst.png` | 1024×1024 jagged irregular starburst mask. R = fill, G = hot rim (tips and edges), A = coverage. Empty rgb is 0. Nine uneven major spikes plus shorter messy intermediates. No circular core, no ring. The star's alpha-weighted centroid is locked to the texture / plane center. Drawn with a soft 9-tap edge so the spikes stay readable but hazy. |
| `haze` | `characters_art/fx_rites/knell/knell_aura_v3/knell_sigil_haze.png` | Soft, blurred outer glow of the same starburst (dilated + gaussian, recentered). Used as a D2-style aura veil under the sigil, not as a ring or disc. |

The marks atlas is **not** duplicated here — load the live v2 file.

## Credits

**Sigil.** Original Sanctuary art (procedural jagged starburst mask).

**Marks.** v2 count-mark atlas, already in the library; this hook only points at it.

**Reused rites textures.** Already in the library under the licences recorded
with those packs; this hook only tints them at runtime and does not copy them.

## Hook (engineer)

```js
const fx = KnellAuraFX.create(THREE, scene, {
  sigil: texSigil,   // characters_art/fx_rites/knell/knell_aura_v3/knell_sigil_starburst.png
  haze: texHaze,     // characters_art/fx_rites/knell/knell_aura_v3/knell_sigil_haze.png
  flame: texFlame,   // fireball/fireball_explosion_flipbook.png
  fork: texFork,     // arc_whip/arc_whip_impact_fork_4x4_v2.png
  embers: texEmbers, // fireball/fireball_sparks_embers.png
  trail: texTrail,   // fireball/fireball_trail_strip.png
  marks: texMarks,   // characters_art/fx_rites/knell/knell_aura_v2/knell_marks_2x1.png
}, { scale: 0.8 });   // default; pass 1.0 for the unscaled 1.62 m size
fx.attach(heroObject3D);          // centered under the character root; follows world position, does not inherit rotation
fx.setOn((player.auraOn || []).includes('knell'));
fx.setCount(game.peal);           // 0–8; lights that many marks (0 = all unlit)
if (justTolledNinthPeal) fx.ninth();  // jagged dark-blue spike flare; all 9 marks light for the toll
fx.update(dt);                    // dt in seconds
fx.dispose();
```

`setCount(n)` clamps to 0–8 to match live `game.peal`. During `ninth()` all
nine marks light, then they restore to the last `setCount` when the peal ends
(call `setCount(0)` after the toll if the game has already reset `peal`).

## Centered under the character root

The aura is **centered under the character root**. The sigil, fire fill,
forks, embers, and peal flare sit at local offset `(0, y, 0)` — no forward or
side offset. The 9 marks are equally spaced (every 40°) around that same
center, at unscaled radius 0.40 m (0.32 m at the default scale of 0.8;
spike bases, just outside the boots). The 9 flame tendrils sit on that same
center at unscaled radius 0.62 m (0.496 m at scale 0.8), pointing outward.

`attach(heroObject3D)` plus `update(dt)` copy the hero's **world position**
(x, y, and z) each frame so the sigil stays under him on raised ground. They
do **not** copy the hero's rotation or scale, so the planes stay world-flat
when he turns or tilts. The FX root's own scale is set to `opts.scale`
(default **0.8**) every frame. Do not parent the FX root to the hero mesh;
leave it on the scene and let `attach` follow.

The current hero body (`characters_art/players/player_warrior.glb`) has its
origin at the feet (Y ≈ 0 to 1.87 m) and is centered on X. The mesh extends a
bit farther in +Z than −Z (visual center is about 0.15 m forward of the root).
The aura is still locked to the **root**, not the visual midpoint. If you
attach a node whose world position is not at the feet (for example a hip
root), the sigil will sit at that node instead — pass an object whose world
position is at the feet.

Flipbook UV: 4×4 flame/fork and the 2×1 marks atlas use the same
`_cellOffset` helper as ritefx2 (`flipY`-aware, cells from the top-left).

## Sizes (metres) and timing

Default `opts.scale` is **0.8** (20% smaller than the unscaled sizes below).
Texture resolution is unchanged; the same pixels on a smaller footprint read
denser. Visual size at the default scale is in parentheses.

- Soft haze veil: **1.98 m** (1.58 m at 0.8), darker blue, slow spin, `y = 0.020`.
- Starburst sigil plane: **1.62 m** (1.30 m at 0.8), chaotic per-spike radial warp ~±20%,
  darker-blue body with a faint gold hint layer. Soft 9-tap edges. `y = 0.024`.
- Fire fill (fireball explosion flipbook, masked by the sigil): **1.62 m** (1.30 m at 0.8), 12 fps,
  main darker-blue layer plus a faint gold hint, both with a slow UV drift, soft-edged. `y = 0.028`.
- Crackle forks: **1.85 m** (1.48 m at 0.8), 10 fps, center faded (radius 0.30 of the plane)
  so the texture's circular core does not show, slow spin, soft-edged, darker blue. `y = 0.032`.
- Ember scatter: **1.50 m** (1.20 m at 0.8), darker blue, soft-edged, `y = 0.034`.
- Tip tendrils: **0.30 × 0.10 m** (0.24 × 0.08 m at 0.8), 9 of them at radius **0.62 m** (0.50 m at 0.8), starting
  at +Z, every 40°. Independent flicker and length pulse. Seven are darker blue; two carry a faint gold hint. Soft-edged. `y = 0.036`.
- Count marks: **0.17 m** (0.14 m at 0.8), 9 pips at radius **0.40 m** (0.32 m at 0.8; spike bases, just outside the boots), starting at +Z,
  every 40°. `y = 0.048`, `renderOrder = 12`. **Kept crisp** (no edge blur).
  Unlit fill `#1A3A80`, lit fill `#2E5AC0`, outline `#0C1A40`.
- Ninth Peal flare: same jagged sigil + soft haze + forks, dark blue, scales **1.0 → 1.55**
  of the already-scaled sigil over **0.45 s**. Soft-edged, no ring. `y = 0.040`.
- Fade in **0.18 s**, fade out **0.25 s**.
- `opts.scale`: default **0.8**. Pass `1.0` to restore the unscaled sizes.

## Colours (runtime tints, hex)

- Deep blue (haze, sigil body): `#1E4C8C`.
- Medium blue (fire fill, forks, most tendrils): `#3A78C0`.
- Brightest core cap: `#6AA8E0` (do not go paler).
- Gold hints only (`#D8A040`), at about 20% of the earlier gold opacities, on a
  faint sigil/fire layer and two spike-tip tendrils.
- Dark blue (Ninth Peal flare, unlit marks): `#1A3A80`.
- Lit marks: `#2E5AC0` (still dark blue, brighter so the count reads).
- Mark outline: `#0C1A40`.

Keep blacks: the shader writes premultiplied `tint * a`. Do not switch to raw
Additive blending or raise the fire peaks without a visual check.

## Files in this folder

| File | Notes |
|------|--------|
| `knell_aura_fx.js` | `KnellAuraFX.create` as above. `node --check` only. |
| `knell_sigil_starburst.png` | 1024 jagged starburst mask (R fill, G rim), centroid-centered. |
| `knell_sigil_haze.png` | Soft blurred outer glow of the same star, centroid-centered. |
| `USAGE.md` | This note. |

Library path:
`characters_art/fx_rites/knell/knell_aura_v3/`. Do not copy the reused
`fx_rites` textures or the v2 marks atlas into this folder (library rule:
one copy of each file). Live v2 was left untouched.

## Runtime status

**NOT TESTED** in three.js or in the game. Only `node --check` was run on the JS.

Previews (Python/headless isometric mimic, **not** the game renderer) were made
locally and are not part of this pack.
