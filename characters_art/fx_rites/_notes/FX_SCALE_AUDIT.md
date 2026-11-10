# FX scale audit — every skill and rite

Generated 2026-11-10, America/Detroit. Read-only. **No game code edited. Nothing pushed.**

Brian asked that this cover **every** skill and rite, not just Fireball, each with a Diablo 2 equivalent, and that unmapped skills are listed.

## How live 3D scale works (applies to many rites at once)

Source: `/workspace/live14/routes-C2sLE0N3.js` (byte-identical to `/workspace/live_bundle_check/routes-C2sLE0N3.js`, mtime 2026-11-09 5:06 PM ET).

| Primitive | Where | Size | Color / blend | Used for |
|-----------|-------|------|----------------|----------|
| `this.boltGeo = new SphereGeometry(0.10, 6, 5)` | line 4523 | radius **0.10 m**, diameter **0.20 m** | `boltColor(kind)` emissive 0.9, or goldMat; untextured | Default travel mesh for most `shape: bolt` rites |
| `this.globGeo = new SphereGeometry(0.28, 10, 8)` | line 4523 | base radius 0.28 m, then scaled | untextured emissive | Motes, spit, mounds |
| Ember / default motes | `syncMotes` scale `.05/.28` | radius **0.05 m** | fire/ember | Fireball impact puffs |
| Glass motes | `syncMotes` scale `.18/.28` | radius **0.18 m**, diameter **0.36 m** | `#FFF2C4`, emissive 1.5 | Heaven's Shrapnel impact — the big white blobs |
| `makeGlass()` boxes | `BoxGeometry(0.03, 0.20, 0.01)` × 4 | 3×20×1 cm cluster, spun | `#FFF8E8` / emissive `#FFE29A` @ 1.6 | Heaven's Shrapnel **travel** stand-in |
| Spear mesh | `askRiteMeshes` + `dressSpear` | unit 1, or ×2 for Javelin | tinted, no Behest textures | Bone Spear, Javelin |
| Arrow mesh | `loadProp(arrow)` | model size | textured arrow | Aimed Shot |
| Grave cross | `grave_burst_stone_cross.glb` scale (1,1,1) | as authored | the one fx_rites pack actually loaded | Grave Burst |
| ice_shards.glb | loaded | as authored (per-pop scale NOT CHECKED) | ice | Glacier impact pops |

**Default bolt color table `DP`:** fire `#FF6630`, frost `#9FD7FF`, spark `#FFEEA8`, holy `#FFF0C0`, bone `#E4E4C4`, arrow, orb, acid, steel, blood. Holy and spark are already near-white. Fallback if kind is missing: `#FFF2C0`.

**D2 read:** D2 Fireball is a modest flying orb (the 0.20 m sphere is in the ballpark, maybe a bit fat). D2 Lightning / Charged Bolt / Holy Bolt / Fist of the Heavens are **thin bolts or small shards**, not 20 cm glowing spheres. D2 Corpse Explosion / Meteor are bigger. Anything still on `boltGeo` will look blobby next to D2 lightning or shrapnel.

## fx_rites / fx_status packs (authored scale)

