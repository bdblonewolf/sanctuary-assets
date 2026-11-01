# Sanctuary SFX Needs: Engine View
Written 2026-11-01 (America/Detroit). Source: `live_12c/r.js` (prettified `routes-CEphLWvJ.js`, 96,960 lines). Every `NNNNN` below is a line in that file unless it is tagged **now** (`/tmp/live_now/r_now.js`, the current live build `routes-qyJ9yETa.js`).
Minified names (`hl`, `dl`, `sl`…) change on every Vite build, so search by method name (`beast(`, `swish(`, `setMood(`…).
Tags: **unverified** means it is inferred and not read in code. **planned** means there is no code yet.

---

## 1. Engine summary

| Area | What the code does (verified) |
|---|---|
| Audio class | `hl` @32700, made once as `this.audio = new hl()` @77932. `unlock()` @32732 creates **one AudioContext with no `latencyHint`**. |
| Graph | master `n` (1, or 0 when muted) → `DynamicsCompressor` (thr −16 dB, knee 8, ratio 2.4, atk 4 ms, rel 180 ms) → destination @32737–32783. The **music** bus `r` (.82) → master feeds **town** `i`, **stone/wild** `a` and **dread** `u`, which all start at 0. The **sfx** bus `o` (1.0) → master. **Rain** `s` and **wind** `c` (start 0) → master. There is no reverb and no separate UI bus. |
| SFX source | **All SFX are synthesized** with oscillators, filtered noise from one cached 0.4 s buffer `noise()` @33186, and envelopes. **There are no SFX files.** `breath()` @33496 and `gate()` @33095 allocate a new buffer on every call. |
| Music source | **File-based Ogg.** `fetch` → `decodeAudioData`, decoding the whole file to PCM (`ll` @32061, returns null on failure). Loops start through `loop()` @32141. |
| Music path | `cl(e)` @32055 returns `/audio/${e}`, **same origin**. A host prefix (`Rl`, `i.js` 22090) applies only on preview hosts. **There is no `?v=` on audio and no raw-GitHub base for audio.** The raw-GitHub base `ps` @27631 with `?v=10a` is used only for models and textures. |
| Ogg/m4a | **None in live_12c.** **now** adds a town theme (`themeZones: town, cottage, taproom`, `town/martsirt_theme.ogg` with an **m4a fallback** picked with `canPlayType('audio/ogg; codecs="vorbis"')`, `themeBus` 1.4, loopStart/loopEnd) @**now**32019–32220. |
| Music manager | `dl` @32077: `ensure` 32098 → `wireTown` 32174 (stems guitar, nylon, pad, woodwind, clockwork; cimbalom is defined but unused), `humUnder` 32198 (synth bass), `wireWild` 32248 (`wild/drone .62, hollow .5, metal .38` → **stone** bus), `wireDread` 32253 (`dread/overworld.ogg`), `loadVoices` 32256 (6 male and 6 female NPC voice oggs). `setZone(e,t)` 32106 crossfades over 2 s between **town, stone and dread only**. `speak` 32123 hard-stops the previous voice. |
| Mood routing | Per frame @81073–81088: `setMood(town ? 'town' : stoneSet ? 'stone' : 'dread')`. See §6. |
| SFX API → call sites | `swish(heavy)` 32994: foe quirk jab 83021, foe swing 83139, foe lunge/charge 83309/83349, player swing 84159 (heavy for axe or mace), amazon ally 85572/85598. `hit(kind,g)` 33157 → `flesh` 33196, `cling` 33227, `heavy` 33242, `plate`, `crunch` 33290, `contact` 33320: player hits foe via `feel()` 84567–84594 (called 81847, 83937, 83983, 88187); player hurt 83733 (kind from `AD()` 91530). `beast(kind, attacking)` 32911 (7 synth groups): foe damaged 84957 (`false`), foe hits player 83734 (`true`). `ching()` 33348: shield block 83682. `rite(key,g)` 33027 + cue table `pl` 32282–32696 (51 keys; unknown keys fall back to a default cue): cast 88324. `levelHum()` 33381: level up 85624. `organ()` 33419: organ prop 90205. `tune()` 32891: near Bram 86589/87122. `greet(name)` 33450 (sample voice, else synth `hum`/`hey`/`hello`): 79234, 79906, 90621. `gate()` 33095: start knock 78324. `setGale`/`setGasp`/`gasp` 32828–32854: intro 90464–90695. `setWeather` 32880 (rain ≤.34, fog→wind ≤.22): 81096–81100. `slash()` 33259 is **dead code**. |
| Throttles | `swish` ≤3 per 90 ms. `rite` ≤3 per 120 ms. `hit` ≤4 per 80 ms with a 28 ms stagger. `beast` passes 50% at random and has a 240 ms gap. `organ` 700 ms. `tickGasp` 3.2 s. |
| Voice limit | **There is no global voice cap or voice stealing.** Only the per-type throttles above limit concurrency. |
| Silent today | Every loot, gold, pickup, equip, stash, UI, door, chest, shrine, potion, quest, vendor, gamble, Boss Stone, foe death, player death, miss/dodge and footstep event. |

