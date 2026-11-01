# Sanctuary: Companion Demons, math design (2026-10-30)

Paper design only. Built on the existing systems: difficulties Normal / Nightmare / Hell / the Margins (Hell only, fixed levels 121-185), monster tiers normal / magic pack / rare pack / boss, 8 gear slots (Weapon, Shield, Armor, Helm, Gloves, Belt, Ring, Amulet; there is no boots slot), item tiers normal / exceptional / elite, the 2-aura rule, the EIAS/EFCR speed breakpoints (cap 75), and D2 wording (value first, full stat names, nothing class-locked). Sim: `companion_sim.py` (output in `companion_sim_out.json`).

## 1. Drop rates (a demon is an event: one per 4-6 hours, Brian's call)
Pace model (mobile, per hour of play): 1,500 normal monsters, 450 magic pack members, 40 rare pack leaders, 4 bosses (~2,000 kills/hour). Normal: 0, solo only.

| Monster tier | Nightmare | Hell | the Margins |
|---|---|---|---|
| normal monster | 1 in 27,000 | 1 in 24,000 | 1 in 21,000 |
| magic pack member | 1 in 8,000 | 1 in 7,200 | 1 in 6,400 |
| rare pack leader | 1 in 1,700 | 1 in 1,500 | 1 in 1,350 |
| act boss / Margins boss | 1 in 80 | 1 in 72 | 1 in 64 |
| first kill of each act boss on Nightmare | guaranteed starter (one time per save) | - | - |

- Bad-luck guard: after **30,000 kills** (~15 hours) with no demon, the next rare pack leader drops one.
- Expected hours per demon (sim, 20,000 simulated hours each, guard included): **Nightmare 5.1 h, Hell 4.6 h, the Margins 4.1 h** (without the guard: 5.4 / 4.8 / 4.3 h). The guard gives 5.4% / 3.8% / 2.4% of demons.
- Magic Find has **no** effect (same as the boss-unique rule now).
- Drop event: soul-flare on the ground, unique-style sound, "A Companion Demon Answers" text. Demon level = area level of the drop (sets its band).

## 2. Slot rules and slot value
- A demon rolls **2 slots (70%)** or **3 slots (30%)**, no repeats. Roll weights: Ring 1.2, Weapon/Armor/Helm/Gloves/Belt 1.0, Shield 0.9, Amulet 0.8.
- 2 slots: 28 combos, 3 slots: 56 combos; 84 total.

| Slot | Value (budget points) | Why |
|---|---|---|
| Weapon | 16 | damage, speed breakpoints, procs |
| Shield | 12 | Chance to Block, Defense, resists |
| Armor | 12 | Defense, Life, resists |
| Helm | 10 | Life, item auras possible |
| Amulet | 10 | +skills, Resist All |
| Gloves | 8 | Attack Speed, Life Stolen per Hit |
| Belt | 6 | Life, Faster Hit Recovery |
| Ring | 6 | small mixed stats |

Slot value range per demon: 12 (Belt+Ring) to 40 (Weapon+Shield+Armor).

## 3. Roll budget
`Total = SlotValue + BaseRoll + PassiveValue`, with Total rolled uniformly inside the band:

| Difficulty | Band (center ±8) |
|---|---|
| Nightmare | 52-68 (60) |
| Hell | 62-78 (70) |
| the Margins | 72-88 (80) |

Procedure: roll Total in the band, roll slots (gives SlotValue), roll 2 passives (60%) or 3 (40%) with tier 1/2/3/4 at 40/32/20/8% worth 6/12/18/24 points. BaseRoll = Total - SlotValue - PassiveValue. If BaseRoll < 10, lower the highest passive tier one step until it fits (drop a passive if needed). BaseRoll is clamped 10-50. The band is kept by construction (100% in band in the sim). Variance stays wide: a demon can be all slots, all passives, or all base stats.

BaseRoll -> stats (per point, at demon level L): +0.9% Life multiplier, +0.6% Damage multiplier, +0.5% Defense multiplier above the base curve below. The demon's archetype (tank / damage / utility / elemental, 25% each) chooses how points are split (tank 60/20/20 Life/Damage/Defense, damage 25/60/15, utility 40/30/30, elemental 30/45/25 plus +10% to one element).

## 4. Scaling and the share cap
- Demon level = hero level - 2 (it follows the hero, the dropped level only sets the band).
- Base curve at level L: Life = 30 + 9·L, Damage = 4 + 0.9·L per hit, Defense = 8·L, 1.6 attacks/sec (15-frame base, uses the axe/spear EIAS table; EIAS cap 75).
- Gear on a demon works at **60%** of its listed values (Item auras on demon gear: listed level - 4, and they count as item auras, so they do not use the 2-aura limit).
- The demon has 0 Resist All at start, -20% per difficulty above Nightmare, like the hero.
- **Share target**: demon DPS = 15-25% of party DPS (sim median 19.5%), demon EHP = 20-35% of party EHP. Soft cap: demon DPS above 30% of hero DPS counts at half value; hard cap 35% of hero DPS (= 26% of party DPS). Same caps for EHP vs hero EHP at 50%/60%. The cap is checked live from the hero's current sheet, so a geared hero always outshines the demon.
- Demon death: comes back at home-base, or 60 seconds after death in the field. No Life loss of the hero.

## 5. Passive and skill pool (18 entries)
Tier values in [T1/T2/T3/T4]. Nothing class-locked.