| Pack | Authored size (from USAGE) | Suggested live scale vs D2 | Status in live 3D |
|------|----------------------------|----------------------------|-------------------|
| `fx_rites/fireball` | core flipbook typically ~0.55–0.75 m (USAGE) | Keep the ball readable (≈0.4–0.7 m) but do not use the 0.20 m untextured sphere once the pack is wired | **Not loaded** |
| `fx_rites/arc_whip` v1 | whip mesh reach ~3.3 m; FX trails are strips | v1 lasso was the latching problem. v2 bolt quad 2.0×0.55 m, thin lightning (D2 Charged Bolt / Lightning) | **Not loaded**. v2 is local handoff only |
| `fx_rites/behest_banspere` | lance mesh as authored | spear-sized, D2 Bone Spear thin shaft — avoid fat orbs | **Not loaded** (live uses weapon_spear.glb instead) |
| `fx_rites/grave_burst` | cross at (1,1,1) | Already wired at (1,1,1). Confirm it does not dwarf the hero (NOT TESTED in-game by art). Local v2 adds 1.8–6.5 cm rocks | Cross **is loaded**; v2 rocks are not |
| `fx_rites/heavens_shrapnel` v1 | shard length **0.36–0.50 m** at (1,1,1) | Too big for "tiny shrapnel." Spawn scale **0.20–0.35** so long axis is **0.07–0.15 m**. Impact fragments 0.05–0.10 m. D2 Fist of the Heavens bolts are small | **Not loaded** — white boxes/spheres used instead |
| `fx_rites/heavens_shrapnel` v2 (local) | 0.55–0.78 m | Even chunkier; if used, scale ~0.12–0.22 to hit 0.05–0.15 m | Not pushed |
| `fx_rites/campfire_flame` | campfire-sized flipbooks | Fine for a fire bed / Cinder placeholder; too big for a spark | Environmental; not a rite wire in this bundle |
| `fx_status/ice_shards` | per-shard heights in `ice_shards_info.json` | D2 Glacial Spike shards are modest; keep pops smaller than a head | **Loaded** |

## The 51 rites and auras