---

## 2. P0: ship first (core loop, read every few seconds, or carries gameplay information)
Columns: **Freq** = how often it fires (H several per 10 s, M per minute, L per zone). **Var** = recorded variants. **Max** = longest variant in ms. **Prio** = 1 (never steal) to 4 (steal first).

| # | Event | Trigger (live_12c r.js) | Freq | Var | Max ms | Loudness / priority |
|---|---|---|---|---|---|---|
| P0-01 | Loot drop: common/uncommon (magic) | `drop()` 85281 from `reward()` 85123–85211 and containers; tier from item rarity (`MD` ~91545) | H | 3 | 350 | −20 LUFS-S; prio 3 |
| P0-02 | Loot drop: rare | same; rarity `rare` | M | 2 | 700 | −16; prio 2; distinct pitch |
| P0-03 | Loot drop: epic/legendary/boss/`doom` | same; `Va(...,'boss'|'doom'|'king')` | L | 2 | 1500 | −14; prio 1; must cut through combat |
| P0-04 | Gold spill (drop) | `spillGold()` 85297 | M | 3 | 500 | −20; prio 3 |
| P0-05 | Gold pickup | loot loop 81932, `r.gold` branch 81937 | H | 4 | 300 | −22; prio 3; random pitch ±3% |
| P0-06 | Item pickup → pack | loot loop `stow()` 81939 (`stow` 79141) | H | 3 by weight (light/armor/weapon) | 300 | −22; prio 3 |
| P0-07 | Pack full / deny (UI error) | `say('Pack full')` 81946, `No room there` 78585, `Not enough mana` 78666/87794, `Not enough gold` 78920, `Need … gold` 78633 | M | 2 | 250 | −24; UI; throttle 400 ms |
| P0-08 | Equip / unequip by slot class | `equip()` 78995, `unequip()` 78566; classes weapon/armor/helm/shield/ring/amulet/belt/gloves | M | 6 classes × 2 | 500 | −20; UI |
| P0-09 | Footsteps: player, 4 core surfaces | **planned**; no step code. Tiles `W` 25775: Grass/Grass2, Dirt/Road, Stone/Plaza/Cave, Plank/Bridge | H (~2–3/s) | 4 surfaces × 6 | 250 | −28; prio 4; per-step stealable |
| P0-10 | Player weapon swing by class | `swish()` 84159 (synth, light/heavy only); classes blade, axe/mace, bow (`armKind()` bow/wand), wand/staff | H | 4 classes × 4 | 350 | −20; prio 3; replaces synth |
| P0-11 | Weapon impact by target material | `feel()` 84567–84594 → `hit(a)`: flesh, cling (bone), heavy, plate, contact (ghost) | H | 5 × 4 | 400 | −16; prio 2; keep the 28 ms stagger |
| P0-12 | Player hurt (impact + grunt) | `suffer()` 83661 → `hit(AD(kind))` 83733 | H | impact reuses P0-11; grunt 4 per class | 600 | −16; prio 1 |
| P0-13 | Player death | `suffer()` `mode='dead'` ~83833 | L | 2 | 3000 | −14; prio 1; duck music |
| P0-14 | Low-health warning (heartbeat loop) | **planned**; no audio hook. Proposed condition hp/maxHp < .3 (**unverified** design value) | M | 1 loop | 1200 loop | −22; prio 1; must not mask combat |
| P0-15 | Foe death per family | `hurtEnemy()` 84841, `e.hp<=0` 84984 (silent today). Families: heavy (zombie, corpse, brute, bear, worm), skeleton, ghost/wraith, small (imp, raver, critters), snake, caller, boss kinds | H | 6 × 3 | 1200 | −18; prio 2; limit to 3 at once |
| P0-16 | Foe hurt / attack vocal per family | `beast(kind, false)` 84957; `beast(kind, true)` 83734 (synth, 7 groups) | H | 7 × 2 types × 3 | 700 | −20; prio 3; keep the 240 ms gap |
| P0-17 | Rite impact by damage type | `hurtEnemy(e,t,n)` 84841 where `n` ∈ phys/fire/cold/magic(lightning)/poison; only `beast` sounds today | H | 5 × 3 | 500 | −18; prio 2; layered under the synth cast |
| P0-18 | Potion drink (health/mana) | `sip()` 79185, health 79198, mana ~79205; `takeSip` 79170 | M | 2 types × 2 | 800 | −18; prio 2 |
| P0-19 | Chest / tomb / body open | `interact()` → `crack()` 85320; chest 89914/89946, crypt tomb 89895, `super` chest 89914 | M | chest 3, tomb slab 2, body 2 | 1200 | −18; prio 2 |
| P0-20 | Crate / log break; barrel stave and barrel explode | crate/log 90025–90059; barrel 90060–90107; explode (`fire` 72% / 22%) 90085 | M | crate 3, barrel 2, explode 2 | 1500 | explode −12, prio 1 |
| P0-21 | Shrine activate (shared base) | `interact` 90188 → `takeShrine(style)` 85931 | L | 2 | 1500 | −16; prio 1 |
| P0-22 | Level up | `checkLevel()` 85606 → `levelHum()` 85624 (synth) | L | 1 | 2500 | −14; prio 1; replace the synth |
| P0-23 | Zone transition: door / stairs / arch | `enter()` 80077 via `interact` 89695, 90171, 90180, 90225 | M | wood door 2, stone stair 2, arch 2 | 1200 | −20; prio 2 |
| P0-24 | Boss telegraph wind-up | `commitBoss()` 82346: generic 82386, `summon` 82397, player-target 82441, `shift`/PHASE ~82358 | M in fights | 4 kinds × 2 | 1500 | −14; prio 1; gameplay critical |
| P0-25 | Boss death sting | `onBossFall()` 82221 (and `reward` boss branches 85122–85190) | L | 2 | 4000 | −12; prio 1; duck music 6 dB |
| P0-26 | UI: panel open/close, button click | `setMenu()` 78363; panel toggles (**unverified** exact handler) | H | open 2, close 2, click 3 | 200 | −26; UI bus, never stolen |
| P0-27 | Vendor buy / sell (coin) | `buy()` 78609, `sell()` 78587 | M | 2 + 2 | 400 | −20; UI |

