# Mesh2Motion animations (CC0)

**Repo path:** `models/3d_rigs/` (renamed from `models/mesh2motion`; nothing live loads this folder yet).

Source: https://github.com/mesh2motion/mesh2motion-app (static/assets), https://github.com/Mesh2Motion/mesh2motion-assets — CC0 1.0. Some human animations from Quaternius, CC0.

## m2m_human_anims_mixamo.glb
221 human clips retargeted onto the mixamorig skeleton (from hero_locomotion_v5), skeleton only, 30 fps, in-place (hips keep vertical bob only; `_rm` clips had root motion, now in-place). Mobile-compressed (no meshopt/Draco). Clips are rotation-only + Hips translation. Load clips by name onto any mixamorig character (tested on player_warrior and npc_mira_body_hair).

Bone mapping (m2m -> mixamorig:): pelvis->Hips, spine_01/02/03->Spine/Spine1/Spine2, neck_01->Neck, head->Head, clavicle_*->*Shoulder, upperarm->Arm, lowerarm->ForeArm, hand->Hand, thigh->UpLeg, calf->Leg, foot->Foot, ball->ToeBase, index/middle/ring/pinky/thumb_0N -> *Hand{Index,Middle,Ring,Pinky,Thumb}N. Method: world-space rest-corrected rotation transfer (source rest-pose.glb, bone directions aligned per chain).

## Known issues
- Finger nodes in the hero rig are not skin joints there; finger tracks only exist where the target skeleton has them (rough).
- Warrior hands/fingers splay slightly in some poses; no foot IK, so some foot sliding/height mismatch on non-standard proportions.
- Rough single pass: only walk, sword_regular_a, two_handed_overhead_slam, sword_block were visually checked.

## Clips

## Deaths (5)
- m2m_death_a
- m2m_death_b
- m2m_death_c
- m2m_death_d
- m2m_death_spin_rm

## Hit reacts (7)
- m2m_dizzy
- m2m_hit_chest
- m2m_hit_head
- m2m_hit_knockback
- m2m_hit_knockback_rm
- m2m_idle_hurt
- m2m_idle_shield_break

## Block / guard (5)
- m2m_defend
- m2m_idle_shield
- m2m_shield_oneshot
- m2m_sword_block
- m2m_weapon_block

## Heavy attacks (8)
- m2m_attack_ground_pound
- m2m_kick_roundhouse
- m2m_kick_spin
- m2m_shield_dash_rm
- m2m_sword_attack_air_vertical
- m2m_two_hand_blast
- m2m_two_handed_horizontal_swing
- m2m_two_handed_overhead_slam

## Weapon / sword attacks (light) (24)
- m2m_dagger_stab
- m2m_dual_wield_combo
- m2m_dual_wield_cross_slash
- m2m_idle_sword
- m2m_melee_hook
- m2m_melee_hook_rec
- m2m_one_hand_slash_combo
- m2m_one_hand_weapon_idle
- m2m_polearm_idle
- m2m_polearm_run
- m2m_spear_throw
- m2m_spear_thrust
- m2m_staff_combo
- m2m_staff_spin
- m2m_sword_attack
- m2m_sword_attack_rm
- m2m_sword_dash_rm
- m2m_sword_regular_a
- m2m_sword_regular_a_rec
- m2m_sword_regular_b
- m2m_sword_regular_b_rec
- m2m_sword_regular_c
- m2m_sword_regular_c_rm
- m2m_sword_regular_combo

## Unarmed attacks (7)
- m2m_fighting_idle
- m2m_fighting_left_jab
- m2m_fighting_right_jab
- m2m_kick_front
- m2m_kick_side
- m2m_punch_cross
- m2m_punch_jab

## Ranged / magic (29)
- m2m_bow
- m2m_bow_pull
- m2m_bow_pull_hold
- m2m_bow_release
- m2m_grenade_throw
- m2m_knife_throw
- m2m_overhandthrow
- m2m_pistol_aim_down
- m2m_pistol_aim_neutral
- m2m_pistol_aim_up
- m2m_pistol_fire
- m2m_pistol_idle
- m2m_pistol_idle_aim
- m2m_pistol_prone
- m2m_pistol_reload
- m2m_pistol_reload_2
- m2m_pistol_shoot
- m2m_pistol_walk
- m2m_power_up
- m2m_rifle_fire
- m2m_rifle_idle
- m2m_rifle_reload
- m2m_rifle_run
- m2m_rifle_walk
- m2m_spell_simple_enter
- m2m_spell_simple_exit
- m2m_spell_simple_idle
- m2m_spell_simple_shoot
- m2m_throw_ball

