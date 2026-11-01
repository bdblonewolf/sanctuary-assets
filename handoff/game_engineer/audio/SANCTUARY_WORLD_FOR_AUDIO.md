# Sanctuary: world brief for the sound designer

Compiled 2026-11-01 (America/Detroit). Everything below comes from the live bundle (`index-3hCT99Bp.js` / `routes-_LaUNfst.js`, unchanged on 2026-11-01), the docs in `/workspace/sanctuary*`, and the live audio files (probed with ffmpeg). **[?]** marks something uncertain. **[REC]** marks a recommendation, not an existing fact.

- Game: https://gold-iris-zippy-bird.grok.me. A Vite + React + Three.js single-page app. Brian edits it through Grok Build.
- Beautified bundle with line refs: `/workspace/sanctuary/live/routes.pretty.js`.
- Reference copies of every live audio file: `/workspace/sanctuary/audio/live_files/`.

---

## 1. Tone, story, acts, cast

### Tone and style
- Diablo 1/2 Act I feel. Realistic, battle-worn, archaic gothic. **Never cartoony.**
- Palette: charcoal, wet stone, rust, bone. Torch-orange against moonlit blue-grey. The town is the only warm-lit place (D1 trick). Dungeons should get a tight light radius.
- Story bible tone: "Bleak, grounded, terse, dread." Horror comes from specific details, not adjectives.
- The D1 study's lessons, which Brian approved on 2026-11-01 (DESIGN_NOTES):
  - A Tristram-style mood theme for Martsirt: a sparse, looping acoustic piece that "never goes anywhere".
  - A distinct **loot-drop sound for each tier**.
  - **Several death and hit-react variants per family.**
- No audio or music direction doc exists yet. This brief is the first.

### Premise
- A parish burned its register of the drowned. The copyist **Ysmer** then wrote every name into a book bound in his own skin: **the Warm Binding**.
- The book rewrites whatever it reads. The dead come home "wrong", and the living start to sound like the page.
- The player crawled out of a lost battle at the north trench with their name burned away, so the book can't read them.
- Theme: what we owe the dead. Every survivor clings to one object (shoes, key, ledger, bell, ribbon, lamp).
- Difficulty is part of the story:
  - Normal: the book is reading.
  - Nightmare: it has read you.
  - Hell: you walk in "the Margins".

