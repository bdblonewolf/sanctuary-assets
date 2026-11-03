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

## Clipping check (Damaged Black, anim_v2 clips, armor verts >3 mm inside *visible* skin)
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
