# README — models/3d_rigs/

Human + creature animation / skeleton assets for Sanctuary.  
Human hero locomotion splits into a **3-file load** (base → gender variant). Clip names never end in `_v2`. Skeleton: **mixamorig**, **30 fps**, **in-place** (hips XZ zeroed).

## File index

| File | What it is | What it's for | What it does | Load order | Gender assignment |
|------|------------|---------------|--------------|------------|-------------------|
| `anim_base_unisex.glb` | Shared combat pack (~70–80% of hero clips) | All heroes + NPCs that fight | Attacks (ss/axe/gs/magic/bow/dagger), heavies, casts, bow draw/release/overdraw, blocks; gender-neutral | **1 — load first** | Unisex (everyone) |
| `anim_variant_male.glb` | Male locomotion / idle / reaction pack | Male bodies | Walks/runs `_2`, armed idles, town/AFK idles, hits, deaths, dodges, draws — heavier/broader gait | **2 — after base** (same name overrides) | **Male:** warrior, necromancer, Wolcen, Quill, Bram, Orrin |
| `anim_variant_female.glb` | Female locomotion / idle / reaction pack | Female bodies | Same clip names as male; `walk_female` / `run_female` + light tweaks (narrower stride, less arm swing, slight hip sway) where no female source | **2 — after base** | **Female:** archer, elementalist, Ilyra, Ysara, Mira, Ness, Ayla, Laya, Bel, Rohesia |
| `m2m_human_anims_mixamo.glb` | Mesh2Motion CC0 master (221 clips) | Source / rebuild | Raw mixamorig retarget master used to bake the 3-file set | — (not loaded in game) | — |
| `ANIM_MAPPING.md` | Clip mapping draft (cab6525) | Authors / rebuild | Game clip ↔ m2m source, old durations, retimes, hand rules | — | — |
| `full_body_check_3file.png` | Graft preview sheet | QA | Sample clips from each of the 3 files grafted onto handrig_b | — | — |
| `README_mesh2motion.md` | Legacy folder readme | History | Pre-rename notes for mesh2motion → 3d_rigs | — | — |
| `creatures/` | Creature clips per species | Creatures | Per-creature rest-pose + actions | Per creature | — |

### Hand poses (baked 3-joint fingers)

| Mode | When | Joints |
|------|------|--------|
| **FLAT** | Walks/runs, most standing/town idles | Archer-style open hand + subtle 3-joint sway |
| **GRIP** | Armed idles, weapon attacks, blocks, bow draw/hold, draws | ~cylinder grip, thumb over index; MCP/PIP/DIP curled |
| **FIST** | Empty-hand fighting (dagger/unarmed attacks, combat hits/dodges) | MCP~90° PIP~100° DIP~70° class curl |

Finger bones: `mixamorig:*Hand{Thumb,Index,Middle,Ring,Pinky}{1,2,3}` (30 tracks), STEP-held for clip duration.

### Loader contract

1. Load `anim_base_unisex.glb` into the AnimationMixer / clip library.  
2. Load `anim_variant_{male|female}.glb` for the character's gender.  
3. **Same clip name in the variant replaces the base entry.**  
4. Keep `hero_locomotion_v5.glb` primary walk/run; the `*_walk_2` / `*_run_2` clips are alternates.

---

## Superseded test files (do not delete)

| File | Commit | Status |
|------|--------|--------|
| `hero_anims_m2m_m.glb` | 91d5236 | **Superseded** small male test pack (22 clips). Replaced by `anim_base_unisex` + `anim_variant_male`. |
| `hero_anims_m2m_f.glb` | 91d5236 | **Superseded** small female test pack (22 clips). Replaced by `anim_base_unisex` + `anim_variant_female`. |
| `hero_anims_m2m_m_b.glb` / `_f_b.glb` | — | **Superseded** planned world-delta retarget test variants (if present). Not used by the 3-file loader. |
| `hands_check.png` / `README_hero_anims_m2m_test.md` | 91d5236 | Historical QA for the small test packs. |