| id | name | locked 18 | FX status | Live 3D scale (this bundle) | Closest D2 skill | Exact D2? |
|----|------|-----------|-----------|-----------------------------|------------------|-----------|
| `fireball` | Fireball | yes | dedicated pack, not wired | Travel: default bolt sphere SphereGeometry(r=0.10 m), diameter 0.20 m, emissive fire color (DP.fire). Impact: puffFx(ember, 8, height 0.55) — ember motes use scale 0.05/0.28 → r=0.05 m. Fireball flipbook pack is NOT loaded. | Fireball (Sorceress) | yes |
| `meteor` | Meteor Shower |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Meteor (Sorceress); Armageddon is the raining cousin | no — closest |
| `inferno` | Inferno |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Inferno (Sorceress) | yes |
| `cinder` | Cinder Bed | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Blaze / Fire Wall / Fissure | no — closest |
| `thunderkiln` | Thunderkiln Trap |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Lightning Sentry / Wake of Fire / Charged Bolt Sentry (Assassin) | no — closest |
| `nova` | Frost Nova |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Frost Nova (Sorceress) | yes |
| `glacier` | Glacier | yes | ice_shards wired | Travel: default bolt sphere r=0.10 m, frost color (DP.frost). Impact: puffFx(icepop, 7, height 0.70). ice_shards.glb IS loaded (syncIcePops) — scale of each pop NOT fully measured in this pass (see Not checked). | Glacial Spike / Frozen Orb / Ice Blast | no — closest |
| `hoarfrost` | Hoarfrost |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Blizzard / Frozen Armor / Holy Freeze (as a field) | no — closest |
| `rimecaltrop` | Rime Caltrop |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Wake of Fire / Shock Web (Assassin traps), cold-tinted | no — closest |
| `spark` | Volt | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Charged Bolt / Chain Lightning / Lightning | no — closest |
| `stormcall` | Storm Call |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Thunder Storm (Sorceress) / Fist of the Heavens (as bolts from above) | no — closest |
| `arcwhip` | Arc Whip | yes | dedicated pack, not wired (v2 local) | No dedicated 3D projectile path found in syncSpearGlass / syncBolts (not in the hide list, so it would use the default r=0.10 m sphere + boltKind spark). v1 lasso/whip mesh is NOT loaded in this live bundle. v2 is local only. | Charged Bolt / Lightning / Lightning Fury | no — closest |
| `elemconsume` | Elemental Consume |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Enchant / Energy Shield / Lower Resist (partial) | no — closest |
| `holy` | Holy Bolt |  | placeholder only | Travel: default bolt sphere r=0.10 m, DP.holy = #FFF0C0 (very pale gold-white). Can read as a white blob, same family as the shrapnel complaint. No Holy Bolt pack loaded. | Holy Bolt (Paladin) | yes |
| `consecrate` | Consecrate |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Sanctuary / Holy Fire / Fist of the Heavens (ground effect) | no — closest |
| `smite` | Smite |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Smite (Paladin) | yes |
| `starlash` | Star Lash / Heaven's Shrapnel | yes | dedicated pack, not wired (white fallback) | Travel: makeGlass() — 4× BoxGeometry(0.03, 0.20, 0.01) almost-white emissive 1.6, spinning. Impact: puffFx(glass, 10, height 0.95) spheres at r=0.18 m (diameter 0.36 m), color #FFF2C4. Shard GLBs NOT loaded. See HEAVENS_SHRAPNEL_FIX.md. | Fist of the Heavens / Blessed Hammer (holy projectiles) | no — closest |
| `kinship` | Kinship Aura |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Prayer / Blood Golem (party share is not a D2 aura) | no — closest |
| `bloodsoaked` | Blood Soaked |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Sacrifice (Paladin) | no — closest |
| `mercy` | Mercy |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | (none exact); Poison Nova / Terror as a pulse shape only | no — closest |
| `crimson` | Crimson Lance |  | placeholder only | Travel: default bolt sphere r=0.10 m, boltKind → blood, DP.blood. Behest lance not used. | Impale / Bone Spear (as a piercing shaft), blood-tinted | no — closest |
| `bonespear` | Bone Spear | yes | dedicated pack, not wired (live uses weapon_spear) | Travel: weapon_spear.glb, dressSpear bone tint, scale spearUnit×1 (spearUnit = 1 if raw size 0.8–3.2 m, else 1.7/raw). Default bolt sphere hidden. Behest pack NOT loaded. | Bone Spear (Necromancer) | yes |
| `summon` | Raise Bone | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Raise Skeleton (Necromancer) | yes |
| `graveburst` | Grave Burst | yes | dedicated pack, cross wired | Stone cross GLB at scale (1,1,1), rises over 0.45 s. Shatter uses the cross mesh pieces, life 0.42 s. Ground-burst v2 (tiny rocks) is local only, not in this live bundle. | Corpse Explosion / Teeth / Bone Spirit | no — closest |
| `fanbone` | Bone Fan | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Teeth (Necromancer) | yes |
| `thorncoat` | Thorn Coat |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Thorns (Paladin) | yes |
| `briar` | Briar Snare |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | (none exact); Decrepify / Clay Golem slow as a snare only | no — closest |
| `wolfhowl` | Wolf Howl | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Howl / Battle Orders / Feral Rage / Heart of Wolverine | no — closest |
| `regrowth` | Regrowth |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Prayer / Meditation / Oak Sage / Cleansing | no — closest |
| `locust` | Locust Cloud |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Poison Nova / Poison Explosion; D3 has Locust Swarm | no — closest |
| `blightcask` | Blight Cask |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Death Sentry / Poison Explosion / Poison Creeper | no — closest |
| `cleave` | Wide Cut |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Whirlwind / Concentrate (no Cleave in D2) | no — closest |
| `bladedance` | Blade Dance |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Whirlwind (Barbarian) | yes |
| `execute` | Execute | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Berserk (as a finishing blow only) | no — closest |
| `rupture` | Rupture | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Impale (stick) + Open Wounds (item mod) | no — closest |
| `javelin` | Javelin | yes | placeholder only | Travel: same spear mesh at spearUnit×2 (twice Bone Spear). Default bolt hidden. | Javelin / Impale / Lightning Fury / Power Strike (Amazon) | yes |
| `aimed` | Aimed Shot | yes | placeholder only | Travel: arrow GLB via loadProp(arrow), not the 0.10 m sphere. Scale from the arrow rig (half-length from bbox). | Guided Arrow / Magic Arrow / Strafe | no — closest |
| `ironjaw` | Ironjaw Trap |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Death Sentry / Blade Sentinel / Shock Web | no — closest |
| `blindrush` | Blind Shield Rush | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Charge (Paladin) / Leap (Barbarian) | no — closest |
| `bulwark` | Bulwark | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Defiance / Shout / Iron Skin / Holy Shield | no — closest |
| `warcry` | War Cry | yes | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | War Cry (Barbarian) | yes |
| `frostward` | Frost Ward |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Frozen Armor / Shiver Armor / Chilling Armor | yes |
| `hearthward` | Hearthward Aura |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Prayer + Defiance / Meditation | no — closest |
| `wrathbanner` | Wrathbanner Aura |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Fanaticism / Might / Concentration | no — closest |
| `telekinesis` | Telekinesis |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Telekinesis (Sorceress) | yes |
| `hex` | Hex |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Amplify Damage / Decrepify / Lower Resist / Life Tap | no — closest |
| `snare` | Mind Snare |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Dim Vision / Attract / Confuse / Slow Missiles | no — closest |
| `blinkstep` | Blink Step |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Teleport (Sorceress) | yes |
| `veil` | Veil |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Fade / Cloak of Shadows / Dodge (Amazon passive) | no — closest |
| `dread` | Dread |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Terror / Howl | yes |
| `truesight` | Truesight Aura |  | placeholder only | No dedicated pack loaded. If the rite is shape `bolt`/`fan` and not in the spear/arrow/starlash exceptions, it uses the **0.10 m untextured sphere**. Other shapes (nova, ground, trap, aura, melee) use procedural rings/puffs — exact metres NOT CHECKED per rite. | Inner Sight / Blessed Aim / Penetrate | no — closest |