**P0 total: 27 events.**

---

## 3. P1: next wave

| # | Event | Trigger | Freq | Var | Max ms | Loudness / priority |
|---|---|---|---|---|---|---|
| P1-01 | Footsteps: extra surfaces | **planned**: Sand/Sand2, Water/shallow, Rug, Blood; 3D `BT()` ~72459 ash, mud, frost (winter overlay) | H | 6 × 4 | 250 | −28; prio 4 |
| P1-02 | Foe footsteps (heavy families only) | **planned**: bear, brute, king, worm (burrow move) | M | 4 × 3 | 300 | −30; prio 4 |
| P1-03 | Miss / dodge / veil | DODGE/VEIL/MISS floats 83672–83684 (silent) | H | 3 | 250 | −24; prio 4 |
| P1-04 | Block | `ching()` 83682 (synth) → shield wood/metal | M | 2 × 3 | 400 | −18; prio 2 |
| P1-05 | Inventory / stash move (grid drop) | `moveItem()` 78578; stash open 89835 (`setMenu stash`) | M | 3 | 250 | −26; UI |
| P1-06 | Shrine type tails | `takeShrine` 85931: angel, curse, speed, lightning, xp, might, fire, cold, magic (resist fallthrough) | L | 9 × 1 | 2000 | −16 |
| P1-07 | Healing well | `interact` well `heal` 90109 | L | 1 | 1500 | −18 |
| P1-08 | Quest accept / complete | `acceptQuest()` 89246; `claimQuest()` 79590 | L | 1 + 2 | 2500 | −16; duck music |
| P1-09 | Town Portal Scroll | item `portal` defined 25009; use path **unverified** | L | open 1, travel 1 | 2000 | −16 |
| P1-10 | Gamble reveal | `gamble()` 78910 → reuse the P0-01…03 tier stings plus a dice/cloth layer | M | 2 | 1200 | −18; UI |
| P1-11 | Boss Stones | `openStone()` 82176, `confirmStone()` 78861, `sellStone()` 78873, `finishStone()` 82189 | L | 4 | 2500 | −16 |
| P1-12 | Rite cast layers by school | `rite()` 33027 + `pl` 32282: schools fire, cold, lightning, holy, bone, blood, mind, nature, steel, guard | H | 10 × 2 (layered on the synth) | 1200 | −18; prio 2 |
| P1-13 | Aura toggle | `toggleAura()` 78652 | L | 2 | 800 | −20 |
| P1-14 | Elite pack spawn/aggro sting | `rollPack()` 80492 (packs `magic`/`rare`, mods Fleet…Caustic) | M | 2 | 1500 | −18; prio 2 |
| P1-15 | Elite aura loops | aura set 80728–80744 (`might`, `fanatic`, `fire`, `cold`, `shock`); tick `tickFoeAuras` 83567 | M | 5 loops | 3000 loop | −26; positional |
| P1-16 | Foe aggro bark per family | **planned**; no aggro hook found (**unverified**) | M | 7 × 2 | 900 | −22; prio 3 |
| P1-17 | Foe quirks: leap, spit, burrow/emerge, snake HISS ambush | quirk roll 80624–80645; HISS float 82512 (silent); burrow 38733 | M | 4 × 2 | 1000 | −18; prio 2 |
| P1-18 | Foe swing whoosh (replace synth) | `swish()` 83139 (heavy for bear, brute, king, zombie, corpse, worm), 83309/83349 | H | 2 × 3 | 350 | −24; prio 3 |
| P1-19 | Ambient bed: forest (`trees`) | zone type `Eo()` 25807; bed **planned** | loop | 1 + day/night | 60 s loop | −30 bed bus |
| P1-20 | Ambient bed: desert/waste (`gap`) | `Eo()` 25807 | loop | 1 | 60 s | −30 |
| P1-21 | Ambient bed: cave (`cave`) | `Eo()` 25807 (den, root, sink, crypts, chasm, hollow, gaol, vault) | loop | 1 | 60 s | −30 |
| P1-22 | Ambient bed: stone/church interior | `Eo()` 25807 (default `stone`) | loop | 1 | 60 s | −30 |
| P1-23 | Ambient bed: coast/sea | sea ring table `RT` ~72440 (wild W, isle, coast, mires, flotsam) | loop | 1 | 60 s | −30 |
| P1-24 | Rain bed (replace the noise loop) | `tickWeather()` 80847; `setWeather` 32880; hard rain 12% 80860 | loop | light + hard | 60 s | −26 |
| P1-25 | New loot containers (props_gothic_v1, 11) | **planned**: bone_pile, skull_heap, burial_urn, sarcophagus_small, sack_pile, remains_heap, rubble_cache, rock_pile, hollow_log, rotten_stump, weapon_rack_wreck (open state swap) | M | 11 × 2 | 1200 | −18; reuse P0-19/20 where close |
| P1-26 | Root cache gold seam | `openCache()` 85326 | L | 1 | 1500 | −16 |
| P1-27 | King death → ascend | `ascend()` 85246 | L | 1 | 4000 | −12 |
| P1-28 | Boss intro / phase shift | `tuneBoss()` 82264; `shift` 82358 | L | 2 | 3000 | −14 |
| P1-29 | Sealed door / locked hatch rattle | sealed arch 90135; deep stairs 90142; trap hatch 90149 | L | 2 | 800 | −20 |