---

## anim_base_unisex.glb — clip list

**asset.extras.description:** Shared unisex combat clips (attacks/blocks/casts/bow); load FIRST then gender variant.

| Clip | Duration (s) | Hands | Notes |
|------|-------------|-------|-------|
| `ss_attack_1` | 1.500 | both_grip | m2m_sword_regular_a + m2m_sword_regular_a_rec |
| `ss_attack_2` | 1.567 | both_grip | m2m_sword_regular_b + m2m_sword_regular_b_rec |
| `ss_attack_3` | 1.367 | both_grip | m2m_sword_regular_c |
| `ss_attack_heavy` | 2.300 | both_grip | m2m_sword_attack |
| `ss_block_idle` | 1.367 | both_grip | m2m_idle_shield |
| `ss_block_hit` | 0.700 | both_grip | m2m_sword_block |
| `axe_attack_1` | 2.400 | both_grip | m2m_melee_hook + m2m_melee_hook_rec |
| `axe_attack_2` | 2.267 | both_grip | m2m_sword_regular_b + m2m_sword_regular_b_rec |
| `axe_attack_3` | 3.167 | both_grip | m2m_one_hand_slash_combo |
| `axe_attack_heavy` | 3.167 | both_grip | m2m_sword_attack |
| `axe_block_idle` | 1.667 | both_grip | m2m_weapon_block |
| `gs_attack_1` | 1.267 | both_grip | m2m_two_handed_horizontal_swing |
| `gs_attack_2` | 1.833 | both_grip | m2m_two_handed_overhead_slam |
| `gs_attack_3` | 1.433 | both_grip | m2m_two_handed_overhead_slam |
| `gs_attack_heavy` | 1.200 | both_grip | m2m_attack_ground_pound |
| `magic_attack_1h` | 2.300 | both_grip | m2m_spell_simple_enter + m2m_spell_simple_shoot + m2m_spell_simple_exit |
| `magic_attack_2h` | 2.667 | both_grip | m2m_staff_combo |
| `magic_cast_1h` | 2.267 | both_grip | m2m_spell_simple_enter + m2m_spell_simple_shoot + m2m_spell_simple_exit |
| `magic_cast_2h` | 2.167 | both_grip | m2m_staff_combo |
| `magic_area` | 2.967 | both_grip | m2m_staff_combo + m2m_two_hand_blast |
| `bow_draw` | 1.000 | lh_grip_rh_flat | m2m_bow_pull |
| `bow_release` | 0.700 | lh_grip_rh_flat | m2m_bow_release |
| `bow_aim_overdraw` | 3.667 | lh_grip_rh_flat | m2m_bow_pull + m2m_bow_pull_hold + m2m_bow_pull_hold |
| `dagger_attack_1` | 1.600 | both_fist | m2m_dagger_stab |
| `dagger_attack_2` | 1.000 | both_fist | m2m_melee_hook + m2m_melee_hook_rec |
| `dagger_attack_3` | 1.367 | both_fist | m2m_dual_wield_cross_slash |
| `dagger_attack_heavy` | 1.600 | both_fist | m2m_dual_wield_combo |
| `unarmed_attack_1` | 0.500 | both_fist | m2m_punch_jab |
| `unarmed_attack_2` | 0.600 | both_fist | m2m_punch_cross |


---

## anim_variant_male.glb — clip list

**asset.extras.description:** Male walks/runs/idles/hits/deaths/dodges; overrides base by name. warrior/necromancer/Wolcen/Quill/Bram/Orrin.

