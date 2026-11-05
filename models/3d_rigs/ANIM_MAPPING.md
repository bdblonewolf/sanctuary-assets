# ANIM_MAPPING — Mesh2Motion → Sanctuary game clips (draft v2)

Source master: `masters/m2m_human_anims_mixamo.glb` (221 CC0 clips, mixamorig, 30 fps, in-place).  
Old durations from `knight_anim_v10b_c.glb`. Draft only — no GLB build yet.

## Loader / file split (required)

| File | Gender | Contents |
|------|--------|----------|
| `hero_anims_m2m_m.glb` | male | all hero clips below |
| `hero_anims_m2m_f.glb` | female | same clip names; non-attack clips use female sources / tweaks |
| `npc_anims_m2m_m.glb` | male NPCs | NPC set |
| `npc_anims_m2m_f.glb` | female NPCs | same NPC clip names |

Loader picks the file by character gender; clip names stay identical.  
**Attacks are shared.** **Non-attacks** differ by gender column.

### Character gender roster
- **Female heroes:** archer, elementalist  
- **Male heroes:** warrior, necromancer  
- **Female NPCs:** Ilyra, Ysara, Mira, Ness, Ayla, Laya, Bel, Rohesia  
- **Male NPCs:** Wolcen, Quill, Bram, Orrin  

### Hand pose rule (Brian / engineer)
- **Town / NPC idles only:** both hands **FLAT**
- **Armed idles** (`ss_idle`, `axe_idle`, `gs_idle`, `magic_idle`, `bow_idle`): **weapon hand = FIST**, free hand = **FLAT**
  - 1H sword/axe/wand: RH-FIST / LH-FLAT
  - Bow: **LH-FIST / RH-FLAT** (bow ends in left hand)
  - 2H (gs/spear/maul/staff): **LEFT-ON-GRIP** (both on grip; no off-hand IK)
- **Moving / attacking / carrying / blocking:** FIST (or LEFT-ON-GRIP for 2H)

### Retime rule
Target play length = **old ±25%**. Prefer chain/trim so retime factor stays near 1.0 when raw length is far off.  
`retime = old / new_raw` (after chain/trim). Applied at build.

### Locomotion
Keep **hero_locomotion_v5** walk/run as primary; m2m as `_2` variants.

### `_rm` clips
Root-motion X/Z travel is stripped in-game → use **in-place** twins when they exist, else mark **plays on the spot**.

### Explicit gendered m2m
Only `m2m_walk_female` (1.333s), `m2m_run_female` (0.833s). Other female non-attacks: soft pick or **needs female tweak**.

### Back-stow draw rule
`m2m_weapon_draw` is a **1H hip draw**. Weapons that stow on **Spine2 (back)** — greataxe/greatsword, spear, maul, bow — must **KEEP OLD** unless an over-shoulder draw exists (none in m2m). Sword/axe hip draw OK.

### 2H grip verify
Mark **verify both hands on grip at build** on: `m2m_attack_ground_pound`, `m2m_sword_attack_air_vertical`, `m2m_power_up`.

---

## Legend

| Column | Meaning |
|--------|---------|
| Game clip | Exact case-sensitive name |
| Male m2m | Male / shared source (KEEP OLD / keep v5) |
| Female m2m | Female non-attack source; attacks = shared |
| Old (s) | Duration in knight_anim_v10b_c |
| New (s) | Source/chain raw duration before retime |
| Retime | old/new (1.0 = no stretch); target play ≈ old |
| Hands | pose rule |
| Notes | mapping / build notes |

---

