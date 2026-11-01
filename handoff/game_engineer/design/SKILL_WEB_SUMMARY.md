# Sanctuary: final skill web and synergy reference (for faction paths and RNG steering)

**Source of truth:** the live bundle `live_12d/r.js` (prettier copy of `routes-BRGAGLf9.js`), synergy table `N` (`v: 6`) at **L280–2760**.
Closest design file: `synergy_web.json` (**v5**, 51 books, 153 buffs, made by `gen_web5.py`). No v6 JSON existed on the box, so the live table is exported here as `design/synergy_web_live_v6.json`.
**v5 → live v6 diff** (from the SKILLS_FIX_PART1 spec): Wrathbanner Aura → **Knell Aura** (guard) and Kinship Aura → **Undertow Aura** (holy). Their locks and the 5 buffs aimed at them point to the new auras, and 3 breakpoint texts changed (Mind Snare *mind_break*, Blink Step *phase_veil*, Veil *phantom_nova*). The other 49 books are identical to v5.
Full per-skill table: `design/skill_web_final.csv` (51 rites + 38 passives; category, damage type, shape, tags, locks, empowers, empowered by, partners, class start pools, bosses whose Boss Stone can offer it).

## 1. Structure (how the web works)
- **51 rites** (active skills) in **10 schools**. **Tomes are the only way to learn or rank a rite.** Each read adds +1 rank, up to **45** (`It` L10710). Gear can add up to +10 levels (`Tt` L10477).
- **The first read is permanent:** it **locks 2 opposing rites forever** (`Et` L10488, `ie` L9234). The game refuses a book that would lock a rite you already know. "Books never unlearn."
- **Every book empowers exactly 3 other rites** (153 buffs), and **every rite receives exactly 3**. No pair buffs each other.
- On top of that: **Bound attacks** (table `P` L2761, 459 rows = 51 rites × 9 weapons, each with a bonus and a tradeoff), a **passive tree** (38 nodes, `Vt` L10765), **Traits** (5 attributes, `Yt` L11149) and **4 class passives**.
- Per level (`checkLevel` L86374) you get +1 passive point and +1 trait point. Rites are never earned by levelling, only by books.

## 2. Skill categories (live `V`, L9843)
| School | # | Damage | Rites |
|---|---|---|---|
| Fire | 5 | Fire | Fireball, Meteor Shower, Inferno, Cinder Bed, Thunderkiln Trap |
| Cold | 4 | Cold | Frost Nova, Glacier, Hoarfrost, Rime Caltrop |
| Lightning | 4 | Lightning | Volt, Storm Call, Arc Whip, Elemental Consume |
| Holy | 5 | Magic | Holy Bolt, Consecrate, Smite, Star Lash, *Undertow Aura* |
| Blood | 3 | Physical, costs life | Blood Soaked, Mercy, Crimson Lance |
| Bone | 4 | Magic | Bone Spear, Raise Bone, Grave Burst, Bone Fan |
| Nature | 6 | Physical/utility | Thorn Coat, Briar Snare, Wolf Howl, Regrowth, Locust Cloud, Blight Cask |
| Steel | 7 | Physical | Wide Cut, Blade Dance, Execute, Rupture, Javelin, Aimed Shot, Ironjaw Trap |
| Guard | 6 | Physical/utility | Blind Shield Rush, Bulwark, War Cry, Frost Ward, Hearthward Aura, *Knell Aura* |
| Mind | 7 | Magic | Telekinesis, Hex, Mind Snare, Blink Step, Veil, Dread, Truesight Aura |

Cross-cutting sub-types: **4 traps** (one each in fire, cold, nature and steel), **4 auras** (max 2 active, each reserves 15% mana), **5 buffs**, 1 heal, 1 summon. **9 weapon skills roll attack rating** (Wide Cut, Blade Dance, Execute, Rupture, Blind Shield Rush, Javelin, Aimed Shot, Smite, Blood Soaked). Shapes: bolt 8, nova 8, ground 4, trap 4, aura 4, buff 5, melee 4, cone 3, seek 3, plus 1 each of rain, dash, blink, heal, summon, shove, pulse and fan.