| Clip | Duration (s) | Hands | Notes |
|------|-------------|-------|-------|
| `ss_idle` | 3.600 | rh_grip_lh_flat | m2m_idle_sword |
| `axe_idle` | 1.800 | rh_grip_lh_flat | m2m_one_hand_weapon_idle |
| `gs_idle` | 2.000 | both_grip | m2m_polearm_idle |
| `magic_idle` | 1.800 | rh_grip_lh_flat | m2m_spell_simple_idle |
| `ss_walk_2` | 1.100 | both_flat | m2m_walk |
| `ss_run_2` | 0.700 | both_flat | m2m_sprint |
| `axe_walk_2` | 1.333 | both_flat | m2m_walk |
| `axe_run_2` | 0.733 | both_flat | m2m_sprint |
| `gs_walk_2` | 1.367 | both_flat | m2m_walk |
| `gs_run_2` | 0.733 | both_flat | m2m_sprint |
| `magic_walk_2` | 1.133 | both_flat | m2m_walk |
| `magic_run_2` | 0.733 | both_flat | m2m_sprint |
| `bow_walk_2` | 1.200 | both_flat | m2m_walk |
| `bow_run_2` | 0.867 | both_flat | m2m_sprint |
| `unarmed_walk_2` | 1.367 | both_flat | m2m_walk |
| `unarmed_run_2` | 0.733 | both_flat | m2m_sprint |
| `town_idle` | 5.967 | both_flat | m2m_idle_a |
| `town_look_around` | 6.333 | both_flat | m2m_confused |
| `town_weight_shift` | 6.333 | both_flat | m2m_idle_subtle |
| `town_idle_2` | 5.000 | both_flat | m2m_idle_foldarms |
| `town_idle_3` | 4.083 | both_flat | m2m_idle_listening |
| `town_idle_4` | 3.500 | both_flat | m2m_meditate |
| `town_wave` | 0.533 | both_flat | m2m_greeting |
| `town_talk` | 5.000 | both_flat | m2m_idle_talking |
| `town_argue` | 1.833 | both_flat | m2m_angry |
| `town_bored` | 2.417 | both_flat | m2m_tired_hunched |
| `town_walk_2` | 1.033 | both_flat | m2m_walk_relaxed |
| `ss_hit` | 0.700 | both_fist | m2m_hit_chest |
| `axe_hit` | 0.917 | both_fist | m2m_hit_chest |
| `gs_hit` | 0.867 | both_grip | m2m_hit_knockback |
| `magic_hit` | 0.917 | both_fist | m2m_hit_chest |
| `bow_hit` | 0.917 | both_fist | m2m_hit_chest |
| `ss_death` | 2.300 | both_flat | m2m_death_a |
| `death_dying` | 4.400 | both_flat | m2m_death_c |
| `death_backwards` | 4.600 | both_flat | m2m_death_b |
| `death_forward` | 3.667 | both_flat | m2m_death_d |
| `gs_death` | 2.400 | both_flat | m2m_death_spin_rm |
| `ss_draw` | 0.600 | both_grip | m2m_weapon_draw |
| `axe_draw` | 1.667 | both_grip | m2m_weapon_draw |
| `ss_dodge_back` | 1.633 | both_fist | m2m_dodge_back |
| `ss_dodge_left` | 1.000 | both_fist | m2m_dodge_left |
| `ss_dodge_right` | 1.000 | both_fist | m2m_dodge_right |
| `axe_dodge_back` | 1.633 | both_fist | m2m_dodge_back |
| `axe_dodge_left` | 1.000 | both_fist | m2m_dodge_left |
| `axe_dodge_right` | 1.000 | both_fist | m2m_dodge_right |
| `gs_dodge_back` | 1.633 | both_fist | m2m_dodge_back |
| `gs_dodge_left` | 1.000 | both_fist | m2m_dodge_left |
| `gs_dodge_right` | 1.000 | both_fist | m2m_dodge_right |
| `magic_dodge_back` | 1.633 | both_fist | m2m_dodge_back |
| `magic_dodge_left` | 1.000 | both_fist | m2m_dodge_left |
| `magic_dodge_right` | 1.000 | both_fist | m2m_dodge_right |
| `bow_dodge_back` | 1.633 | both_fist | m2m_dodge_back |
| `bow_dodge_left` | 1.000 | both_fist | m2m_dodge_left |
| `bow_dodge_right` | 1.000 | both_fist | m2m_dodge_right |
| `unarmed_dodge_back` | 1.633 | both_fist | m2m_dodge_back |
| `unarmed_dodge_left` | 1.000 | both_fist | m2m_dodge_left |
| `unarmed_dodge_right` | 1.000 | both_fist | m2m_dodge_right |