## Passives, class passives, item procs, Bound, synergies

Source of the list: `/workspace/sanctuary/all_skills.csv` (113 rows). Item procs and item auras **reuse the parent rite** and should inherit that rite's FX and scale. Bound attacks and book synergies are not separate travel FX.

| id | name | type | FX / scale | Closest D2 | Exact D2? |
|----|------|------|------------|------------|-----------|
| `might` | Might | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Might (Paladin aura) | yes |
| `vit` | Vitality | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (no skill — Vitality is a D2 stat) | no — closest or none |
| `reap` | Reap | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact); Life Tap / Find Potion as loose cousins | no — closest or none |
| `whetstone` | Whetstone | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact) | no — closest or none |
| `bloodthirst` | Bloodthirst | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact); Life Tap / Hunger | no — closest or none |
| `openvein` | Open Vein | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Open Wounds (D2 item modifier, not a skill) | no — closest or none |
| `cruor` | Cruor | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact) | no — closest or none |
| `marrow` | Marrow | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact); Bone skill mastery family | no — closest or none |
| `ossuary` | Ossuary | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact); Bone skill mastery family | no — closest or none |
| `elemwell` | Elemental Well | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact); elemental mastery family | no — closest or none |
| `kindling` | Kindling | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Fire Mastery (Sorceress) | yes |
| `frostbite` | Frostbite | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Cold Mastery (Sorceress) | yes |
| `stormglass` | Stormglass | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Lightning Mastery (Sorceress) | yes |
| `sanctify` | Sanctify | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact); Sanctuary / holy mastery | no — closest or none |
| `wildheart` | Wildheart | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact); Druid shapeshift / HoW family | no — closest or none |
| `haste` | Haste | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Burst of Speed / Increased Speed / Fanaticism | no — closest or none |
| `cleave` | Cleave (passive, not Wide Cut) | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact) — this is the Cleave *passive*, not Wide Cut | no — closest or none |
| `exec` | Executioner | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact) | no — closest or none |
| `needle` | Needle | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact) | no — closest or none |
| `serrate` | Serrate | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact) | no — closest or none |
| `cripple` | Cripple | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact); Slow Missiles as a loose cousin | no — closest or none |
| `trueflight` | Trueflight | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Penetrate / Pierce / Critical Strike (Amazon) | no — closest or none |
| `tough` | Toughness | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Iron Skin / Natural Resistance | no — closest or none |
| `ward` | Ward | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Defiance / Energy Shield | no — closest or none |
| `thorns` | Thorns | passive | Reflect proc; no travel bolt. Hit sparks only. | Thorns (Paladin) | yes |
| `sidestep` | Sidestep | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Dodge / Avoid / Evade (Amazon) | yes |
| `aegis` | Aegis | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Holy Shield / Defiance | no — closest or none |
| `focus` | Focus | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact) | no — closest or none |
| `alchemy` | Alchemy | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact) | no — closest or none |
| `wellspring` | Wellspring | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Prayer / Meditation | no — closest or none |
| `greed` | Greed | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (no skill — Gold Find is a D2 item modifier) | no — closest or none |
| `finder` | Finder | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (no skill — Magic Find is a D2 item modifier) | no — closest or none |
| `recovery` | Recovery | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Prayer / Cleansing / Meditation | no — closest or none |
| `fleetfoot` | Fleetfoot | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | Increased Speed / Burst of Speed | no — closest or none |
| `discipline` | Discipline | passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact) | no — closest or none |
| `hammer` | Orbiting Hammer | passive | Has (or should have) orbiting projectile FX. Closest D2 is Blessed Hammer — those hammers are **small**. Live orbit scale NOT CHECKED in this bundle. | Blessed Hammer (Paladin) | yes |
| `embers` | Ember Orbit | passive | Orbiting fire motes. If they use boltGeo / globGeo at 0.10–0.28 m they will read as blobs. NOT CHECKED. | (none exact); Firestorm / Hydra / Armageddon as orbit/fire cousins | no — closest or none |
| `frostsat` | Frost Satellite | passive | Orbiting ice. ice_shards is available. Live scale NOT CHECKED. | Frozen Orb / Hurricane (as a circling cold companion) | no — closest or none |
| `grit` | Grit (Ironvow) | class passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact — Ironvow class passive) | no — closest or none |
| `stride` | Stride (Longmark) | class passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact — Longmark class passive) | no — closest or none |
| `resonance` | Resonance (Cinderwake) | class passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact — Cinderwake class passive) | no — closest or none |
| `toll` | Toll (Gravewell) | class passive | No travel projectile expected (stat / stance / proc). No live scale issue unless a later visual is added. | (none exact — Gravewell class passive) | no — closest or none |