## Sword / shield (ss)

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| ss_idle | m2m_idle_sword | needs female tweak (same) | 3.600 | 2.033 | 1.77 | RH-FIST / LH-FLAT | Armed idle; factor high — loop/hold mid or soft stretch |
| ss_walk | KEEP OLD (v5) | KEEP OLD (v5); `_2`←walk_female | 1.100 | — | — | FIST | keep v5 |
| ss_run | KEEP OLD (v5) | KEEP OLD (v5); `_2`←run_female | 0.700 | — | — | FIST | keep v5 |
| ss_attack_1 | m2m_sword_regular_a **+** m2m_sword_regular_a_rec | *(shared)* | 1.500 | 1.333 | 1.13 | FIST | a alone 0.40 too short; chain a+rec |
| ss_attack_2 | m2m_sword_regular_b **+** m2m_sword_regular_b_rec | *(shared)* | 1.567 | 1.500 | 1.04 | FIST | |
| ss_attack_3 | m2m_sword_regular_c | *(shared)* | 1.367 | 1.667 | 0.82 | FIST | in-place c (not c_rm) |
| ss_attack_heavy | m2m_sword_attack | *(shared)* | 2.300 | 1.867 | 1.23 | FIST | within ±25% |
| ss_hit | m2m_hit_chest | m2m_hit_head / needs female tweak | 0.700 | 0.367 | 1.91 | FIST | short source — soft stretch or pad |
| ss_draw | m2m_weapon_draw | needs female tweak | 0.500 | 1.500 | 0.33 | FIST | hip draw OK for 1H sword; trim/speed-up to ~0.5 |
| ss_sheath | KEEP OLD | KEEP OLD / needs female tweak | 1.267 | — | — | FIST | **GAP** |
| ss_block_idle | m2m_idle_shield | needs female tweak | 1.367 | 2.467 | 0.55 | FIST | trim/loop to ~1.37 |
| ss_block_hit | m2m_sword_block | needs female tweak | 0.700 | 1.200 | 0.58 | FIST | trim; alt shield_oneshot 0.800 |

---

## Axe 1H (axe)

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| axe_idle | m2m_one_hand_weapon_idle | needs female tweak | 1.800 | 2.633 | 0.68 | RH-FIST / LH-FLAT | Armed idle |
| axe_walk | KEEP OLD (v5) | KEEP OLD; `_2`←walk_female | 1.333 | — | — | FIST | |
| axe_run | KEEP OLD (v5) | KEEP OLD; `_2`←run_female | 0.733 | — | — | FIST | |
| axe_attack_1 | m2m_melee_hook **+** m2m_melee_hook_rec | *(shared)* | 2.400 | 1.067 | 2.25 | FIST | chain short; may need pad/hold to approach ±25% |
| axe_attack_2 | m2m_sword_regular_b **+** b_rec | *(shared)* | 2.267 | 1.500 | 1.51 | FIST | stretch; alt slash_combo piece |
| axe_attack_3 | m2m_one_hand_slash_combo | *(shared)* | 3.167 | 1.800 | 1.76 | FIST | soft stretch / pad |
| axe_attack_heavy | m2m_sword_attack | *(shared)* | 3.167 | 1.867 | 1.70 | FIST | soft stretch |
| axe_hit | m2m_hit_chest | m2m_hit_head / needs female tweak | 1.467 | 0.367 | 4.00 | FIST | **weak** — prefer KEEP OLD if stretch ugly |
| axe_draw | m2m_weapon_draw | needs female tweak | 1.667 | 1.500 | 1.11 | FIST | hip draw OK if axe is hip-stowed |
| axe_sheath | KEEP OLD | KEEP OLD | 1.633 | — | — | FIST | **GAP** |
| axe_block_idle | m2m_weapon_block | needs female tweak | 1.667 | 1.500 | 1.11 | FIST | |

---

## Greataxe / greatsword 2H (gs)