**P1 total: 29 events.**

---

## 4. P2: later / planned stages

| # | Event | Trigger | Freq | Var | Max ms | Loudness / priority |
|---|---|---|---|---|---|---|
| P2-01 | Thunder | **planned** (hard rain 80860 is a natural hook) | L | 4 | 6000 | −16; far/near |
| P2-02 | Fog bed | `fogFor`/`fogThick` ~80866 (today the wind noise is ≤.22) | loop | 1 | 60 s | −32 |
| P2-03 | Birds (day) / insects (night, summer–autumn) | **planned**; night from `isNight()` 79839, phase `phaseId()` 80756 | loop + one-shots | 2 beds + 8 one-shots | 60 s / 1500 | −32 |
| P2-04 | Winter wind bed | zones `iron`, `ascent` (winter frost overlay) | loop | 1 | 60 s | −30 |
| P2-05 | Boat creaks + oars (ferry ride) | **planned**: `boat_longship_ride_v1`; today `interact` boat 89799 → ferry NPC | loop | creak 1 + oar 4 | 60 s / 900 | −26 |
| P2-06 | Wreck / hull board and leave | `boardWreck()` 85840, `leaveHull()` 85851 | L | 2 | 2000 | −20 |
| P2-07 | Angel presence | **planned** (LORE_ANGELS); hook: angel shrine `takeShrine('angel')` ~85933 | L | 1 loop + 2 | 8000 | −24 |
| P2-08 | Faction events (witness/regard) | `witness('theft')` 89952, `witness('aid')` 85216, `noteRegard()` (from `sell`/`gamble`) | L | 3 | 1500 | −22 |
| P2-09 | NPC/vendor extras (shop open, idle barks) | `setMenu({kind:'shop'})` (**unverified** line); `greet` 33450 already plays voices | M | 2 per vendor | 1500 | voice bus .7 |
| P2-10 | Folio / sign / book read (page turn) | folio 89827, plea 89819, bookshelf 89961, chart 89978 | L | 3 | 600 | −24; UI |
| P2-11 | Bed rest / sit | bed 89971 → `sleepHours()` 85888; `sitAt()` 85366 | L | 2 | 2000 | −24 |
| P2-12 | Bonfire / town pyre crackle (positional) | bonfire 89843; `setFire()` (music delay only); `townPyre()` 86650 | loop | 2 | 30 s | −24 (see SFX_NEEDS_ENVIRONMENT.md) |
| P2-13 | Waypoint / fast travel | no waypoint in live_12c; `travelBed()` 89557, chart menu 89980 (**unverified** as travel) | L | 2 | 2000 | −18 |
| P2-14 | On-kill explode | `i.explode` "BOOM" 85219 | M | 2 | 800 | −16 |
| P2-15 | Servant raise / gravity well | `raiseServant` 84992, `gravityWell` 84997 | M | 2 | 1200 | −20 |
| P2-16 | Critters (rabbit, rat, deer, crow) idle/flee | `fD` 77108 critters | M | 4 × 2 | 800 | −30 |