## 3. Synergy rules
- **Formula** (`te` L9218): `bonus = sign·cap·(1 − e^(−pp·rank/cap))`. This is a soft cap: it climbs steeply at first, then flattens toward the cap. Breakpoint effects unlock at book rank 10, 15 or 20.
- **Clamps** (`ae` L9254): synergy damage ≤ +100%, cost ≥ −50%, cooldown ≥ −40%. At most 1 extra-projectile buff per rite and ≤ 2 extra projectiles per cast.
- **Design rules** (v5 JSON, Brian 2026-10-26): 3 buffs per book; every buff is unique, with its own breakpoints and budget (about 150 per book); **no generic "+% damage"**; each status keyword is used at most 3 times.
  - Proc caps: ignite/bleed/poison 40, shock 35, freeze 20, root 15, stun 12.
  - Bosses: stun is a 0.01 s flinch; freeze is 50% with 1 s immunity; slows are halved and capped at 25%; anti-cheese regen.
- **Buff kinds:** HEAL 23, AREA 19, DEBUFF 15, DUR 14, CHANCE 11, DOT 10, HIT 10, BOLT 10, SLOW 8, COST 7, KEEP 5, SPEED 5, CRIT 5, DEF 5, DMG 3, OTHER 3.
- ⚠ **Implementation status:** only the generic DMG, COST and extra-projectile hooks plus 4 bespoke mechanics are wired in live code (fireball *flame_wake*, nova *rime_ring*, hex *grave_curse* and *gravity_hex*). The other bespoke effects are tooltip text only. The audit says "148/153 dead"; the SKILLS_FIX spec to build them is pending.

## 4. Clusters and top cross-links (153 buffs: 76 within a school, 77 across)
| Cluster | Links | Examples |
|---|---|---|
| **Sanctum/Grove** (holy+nature) | 8 | Holy Bolt→Regrowth, Locust Cloud→Consecrate, Briar Snare→Smite, Undertow→Blight Cask |
| **Elemental storm** (fire+lightning, hub Elemental Consume) | 7 | Fireball→Volt, Meteor→Storm Call, Storm Call→Inferno, Consume→Fireball |
| **Underworld** (blood+bone) | 7 | Blood Soaked→Bone Spear/Raise Bone, Grave Burst→Mercy/Crimson Lance |
| **Wildfire** (fire+nature) | 5 | Blight Cask→Cinder Bed/Thunderkiln, Wolf Howl→Inferno |
| **Frost hub** (cold + lightning/guard/mind) | 5+5+5 | Glacier→Volt, Hoarfrost→Frost Ward, Rime Caltrop→Hearthward, Veil→Frost Nova |
| **Blade** (steel internal 14 + blood) | 4 | Crimson Lance→Execute, Blade Dance→Blood Soaked/Mercy, Rupture→Crimson Lance |
| **Mind** (internal 13) | — | control loop; bridges to holy, bone and cold |

**Most cross-school hubs:** Ironjaw Trap, Rime Caltrop and Hearthward Aura (5 schools each); Blight Cask, Thunderkiln Trap and all four auras (4 each).
**Lock oppositions by school pair:** mind↔steel 16, cold↔fire 6, lightning↔nature 6; guard↔(lightning, nature, mind, steel), bone↔holy, blood↔holy and bone↔nature 4 each.

## 5. Passives and other layers
- **Passive tree (38 nodes, max 12 each):**
  - Flesh 4: Might, Vitality, Reap, Whetstone
  - Blood 3: Bloodthirst, Open Vein, Cruor
  - Bone 2: Marrow, Ossuary
  - Element 6: Elemental Well, Kindling, Frostbite, Stormglass, Sanctify, Wildheart
  - Steel 7: Haste, Cleave, Executioner, Volley Shot, Serrate, Cripple, Trueflight
  - Guard 5: Toughness, Ward, Thorns, Sidestep, Aegis
  - Mind 8: Focus, Alchemy, Wellspring, Greed, Finder, Recovery, Fleetfoot, Discipline
  - Orbit 3: Orbiting Hammer, Ember Orbit, Frost Satellite