Must use 2H clips only. **No staff_spin** (staff-only). Left hand on grip.

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| gs_idle | m2m_polearm_idle | needs female tweak | 2.000 | 2.633 | 0.76 | LEFT-ON-GRIP | Armed 2H idle |
| gs_run | KEEP OLD (v5); `_2`←polearm_run | KEEP OLD; `_2`←run_female+grip | 0.733 | 0.800 | — | LEFT-ON-GRIP | keep v5 primary |
| gs_attack_1 | m2m_two_handed_horizontal_swing | *(shared)* | 1.267 | 1.633 | 0.78 | LEFT-ON-GRIP | |
| gs_attack_2 | m2m_two_handed_overhead_slam | *(shared)* | 1.833 | 1.800 | 1.02 | LEFT-ON-GRIP | |
| gs_attack_3 | m2m_two_handed_overhead_slam *(retimed)* | *(shared)* | 1.433 | 1.800 | 0.80 | LEFT-ON-GRIP | ~1.4s target; **not** air_vertical. air_vertical → trimmed variant only (`gs_attack_3_2`) |
| gs_attack_heavy | m2m_attack_ground_pound **trimmed ~1.2s** | *(shared)* | 1.200 | ~1.200 | ~1.0 after trim | LEFT-ON-GRIP | raw 2.700 too long; trim to impact window. **verify both hands on grip at build** |
| gs_hit | m2m_hit_knockback *(in-place)* | needs female tweak | 0.867 | 0.800 | 1.08 | LEFT-ON-GRIP | not hit_knockback_rm |
| gs_draw | KEEP OLD | KEEP OLD / needs female tweak | 0.467 | — | — | LEFT-ON-GRIP | back-stow Spine2; weapon_draw is hip — **KEEP OLD** |
| gs_spin | KEEP OLD | KEEP OLD | 1.867 | — | — | LEFT-ON-GRIP | **GAP** — staff_spin dropped (staff only); no 2H spin |
| gs_death | m2m_death_spin_rm **plays on the spot** | same unique / see Deaths | 2.400 | 4.933 | 0.49 trim | FLAT | unique male slot; trim or speed |

---

## Staff / wand (magic)

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| magic_idle | m2m_spell_simple_idle | **m2m_spell_simple_idle** (needs female tweak) | 1.800 | 2.633 | 0.68 | RH-FIST / LH-FLAT (wand) or LEFT-ON-GRIP (staff) | **Not** levitate_idle |
| magic_walk | KEEP OLD (v5) | KEEP OLD; `_2`←walk_female | 1.133 | — | — | FIST | |
| magic_run | KEEP OLD (v5) | KEEP OLD; `_2`←run_female | 0.733 | — | — | FIST | |
| magic_attack_1h | enter **+** shoot **+** exit | *(shared)* | 2.300 | 1.733 | 1.33 | FIST | spell_simple_enter+shoot+exit; soft stretch |
| magic_attack_2h | m2m_staff_combo | *(shared)* | 2.667 | 2.333 | 1.14 | LEFT-ON-GRIP | |
| magic_cast_1h | enter **+** shoot **+** exit | *(shared)* | 2.267 | 1.733 | 1.31 | FIST | same chain as attack_1h; distinguish via VFX/timing |
| magic_cast_2h | m2m_staff_combo *(windup lean)* / power_up **+** staff | *(shared)* | 2.167 | 2.333 | 0.93 | LEFT-ON-GRIP | prefer staff_combo; if power_up used: **verify both hands on grip at build** |
| magic_area | m2m_staff_combo **+** m2m_two_hand_blast | *(shared)* | 2.967 | 2.733 | 1.09 | LEFT-ON-GRIP | chain; alt consume_powerup 4.133 @ 0.72 |
| magic_hit | m2m_hit_chest | m2m_hit_head / needs female tweak | 1.167 | 0.367 | 3.18 | FIST | weak fit — consider KEEP OLD |
| magic_block_idle | m2m_defend | needs female tweak | 2.767 | 0.933 | 2.97 | FIST | weak — KEEP OLD if stretch bad |

---

## Bow

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| bow_idle | KEEP OLD | KEEP OLD / needs female tweak | 3.967 | — | — | LH-FIST / RH-FLAT | KEEP OLD unless calm hold cut from m2m_bow (full cycle 3.667s) — if cut, note frames at build (candidate: mid hold ~1.5–3.0s of m2m_bow @30fps ≈ f45–f90) |
| bow_walk | KEEP OLD (v5) | KEEP OLD; `_2`←walk_female | 1.200 | — | — | FIST | |
| bow_run | KEEP OLD (v5) | KEEP OLD; `_2`←run_female | 0.867 | — | — | FIST | |
| bow_draw | m2m_bow_pull | *(shared)* | 1.000 | 1.267 | 0.79 | LH-FIST | shared attack-family |
| bow_release | m2m_bow_release | *(shared)* | 0.700 | 0.467 | 1.50 | LH-FIST | soft stretch |
| bow_aim_overdraw | m2m_bow_pull **+** extended m2m_bow_pull_hold loop | *(shared)* | 3.667 | ~3.5–3.7 | ~1.0 | LH-FIST | pull 1.267 + hold loop ~2.4s → ~3.67 held draw |
| bow_hit | m2m_hit_chest | m2m_hit_head / needs female tweak | 1.267 | 0.367 | 3.45 | FIST | weak — consider KEEP OLD |
| bow_equip | KEEP OLD | KEEP OLD / needs female tweak | 0.900 | — | — | LH-FIST | back-stow; bow ends LEFT hand — **KEEP OLD** |
| bow_sheath | KEEP OLD | KEEP OLD | 1.100 | — | — | FIST | **GAP** |
| bow_dodge_back | m2m_dodge_back *(in-place)* | needs female tweak | 1.633 | 1.000 | 1.63 | FIST | not dodge_back_rm; soft stretch |

