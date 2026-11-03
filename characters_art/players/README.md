# Sanctuary — final PLAYER class bodies

Bare player bodies for the four classes. Each one uses the shared **mixamorig 52-bone rig** (the same bone names and rest pose convention as `characters_art/bodies/`). Units are metres, Z-up in Blender and Y-up in glTF. There are no animations or morphs. Clothing and armor are **separate, swappable skinned meshes**: attach them to the body's armature and hide the body vertices listed in the piece's `*.mask.json`.

| File | Class | Base / build | Height | Skin (sRGB) | Verts (Blender) |
|---|---|---|---|---|---|
| `player_warrior.glb` | Warrior (male) | `male_regular` scaled 1.08 / 1.08 / 1.05 (x/y/z), a slightly above-average brawler build | 1.87 m (6'1.5") | `#AA8976` (stock MPFB skin) | 14 772 |
| `player_necromancer.glb` | Necromancer (male) | `male_regular` stretched thinner, 0.90 / 0.92 / 1.105, the tallest | 1.97 m (6'5.5") | `#C4BFAA` sickly pale with a faint grey-green cast, still human | 14 772 |
| `player_archer.glb` | Archer (female) | `female_skinny` scaled to 5'3", with **Ayla's look** | 1.61 m (5'3") | Ayla's slate grey-blue texture, about `#5C6170`, with her red runes | 14 898 |
| `player_archer_hair.glb` | Archer hair | Ayla's long black strand-card hair, refit to this body, as a separate skinned mesh | top at 1.627 m | `hair_basecolor` (alpha) | 26 720 (glTF) |
| `player_elementalist.glb` | Elementalist (female) | 50/50 per-vertex blend of `female_medium` and `female_curvy` (bones averaged too) | 1.68 m (5'6") | `#AA8976` (stock MPFB skin) | 14 892 |

Node names are `player_<class>` (armature) and `player_<class>_body` (mesh). The archer's hair node is `player_archer_hair`, parented to its own copy of the `player_archer` armature. Every body keeps the MPFB `linen_undergarment` material for decency.

## Per-class notes
- **Warrior / Elementalist:** these are the approved test bodies, re-exported under final names. Vertex order is identical to the test bodies (checked index by index, max diff 0.001 mm), so the existing Damaged Black fits and masks still apply.
- **Necromancer:** only the material changed. The skin base colour is now `#C4BFAA` (it was stock `#AA8976`). Geometry and vertex order are identical, so the fit and masks are unchanged.
- **Archer:** built from Ayla Phimn (`characters_art/npcs/ayla_phimn/`):
  - **Skin and face texture:** Ayla's skin material (`skin_ayla`: 2K basecolor with AO, the red stave runes on stomach, waist, arms, thighs and back, plus roughness and normal maps) is applied to the skin slot. Both bodies share the MPFB UV layout, so the texture carries over 1:1, face included.
  - **Face shape:** Ayla's head is blended onto `female_skinny` through the UV vertex correspondence. It uses a least-squares similarity (scale 1.146, so the head is sized for a 1.60 m body), weighted by the Head bone weight with a smoothstep across the neck. The eyes move rigidly with the lids. The change is up to about 9 mm.
  - **Modesty pass:** the bust under the linen band is Taubin-smoothed so no anatomical detail shows through the undergarment, and the archer's linen is a dark undyed `#4A423A`. The look stays non-sexualized.
  - **Hair:** this is `npc_f_ayla_hair.glb` moved with the Ayla→archer body displacement field (IDW, k=16, 2 cm blur). Ayla's original skin weights are kept, since the bone names are the same. Strands that sat outside Ayla's skin are kept at least 2 mm outside the archer's skin, and roots tucked under the scalp stay tucked. Hide it when a helm is worn.
  - Because the archer's geometry changed, the Damaged Black archer variants were **refit** with `work/fit.py -- archer`, and their pieces and masks were regenerated.

## Damaged Black masks
`characters_art/equipment/damaged_black/pieces/*_<class>.mask.json` now point `body_file` at `characters_art/players/player_<class>.glb`. The base (male_regular) masks point at `characters_art/bodies/male_regular.glb`, which fixes a stray `tmp/...` path. Mask indices are body vertex indices as imported in Blender.

## Clipping check (Damaged Black, anim_v2 clips, armor verts >3 mm inside *visible* skin), pre-mobile masters
> Superseded by the final mobile pass. See `characters_art/equipment/damaged_black/README.md` (“Clipping / gap check (final)”). Boots now have 0 skin gaps in every pose.

| Class (clips) | Rest | Walk a / b | Sit | Stand up |
|---|---|---|---|---|
| warrior (male_regular) | knee 28 | knee 27/27, shoulder 0/6 | knee 38, shoulder 2, hip 1 | knee 36, shoulder 1, hip 1 |
| necromancer (male_regular) | knee 39 | knee 40/38, shoulder 0/11 | knee 46, shoulder 2 | knee 47, shoulder 1 |
| archer (female_skinny) | hip 10, knee 40 | hip 10/10, knee 37/36, shoulder 0/4 | hip 149, knee 45 | hip 113, knee 59 |
| elementalist (female_medium) | knee 44 | knee 47/56, shoulder 2/1 | knee 51, hip 11, shoulder 4 | knee 67, hip 4, shoulder 3 |

"Other" region counts (mostly the cape and greave edges) run from 15 to 56. These match the earlier fit, and the archer refit did not regress. Most of the remaining contact is the greave or boot top at the knee and the stiff skirt and cape against the thighs when seated.
Archer hair vs body (new pokes beyond the tucked roots): walk 42–68, sit 204, stand up 222 verts. Ayla's own hair on Ayla is in the same range (walk 72–239, sit 51, stand up 172).

## Renders (`renders/`)
`player_<class>_bare_{front,q34}.png`, `player_<class>_damaged_black_{front,q34}.png`, `player_<class>_sheet.png`, and the lineup `players_lineup_sheet.png` (all four bodies, bare and in the full set). They are Eevee renders on a dark background. Armored renders hide the masked body faces and the archer's hair.

### Final Damaged Black mobile pass
- The bodies in this folder are **unchanged** (52 mixamorig bones, metres, primitives skin/linen/eye, same vertex order). They are not decimated or compressed, so there is no `masters/` copy here.
- The armored renders, the per-class sheets and `players_lineup_sheet.png` were regenerated with the mobile `pieces/` (shared WebP atlas). The bare renders are unchanged.
- The optional skin-texture pass was skipped.

## Locked faces and hair (Nov 3 2026)
Faces and hair now follow Brian's locked look sheet (`starter_faces_2026-11-03`, Artspace.ai, owner's own images). Everything reuses existing meshes. The only new geometry is the necromancer's piercings.

| File (mobile, in this folder) | Tris | MB | Source |
|---|---|---|---|
| `player_archer.glb` | 27 036 | 1.06 | Body and face **geometry unchanged** (already Ayla-based). The skin texture was recoloured from Ayla's slate blue to a pale cool tone. The red runes are kept and faint face markings were added. The grey eye texture is new. |
| `player_archer_hair.glb` | 7 664 | 0.83 | Ayla hair (`npcs/ayla_phimn/pieces/npc_f_ayla_hair.glb`), refit and decimated, with long black waves (post-decimation curl) |
| `player_elementalist.glb` | 27 036 | 0.97 | MPFB face blended 0.35 toward Ayla's face (softer features), with a fair skin texture and light blue-grey eyes |
| `player_elementalist_hair.glb` | 7 654 | 0.83 | Ayla hair, refit, with long burgundy waves |
| `player_necromancer.glb` | 27 036 | 0.96 | MPFB `male_skinny` faceshape at 1.0 (gaunt, hollow cheeks, deep-set eyes, up to 23 mm), with a very pale aged skin texture |
| `player_necromancer_hair.glb` | 3 620 | 0.66 | Ayla hair, refit and slicked back, long straight white hair, cleared in front of the ears |
| `player_necromancer_piercings.glb` | 440 | 0.04 | Procedural bronze gothic brow crosses (both brows) plus dangling earrings (stud, ring, bar, cross, spike). Rigid to `mixamorig:Head`. |
| `player_warrior.glb` | 27 036 | 0.96 | MPFB `male_brute_muscular` faceshape at 0.5 (rugged jaw), with heavy stubble and the cheek scar painted into the skin texture, and brown eyes |
| `player_warrior_hair.glb` | 5 714 | 0.68 | Ayla hair, cut to shoulder length, dark brown, loose curl |

- **Vertex order is unchanged.** Every body keeps the same vertex count and order, indices, JOINTS/WEIGHTS and skin UVs, the 52 mixamorig joints with identical inverse bind matrices, and the primitive order skin/linen/eye. Only POSITION/NORMAL on the face moved. The eye `TEXCOORD_0` was rewritten for the new eye texture, with the same vertex count. The existing Damaged Black fits and `*.mask.json` files still apply.
- Each hair and piercing GLB is a separately skinned mesh on its own copy of the same 52-bone rig, with no animations. Attach it the same way as an armour piece.
- **Hide under a helm:** when the helm is equipped, hide the `player_<class>_hair` mesh node and `player_necromancer_piercings`.
- **Warrior scar side:** the scar follows the reference image, so it is on the viewer's left, which is the character's **right** cheek. The written spec says "left cheek". Flipping it is a single parameter (`scar.side`) plus a rebuild.
- **Mobile:** textures are ≤1024 WebP and the files went through `tools/mobile_compress.sh` without meshopt or Draco. There is no compression extension, only `EXT_texture_webp`. The uncompressed 2048 masters are in `masters/`.
- **Clipping check** (idle, run, ss_attack_heavy, bow_draw, magic_cast, against the body and the Damaged Black plate/helm): hair inside the body is 0–1 verts in every pose (0 new versus rest); hair inside the plate is ≤1 vert; piercings inside the body or plate are 0. The head-versus-helm counts match the original bodies: necromancer 180 versus 231 before, the others within ±5. These are the helm's open face area, so there is no regression.
- Renders: the per-view head close-ups are `renders/heads/player_<class>_head_{front,q34,side,back}.png`, the per-class reference comparisons are `renders/heads/heads_<class>.png`, and the combined sheet is `renders/heads/heads_sheet.png`. The bare renders, the per-class sheets and `players_lineup_sheet.png` were regenerated with the new heads and hair. The armoured views are unchanged because the helm covers the head.

## Pass 2: refined faces and hair (Nov 3 2026)
This pass responds to Brian's review: the top of the head looked the same on every class, the brows were identical, and the faces read as too similar. Each class now has its own crown volume, parting and hairline, its own brow, and a face morphed toward its reference photo.

**Method.** Landmark-driven morph only; no photo-to-3D fitter was needed.
- MediaPipe Face Mesh landmarks were measured on each reference crop and on orthographic front renders of the current head.
- Everything is normalised by IPD (eye-centre distance), which is held fixed so the helm fit is unchanged.
- An RBF displacement field (POSITION only) was solved and applied to the face vertices, then re-measured and iterated.
- Face shape class follows Loomis/Reilly-style rules: L/W ≥ 1.45 is long; forehead and jaw both < 0.80 of cheek width is diamond; L/W < 1.25 is square (jaw/cheek > 0.86) or round; anything else is oval.
- Thirds are hairline→brow, brow→nose base and nose base→chin, as fractions of face length.
- Every value below is in IPD units unless it is a ratio.

| metric | necromancer ref / v1 / **v2** (err) | archer ref / v1 / **v2** (err) | elementalist ref / v1 / **v2** (err) | warrior ref / v1 / **v2** (err) |
|---|---|---|---|---|
| shape | oval / long / **oval** | oval / oval / **oval** | oval / oval / **oval** | oval / oval / **oval** |
| len_over_w | 1.366 / 1.507 / **1.363** (-0%) | 1.354 / 1.372 / **1.306** (-3%) | 1.320 / 1.360 / **1.284** (-3%) | 1.299 / 1.312 / **1.300** (+0%) |
| jaw_over_cheek | 0.791 / 0.815 / **0.792** (+0%) | 0.777 / 0.783 / **0.786** (+1%) | 0.783 / 0.784 / **0.788** (+1%) | 0.844 / 0.812 / **0.840** (-0%) |
| fore_over_cheek | 0.847 / 0.861 / **0.872** (+3%) | 0.888 / 0.881 / **0.909** (+2%) | 0.836 / 0.858 / **0.882** (+5%) | 0.806 / 0.855 / **0.846** (+5%) |
| third_top | 0.221 / 0.297 / **0.227** (+3%) | 0.274 / 0.280 / **0.275** (+1%) | 0.255 / 0.268 / **0.247** (-3%) | 0.248 / 0.254 / **0.259** (+4%) |
| third_mid | 0.407 / 0.362 / **0.410** (+1%) | 0.407 / 0.392 / **0.406** (-0%) | 0.405 / 0.401 / **0.414** (+2%) | 0.365 / 0.398 / **0.361** (-1%) |
| third_low | 0.372 / 0.341 / **0.363** (-3%) | 0.319 / 0.328 / **0.319** (-0%) | 0.340 / 0.331 / **0.338** (-0%) | 0.387 / 0.348 / **0.380** (-2%) |
| eye_w | 0.428 / 0.426 / **0.435** (+2%) | 0.431 / 0.458 / **0.455** (+5%) | 0.436 / 0.440 / **0.437** (+0%) | 0.432 / 0.446 / **0.445** (+3%) |
| eye_gap | 0.501 / 0.564 / **0.542** (+8%) | 0.540 / 0.536 / **0.530** (-2%) | 0.519 / 0.539 / **0.520** (+0%) | 0.558 / 0.543 / **0.548** (-2%) |
| eyew_over_gap | 0.856 / 0.755 / **0.803** (-6%) | 0.799 / 0.855 / **0.858** (+7%) | 0.840 / 0.815 / **0.841** (+0%) | 0.774 / 0.821 / **0.813** (+5%) |
| brow_h | 0.318 / 0.372 / **0.338** (+7%) | 0.373 / 0.521 / **0.371** (-1%) | 0.366 / 0.508 / **0.387** (+6%) | 0.271 / 0.429 / **0.288** (+6%) |
| nose_len | 0.823 / 0.867 / **0.850** (+3%) | 0.760 / 0.814 / **0.726** (-4%) | 0.719 / 0.806 / **0.752** (+5%) | 0.811 / 0.859 / **0.820** (+1%) |
| nose_w | 0.631 / 0.644 / **0.610** (-3%) | 0.582 / 0.616 / **0.562** (-4%) | 0.567 / 0.617 / **0.562** (-1%) | 0.691 / 0.683 / **0.719** (+4%) |
| mouth_w | 0.729 / 0.766 / **0.742** (+2%) | 0.688 / 0.768 / **0.680** (-1%) | 0.744 / 0.765 / **0.740** (-0%) | 0.901 / 0.805 / **0.890** (-1%) |
| lip_up | 0.072 / 0.136 / **0.092** (+29%) | 0.111 / 0.121 / **0.085** (-23%) | 0.097 / 0.149 / **0.104** (+7%) | 0.102 / 0.120 / **0.098** (-3%) |
| lip_lo | 0.146 / 0.180 / **0.161** (+11%) | 0.175 / 0.181 / **0.173** (-1%) | 0.171 / 0.202 / **0.170** (-0%) | 0.173 / 0.179 / **0.160** (-8%) |
| lip_chin | 0.618 / 0.597 / **0.575** (-7%) | 0.401 / 0.505 / **0.370** (-8%) | 0.440 / 0.468 / **0.415** (-6%) | 0.624 / 0.537 / **0.631** (+1%) |
| cheek_w | 2.118 / 2.279 / **2.160** (+2%) | 2.026 / 2.279 / **2.024** (-0%) | 2.047 / 2.242 / **2.066** (+1%) | 2.309 / 2.372 / **2.363** (+2%) |
| jaw_w | 1.675 / 1.858 / **1.711** (+2%) | 1.574 / 1.785 / **1.591** (+1%) | 1.602 / 1.759 / **1.627** (+2%) | 1.949 / 1.927 / **1.985** (+2%) |

- **Necromancer reference correction.** The earlier "L/W 1.750" target for the necromancer came from a hairline detector that ran up to the top of the photo through the white hair. With the hairline hand-placed at the real temple line (about 1.0 IPD, ~50 mm, above the eyes), the reference is **1.366, oval**. Pass 1 was 1.507 (long); pass 2 is 1.363. The 93 mm hairline in the old ref geometry was wrong for the same reason.
- **Known remaining gaps.**
  - Necromancer upper lip is still ~+29% thick (thin-lip target).
  - Archer upper lip is −23%.
  - Necromancer eye gap is +8%.
  - Foreheads are +3–7% wide.
  - The archer crown has one hair card standing up at the top right.
  - The warrior fringe still reads slightly like bangs, and he looks younger than his reference.

### Changes per class
- **Necromancer.**
  - Face: long hooked nose, hollow cheeks, thin lips, and length cut back from 1.51 to 1.36 L/W to match the corrected reference.
  - Brows: thin, white/grey, arched with a furrow.
  - Hair: slicked back from a low, slightly receding M-shaped temple line (new `th0` start angle), with crown volume.
  - Piercings: the bronze brow crosses were re-placed from the reference (0.77 IPD off the midline, 0.40 IPD above the eye centre).
- **Warrior.**
  - Face: broad jaw (jaw/cheek 0.84), heavy low brow ridge, wide nose; stubble and scar kept.
  - Brows: thick, dark, low and nearly flat.
  - Hair: curly dark-brown hair to the shoulders, with a curled forelock fringe and crown volume.
- **Elementalist.**
  - Face: soft, rounder oval with fuller lips; nose shortened.
  - Brows: auburn with a soft arch.
  - Hair: side part with a higher crown.
- **Archer.**
  - Face: oval with high cheekbones; mouth and nose narrowed; lower face shortened (lip–chin was +26%, now −8%).
  - Brows: dark and fairly straight.
  - Hair: centre part with a layered crown lift.

### Files and integrity
| File (mobile) | Tris | MB |
|---|---|---|
| `player_archer.glb` | 27 036 | 1.06 |
| `player_archer_hair.glb` | 7 586 | 0.82 |
| `player_elementalist.glb` | 27 036 | 0.97 |
| `player_elementalist_hair.glb` | 7 480 | 0.82 |
| `player_necromancer.glb` | 27 036 | 0.96 |
| `player_necromancer_hair.glb` | 3 620 | 0.66 |
| `player_warrior.glb` | 27 036 | 0.97 |
| `player_warrior_hair.glb` | 5 916 | 0.69 |
| `player_necromancer_piercings.glb` | 440 | 0.04 |

- **Bodies.** Vertex count and order, indices, JOINTS/WEIGHTS, UVs, the 52 mixamorig joints, the IBMs and the primitive order skin/linen/eye are all identical to pass 1. Only face POSITION/NORMAL moved: up to 13 mm on the archer, elementalist and warrior and 25 mm on the necromancer. The Damaged Black fits and masks still apply.
- **Budgets.** Hair is within budget (male ≤ 6k, long female ≤ 8k) and piercings are ≤ 500. Textures are ≤ 1024 WebP. Files went through `mobile_compress.sh` without meshopt or Draco; the only extensions are `EXT_texture_webp` and `KHR_materials_specular`. Masters are in `masters/`.
- **Clipping.** Poses checked: idle, run, ss_attack_heavy, bow_draw and magic_cast.
  - Hair inside the body is ≤ 1 vert (0 new versus rest).
  - Hair inside the plate is ≤ 1.
  - Piercings inside the body or plate are 0.
  - Head through the helm is 0.
  - Head outside the helm is the helm's open face, same as at rest.
- **Hide under a helm (unchanged):** hide the `player_<class>_hair` node, plus `player_necromancer_piercings`.
- **Renders.**
  - `renders/heads/heads_sheet.png`: reference, front, 3/4, side and back for each class.
  - `renders/heads/heads_before_after.png`: reference, then pass 1 (a9a2e87) versus pass 2 in front, 3/4 and side.
  - `renders/heads/heads_<class>.png` and `player_<class>_head_*.png`.
  - The bare renders, per-class sheets and lineup were regenerated. The armoured views are unchanged.

## Pass 3: hairline/crown, skin projection, metric touch-ups (2026-11-03)

### What changed
- **Hairline and crown (no cap, no bangs).**
  - The base hair strips now fade out at the root with an irregular, per-strand gradient, so there is no opaque cap edge at the forehead.
  - Crown cards get feathered side edges and a randomised root fade. Thin wisp cards are 1.7× denser at the hairline.
  - Flow cards leave the hairline going **up and back** first, then fall, and the inner layers lie flat at the root, so no card forms a horizontal fringe.
  - Per class:
    - **Necromancer:** slicked straight back, temples visible.
    - **Elementalist:** side part, swept to the side, framing the face.
    - **Warrior:** swept back and to the side with no fringe, and the front drop strips removed.
    - **Archer:** centre part, stray top-right card removed, fuller layered crown.
- **Skin.**
  - Each ref's face colour is projected onto the face UVs (Brian's own Artspace refs), with a tangent-space normal map for wrinkles, the scar and the markings.
  - Iris colour comes from the ref, with a catchlight. Lip colour, eye-socket depth and a sclera falloff toward the canthi were added.
  - The necromancer stays very pale.
  - The warrior's age/weathering was re-tuned, and the projection carries the ref's wrinkles and stubble.
- **Geometry touch-ups** (face POSITION/NORMAL only, ≤ 3 mm on top of pass 2):
  - Upper-lip height: archer +, elementalist +, warrior +, necromancer −.
  - Forehead/temple width narrowed: elementalist −10 %, warrior −8 %, archer −5 %.

### Integrity
- **Bodies.** Same vertex count/order, indices, JOINTS/WEIGHTS, UVs, 52 joints, IBMs and skin/linen/eye primitive order as pass 1/2. The only addition is a normal texture on the skin material. Max face move from the base: archer 13 mm, elementalist 18 mm, warrior 13 mm, necromancer 25 mm.
- **Hair tris** (all skinned to the 52-bone mixamorig rig):

  | Class | Hair tris | Budget |
  |---|---|---|
  | warrior | 5 662 | ≤ 6k |
  | necromancer | 5 768 | ≤ 6k |
  | archer | 7 696 | ≤ 8k |
  | elementalist | 7 660 | ≤ 8k |

  Necromancer piercings are 440 tris.
- **Mobile files.** Textures are ≤ 1024 WebP. Files went through `mobile_compress.sh` without meshopt or Draco; extensions are `EXT_texture_webp` and `KHR_materials_specular` only. Masters are in `masters/`.
- **Clipping.** Poses checked: idle, run, ss_attack_heavy, bow_draw and magic_cast.
  - Hair inside the body is ≤ 1 vert.
  - Hair inside the plate is ≤ 1.
  - Piercings inside the body or plate are 0.
  - Head through the helm is 0.
  - Head outside the helm is the helm's open face, the same as pass 2.

### Renders
- `renders/heads/heads_sheet.png`: ref, front, 3/4, side and back.
- `renders/heads/heads_before_after.png`: pass 2 (b9b05b3) versus pass 3.
- Per-class heads, bare renders, per-class sheets and the lineup were regenerated. Armoured views are unchanged.

### Known gaps
- Elementalist scalp streaks are too vivid red, and there is a slight edge at the temples in 3/4.
- Archer hair is less wild/curly than the ref.
- Warrior hair is shorter than the ref's collar-length curls. The projection leaves a greenish stubble tint and a faint jaw seam.
- The landmark metrics (MediaPipe on renders) now respond more to the projected textures than to the small geometry moves, so see the report table before trusting single ±5 % numbers.

## Pass 4: real curly hair, face fixes, plain-shaded metrics (2026-11-03)

### Hair sources
The procedural card hair is gone for three classes. Each one now uses a MakeHuman community strand-tube hair, fitted to the hm08 body through its `.mhclo` refs. The files are unmodified in `/workspace/free_packs/mh_hair03/`, with a SOURCE.txt.

| Class | Asset | Author | Pack / licence | Tris (budget) |
|---|---|---|---|---|
| archer | `punkduck_alpha7_curly` (node/480) | MakeHuman team; MH 1.1 adaptation by punkduck | MakeHuman Community hair03, **CC-BY** | 7 524 (≤ 8k), one ring in three collapsed |
| elementalist | `punkduck_alpha7_curly2` (node/477) | MakeHuman team; MH 1.1 adaptation by punkduck | hair03, **CC-BY** | 6 026 (≤ 8k) |
| warrior | `punkduck_alpha7_curly2`, cut to collar length | as above | hair03, **CC-BY** | 5 972 (≤ 6k), one inner strand dropped |
| necromancer | pass-3 flow hair (own), with a taller crown | — | — | 5 768 (≤ 6k), piercings 440 |

**Licence note.** The pack is distributed as CC-BY (`hair03_ccby.zip`). The asset JSON says the original licence "was GPL but author was set to unknown", so it is treated as CC-BY by the MakeHuman team. The `.mhclo` headers say "AGPL3", which is the MakeHuman exporter's boilerplate line. **Credit:** "Hair: alpha7 curly / curly2 by the MakeHuman team, adapted by punkduck, MakeHuman Community asset repository, CC-BY."

### Processing (tools in `work/faces/tools/hair4.py`)
- **Fitting and colour.** Each hair is fitted with the `.mhclo` offsets (×0.6 for curly2, which lowers its tall crown) and skinned from the nearest body skin weights to the 52-bone rig. It is recoloured per class: archer blue-black, elementalist deep red, warrior dark brown. A scalp-coloured hair base is painted under each hairline.
- **Warrior:** the length is compressed smoothly to collar length, with the curls pulled in toward the neck.
- **Warrior and elementalist:** strands hanging in front of the face are swept out to the sides and back.

### Face fixes
- **Elementalist:** the red scalp streaks, temple edge and cheek streaks are reduced. The photo weight is blurred and the photo luminance is hue-locked to the skin hue.
- **Archer:**
  - The upper lip is fuller.
  - The dark forehead band is gone, now that the old cap hair has been replaced.
- **Warrior:** the green stubble tint and the jaw seam are removed, using hue-lock 0.75 and a blurred photo mask.
- **Necromancer:** the crown flow layers are 1.8× taller and lifted 3 mm.

### Integrity
- Body vertex count and order, indices, JOINTS/WEIGHTS, UVs, 52 joints, IBMs and the skin/linen/eye primitive order are unchanged.
- Each hair is still a separate skinned GLB.
- **Mobile files:** textures are WebP ≤ 1024, there is no meshopt or Draco, and the extensions are `EXT_texture_webp` and `KHR_materials_specular` only.
- Masters are in `masters/`.

### Clipping (rest + idle, run, ss_attack_heavy, bow_draw, magic_cast; 3 mm threshold)
**Correction.** The pass 2 and pass 3 hair numbers (≤ 1 vert) were wrong. The checker picked a 42-vert helper mesh instead of the hair mesh. That is fixed, and both passes were re-measured.

Maximum verts over all poses:

| Class | Hair verts | Hair in body (pass 3 → 4) | Hair in plate (pass 3 → 4) | Head out of helm (open face) |
|---|---|---|---|---|
| archer | 4 856 | 35 → 5 | 261 → 346 | 245 (= pass 3) |
| elementalist | 4 068 | 44 → 27 | 248 → 462 | 241 (= pass 3) |
| necromancer | 5 751 | 78 → 78 | 263 → 254 | 133 (= pass 3) |
| warrior | 4 028 | 80 → 51 | 43 → 419 | 229 (= pass 3) |

- Piercings: in the body 2 (as at rest), in the plate 27.
- **Hair in body:** all clipping is pose-only, where shoulder/neck motion pushes into the hair ends. Rest is 0–3.
- **Hair in plate:** this is hair resting on the shoulder plates. It is hidden only when the helm is worn (`player_<class>_hair` hidden with the helm, as before). If the plate can be worn without the helm, the long hair needs an armour-on variant or a shoulder-region cut.

### Metrics
Metrics come from MediaPipe on **plain-shaded untextured** renders (`PLAIN=1`: grey skin, flat dark hair alpha, iris kept). See `work/faces/meas/table_v4.md`. Brow metrics read low in plain mode on every pass, because the brows are mostly texture.

### Renders
- `renders/heads/heads_sheet_v4.png` (also `heads_sheet.png`): ref, front, 3/4, side and back.
- `renders/heads/heads_before_after_v4.png` (also `heads_before_after.png`): pass 3 (e1aec46) versus pass 4.
- Bare renders, per-class sheets and the lineup were regenerated.

### Known gaps
- curly2 keeps a slightly peaked, hood-like outline above the crown for the elementalist and warrior.
- The warrior is centre-parted rather than side-swept, and the hair is a little straighter and heavier than the ref's tight curls.
- The elementalist red is darker and browner on the front-lit side than the ref's crimson.
- The necromancer's crown still reads as flat or painted in the side view.
- Archer lip_up is still about −12 %.