- **Traits:** Brawn, Vigor, Mark, Reverie, Fortune.
- **Classes** (`Ri` L21970) and class passives: Ironvow (melee, *Grit*), Longmark (ranged, *Stride*), Cinderwake (elemental, *Resonance*), Gravewell (underworld, *Toll*).
- **18 uniques cast or carry rites**, for example Font of Ash (Fireball), Confessor's Edge (Holy Bolt), Spear of the Toll Court (Storm Call), Hammer of the Ninth Bell and Kingsfell (Knell), Rib of Kinship (Undertow) and Tallow Cathedral Censer (Consecrate). These are natural places for faction-flavoured sidegrades.

## 6. Existing RNG for skill offers
| Offer | Function (line) | Seeded? |
|---|---|---|
| Start book | `$a` L25279: FNV-1a `Qa(name:createdAt)` % class pool `Za` L25267 | **Seeded** |
| Boss Stone (pick 1 of 6) | `no` L25335: Park-Miller `ao(Qa(createdAt:boss:diff))` builds the 6 choices: 1 from your class pool, ≥1 outside the boss's schools, the rest from boss-school and off-school rites mixed **with no extra weight for the boss's schools**. Quest-owed stones: `eo` L25290 | **Seeded** |
| Tome pick (quest `tomes` reward, first-read re-offer) | `oo(player,6)` L25405 (calls at L90000/90366/90380): `Math.random` over eligible rites, plus up to 2 sealed books shown | Unseeded |
| Scribe shop | `so` L25424 = `oo(3)` + ring (L80336, L90216) | Unseeded |
| Random tome drops | `Xa` L25251 with no id → uniform over all 51: loot `za` L25116 (0.35/0.55/0.8%), quest `book` reward L80280, king 6% L85899, bookshelf 3.5% L90734, Vesper secret L86765 | Unseeded |
| Fate meter | −10..+10 (`shiftFate` L80802); fate > 0 makes shrines last ×1.25 | n/a (a mild power effect already exists) |

## 7. Faction steering hooks (SUGGESTION, not canon; power-neutral)
**Power-neutral levers:**
- Change **which** eligible rites fill offer slots, never how many slots there are or how many ranks a pick gives.
- Swap faction-flavoured **Bound rows** or unique **proc rites** at the same budget.
- Leave the Boss Stone class slot alone.

**Mechanism:**
1. Make `oo` and `Xa` use seeded randomness, `ao(Qa(createdAt:context))`, the same way `no` already does.
2. Give each rite a small weight (e.g. ×1.5–2, at most 2 of 6 slots) from faction standing. Also apply the unused boss `schools` weight in `no`.

**Caveat:** duplicate books are what raise rank. Steering only menus where the player picks 1 (Boss Stone, tome pick) keeps book throughput unchanged. Steering *random drops* would speed up ranks, which is indirect power, so don't. The lock graph also gives factions natural rivals: mind↔steel, cold↔fire, lightning↔nature.

| Faction (bible §4) | Suggested schools | Flavour rites | Lore tie |
|---|---|---|---|
| Parish of Martsirt (gone) | holy, bone | Consecrate, Holy Bolt, Undertow Aura, Grave Burst | register of the drowned; salt statues; Tallow Censer |
| Halvane's Inquisition | mind, lightning (+ holy proc) | Hex, Mind Snare, Dread, Storm Call | Halvane's boss schools are lightning+mind; Confessor's Edge |
| Open Eye / iron citadel | guard, cold | Bulwark, Frost Ward, Glacier, Truesight Aura | cold-iron knights; Castellan; Wall of the Hollow King |
| Toll families (Hask, Kell, Kessane) | steel, lightning/fire | Javelin, Aimed Shot, Ironjaw Trap, Execute | Kessane is fire+steel, the Assessor lightning+steel; Spear of the Toll Court |
| Hollow smugglers (Jas) | nature (traps/poison), steel blades, blood | Blight Cask, Locust Cloud, Rupture, Blade Dance, Veil | Tallyman is blood+nature |
| Ash-camp of the Touched | fire, blood | Inferno, Cinder Bed, Mercy, Blood Soaked, Elemental Consume | Vhorr-Akesh is fire+lightning; Font of Ash |
| Survivors | nature (heal), guard support | Regrowth, Wolf Howl, Hearthward Aura, Knell Aura | Ninth Bell; "holding on"; Vault Bell |