---

## Dagger

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| dagger_attack_1 | m2m_dagger_stab | *(shared)* | 1.600 | 1.400 | 1.14 | FIST | |
| dagger_attack_2 | m2m_melee_hook **+** rec | *(shared)* | 1.000 | 1.067 | 0.94 | FIST | |
| dagger_attack_3 | m2m_dual_wield_cross_slash | *(shared)* | 1.367 | 1.633 | 0.84 | FIST | |
| dagger_attack_heavy | m2m_dual_wield_combo | *(shared)* | 1.600 | 2.200 | 0.73 | FIST | |

---

## Peace / town

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| town_idle | m2m_idle_a | m2m_idle_subtle | 5.967 | 3.067 / 2.533 | ~1.95 / 2.36 | **FLAT** | both hands flat; loop |
| unarmed_walk | KEEP OLD (v5) | KEEP OLD; `_2`←walk_female | 1.367 | — | — | FIST | |
| unarmed_run | KEEP OLD (v5) | KEEP OLD; `_2`←run_female | 0.800 | — | — | FIST | |
| town_look_around | m2m_confused | m2m_idle_listening | 6.333 | 2.833 / 1.633 | ~2.2 / 3.9 | FLAT | loop/pad |
| town_weight_shift | m2m_idle_subtle | needs female tweak | 6.633 | 2.533 | 2.62 | FLAT | loop |
| town_wave | m2m_greeting | needs female tweak | 0.533 | 4.733 | 0.11 | FLAT→FIST | trim greeting to wave beat ~0.5s |
| town_talk | m2m_idle_talking | needs female tweak | 5.000 | 3.633 | 1.38 | FLAT | loop |
| town_argue | m2m_angry | m2m_reject / needs female tweak | 9.967 | 0.733 / 3.700 | loop | FIST | loop angry/reject |
| town_bored | m2m_tired_hunched | m2m_idle_rail | 7.967 | 0.967 / 2.467 | loop | FLAT | |
| town_walk | KEEP OLD (v5); `_2`←walk_relaxed | m2m_walk_female | 1.033 | 1.367 / 1.333 | — | FIST | |

---

## Deaths

Only 5 m2m death clips. **Each gender’s random death list must use unique sources** (no repeats). Extra slots → KEEP OLD.

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| ss_death | m2m_death_a | m2m_death_b | 2.300 | 4.500 / 1.867 | 0.51 / 1.23 | FLAT | unique per gender |
| death_dying | m2m_death_c | m2m_death_d | 4.400 | 2.200 / 2.167 | 2.00 / 2.03 | FLAT | unique |
| death_backwards | m2m_death_b | m2m_death_c | 4.600 | 1.867 / 2.200 | 2.46 / 2.09 | FLAT | unique; verify facing |
| death_fall_back | KEEP OLD | KEEP OLD | 2.600 | — | — | FLAT | no free unique death left |
| death_forward | m2m_death_d | m2m_death_a | 3.667 | 2.167 / 4.500 | 1.69 / 0.81 | FLAT | unique |
| death_left | KEEP OLD | KEEP OLD | 3.433 | — | — | FLAT | **GAP** directional |
| death_right | KEEP OLD | KEEP OLD | 3.500 | — | — | FLAT | **GAP** |
| death_react_back | m2m_hit_knockback *(in-place)* | m2m_hit_head | 3.633 | 0.800 / 0.500 | soft | FIST | not `_rm`; unique non-death sources |
| gs_death | m2m_death_spin_rm **plays on the spot** | m2m_death_spin_rm **plays on the spot** | 2.400 | 4.933 | trim~0.49 | FLAT | only spin left; same clip OK across weapon sets if not in same random pool — if gs shares hero death pool, KEEP OLD female and assign spin only to male (or vice versa). **Prefer:** male=spin on spot, female=KEEP OLD for uniqueness inside shared pool |