### Item procs and item auras (reuse the parent rite)

| id | name | parent rite | Closest D2 (parent) | Exact D2? |
|----|------|-------------|---------------------|-----------|
| `fireball@Wick of the Ninth Bell` | 10% Chance to Cast Level 1 Fireball on Striking | `fireball` | Fireball (Sorceress) | yes |
| `spark@Ferryman's Coin` | 3% Chance to Cast Level 2 Volt when Struck | `spark` | Charged Bolt / Chain Lightning / Lightning | no — closest |
| `holy@The Confessor's Edge` | 10% Chance to Cast Level 6 Holy Bolt on Striking | `holy` | Holy Bolt (Paladin) | yes |
| `wrathbanner@Hammer of the Ninth Bell` | Level 5 Wrathbanner Aura when Equipped | `wrathbanner` | Fanaticism / Might / Concentration | no — closest |
| `crimson@Needle of Mercy` | 8% Chance to Cast Level 5 Crimson Lance on Striking | `crimson` | Impale / Bone Spear (as a piercing shaft), blood-tinted | no — closest |
| `kinship@Rib of Kinship` | Level 4 Kinship Aura when Equipped | `kinship` | Prayer / Blood Golem (party share is not a D2 aura) | no — closest |
| `holy@The Last Page` | 15% Chance to Cast Level 18 Holy Bolt on Striking | `holy` | Holy Bolt (Paladin) | yes |
| `wrathbanner@Kingsfell` | Level 8 Wrathbanner Aura when Equipped | `wrathbanner` | Fanaticism / Might / Concentration | no — closest |
| `graveburst@Hollow Star Reaver` | Kills Have 25% Chance to Cast Level 15 Grave Burst | `graveburst` | Corpse Explosion / Teeth / Bone Spirit | no — closest |
| `stormcall@Spear of the Toll Court` | 10% Chance to Cast Level 14 Storm Call on Striking | `stormcall` | Thunder Storm (Sorceress) / Fist of the Heavens (as bolts from above) | no — closest |
| `hearthward@The Vault Bell` | Level 10 Hearthward Aura when Equipped | `hearthward` | Prayer + Defiance / Meditation | no — closest |
| `consecrate@Tallow Cathedral Censer` | 20% Chance to Cast Level 12 Consecrate when Struck | `consecrate` | Sanctuary / Holy Fire / Fist of the Heavens (ground effect) | no — closest |
| `meteor@Spire-Heart Longbow` | 12% Chance to Cast Level 10 Meteor Shower on Striking | `meteor` | Meteor (Sorceress); Armageddon is the raining cousin | no — closest |
| `fireball@Font of Ash` | 25% Chance to Cast Level 12 Fireball on Striking | `fireball` | Fireball (Sorceress) | yes |
| `frostward@Wall of the Hollow King` | Blocked Hits Have 20% Chance to Cast Level 10 Frost Ward | `frostward` | Frozen Armor / Shiver Armor / Chilling Armor | yes |
| `hearthward@Tallow Plate` | Level 8 Hearthward Aura when Equipped | `hearthward` | Prayer + Defiance / Meditation | no — closest |
| `nova@Hands That Turn Pages` | 5% Chance to Cast Level 10 Frost Nova when Struck | `nova` | Frost Nova (Sorceress) | yes |
| `truesight@The Ninth Bell's Clapper` | Level 6 Truesight Aura when Equipped | `truesight` | Inner Sight / Blessed Aim / Penetrate | no — closest |