**P2 total: 16 events.**  **Grand total: 72 events** (27 / 29 / 16).

---

## 5. Tech recommendation: hybrid (files for the content, synth for rites and fallback)

| Factor | Synth (today) | Ogg files | Verdict |
|---|---|---|---|
| Android CPU | Each hit/rite builds 3–8 nodes with filters; it gets heavy in packs, and `breath()`/`gate()` allocate on every call | One `AudioBufferSourceNode` + gain per voice; cheapest at play time | Files are lighter per voice |
| Bundle / fetch | ~0 KB | ~150 sounds × ~10–25 KB (mono Vorbis q3, 22–44 kHz) ≈ 2–3 MB total, lazily loaded | Fine if loaded per group |
| Decode cost | none | `decodeAudioData` turns everything into PCM in RAM (≈88 KB per s mono at 44.1 kHz in float32) | Short SFX are cheap; decode once at load, never per play |
| Concurrency | No cap; only per-type throttles | Same risk | **Add a voice manager**: cap ~24 SFX voices (16 on low `deviceMemory`, **unverified** threshold), prio 1–4 from the tables, steal the oldest lowest-priority voice |
| Sprites vs files | n/a | Sprites cut requests but force one big decode and make variant edits painful | **Individual files per group, preloaded per zone/class**; HTTP/2 makes many small files fine |
| Ogg + m4a | n/a | iOS/older Safari Vorbis support is the risk | Use the **now** pattern: `canPlayType('audio/ogg; codecs="vorbis"')` → `.ogg`, else a `.m4a` (AAC-LC) twin with the same name |