| # | Name | Archetype | Text (T1/T2/T3/T4) |
|---|---|---|---|
| 1 | Bulwark | tank | +[10/18/26/35]% Max Life |
| 2 | Taunting Roar | tank | Monsters within 6 yards attack the demon, 6s, every [14/12/10/8]s |
| 3 | Iron Hide | tank | +[15/30/45/60]% Defense |
| 4 | Leap Guard | tank | [20/30/40/50]% Chance to Intercept Leap and Charge Attacks aimed at you |
| 5 | Ward of Thorns | tank | Attacker Takes Damage of [5/10/16/24] per Demon Level/4 |
| 6 | Bloodfrenzy | damage | +[10/20/30/40]% Attack Speed |
| 7 | Rending Claws | damage | +[8/14/20/28]% Deadly Strike |
| 8 | Crushing Maw | damage | [5/9/13/18]% Chance of Crushing Blow |
| 9 | Hunting Pack | damage | +[10/18/26/35]% Damage to Monsters you Hit in the last 3s |
| 10 | Soul Siphon | utility | [2/3/4/6]% Life Stolen per Hit, shared with you at half value |
| 11 | Mana Tithe | utility | +[1/2/3/4] Mana per Kill to you |
| 12 | Hasting Howl | utility | +[5/8/11/15]% Faster Run/Walk to Members within 8 yards |
| 13 | Gleaning Eye | utility | +[5/10/15/20]% Better Chance of Getting Magic Items from Monsters the demon kills |
| 14 | Mending Pulse | utility | Heals Members [2/3/4/5]% Max Life every 5s |
| 15 | Ember Blood | elemental | Adds [3-6/6-11/9-17/13-24] Fire Damage, +[10/15/20/30]% Fire Resist |
| 16 | Rime Blood | elemental | Adds [2-5/5-9/7-14/10-20] Cold Damage, Chills, +[10/15/20/30]% Cold Resist |
| 17 | Storm Blood | elemental | Adds [1-9/1-16/2-24/3-34] Lightning Damage, +[10/15/20/30]% Lightning Resist |
| 18 | Undertow Bond | elemental | Level [2/4/6/8] Undertow Aura (item-aura rules: reserves nothing) |

Rules: no duplicate passives on one demon; at most 1 aura passive; the archetype weights passive rolls 2:1 toward its own group. Gleaning Eye is capped at T2 in the Margins (keeps MF off the demon as a farm tool).

## 6. Roster and swap rules
- Home-base roster: 6 bench slots (+1 per Margins boss first kill, max 10). One active demon at a time.
- Swap only at home base (town), free. Gear stays on the demon when benched.
- **Zone Affinity**: each zone rolls a daily "favored archetype" and "hostile element" (shown on the waypoint). Favored archetype: +10% to the demon's share cap. Element match vs hostile element: +20% that resist. This rotates the right pick daily.
- **Bond fatigue**: an active demon gains Bond for each zone cleared; after 5 zones in a row, -2% damage per zone (max -10%) until benched for 1 zone. Small enough to ignore, big enough to reward a second pick.
- Re-roll ("Unbinding", costs gold + a Soul Shard from Margins bosses): re-rolls passives inside the same budget, keeps slots. No way to add slots.
- Demons cannot be traded (no multiplayer).

## 7. Visuals and UI (Canvas 2D)
- Gear layers: Weapon and Shield are drawn as held sprites, Helm as a head overlay, Armor as a body tint plus plates, Gloves/Belt/Ring/Amulet as small glow sockets. Item tier = palette (normal dull, exceptional bronze, elite bright plus glow), uniques get their own glow color.
- Health: thin bar over its head (hidden at full Life), plus a 4px bar under the hero's resource bar with a demon icon.

## 8. Sim results (100,000 demons per difficulty, seed 7)
| | Nightmare | Hell | the Margins |
|---|---|---|---|
| in band | 100% | 100% | 100% |
| Total mean / sd | 60.0 / 4.6 | 70.0 / 4.6 | 79.5 / 4.6 |
| combo mean spread (best vs worst of 84) | 2.9% | 1.3% | 1.9% |
| any combo strictly best (p10 > another's p90) | no | no | no |
| avg BaseRoll 2-slot vs 3-slot | 17.4 vs 13.9 | 23.7 vs 17.4 | 32.3 vs 23.9 |
| avg PassiveValue 2-slot vs 3-slot | 22.8 vs 16.6 | 26.5 vs 22.8 | 27.7 vs 26.4 |
| demon DPS share of party (p10/p50/p90) | 17.1/19.4/21.6% | 17.5/19.5/21.3% | 17.8/19.5/21.1% |

Trade-off confirmed: more/better slots mean lower base and passives. Gear-heavy demons have the widest spread (they depend on what loot you feed them); base-heavy ones are steady. Tuning done: base clamp raised 45 -> 50 because Belt+Ring in the Margins lost 3.7% to clipping.

## Open questions for Brian
1. (Decided: 4-6 hours per demon.) Is the ~2,000 kills/hour pace model close to real play? If players kill slower, hours per demon go up in step.
2. MF no effect on demons: okay?
3. One active demon, or two in the Margins?
4. Gear at 60% on a demon: okay, or full value with a lower share cap?
5. Demon death: 60s field respawn or back to town only?
6. Bond fatigue: keep or cut (some players hate forced swaps)?
7. Unbinding re-roll: allowed at all?