## Dodge / roll (14)
- m2m_backflip
- m2m_dance_body_roll
- m2m_dodge_back
- m2m_dodge_back_rm
- m2m_dodge_left
- m2m_dodge_left_rm
- m2m_dodge_right
- m2m_dodge_right_rm
- m2m_roll
- m2m_roll_rm
- m2m_slide
- m2m_slide_exit
- m2m_slide_start
- m2m_tumbling

## Locomotion (54)
- m2m_climb_ladder
- m2m_climb_pipe
- m2m_climb_wall
- m2m_climbup_1m_rm
- m2m_crawl
- m2m_crawl_rm
- m2m_crouch_idle
- m2m_crouch_walk
- m2m_drunk_walk
- m2m_flying_forward
- m2m_flying_forward_super
- m2m_freefall
- m2m_glide
- m2m_jog
- m2m_jump_2
- m2m_jump_2_rm
- m2m_jump_air
- m2m_jump_land
- m2m_jump_running
- m2m_jump_start
- m2m_jumping_jacks
- m2m_ladder_idle
- m2m_land_three_point
- m2m_ledge_climb_up
- m2m_ledge_hang
- m2m_moonwalk
- m2m_ninjajump_idle
- m2m_ninjajump_land
- m2m_ninjajump_start
- m2m_run_anime
- m2m_run_female
- m2m_run_stealth
- m2m_sprint
- m2m_strafe_left
- m2m_strafe_right
- m2m_swim_2
- m2m_swim_fwd
- m2m_swim_idle
- m2m_walk
- m2m_walk_backwards
- m2m_walk_carry
- m2m_walk_cautious
- m2m_walk_female
- m2m_walk_formal
- m2m_walk_happy
- m2m_walk_injured
- m2m_walk_large
- m2m_walk_relaxed
- m2m_walk_stealth
- m2m_wall_run
- m2m_zombie_run
- m2m_zombie_walk
- m2m_zombie_walk_2
- m2m_zombie_walk_3

## Idles (19)
- m2m_idle_a
- m2m_idle_foldarms
- m2m_idle_lantern
- m2m_idle_listening
- m2m_idle_rail
- m2m_idle_rail_call
- m2m_idle_shakeoff
- m2m_idle_subtle
- m2m_idle_talking
- m2m_idle_talkingphone
- m2m_idle_torch
- m2m_laytoidle
- m2m_levitate_idle
- m2m_meditate
- m2m_mount_idle
- m2m_sit_ground_idle
- m2m_sitting_idle
- m2m_zombie_idle
- m2m_zombie_idle_2

## Misc / emotes / work (49)
- m2m_angry
- m2m_chest_open
- m2m_chop_tree
- m2m_chop_wood
- m2m_clapping
- m2m_confused
- m2m_consume
- m2m_consume_powerup
- m2m_dab
- m2m_dance_arm_pump
- m2m_dance_charleston
- m2m_dance_reach_hip
- m2m_dance_simple
- m2m_driving
- m2m_farm_harvest
- m2m_farm_plantseed
- m2m_farm_watering
- m2m_fixing_kneeling
- m2m_greeting
- m2m_hammering
- m2m_head_nod
- m2m_interact
- m2m_knock
- m2m_levitate_entrance
- m2m_mining
- m2m_pick_up
- m2m_pickup_table
- m2m_push
- m2m_pushup
- m2m_reject
- m2m_rope_hang
- m2m_rope_pull
- m2m_rope_swing
- m2m_shiver
- m2m_shovel_dig
- m2m_sit_ground_crying
- m2m_sitting_enter
- m2m_sitting_exit
- m2m_sitting_talking
- m2m_sleeping
- m2m_tired_hunched
- m2m_tired_kneeling
- m2m_victory
- m2m_victory_fist_pump
- m2m_weapon_draw
- m2m_yes
- m2m_zombie_rise
- m2m_zombie_scratch
- m2m_zombie_yell

## creatures/
Mesh2Motion creature rigs (skeleton.glb + original animation GLBs, decompressed, not retargeted). See CREATURE_ANIM_LIST.md.