---

## anim_variant_female.glb — clip list

**asset.extras.description:** Female walks/runs/idles/hits/deaths/dodges; walk_female/run_female + light tweaks. archer/elementalist/Ilyra/Ysara/Mira/Ness/Ayla/Laya/Bel/Rohesia.

### Female light tweaks applied (no dedicated female source)

- `ss_idle`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `axe_idle`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `gs_idle`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `magic_idle`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `town_weight_shift`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `town_idle_2`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `town_idle_3`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `town_idle_4`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `town_wave`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `town_talk`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `gs_hit`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `ss_draw`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `axe_draw`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `ss_dodge_back`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `ss_dodge_left`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `ss_dodge_right`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `axe_dodge_back`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `axe_dodge_left`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `axe_dodge_right`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `gs_dodge_back`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `gs_dodge_left`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `gs_dodge_right`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `magic_dodge_back`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `magic_dodge_left`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `magic_dodge_right`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `bow_dodge_back`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `bow_dodge_left`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `bow_dodge_right`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `unarmed_dodge_back`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `unarmed_dodge_left`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway
- `unarmed_dodge_right`: narrower stride (~0.82× hip X / 0.88× Z before in-place), −18% arm swing toward rest, slight hip sway

| Clip | Duration (s) | Hands | Notes |
|------|-------------|-------|-------|
| `ss_idle` | 3.600 | rh_grip_lh_flat | **light tweak** · m2m_idle_sword |
| `axe_idle` | 1.800 | rh_grip_lh_flat | **light tweak** · m2m_one_hand_weapon_idle |
| `gs_idle` | 2.000 | both_grip | **light tweak** · m2m_polearm_idle |
| `magic_idle` | 1.800 | rh_grip_lh_flat | **light tweak** · m2m_spell_simple_idle |
| `ss_walk_2` | 1.100 | both_flat | m2m_walk_female |
| `ss_run_2` | 0.700 | both_flat | m2m_run_female |
| `axe_walk_2` | 1.333 | both_flat | m2m_walk_female |
| `axe_run_2` | 0.733 | both_flat | m2m_run_female |
| `gs_walk_2` | 1.367 | both_flat | m2m_walk_female |
| `gs_run_2` | 0.733 | both_flat | m2m_run_female |
| `magic_walk_2` | 1.133 | both_flat | m2m_walk_female |
| `magic_run_2` | 0.733 | both_flat | m2m_run_female |
| `bow_walk_2` | 1.200 | both_flat | m2m_walk_female |
| `bow_run_2` | 0.867 | both_flat | m2m_run_female |
| `unarmed_walk_2` | 1.367 | both_flat | m2m_walk_female |
| `unarmed_run_2` | 0.733 | both_flat | m2m_run_female |
| `town_idle` | 5.967 | both_flat | m2m_idle_subtle |
| `town_look_around` | 4.083 | both_flat | m2m_idle_listening |
| `town_weight_shift` | 6.333 | both_flat | **light tweak** · m2m_idle_subtle |
| `town_idle_2` | 5.000 | both_flat | **light tweak** · m2m_idle_foldarms |
| `town_idle_3` | 4.083 | both_flat | **light tweak** · m2m_idle_listening |
| `town_idle_4` | 3.500 | both_flat | **light tweak** · m2m_meditate |
| `town_wave` | 0.533 | both_flat | **light tweak** · m2m_greeting |
| `town_talk` | 5.000 | both_flat | **light tweak** · m2m_idle_talking |
| `town_argue` | 9.250 | both_flat | m2m_reject |
| `town_bored` | 6.167 | both_flat | m2m_idle_rail |
| `town_walk_2` | 1.033 | both_flat | m2m_walk_female |
| `ss_hit` | 0.700 | both_fist | m2m_hit_head |
| `axe_hit` | 1.250 | both_fist | m2m_hit_head |
| `gs_hit` | 0.867 | both_grip | **light tweak** · m2m_hit_knockback |
| `magic_hit` | 1.167 | both_fist | m2m_hit_head |
| `bow_hit` | 1.250 | both_fist | m2m_hit_head |
| `ss_death` | 2.300 | both_flat | m2m_death_b |
| `death_dying` | 4.400 | both_flat | m2m_death_d |
| `death_backwards` | 4.600 | both_flat | m2m_death_c |
| `death_forward` | 3.667 | both_flat | m2m_death_a |
| `ss_draw` | 0.600 | both_grip | **light tweak** · m2m_weapon_draw |
| `axe_draw` | 1.667 | both_grip | **light tweak** · m2m_weapon_draw |
| `ss_dodge_back` | 1.633 | both_fist | **light tweak** · m2m_dodge_back |
| `ss_dodge_left` | 1.000 | both_fist | **light tweak** · m2m_dodge_left |
| `ss_dodge_right` | 1.000 | both_fist | **light tweak** · m2m_dodge_right |
| `axe_dodge_back` | 1.633 | both_fist | **light tweak** · m2m_dodge_back |
| `axe_dodge_left` | 1.000 | both_fist | **light tweak** · m2m_dodge_left |
| `axe_dodge_right` | 1.000 | both_fist | **light tweak** · m2m_dodge_right |
| `gs_dodge_back` | 1.633 | both_fist | **light tweak** · m2m_dodge_back |
| `gs_dodge_left` | 1.000 | both_fist | **light tweak** · m2m_dodge_left |
| `gs_dodge_right` | 1.000 | both_fist | **light tweak** · m2m_dodge_right |
| `magic_dodge_back` | 1.633 | both_fist | **light tweak** · m2m_dodge_back |
| `magic_dodge_left` | 1.000 | both_fist | **light tweak** · m2m_dodge_left |
| `magic_dodge_right` | 1.000 | both_fist | **light tweak** · m2m_dodge_right |
| `bow_dodge_back` | 1.633 | both_fist | **light tweak** · m2m_dodge_back |
| `bow_dodge_left` | 1.000 | both_fist | **light tweak** · m2m_dodge_left |
| `bow_dodge_right` | 1.000 | both_fist | **light tweak** · m2m_dodge_right |
| `unarmed_dodge_back` | 1.633 | both_fist | **light tweak** · m2m_dodge_back |
| `unarmed_dodge_left` | 1.000 | both_fist | **light tweak** · m2m_dodge_left |
| `unarmed_dodge_right` | 1.000 | both_fist | **light tweak** · m2m_dodge_right |


---

## Build notes

- Source: `m2m_human_anims_mixamo.glb` per `ANIM_MAPPING.md` (cab6525) with chain/trim/retime to old knight durations (factor soft-clamped to [0.4, 2.5]).
- Skeleton host: warrior handrig_b mixamorig (52 bones incl. full 3-joint fingers); meshes stripped.
- Hips translation X/Z zeroed (in-place).
- KEEP OLD / GAP clips from the mapping are **not** in these packs (remain on `hero_locomotion_v5` / older knight packs).
- Preview graft onto character meshes can show IBM/bind tears when character rest ≠ m2m/v5 rest; live absolute mixer expects matching rest or a follow-up world-delta pass.