**Male unique death set:** death_a, death_c, death_b, death_d, death_spin_rm (on spot).  
**Female unique death set:** death_b, death_d, death_c, death_a; gs_death/fall/left/right KEEP OLD.

---

## NPC (`npc_anims_m2m_*.glb`)

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| idle | m2m_idle_a | m2m_idle_subtle | — | 3.067 / 2.533 | — | **FLAT** | |
| walk | m2m_walk | m2m_walk_female | — | 1.633 / 1.333 | — | FIST | real gendered pair |
| talk | m2m_idle_talking | needs female tweak | — | 3.633 | — | FLAT | |
| sit | m2m_sitting_idle | m2m_sit_ground_idle / tweak | — | 2.033 / 2.967 | — | FLAT | |
| sit_talk | m2m_sitting_talking | needs female tweak | — | 3.633 | — | FLAT | |
| sleep | m2m_sleeping | needs female tweak | — | 1.600 | — | FLAT | |
| work_hammer | m2m_hammering | needs female tweak | — | 0.967 | — | FIST | |
| work_write | KEEP OLD | KEEP OLD | — | — | — | FIST | **GAP** |

---

## Proposed future: spear_*

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| spear_idle | m2m_polearm_idle | needs female tweak | — | 2.633 | — | LEFT-ON-GRIP | |
| spear_walk | KEEP OLD (v5) | KEEP OLD; `_2`←walk_female | — | — | — | LEFT-ON-GRIP | |
| spear_run | m2m_polearm_run | needs female tweak | — | 0.800 | — | LEFT-ON-GRIP | |
| spear_attack_1 | m2m_spear_thrust | *(shared)* | — | 1.333 | — | LEFT-ON-GRIP | |
| spear_attack_2 | m2m_spear_thrust retimed variant | *(shared)* | — | 1.333 | — | LEFT-ON-GRIP | only one thrust |
| spear_attack_3 | m2m_staff_combo | *(shared)* | — | 2.333 | — | LEFT-ON-GRIP | pole flourish |
| spear_attack_heavy | m2m_spear_throw | *(shared)* | — | 1.667 | — | LEFT-ON-GRIP | |
| spear_hit | m2m_hit_chest | m2m_hit_head | — | 0.367 | — | LEFT-ON-GRIP | |
| spear_draw | KEEP OLD | KEEP OLD | — | — | — | LEFT-ON-GRIP | back-stow Spine2 |
| spear_sheath | KEEP OLD | KEEP OLD | — | — | — | LEFT-ON-GRIP | **GAP** |

---

## Proposed future: maul_*

| Game clip | Male m2m | Female m2m | Old | New | Retime | Hands | Notes |
|-----------|----------|------------|-----|-----|--------|-------|-------|
| maul_idle | m2m_polearm_idle | needs female tweak | — | 2.633 | — | LEFT-ON-GRIP | |
| maul_walk | KEEP OLD (v5) | KEEP OLD; `_2`←walk_female | — | — | — | LEFT-ON-GRIP | |
| maul_run | KEEP OLD (v5) | run_female+grip | — | — | — | LEFT-ON-GRIP | |
| maul_attack_1 | m2m_two_handed_horizontal_swing | *(shared)* | — | 1.633 | — | LEFT-ON-GRIP | |
| maul_attack_2 | m2m_two_handed_overhead_slam | *(shared)* | — | 1.800 | — | LEFT-ON-GRIP | |
| maul_attack_3 | m2m_attack_ground_pound **trimmed** | *(shared)* | — | trim | — | LEFT-ON-GRIP | **verify both hands on grip at build** |
| maul_attack_heavy | m2m_sword_attack_air_vertical **trimmed** | *(shared)* | — | trim | — | LEFT-ON-GRIP | **verify both hands on grip at build** |
| maul_hit | m2m_hit_knockback | needs female tweak | — | 0.800 | — | LEFT-ON-GRIP | in-place |
| maul_draw | KEEP OLD | KEEP OLD | — | — | — | LEFT-ON-GRIP | back-stow |
| maul_sheath | KEEP OLD | KEEP OLD | — | — | — | LEFT-ON-GRIP | **GAP** |