**Recommendation:** keep the synth `rite()` cues (51 keys, already tuned) and keep synth as the fallback when a file is missing or `ll()` returns null. Ship Ogg files (with m4a twins) for everything in P0/P1 that is a physical sound: loot, gold, hits, deaths, footsteps, UI, containers, ambience. Add a small voice manager and a separate **UI bus** and **ambience bus**, create the AudioContext with `latencyHint: 'playback'` on mobile (**unverified** improvement; see AUDIO_CHOPPY_INVESTIGATION.md), and keep the master compressor gentle so it does not pump.

**File specs (proposal):**
- 44.1 kHz (22.05 kHz is fine for ambience beds and footsteps, matching today's existing files), **mono** for all positional and one-shot SFX, **stereo** only for ambience beds and stingers.
- Ogg Vorbis q3–q4 plus an AAC-LC 96–128 kbps m4a twin.
- One-shots peak at ≤ −1 dBTP, normalized to the per-row LUFS-S target above (short-term, measured over the full sound). Beds at about −30 LUFS-I. No baked reverb on footsteps or impacts. Trim silence to <5 ms at the head; fade out over 10 ms.
- Naming: `audio/sfx/<group>/<name>_<nn>.ogg` (and `.m4a`), lower_snake, `nn` = 01…, e.g. `audio/sfx/loot/drop_rare_02.ogg`, `audio/sfx/foot/stone_04.ogg`, `audio/sfx/foe/skeleton_death_01.ogg`.
- Folders: `audio/sfx/{loot,gold,item,ui,foot,weapon,impact,player,foe,boss,rite,potion,shrine,container,door,quest,vendor,weather,amb,boat}/`, plus `audio/amb/<zone_type>.ogg` for beds.
- Served same-origin under `/audio/` like the music (not raw GitHub). Add a `?v=` build tag for cache busting (**unverified** whether the host caches `/audio/` aggressively).
- Assumptions: the variant counts and LUFS targets are design proposals, not code facts. The hp<30% low-health threshold and the voice-cap numbers are unverified.

---

## 6. Crypt theme routing (list only)

Asset: `/workspace/sanctuary_audio/release/audio/dungeon/crypt_theme.ogg` (44.1 kHz stereo, 233 s, 1.47 MB). It is approved for crypts, basements, cellars, church dungeons and hostile interiors.

**Bug cause (verified):** the mood expression @81073–81088 sends `crypts`, `nave`, `church*` and `castle*` to **`stone`**, and `stone` is the bus that `wireWild()` 32248 fills with the **`wild/drone`, `wild/hollow` and `wild/metal`** stems. Every other hostile interior falls through to **`dread`** = `dread/overworld.ogg` (the outdoor overworld loop). In **now** the same expression is @81713–81735; it also calls `setPlace(n)` (**now** 32900, which only stores `this.place`), and `dl.setZone(e,t,n='')` @**now**32121 takes the zone id but only uses it for the town theme.

| Zone id | Name | Interior? (`Bl` 33625) | Current music | Should get crypt theme? |
|---|---|---|---|---|
| crypts | Sunken Crypts | yes | stone (wild/* stems) | **Yes** |
| church1 | Church L1 | yes | stone (wild/*) | **Yes** |
| church2 | Basement | yes | stone (wild/*) | **Yes** |
| nave | The Sealed Nave | yes | stone (wild/*) | **Yes** |
| castle1–castle4 | Gate Hall … The Castellan | yes | stone (wild/*) | Yes, as a hostile interior (**unverified** design intent; could keep its own theme) |
| sewer | The Salt Cellar | yes | dread overworld | **Yes** (cellar) |
| den | Den | yes | dread overworld | **Yes** |
| vault | Black Vault | yes | dread overworld | **Yes** |
| gaol | Inquisitor's Gaol | yes | dread overworld | **Yes** |
| hollow | Smuggler's Hollow | yes | dread overworld | **Yes** |
| chasm | Drowned Chasm | yes | dread overworld | **Yes** |
| sink | The Putrid Sink | yes | dread overworld | **Yes** |
| hull | Split Hull | yes | dread overworld | **Yes** |
| root | Blackroot Cavern | **no** (in `Us` 28149 and `Eo` 25807 cave list, not in `Bl`) | dread overworld | **Yes** |
| undercroft | Highmarket Undercroft | **no** (level table `lc` 28918; side door from `market` 28956) | dread overworld | **Yes** |
| antechamber, stacks | Vault Antechamber, Unread Stacks | no | dread overworld | **Yes** (church-type) |
| choir, reliquary, fontnave, ashfont, mirth, tallyden, wealdedge | boss / side rooms (`pc` 28952–28972) | no | dread overworld | Yes (church-type interiors); boss rooms may get a boss cue later (**unverified** intent) |
| tideclock, tallow, tollcourt, hollowstar, scriptorium, lastpage, uberysmer, uberbind | Margins / Ubers | no | dread overworld | Optional (**unverified** intent) |
| cottage, taproom, inn, house | town interiors | yes | town | **No**: keep town / town theme |

**Routing code to change:**
- The mood expression @81073–81088 (**now** 81713–81735): add a `crypt` mood for the zone list above. `Bl()` 33625 is close to the right predicate, but it includes the town interiors and misses root, undercroft and the church-type rooms.
- `dl.setZone()` 32106 (**now** 32121): it only knows town/stone/dread; it needs a crypt bus.
- `wireWild()` 32248 and the graph in `unlock()` 32737–32783 need a new music-bus gain; the stem config is `sl` 32000–32054 (**now** `q` 32019+).
- `cl()` 32055 builds the path `/audio/dungeon/crypt_theme.ogg`. Note that the release folder also renames dread to `dread/overworld_theme.ogg`, while the code still loads `dread/overworld.ogg`.