### Acts (story bible §3, study §1)
| Act | Hub | Act boss |
|---|---|---|
| I | Martsirt | Vessaline, the Thorn Abbess (Thorn Choir, poison) |
| II | Qadren (desert; reached via Holt's skiff across Blackwater) | Ossgrind, the Reliquary Grub (Dry Reliquary, cold) |
| III "Coast road" (south gate) | Bastion of Hope (field camp) | Inquisitor Halvane (Inquisitor's Gaol, lightning) |
| IV | Highmarket (Lampwick Inn) | Vhorr-Akesh, the Ember Saint (Ashen Font, fire) |
| V | none named [?] | Ysmer, Who Wrote the Plague (Unread Stacks, "magic") |
| Hell | the Margins | Pinnacle: the Warm Binding (The Last Page) |

- [?] The Act III coast zones start at area level 1–3, so they work as a parallel side road. Brian hasn't confirmed this.

### NPCs (name: role, voice register from `story/data/voices.json`)
- **Martsirt**
  - Wolchen: smith, gruff workman
  - Ysara: healer, clinical
  - **Ilyra**: gate herald. The only archaic (KJV) speaker by canon.
  - Quill: scribe, anxious scholar
  - Bram: logger, few words. Plays a flute (see `tune()`).
- **Martsirt taproom**: Mira (innkeeper, teasing), Orrin (drunk ex-bell-ringer), Ness (homesick widow)
- **Briarwood**: Holt (deadpan ferryman), Myrine (grieving spear-hand), Orithya (ex-citadel scout), Sable (sly merchant)
- **Coast road**
  - Wynn (gravedigger), Rusk (captain), Sera (mud surgeon), Odder (young smith), Iskra (cliff widow)
  - Moth (fen proverbs), Calder, Hask and Kell (toll grandsons), Nim (coward wit)
  - Vellum (crypt warden), Lute (frightened diver), Brine (lamp-keeper), Jas (smuggler accountant), Piet (ex-gaoler)
  - Ors (unfrocked priest, liturgy quotes)
- **Qadren**: Orlem (headman), Heska (guard), Vetch (gambler). **Salt House**: Tamsin (cook-innkeeper).
- **Highmarket**: Cal (parts buyer), Pell (gate-crier). **Lampwick Inn**: Hesta, Voss, Ilen.
- **Cinder Barrens**: Sarn (camp boss). **Under the castle**: Vesper (fence).
- [?] The canon says only Ilyra speaks archaically, but many live NPC lines still use "thou" or "-eth" (Orlem, Ness, Voss, Nim, Tamsin). Don't lock VO style to the live text. The bible wins.

---

## 2. Locations

### How areas are typed and moods chosen
- Size is in tiles (1 tile ≈ 1 m in 3D). Data comes from a live probe on 2026-11-01 (`probe/zones_now.json`).
- Season (table `GT`):
  - winter: iron, ascent
  - autumn: tollarch
  - "dead": waste, ashcamps, coast, spireroots, weald
  - summer: everything else
- Type sets in code:
  - **Town** (UT/KT): town, lut, market, cottage, taproom, inn, house, bastion
  - **Cave dungeons** (qT): den, vault, root, sink, crypts, chasm, hollow, gaol, hull, sewer, undercroft
  - **Church-type** (JT): nave, reliquary, fontnave, ashfont, antechamber, stacks, choir, tallyden, mirth, tideclock, tallow, tollcourt, hollowstar, scriptorium, lastpage, uberysmer, uberbind, wealdedge, plus church\* and castle\*
  - **Outdoor**: everything else
- **Music mood** (code line 54612) is not the same as type:
  - `town`: the town set above
  - `stone`: crypts, nave, church\*, castle\*
  - `dread`: **all other areas**, including outdoors, caves and all the other JT boss rooms
- Sea sides (from the Stage 12B ring/sea table, **pending, not live yet**):
  - wild: W
  - coast: E/W/S
  - flotsam: N
  - isle and mires: all sides
  - all others: none

### Area list
| id | Display name | Size | Season | Type / mood | Foes (live probe) | NPCs |
|---|---|---|---|---|---|---|
| town | Martsirt | 2D 40x34; **3D 162x154** | summer | town | none | Wolchen, Ysara, Ilyra, Quill, Bram |
| cottage | Cottage | 16x13 | summer | town interior | none | none |
| taproom | Taproom | 16x13 | summer | town interior | none | Mira, Orrin, Ness |
| wild | Briarwood | 72x56 | summer | outdoor/dread, sea W* | imp, bear, snake, raver, ghost, zombie, caller, **Melakirniz** (boss) | Holt, Myrine, Orithya, Sable |
| briarE | Briarwood East | 52x40 | summer | outdoor | imp, snake, raver | none |
| duneW | The Narrow | 28x16 | summer | outdoor | brute, imp | none |
| desert | Desert | 36x30 | summer | outdoor | worm, ghost, brute | none |
| lut | Qadren | 30x24 | summer | town | none | Orlem, Heska, Vetch |
| house | Salt House | 16x13 | summer | town interior | none | Tamsin |
| reliquary | Dry Reliquary | 22x18 | summer | church-type/dread | **Ossgrind** (worm boss) | none |
| isle | Blackwater | 44x36 (**96x80 pending**) | summer | outdoor, sea all sides* | skeleton, caller, zombie, brute, ghost | Holt |
| market | Highmarket | 48x40 | summer | town | caller, imp, skeleton, ghost, brute [?] | Cal, Pell |
| inn | Lampwick Inn | 16x13 | summer | town interior | none | Hesta, Voss, Ilen |
| undercroft | Highmarket Undercroft | 22x18 | summer | cave/dread | skeleton | none |
| waste | Cinder Barrens | 50x42 | dead | outdoor | brute (14), raver, caller | Sarn |
| ashcamps | Ash-Camp Ruins | 22x18 | dead | outdoor | raver | none |
| fontnave | Ashen Font, Upper Nave | 22x18 | summer | church-type/dread | caller | none |
| ashfont | The Ashen Font | 22x18 | summer | church-type/dread | **Vhorr-Akesh** | none |
| vault | Black Vault | 34x36 | summer | cave/dread | ghost, corpse, skeleton, caller, **Hollow King** | none |
| den | Den | 30x24 | summer | cave/dread | skeleton, zombie, corpse | none |
| church1 | Church L1 | 26x22 | summer | stone | zombie, skeleton (has the **organ** prop) | none |
| church2 | Basement | 26x22 | summer | stone | skeleton (18) | none |
| choir | The Thorn Choir | 22x18 | summer | church-type/dread | **Vessaline** | none |
| root | Blackroot Cavern | 22x16 | summer | cave/dread | bear, **Scar-Eye** | none |
| sewer | The Salt Cellar | 29x21 | summer | cave/dread | 38 zombies plus **Saltmouth** | none |
| nave | The Sealed Nave | 28x22 | summer | stone | none | none |
| castle1 | Gate Hall | 34x30 | summer | stone | imp (19) | none |
| castle2 | Burning Gallery | 34x30 | summer | stone | ghost, imp, raver | none |
| castle3 | The Fence's Floor | 34x30 | summer | stone | ghost, caller, brute | Vesper |
| castle4 | The Castellan | 34x30 | summer | stone | brute (16), **The Castellan** | none |
| antechamber | Vault Antechamber | 22x18 | summer | church-type/dread | skeleton | none |
| stacks | Unread Stacks | 22x18 | summer | church-type/dread | **Ysmer** | none |
| coast | Ashen Coast | 42x56 | dead | outdoor, sea E/W/S* | zombie, corpse | Wynn |
| hull | Split Hull | 14x11 | summer | cave/dread | corpse, **Bilge-Wight** | none |
| bastion | Bastion of Hope | 34x28 | summer | town | none | Rusk, Sera, Odder |
| bluffs | Mourning Bluffs | 52x44 | summer | outdoor | skeleton, imp | Iskra |
| mires | Silt Mires | 40x34 | summer | outdoor, sea all sides* | corpse, snake | Moth |
| sink | The Putrid Sink | 28x24 | summer | cave/dread | worm | Calder |
| ridge | Razor Ridge | 44x46 | summer | outdoor | brute (14), skeleton, bear | Hask |
| ascent | Bitter Ascent | 32x30 | **winter** | outdoor | imp, raver | Nim |
| mirth | The Laugh That Stays | 22x18 | summer | church-type/dread | **Ghel** | none |
| crypts | Sunken Crypts | 34x28 | summer | stone | ghost, caller | Vellum |
| chasm | Drowned Chasm | 26x28 | summer | cave/dread | corpse, ghost | Lute |
| iron | Iron Bastion Pass | 38x24 | **winter** | outdoor | skeleton, zombie | Kell |
| tollarch | Toll Arch | 22x18 | **autumn** | outdoor | **Kessane** | none |
| flotsam | Bleak Flotsam | 36x28 | summer | outdoor, sea N* | ghost, corpse | Brine |
| hollow | Smuggler's Hollow | 26x22 | summer | cave/dread | imp | Jas |
| tallyden | The Tallyman's Den | 22x18 | summer | church-type/dread | **Tallyman** | none |
| gaol | Inquisitor's Gaol | 32x42 | summer | cave/dread (has an organ) | corpse, brute, **Halvane** | Piet |
| weald | Obsidian Spires | 44x40 | dead | outdoor | skeleton, zombie, snake, **Spire-Heart → Goreth-Vaal** | Ors |
| wealdedge | The Weald Edge | 22x18 | summer | church-type/dread | snake | none |
| spireroots | Spire Roots | 22x18 | dead | outdoor | worm | none |
| Margins (Hell) | tideclock, tallow, tollcourt, hollowstar, scriptorium, lastpage | 22x18 each | summer | church-type/dread | Bell-Wright, Mother Wick, Assessor, Nul-Osse, Errata, Warm Binding | none |
| Ubers | uberysmer "Ysmer Unbound", uberbind "The Unbinding" | 22x18 | summer | church-type/dread | the uber bosses | none |

\* Sea sides come from Stage 12B, which is pending. [?] The 22x18 rooms are generic boss or side rooms and may change.

### Martsirt in detail (3D v2.2)
Sources: `martsirt_world.json` and `placements.json` from the assets repo.
- **Grid and lights**
  - The grid is 162x154 m. A north road leads to Briarwood.
  - There are 36 light anchors: 11 fires (main bonfire, gate campfire, hearths, forge fire, gatehouse and watch-house braziers) and 25 lit windows, door glows and wall torches. There are no lamp posts.
- **Buildings**
  - Salted Kettle inn and Wolchen's Forge
  - Chapel of St. Noll (with a tower), Graveyard, and the **Weeping Angel shrine** beside the graveyard (tile ~124,48)
  - Ysara's herbs and Quill's scriptorium
  - South gatehouse (Ilyra), with curtain walls
  - **Miller's house + water wheel** (it rotates about 0.15 rad/s)
  - Ness's cottage, Orrin's lodge, Stable + yard
  - **Watch-house + gibbet**
  - Town square with a **bonfire** and market stall
  - 111 palisade pieces
- **Water**: a **creek** runs 144 tiles from the NW palisade culvert to the mill flume. There's a walkable plank footbridge on the forge road.
- **Exits**: Briarwood (N), Church (chapel, NE), "ACT I" south gate to the Ashen Coast, Castle, Cottage, Taproom. The 2D map also exits to tideclock and uberysmer (Hell/uber portals).
- **Salt statues**: Noll's flock turned to salt are canon set dressing.
- [?] The town's bonfire has `fuel`. The 2D map also has an ash bonfire, a well, an anvil barrel, benches and logs.

### The ferry and the isle
- Holt (role `ferry`) stands in Briarwood and on Blackwater. The fare is **10,000 gold** ("Lake doesn't haggle").
- Stage 12B (**pending**) changes the isle:
  - 96x80 with a landing bay, a pier and the boat at (48.5, 76.15)
  - a bonfire at (48.5, 67.4); the arrival point is (48.5, 72.2)
  - ocean, foam strips and shore rocks around every ring
  - Briarwood also gets a weeping angel statue at (24, 22)

---

## 3. Enemies, AI, bosses

### Families and AI types
Family roster and variant names are from the art-direction docs and family sheets in `/workspace/sanctuary_art/monsters/families/` [?] (the lock date is unconfirmed). Every family has a physical and an elemental variant.

| code kind | in-game name | AI | speed | elemental variant | sound notes from the code |
|---|---|---|---|---|---|
| zombie | Shambler (Grave-Risen) | lumber, `shamblerWalk` | .72 | Plague-Spitter (poison) | heavy group; may **spit** acid |
| corpse | Risen (Gibbet Remains) | lumber, shambler | .88 | Plague Bloat (poison) | heavy group |
| skeleton | Bone Archer (Ossuary Footman; swordsmen and axemen too) | archer | 1.6 | Frost-Bound Sentinel (ice) | rattling square wave; `cling` on hit; swings 1.67× slower |
| ghost | Shade (Rope-Shade) | phase | 2.2 | Bell-Wraith (lightning) | sine 520–680 Hz; `contact` on hit |
| imp | Briar Imp (Ledger Imp) | swarm | 2.7 | Cinder Imp (fire) | small group; **leap** |
| caller | Gravecaller (Vesper Caller) | summon | 1.15 | Pyre Caller (fire) | raises the dead; may spit |
| brute | Mauler (Razor Tollman: hooks, chains) | charge | 1.2 | Cinder Tollman (fire) | heavy group; leap |
| bear | Demon Bear (Grove Mauler) | lumber | 1.35 | Rime Bear (ice) | heavy; leap |
| snake | Briar Serpent (Blackroot Adder) | lumber, **hides** and ambushes within 3.35 m ("HISS") | 2.15 | Venom Asp (poison) | 1.8 kHz bandpass hiss; may spit |
| raver | Raver (Thin Laugher) | swarm | 3.15 | Storm Laugher (lightning) | small; leap |
| worm | Dune Maw (Purse-Jaw) | lumber, **burrows** and emerges with screen shake | 1.05 | Bile Crawler (poison) | heavy |
| wraith | Ash Wraith (boss template) | boss/phase | 2.3 | n/a | sine group |
| melakir | Melakirniz (twin boss) | charge | 2.9 | n/a | slash on hit |
| king | Hollow King (boss template) | boss | 1.65 | n/a | heavy plus cling (plate) |

- Planned basics, not all built yet [?]:
  - Shambler v2
  - Bone axemen, swordsmen and archers
  - Fallen Spawn (Spawnling, Spawn Shaman)
  - Corrupted Phimn (Winged Caster, Feral Stalker; fire, ice, lightning and poison)
- **Quirks**: 20% of normal foes get one.
  - `spit`: zombie, snake, caller. Fires an acid fan.
  - `burrow`: worm
  - `leap`: bear, brute, deer, rabbit, crow, imp, raver
  - `jab`: everyone else (a quick swing; archers loose a weak arrow instead)
- **Packs and night**
  - Champion (blue) packs have 1 mod and unique (gold) leaders have 2–3. Mods: Fleet, Brutal, Knitting, Hulking, Ironhide, Spiteful, plus Warded, Venomous and Caustic from Nightmare.
  - **At night foes are boosted and nests wake** ("Night. They strike harder…").
  - Ambush marks (`mark/ambush:<kind>`) spring 3 foes out of the grass with a screen shake.
- **Critters**: rabbit (Grey Hare), rat (Crypt Rat), crow (Ash Crow), deer (Briar Hart). Rats appear in dungeons. Hares, deer and birds appear outdoors.

### Bosses (code table: zone, element)
- **Act bosses**: Vessaline (choir, poison), Ossgrind (reliquary, cold), Halvane (gaol, lightning), Vhorr-Akesh (ashfont, fire), Ysmer (stacks, magic)
- **Side bosses**: Tallyman (tallyden, poison), Ghel (mirth, cold), Kessane the Toll Baron (tollarch, fire)
- **Existing bosses**: Saltmouth (sewer, poison), Ash Wraith (wild, fire), Melakirniz (wild, phys), Scar-Eye (root, phys), Bilge-Wight (hull, cold), Spire-Heart (weald, poison) then Goreth-Vaal (weald, magic), The Castellan (castle4, phys), Hollow King (vault, magic)
- **Endgame (Margins)**: Bell-Wright (tideclock, cold/time, Lute's bell), Mother Wick (tallow, fire, Brine's lamps), the Assessor (tollcourt, lightning), Nul-Osse (hollowstar, magic/gravity, hovering), Errata (scriptorium, magic/copy)
- **Pinnacle and ubers**: the Warm Binding (lastpage; "grief", ash-grey). Ubers: Ysmer Unbound and The Unbinding.
- **Boss rules**
  - Arenas seal and every big attack is telegraphed.
  - Attack shapes in code: melee, cone, dash, line, nova, slam, zone, pull, projectile, summon, aura, special.
  - The first kill per difficulty drops a Boss Stone.
- **Audio implication [REC]**: every telegraph shape needs a readable wind-up cue.

---

## 4. Weapons, skills, damage, colours
- **Weapon kinds**: sword, axe, mace, spear, dagger, bow, javelin, wand, staff, shield (plus hammer and orb references).
  - Axe and mace use the **heavy swish**.
  - Classes: Ironvow (warrior, Rusted Iron Sword), Longmark (archer, Ashwood Short Bow), Cinderwake (elementalist, Gnarled Yew Wand), Gravewell (blood/bone necromancer, Chipped Bone Dagger).
- **Damage types in code**: `phys`, `fire`, `cold`, lightning, `poison`, `magic`. Foes can be immune ("IMMUNE" popup).
  - Statuses: ignite/burn, chill (stacks), freeze, shock, poison, wound/bleed, blight, curse.
- **Rite schools (VFX palettes) with their 51 rites**
  - steel: cleave, execute, aimed, bladedance, javelin, ironjaw
  - fire: fireball, inferno, meteor, elemconsume, cinder, thunderkiln
  - cold: nova, glacier, frostward, hoarfrost, rimecaltrop
  - lightning: spark, stormcall, arcwhip, starlash
  - holy: smite, holy, consecrate, undertow
  - blood: bloodsoaked, rupture, crimson, mercy
  - bone: bonespear, summon, graveburst, fanbone
  - nature: wolfhowl, thorncoat, regrowth, briar, locust
  - mind: hex, veil, telekinesis, snare, blinkstep, dread, truesight
  - guard: bulwark, blindrush, warcry, hearthward, knell
  - poison: blightcask
  - Traps: ironjaw, blightcask, rimecaltrop, thunderkiln. Auras include hearthward and truesight.
  - A **Bound Rite** fuses a rite into the basic attack, with a separate variant for each weapon kind.
- **Colour rules (Brian; the newest rule wins)**
  - Magic has no colour of its own. It takes its element's colour **with a dark hint**:
    - fire: dark realistic red
    - physical: near-invisible smoky grey
    - cold: dark blue with light-blue streaks
    - poison: sickly green
    - lightning: pale violet-white
  - Hue shifts on monster bodies apply only to monsters Brian names.
- **Code palettes** (core / mid / edge / dark)
  - fire #fff2c8/#ff8a2a/#ff4a1a/#5a1a08
  - cold #fff/#bfe6ff/#6eb6ff/#1e3a66
  - lightning #fff/#e4f2ff/#9ad0ff/#2a3a80
  - poison #e8ff8a/#8ad04a/#3f7a2a/#1c3010
  - holy #fffbe8/#fff0b0/#e0a84a/#6a4a10
  - blood #ff8a7a/#c8241c/#7a0e0e/#2a0606
  - bone #fffaf0/#e4e0d4/#b8ad98/#4a4238
  - steel #fff/#e6ebf2/#a9b4c2/#3a4250
  - nature #e8ffd0/#7dcc7a/#3f8a3a/#1c3a18
  - mind #f4eeff/#c9b6ff/#8a6ad0/#2a1a4a
  - guard #fff6e0/#f0d28a/#b8903a/#4a3818
- **Projectile colours**: fire #FF6A20, frost #9FD8FF, spark #FFF2A8, holy #FFF0C0, bone #E4D8C4, arrow #C6A15A, orb #C080FF, acid #9AD85A, steel #D8DCE4, blood #AA2030.
- **[REC] Element sound identity**, to match the colour rules:
  - fire: low roar and crackle
  - cold: glassy cracks and a breath hiss
  - lightning: dry snaps, no sci-fi zaps
  - poison: wet bubbling
  - physical: dull and weighty
  - Keep "magic" sounds tied to an element. There is no generic sparkly "arcane" layer.

---

## 5. Items, loot, interactables
- **Rarity tiers in code**: common, uncommon (#6EA2FF), rare (#E6C15A), epic (#5CBA78), legendary (#E8A04A).
  - Base chances: 15 / 3.4 / 0.8 / 0.24%.
  - The approved direction is D2-order colours, toned down, with **one distinct drop sound per tier**. The table isn't locked yet [?].
- **Other loot**
  - 93 uniques, ethereal items, sockets (epic only)
  - Rite tomes (legendary, 10,000 gold)
  - Potions, gold spills, folios (lore pages), Boss Stones, Town Portal Scrolls
- **Containers**
  - `chest`, `chest/super`, `chest/stash`
  - Crates and logs crack open (55% chance of a drop)
  - Barrels stave in. `barrel/fire` explodes 72% of the time (a normal barrel 22%): fire damage plus screen shake ("The barrel goes up.")
- **Shrines** (styles): curse, xp, speed, lightning (a 25% blast on foes within 4.5 m), magic, cold, might, fire, angel.
  - The **Weeping Angel** cleanses all ailments ("The angel weeps. Your wounds close.").
  - A spent shrine says "The shrine is spent."
- **Other interactables**
  - stairs: trap, hatch, ladder, deep
  - arches: stone, cave, trees, gap, sand, road, sealed, wood
  - **organ**: church1 and gaol ("The pipes answer with a low hum.")
  - `well/heal`, `boat` (the ferry), signs, seats (chair, stool, bench, pew, log seat)
  - bonfire (town, camp, ash), lamps, torches, hearths, the anvil barrel

---

## 6. Weather, day/night, sun (live code)
- **Clock**
  - One in-game day is `daySeconds = 21600` real seconds (**6 real hours**) [?]. That is what the code says; it may be meant to be faster.
  - A new game starts at 09:15.
  - Night runs 18:00–05:30 (`isNight`). The darkness factor ramps 05:30–08:00 and 16:30–18:00.
  - Clock labels: Morning <11, Afternoon <17, Dusk, Night.
  - At dusk: "Night. They strike harder, and the nests wake far swifter." At dawn: "Dawn. The thin light is no promise."
- **Rain**
  - A random event: about 1 per 420 s when clear.
  - Normal rain ramps to 0.34 and lasts 24–74 s.
  - **Hard rain** (12% of events) ramps to 0.92 and lasts 28–54 s ("A hard rain. The road floods for a while.").
  - Rain decays at 0.07/s.
- **Fog**
  - About 1 per 480 s by day and 1 per 320 s at night. Lasts 36–86 s.
  - Thin fog reaches 0.3. **Thick fog** (14%) reaches 0.7 ("A thick fog. Shapes forget their edges.").
  - The intro starts in thick fog (0.7).
- **Where weather plays**: weather ticks in every area, and the audio `setWeather` is **not gated by indoor/outdoor**, so rain hiss also plays in taverns and crypts. [?] This is probably a bug worth flagging.
  - 3D rain and fog visuals aren't drawn yet (`wxRain`/`wxFog` are unused). Sky tints are day, dusk, overcast and dead.
- **Moving sun**
  - From 06:00 to 18:00 the sun arcs east to west at an elevation of 10° + 55°·sin.
  - Its colour lerps from warm #FFB070 at the horizon to moon-blue #9FB8FF (10467583).
  - At night a fixed moon light is used (offset −6, 16, 6; blue).
- **Other motion**: the water wheel rotates and the creek normal map scrolls.
  - [REC] Give the wheel and creek positional loops. Nothing like that exists yet.

---

## 7. Existing audio tech (live)

### Engine
- Plain **Web Audio API**, with one `AudioContext` and no middleware.
- It unlocks on the first gesture by playing a silent 8-sample buffer.
- Classes in the minified bundle:
  - `hl`: the audio class, `this.audio`, at line 23447
  - `dl`: the music manager, at 22388
  - `sl`: config, at 22325
  - `pl`: the rite cue table, at 22534

### Graph (created in `unlock()`)
```
master (1, or 0 when muted) → DynamicsCompressor(thr −16 dB, knee 8, ratio 2.4, att 4 ms, rel 180 ms) → destination
  music (.82) → master
    town bus (0..townBus .9)   ← guitar, nylon, pad, woodwind, clockwork loops + humUnder synth
    stone bus (0..stoneBus .74) ← wild/drone, wild/hollow, wild/metal loops
    dread bus (0..dreadBus .8)  ← dread/overworld loop
  sfx (1) → master              ← all procedural one-shots, voice gain (.7)
  rain (0..) → master           ← 2 s random-walk noise loop, lowpass 900 Hz, .45
  wind (0..) → master           ← same noise loop, lowpass 420 Hz, .28
```
- Mute is stored in `localStorage["sanctuary-mute"]` and applied instantly with `setValueAtTime`.

### Music manager (`dl`)
- Mood changes crossfade the three buses with linear ramps over **2 s**.
- **Bonfire proximity**: within 5 tiles of an unashed bonfire, `setFire(near)` ramps over 2 s:
  - nylon from .15 to .46
  - the guitar's ping-pong delay wet from .66 to .462
- **Guitar chain**
  - Dry .28, plus two delay sends: L .38 s and R .57 s
  - Feedback .48, damped by a 1200 Hz lowpass, merged as L/R ping-pong
- **humUnder**: a synthesized bass bed with the same length as guitar.ogg. Sine plus a .35 sub-octave, lowpass 170 Hz, gain .3.
  - Note schedule (s→Hz): 0 D2 73.42 · 4 D2 · 8 A2 110 · 12 D2 · 16 F2 87.31 · 20 F2 · 24 C2 65.41 · 28 A2 · 32 B♭2 116.54 · 36 D2.
  - So the town loop is **in D minor**, with 4 s chord steps. [REC] New town material should fit D minor and the 44.4 s loop.
- **Stem gains**: nylon .15–.46, pad .55, woodwind .14, clockwork .12, cimbalom .2 (unused), drone .62, hollow .5, metal .38.
- **Voices**: `speak(female)` plays one random greeting sample on NPC talk, hard-stopping the previous one.
  - Female set (`fl`): Ysara, Heska, Ilyra, Cal, Mira, Ness, Hesta, Ilen, Tamsin, Sable.
  - Everyone else gets the male set. [?] Myrine, Iskra and Moth are written as women ("widow", "her mother") but are missing from `fl`.
  - If a sample fails, `greet()` falls back to a synthesized formant "hm/hey/hello" (f0 188 Hz female, 112 Hz male).

### Every audio file
- **Hosting**
  - Files are same-origin under `/audio/` on the app host, e.g. `https://gold-iris-zippy-bird.grok.me/audio/town/guitar.ogg`. Path builder: `cl(e)` → `/audio/${e}`.
  - The prefix is only used on preview.grok.\*mil hosts.
  - Audio is **not** in the `bdblonewolf/sanctuary-assets` GitHub repo; that repo holds models, HUD and icons only.
  - [?] Presumably files go in the Grok Build project's public `/audio/` folder. Adding files goes through Brian and Grok Build.
- **Format**: all files are **Ogg Vorbis**.
- **Naming**: lowercase, `<bus>/<stem>.ogg`.

| Path | Use | Format | Length | Integrated / true peak |
|---|---|---|---|---|
| dread/overworld.ogg | dread bus loop | 16 kHz stereo, 171 KB | 66.0 s | −20.4 LUFS / −8.0 dBTP |
| town/guitar.ogg | town lead (dry plus delays) | 22.05 kHz mono | 44.4 s | −30.8 / −10.1 |
| town/nylon.ogg | fire-reactive layer | 22.05k mono | 44.4 s | −29.3 / −10.6 |
| town/pad.ogg | town | 22.05k mono | 44.4 s | −27.1 / −11.6 |
| town/woodwind.ogg | town | 22.05k mono | 44.4 s | −28.2 / −12.3 |
| town/clockwork.ogg | town | 22.05k mono | 44.4 s | −35.2 / −13.8 |
| town/cimbalom.ogg | **defined, never loaded** | 22.05k mono | 44.4 s | −26.2 / −10.8 |
| wild/drone.ogg | **stone** bus (church/castle/crypts/nave) | 22.05k mono | 60 s | −26.9 / −9.8 |
| wild/hollow.ogg | stone bus | 22.05k mono | 60 s | −24.6 / −10.3 |
| wild/metal.ogg | stone bus | 22.05k mono | 60 s | −29.5 / −11.3 |
| voice/male/{hm,hey,hello,yes,speak,news}.ogg | NPC greeting | 22.05k mono, 5–8 KB | 0.35–0.84 s | about −5 dBTP (peak-normalised) |
| voice/female/{hm,hey,hello,yes,quick,looking}.ogg | NPC greeting | same | same | same |

- **Naming trap**: "wild/\*" plays in **stone interiors**, not the wilderness. The outdoors and most caves use **dread/overworld.ogg**.
- All loops are `BufferSource` with `loop=true`. Loops of different lengths drift against each other freely.

### Procedural SFX (all synthesized; there are no SFX files)
| Call | Trigger | Recipe (short) |
|---|---|---|
| `hit(kind,s)` | player hits foe / foe hits player | `flesh`, `cling`, `heavy` (sine 110→42 Hz), `plate` (heavy + cling), `crunch` (168→48 Hz), `contact`. ≤4 per 80 ms. |
| Foe-to-kind mapping | player hits | boss/bear/brute/worm/king/wraith → heavy (plate if skeleton or king); skeleton → cling; ghost → contact; else flesh |
| Foe-to-kind mapping | foe hits player | bear/brute/king/zombie/corpse/worm → crunch; skeleton/snake/melakir → slash; else contact |
| `beast(kind,hurt)` | foe hurt or attacks | 50% chance, 240 ms limit. Oscillator sweeps per group (heavy / skeleton square / ghost sine / small triangle / snake hiss / deer / other). |
| `swish(heavy)` | swings | bandpass noise sweep 640→2800 Hz (heavy 240→1600) |
| `rite(skill,scale)` | every rite cast | one `pl` cue per rite key (wave, freq sweep, ≤0.36 s, noise layer); 0.5 scale for echoes |
| `ching()` | block | square 1680→520 plus triangle 2460→880 |
| `levelHum()` | level-up | sawtooth 70→92→78 with resonant LP, about 1 s |
| `organ()` | organ prop | sine chord C2/E♭2/G2/C3 plus triangle, 2.2 s |
| `tune()` | near Bram | triangle flute G4 A4 B4 A4 F4 G4, gain .035 |
| `gate()` | title-screen gate knock / continue | 1.2 s saw 78→36 Hz, noise sweeps, thunk at .92 s |
| `gasp(amt)` | intro wake, every 3.2 s | filtered noise breath, 1.05 s |
| `setGale` / `setWeather` | intro gale, rain, fog | ramps the wind and rain noise buses (rain ≤ .34, wind/fog ≤ .22) |

- **Not sounded at all today**:
  - loot drop or pickup, gold, potions
  - doors, stairs, chests, shrines, barrels exploding
  - footsteps, UI clicks
  - deaths, boss telegraphs, the ferry
  - water, the wheel, birds and other critters, the bonfire crackle itself

---

## 8. Known problems and the pending A1 fix
Sources: `port_audit_2d_to_3d.md` §A and `send/STAGE_A1_AUDIO_FIX_PROMPT.txt`. Status: **written, not yet applied** [?]. Check the live bundle for `[a1] peakVoices` once it ships.
- **Root causes of crackle and static**
  1. There is no limiter. A soft compressor alone lets stacked one-shots clip.
  2. The 2 s rain and wind noise loops have no seam fade, so they click every 2 s.
  3. About 11 always-on loops plus 2 feedback delays run in every zone. Silent buses still decode and mix.
  4. One-shots start at `currentTime` with no lookahead.
  5. Hard stops (voice, mute) click.
  6. `gate()` and `gasp()` allocate new noise buffers on every call.
- **The A1 fix**
  - Add a brickwall limiter after the compressor (−3 dB threshold, knee 0, ratio 20, 1 ms attack, 100 ms release).
  - Lower master to .8 and music to .7. Lower delay feedback to .35 and wet to .45 (.32 near the fire).
  - Equal-power 50 ms seam crossfade on the noise loops. Cache the noise buffers.
  - 24-voice cap; hits limited to ≤3 per 100 ms. +20 ms scheduling lead on one-shots.
  - `setTargetAtTime` mute fade. Voice gets a 10 ms fade-in and 30 ms fade-out.
  - Stop inactive mood groups 3 s after they fade out, and rebuild them from cached buffers.
  - Rules: a single AudioContext, **no new files or dependencies in A1**.
- **Mastering implications for new assets [REC]**
  - Effective music gain after A1 is about .8 × .7 × bus (.74–.9) × stem gain, which is already −10 to −20 dB.
  - Many layers sum, and the limiter sits at −3 dBFS.
  - So deliver with headroom and **never brickwall-master stems to 0 dBFS**.

---

## 9. Recommended asset specs [REC: all of this section]
- **Format**
  - Keep Ogg Vorbis (`.ogg`) so files drop into the existing paths and loader.
  - [?] Older iOS Safari can't decode Ogg Vorbis (support arrived around Safari 18.4; unverified). A failed decode is **silent** (the loader returns null), so test on iPhone.
  - If that matters, propose an AAC `.m4a` twin as a code change.
- **Sample rate and channels**
  - Music: 44.1 kHz stereo, Vorbis q4–q5 (~128 kbps).
  - Ambience beds: 44.1 kHz stereo, q3.
  - SFX and voice: 44.1 kHz mono, q4.
  - The current 16 kHz and 22.05 kHz files are lo-fi placeholders.
- **Loudness, measured on the file itself (Brian's mixer adds gain on top)**
  - Music stems and loops: about **−23 LUFS integrated**, true peak ≤ **−6 dBTP**.
  - Ambience beds: −26 to −30 LUFS, ≤ −8 dBTP.
  - SFX one-shots: peak ≤ **−6 dBFS**, short-term loudness −16 to −20 LUFS.
  - Voices and barks: peak ≤ −6 dBFS, about −20 LUFS (not peak-normalised).
  - Leave the limiting to the game's A1 limiter.
- **Loops**
  - Sample-accurate seamless loops, cut at zero crossings with no fade-in or fade-out at the file edges.
  - Town stems must be exactly the guitar length (**44.4 s**; `humUnder` is built from that length). Use 4 s bars in D minor.
  - Keep a common length per bus so the stems stay locked together.
- **Variations**: 3–5 variants per repeated sound (hits, deaths, footsteps, loot drops), each 0.1–1.5 s, trimmed tight (≤10 ms pre-roll).
  - Deaths and hit-reacts: 2–3 variants per family, as approved.
  - Loot drops: one per tier, 5 tiers.
- **Naming**
  - Lowercase snake_case under `/audio/<category>/`, matching the existing `town/`, `wild/`, `dread/` and `voice/<sex>/` folders.
  - Example layout: `sfx/hit/flesh_01.ogg`, `foe/zombie/death_02.ogg`, `loot/drop_legendary.ogg`, `amb/creek_loop.ogg`.
  - Code would have to be added for any new folder. [?] Whether the existing procedural sounds should be replaced or layered is Brian's call.
- **Size**: the whole audio set currently totals about 1 MB. Aim to keep a zone's music plus ambience under about 3 MB, because everything is decoded fully into memory.
- **Style**: acoustic, organic, aged. Use real wood, iron, stone, cloth, water and breath.
  - Avoid synth sparkle, sci-fi zaps, cartoon squeaks and modern drum-kit hits.
  - The town is warm (12-string or nylon, hearth). Everything else is cold and dreadful (low drones, distant metal, wind).