| id | name | type | FX / D2 |
|----|------|------|---------|
| `bound_*` | 459 Bound rows (rite × weapon) | Bound attack | Reuse the bound rite's FX and scale. Not a separate D2 skill (D2 "charged" attacks are the loose cousin). |
| `synergy_*` | 153 book synergies | synergy | D2-style synergies: no unique travel FX. |

## Skills with no exact Diablo 2 equivalent

These still have a **closest** D2 skill in the tables above. "Unmapped" here means no honest 1:1 name or behavior match.

- `meteor` Meteor Shower — closest: Meteor (Sorceress); Armageddon is the raining cousin. D2 Meteor is one large stone; this rite is a shower.
- `cinder` Cinder Bed — closest: Blaze / Fire Wall / Fissure. No exact "burning bed" skill; closest are ground-fire trails and patches.
- `thunderkiln` Thunderkiln Trap — closest: Lightning Sentry / Wake of Fire / Charged Bolt Sentry (Assassin). No kiln; closest are elemental sentries.
- `glacier` Glacier — closest: Glacial Spike / Frozen Orb / Ice Blast. No skill named Glacier; closest is a heavy ice projectile (Glacial Spike).
- `hoarfrost` Hoarfrost — closest: Blizzard / Frozen Armor / Holy Freeze (as a field). Spreading rime field has no exact name-match.
- `rimecaltrop` Rime Caltrop — closest: Wake of Fire / Shock Web (Assassin traps), cold-tinted. No caltrops in D2.
- `spark` Volt — closest: Charged Bolt / Chain Lightning / Lightning. Volt jumps like Chain Lightning more than a single Lightning beam.
- `stormcall` Storm Call — closest: Thunder Storm (Sorceress) / Fist of the Heavens (as bolts from above). Closest is Thunder Storm.
- `arcwhip` Arc Whip — closest: Charged Bolt / Lightning / Lightning Fury. No whip skill in D2. v2 is a zig-zag lightning projectile, closest to Charged Bolt or Lightning.
- `elemconsume` Elemental Consume — closest: Enchant / Energy Shield / Lower Resist (partial). No exact "consume elements" skill.
- `consecrate` Consecrate — closest: Sanctuary / Holy Fire / Fist of the Heavens (ground effect). No Consecrate in D2; holy ground burn is the idea.
- `starlash` Star Lash / Heaven's Shrapnel — closest: Fist of the Heavens / Blessed Hammer (holy projectiles). No "Heaven's Shrapnel" in D2. Tiny stained-glass shards are original; closest holy multi-projectile is Fist of the Heavens.
- `kinship` Kinship Aura — closest: Prayer / Blood Golem (party share is not a D2 aura). No exact damage-share aura.
- `bloodsoaked` Blood Soaked — closest: Sacrifice (Paladin). Life-priced hit; not a 1:1.
- `mercy` Mercy — closest: (none exact); Poison Nova / Terror as a pulse shape only. Life-priced blood pulse — no D2 Mercy.
- `crimson` Crimson Lance — closest: Impale / Bone Spear (as a piercing shaft), blood-tinted. No Crimson Lance in D2.
- `graveburst` Grave Burst — closest: Corpse Explosion / Teeth / Bone Spirit. Ground-burst bone is closest to Corpse Explosion in feel, not a 1:1.
- `briar` Briar Snare — closest: (none exact); Decrepify / Clay Golem slow as a snare only. No briar/root snare skill in D2.
- `wolfhowl` Wolf Howl — closest: Howl / Battle Orders / Feral Rage / Heart of Wolverine. Buff howl; no exact "Wolf Howl." Howl is a fear shout; Battle Orders / HoW are the buff cousins.
- `regrowth` Regrowth — closest: Prayer / Meditation / Oak Sage / Cleansing. HoT; no Regrowth in D2.
- `locust` Locust Cloud — closest: Poison Nova / Poison Explosion; D3 has Locust Swarm. No Locust Cloud in D2.
- `blightcask` Blight Cask — closest: Death Sentry / Poison Explosion / Poison Creeper. Trap cask has no exact name-match.
- `cleave` Wide Cut — closest: Whirlwind / Concentrate (no Cleave in D2). Wide melee cut — no Cleave skill in D2.
- `execute` Execute — closest: Berserk (as a finishing blow only). No Execute skill in D2.
- `rupture` Rupture — closest: Impale (stick) + Open Wounds (item mod). No Rupture skill; Open Wounds is a modifier.
- `aimed` Aimed Shot — closest: Guided Arrow / Magic Arrow / Strafe. No skill named Aimed Shot in D2 (that name is later Diablo).
- `ironjaw` Ironjaw Trap — closest: Death Sentry / Blade Sentinel / Shock Web. No Ironjaw; assassin traps are the closest.
- `blindrush` Blind Shield Rush — closest: Charge (Paladin) / Leap (Barbarian). Shield rush with a blind — Charge is the closest.
- `bulwark` Bulwark — closest: Defiance / Shout / Iron Skin / Holy Shield. Brace / DR buff — no Bulwark name in D2.
- `hearthward` Hearthward Aura — closest: Prayer + Defiance / Meditation. Regen + armor aura; no Hearthward.
- `wrathbanner` Wrathbanner Aura — closest: Fanaticism / Might / Concentration. Damage-stacking banner; Fanaticism is the closest.
- `hex` Hex — closest: Amplify Damage / Decrepify / Lower Resist / Life Tap. Curse family; no Hex name as a Paladin/Necro curse title in the same way (D2 has "Hex" only as flavor). Closest: Decrepify / Amp.
- `snare` Mind Snare — closest: Dim Vision / Attract / Confuse / Slow Missiles. Mind bind; no Mind Snare.
- `veil` Veil — closest: Fade / Cloak of Shadows / Dodge (Amazon passive). Dodge cloak; no Veil skill.
- `truesight` Truesight Aura — closest: Inner Sight / Blessed Aim / Penetrate. AR aura; Blessed Aim / Inner Sight are the closest.
- `vit` Vitality (passive) — closest: (no skill — Vitality is a D2 stat)
- `reap` Reap (passive) — closest: (none exact); Life Tap / Find Potion as loose cousins
- `whetstone` Whetstone (passive) — closest: (none exact)
- `bloodthirst` Bloodthirst (passive) — closest: (none exact); Life Tap / Hunger
- `openvein` Open Vein (passive) — closest: Open Wounds (D2 item modifier, not a skill)
- `cruor` Cruor (passive) — closest: (none exact)
- `marrow` Marrow (passive) — closest: (none exact); Bone skill mastery family
- `ossuary` Ossuary (passive) — closest: (none exact); Bone skill mastery family
- `elemwell` Elemental Well (passive) — closest: (none exact); elemental mastery family
- `sanctify` Sanctify (passive) — closest: (none exact); Sanctuary / holy mastery
- `wildheart` Wildheart (passive) — closest: (none exact); Druid shapeshift / HoW family
- `haste` Haste (passive) — closest: Burst of Speed / Increased Speed / Fanaticism
- `cleave` Cleave (passive, not Wide Cut) (passive) — closest: (none exact) — this is the Cleave *passive*, not Wide Cut
- `exec` Executioner (passive) — closest: (none exact)
- `needle` Needle (passive) — closest: (none exact)
- `serrate` Serrate (passive) — closest: (none exact)
- `cripple` Cripple (passive) — closest: (none exact); Slow Missiles as a loose cousin
- `trueflight` Trueflight (passive) — closest: Penetrate / Pierce / Critical Strike (Amazon)
- `tough` Toughness (passive) — closest: Iron Skin / Natural Resistance
- `ward` Ward (passive) — closest: Defiance / Energy Shield
- `aegis` Aegis (passive) — closest: Holy Shield / Defiance
- `focus` Focus (passive) — closest: (none exact)
- `alchemy` Alchemy (passive) — closest: (none exact)
- `wellspring` Wellspring (passive) — closest: Prayer / Meditation
- `greed` Greed (passive) — closest: (no skill — Gold Find is a D2 item modifier)
- `finder` Finder (passive) — closest: (no skill — Magic Find is a D2 item modifier)
- `recovery` Recovery (passive) — closest: Prayer / Cleansing / Meditation
- `fleetfoot` Fleetfoot (passive) — closest: Increased Speed / Burst of Speed
- `discipline` Discipline (passive) — closest: (none exact)
- `embers` Ember Orbit (passive) — closest: (none exact); Firestorm / Hydra / Armageddon as orbit/fire cousins
- `frostsat` Frost Satellite (passive) — closest: Frozen Orb / Hurricane (as a circling cold companion)
- `grit` Grit (Ironvow) (class passive) — closest: (none exact — Ironvow class passive)
- `stride` Stride (Longmark) (class passive) — closest: (none exact — Longmark class passive)
- `resonance` Resonance (Cinderwake) (class passive) — closest: (none exact — Cinderwake class passive)
- `toll` Toll (Gravewell) (class passive) — closest: (none exact — Gravewell class passive)