---

## Dodges (`<set>_dodge_*`)

| Pattern | Male m2m | Female m2m | Hands | Notes |
|---------|----------|------------|-------|-------|
| `*_dodge_back` | m2m_dodge_back | needs female tweak | FIST | in-place; not `_rm` |
| `*_dodge_fwd` | KEEP OLD / m2m_roll **plays on the spot** | same | FIST | **soft GAP** |
| `*_dodge_left` | m2m_dodge_left | needs female tweak | FIST | |
| `*_dodge_right` | m2m_dodge_right | needs female tweak | FIST | |

---

## GENDER

| Clip | Dur | Assign |
|------|-----|--------|
| m2m_walk_female | 1.333 | Female walk / town_walk / NPC walk |
| m2m_run_female | 0.833 | Female run `_2` / NPC run |

No `*_male` clips. Soft picks: male←walk_large/formal/sprint/idle_a/foldarms; female←walk_female/relaxed/happy/idle_subtle/listening.  
File split `*_m.glb` / `*_f.glb` with identical names. Female non-attacks mostly **needs female tweak**.

---

## VARIANTS (`<existing>_<n>`, never `*_v2`)

| Variant | m2m | New | Hands | Notes |
|---------|-----|-----|-------|-------|
| ss_walk_2 / ss_run_2 | walk / sprint · walk_female / run_female | 1.633 / 0.800 | FIST | vs v5 |
| ss_attack_1_2 | sword_regular_a alone | 0.400 | FIST | short poke variant |
| ss_attack_heavy_2 | one_hand_slash_combo | 1.800 | FIST | |
| ss_attack_heavy_3 | sword_dash_rm **plays on the spot** | 1.533 | FIST | no XZ travel |
| gs_attack_3_2 | air_vertical **trimmed ~1.4s** | trim | LEFT-ON-GRIP | **verify both hands on grip**; not primary |
| gs_attack_heavy_2 | two_hand_blast | 0.400 | LEFT-ON-GRIP | short |
| ss_hit_2 | hit_head | 0.500 | FIST | |
| ss_hit_3 | dizzy | 2.367 | FIST | |
| ss_death_2.. | *(do not duplicate active death pool)* | — | FLAT | only unused deaths |
| town_idle_2 | idle_foldarms | 2.467 | FLAT | |
| town_idle_3 | idle_listening | 1.633 | FLAT | |
| idle_2 (NPC) | idle_subtle | 2.533 | FLAT | |
| bow_dodge_back_2 | dodge_back (already primary) | — | FIST | skip `_rm` |
| magic_area_2 | consume_powerup | 4.133 | FIST | retime 0.72 vs old 2.97 |
| dagger_attack_heavy_2 | knife_throw | 1.167 | FIST | |

**Removed vs draft v1:** `gs_spin`←staff_spin, `gs_attack_1_2`←staff_spin (staff only).

---

## GAPS (remaining)

| Clip | Why |
|------|-----|
| ss_sheath, axe_sheath, bow_sheath, spear_sheath, maul_sheath | no sheath clips |
| gs_draw, spear_draw, maul_draw, bow_equip | back-stow; no over-shoulder draw |
| gs_spin | no 2H spin (staff_spin rejected) |
| death_left, death_right, death_fall_back | no free unique directional deaths |
| gs_death (female if shared pool) | uniqueness vs male spin |
| work_write | no writing clip |
| `*_dodge_fwd` | no true forward dodge |
| axe_hit, magic_hit, bow_hit, magic_block_idle | source far from old duration — may KEEP OLD |
| Most female non-attacks | only walk/run_female truly gendered |
| bow_idle | KEEP OLD pending optional m2m_bow hold cut |

---

## Build notes (later)

1. Gender file split; identical clip names.  
2. Armed idles: weapon-hand FIST + free FLAT; town/NPC idle both FLAT.  
3. Retime/chain/trim per table to land within old ±25%.  
4. Strip/ignore `_rm` XZ — use in-place or mark plays-on-spot.  
5. Verify grip on ground_pound, air_vertical, power_up.  
6. Keep hero_locomotion_v5 walk/run primary.