## Could not map to any D2 skill even loosely

None of the 51 rites were left without at least a closest D2 cousin. The following passives / class passives have **no useful D2 skill cousin** (they are stats, item-mod analogues, or class-only):

- `vit` Vitality (D2 stat, not a skill)
- `whetstone`, `cruor`, `reap`, `bloodthirst` (very loose at best)
- `marrow`, `ossuary`, `elemwell`, `sanctify`, `wildheart`, `focus`, `alchemy`, `discipline`, `exec`, `needle`, `serrate`
- `greed`, `finder` (D2 item modifiers, not skills)
- Class passives `grit`, `stride`, `resonance`, `toll`
- `bound_*` as a system (not one skill)

If Brian wants those visually tagged anyway, they should stay as icons / numbers, not travel FX.

## Not checked / not tested

- **NOT TESTED in the running game.** All live findings are from reading `/workspace/live14/routes-C2sLE0N3.js`. I did not launch the client or watch a cast.
- Exact metres for **every** nova / ground / aura / trap / melee shape (Inferno cone width, Consecrate decal, War Cry ring, etc.) were **not** measured one-by-one. The bolt-sphere and Heaven's Shrapnel paths were.
- `syncIcePops` / ice_shards instance scale: pack is loaded; per-shard world size **NOT CHECKED**.
- Orbiting passives (`hammer`, `embers`, `frostsat`) scale **NOT CHECKED**.
- Older live bundles (`/workspace/sanctuary/live_*`, `/workspace/live`, live11–13) were searched for `heavens_shrapnel` (none) but not re-audited for bolt radius (they may share the same `ug(.1,6,5)` pattern; **not re-verified** in each file).
- Canvas 2D `vfx_spec.md` describes Star Lash as a "small 4-point star sprite" — that is a different (2D) contract, also not our shard pack, and was not measured in a running 2D build.
