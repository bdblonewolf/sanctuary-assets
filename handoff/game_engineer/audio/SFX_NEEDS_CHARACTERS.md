# Sanctuary: SFX needs, characters (monsters, bosses, NPCs, player classes)

For the sound designer. Compiled 2026-11-01 (America/Detroit) from the read-only sources: `sanctuary_art/monsters/LOG.md` and its sheets, `sanctuary/bosses.md` and `bosses.json`, `sanctuary/monster_levels.md`, `sanctuary/story/story_bible.md`, `story/data/voices.json`, `sanctuary/class_passives.md`, `skills_and_rites.md`, `sanctuary/audio/SANCTUARY_WORLD_FOR_AUDIO.md`, plus the 3D folders in `sanctuary_npc`.
Companion brief: `/workspace/sanctuary/audio/SANCTUARY_WORLD_FOR_AUDIO.md`. It covers the engine, buses, the existing procedural `hit()`/`beast()` calls and the file format (Ogg Vorbis, `<bus>/<stem>.ogg`).

**Tone.** D1/D2 Act I. Realistic, battle-worn, archaic gothic. Never cartoony.
- Creature voices are organic and processed: breath, throat, teeth and wet sounds. Avoid synth "monster" tones.
- Today nothing in the game plays footsteps or deaths, and there are no boss telegraphs. Everything below is new work.
- Approved D1 lesson: **several hit-react and death variants per family**. Aim for at least 3 of each and 4 or more footstep variants per surface.

**Path roots.** `ART` = `/workspace/sanctuary_art`. `NPC3D` = `/workspace/sanctuary_npc`.

**Priority.**
- **P0**: Act I starter set, player classes, Martsirt NPCs.
- **P1**: the rest of the Act I–II monsters, bosses and NPCs.
- **P2**: Act III and later, the Margins (Hell) and the ubers.

**Death types.** Collapse (body falls), Shatter (bones or crystal break and scatter), Burst (body ruptures or pops), Dissolve (fades to wisps, embers, ink or ash).

---

## 1. Summary table

| # | Name | Type | Pri | Closest Diablo 1/2 | Death type |
|---|---|---|---|---|---|
| 1 | Grave-Risen | Monster, zombie (phys) | P0 | D1/D2 Zombie | Collapse (wet, blood decal) |
| 2 | Shambler (4 bodies: rag man, rag woman, near-bare old man, crawler husk) | Monster, zombie basic | P0 | D2 Zombie / Hungry Dead | Collapse |
| 3 | Mummified Crawler (shambler husk) | Monster, zombie basic | P0 | D2 Dried Corpse (crawling) | Collapse, dry crumble |
| 4 | Bone Axeman | Monster, skeleton basic | P0 | D1 Skeleton (axe) / D2 Skeleton | Shatter (bone scatter) |
| 5 | Bone Swordsman | Monster, skeleton basic | P0 | D1 Skeleton / D2 Returned | Shatter |
| 6 | Bone Archer | Monster, skeleton basic | P0 | D1 Skeleton Archer / D2 Corpse Archer | Shatter |
| 7 | Ossuary Footman | Monster, skeleton (phys) | P0 | D2 Returned / D1 Skeleton Captain | Shatter, mail and shield drop |
| 8 | Fallen Spawnling | Monster, lesser demon | P0 | D2 Fallen | Burst (small pop puff) |
| 9 | Razor Tollman | Monster, brute (phys) | P0 | D1 Butcher / Overlord; D2 Minion of Destruction | Collapse (heavy, dust ring) |
| 10 | Ironvow | Player class (warrior) | P0 | D2 Barbarian / Paladin | Collapse (player) |
| 11 | Longmark | Player class (archer) | P0 | D2 Amazon (bow) / D1 Rogue | Collapse (player) |
| 12 | Cinderwake | Player class (elementalist) | P0 | D2 Sorceress / D1 Sorcerer | Collapse (player) |
| 13 | Gravewell | Player class (blood and bone necro) | P0 | D2 Necromancer | Collapse (player) |
| 14 | Wolchen | NPC, Martsirt smith | P0 | Charsi / Griswold | n/a |
| 15 | Ysara | NPC, Martsirt healer | P0 | Akara / Pepin | n/a |
| 16 | Ilyra | NPC, Martsirt gate herald | P0 | Kashya / Cain register | n/a |
| 17 | Quill | NPC, scribe and tome-keeper (Boss Stones) | P0 | Deckard Cain | n/a |
| 18 | Bram | NPC, logger (Martsirt / Briarwood) | P0 | Wirt / Farnham register | n/a |
| 19 | Mira | NPC, taproom innkeeper | P0 | Ogden / Gillian | n/a |
| 20 | Orrin | NPC, drunk ex bell-ringer | P0 | Farnham | n/a |
| 21 | Ness | NPC, homesick widow | P0 | Gillian / Adria register | n/a |
| 22 | Spawn Shaman | Monster, lesser demon caster | P1 | D2 Fallen Shaman | Burst (pop puff) |
| 23 | Plague-Spitter | Monster, zombie (poison) | P1 | D2 Plague Bearer / Gorebelly | Burst (green spray) then collapse |
| 24 | Frost-Bound Sentinel | Monster, skeleton (cold) | P1 | D2 Horror / Burning Dead (cold) | Shatter (bone and ice) |
| 25 | Rope-Shade | Monster, ghost (phys) | P1 | D2 Ghost / Wraith | Dissolve (upward wisps) |
| 26 | Bell-Wraith | Monster, ghost (lightning) | P1 | D2 Spectre / Apparition | Dissolve and bell crack |
| 27 | Ledger Imp | Monster, imp (phys) | P1 | D2 Fallen / D1 Imp | Burst (pop puff) |
| 28 | Cinder Imp | Monster, imp (fire) | P1 | D2 Imp (Act V) | Burst (ember pop) |
| 29 | Vesper Caller | Monster, caller (cold-blue rune, raises dead) | P1 | D2 Greater Mummy / Fallen Shaman | Collapse (robe crumple, rune decal) |
| 30 | Pyre Caller | Monster, caller (fire) | P1 | D2 Fallen Shaman / Zealot | Collapse (robe crumple, embers) |
| 31 | Gibbet Remains | Monster, corpse (phys) | P1 | D2 Hungry Dead in a gibbet | Collapse inside the cage |
| 32 | Plague Bloat | Monster, corpse (poison) | P1 | D2 corpse-explosion bloated dead | Burst (goo, poison cloud) |
| 33 | Cinder Tollman | Monster, brute (fire) | P1 | D2 Minion of Destruction (fire) | Collapse plus ember gutter |
| 34 | Grove Mauler | Monster, bear (phys) | P1 | D2 Grizzly / Werebear | Collapse (heavy, dust ring) |
| 35 | Rime Bear | Monster, bear (cold) | P1 | D2 Werebear, frost | Collapse plus frost crackle |
| 36 | Blackroot Adder | Monster, snake (phys) | P1 | D2 Sand Viper / Tomb Viper | Collapse (coil fade) |
| 37 | Venom Asp | Monster, snake (poison) | P1 | D2 Tomb Viper / Serpent | Collapse (coil fade, green hiss) |
| 38 | Thin Laugher | Monster, raver (phys) | P1 | D2 Flayer (swarm) | Burst |
| 39 | Storm Laugher | Monster, raver (lightning) | P1 | D2 Soul Killer / Flayer Shaman | Burst (crackle) |
| 40 | Purse-Jaw | Monster, worm (phys) | P1 | D2 Sand Maggot | Burst (goo, coins) |
| 41 | Bile Crawler | Monster, worm (poison) | P1 | D2 Rock Worm / Maggot | Burst (bile) |
| 42 | Corrupted Phimn, Winged Caster | Monster, demon caster (fire/ice/lightning/poison) | P1 | D2 Dark Spearwoman plus D1/D2 Succubus | Collapse from hover (wings fold) |
| 43 | Corrupted Phimn, Feral Stalker | Monster, demon ambusher (same 4 elements) | P1 | D2 Dark Stalker plus Succubus | Collapse |
| 44 | Critters: Grey Hare, Crypt Rat, Ash Crow, Briar Hart | Ambient wildlife (killable) | P1 | D2 critters / D1 rats | Collapse (small) |
| 45 | Saltmouth | Boss, existing (sewer, poison) | P1 | D2 Corpsefire / D1 Butcher's den | Collapse, then dissolve to brine-ink |
| 46 | Ash Wraith | Boss, existing (wild, fire) | P1 | D2 Blood Raven | Dissolve to embers |
| 47 | Melakirniz (twins) | Boss, existing (wild, phys) | P1 | D2 Moon Clan goatman uniques | Collapse x2, then ember dissolve |
| 48 | Scar-Eye | Boss, existing (root, phys) | P1 | D2 Act I unique beast (Treehead-style) | Collapse (huge), then dissolve |
| 49 | Vessaline, the Thorn Abbess | Boss, Act I (poison/blood) | P1 | Andariel | Collapse to knees, then dissolve to rot-ash |
| 50 | Bilge-Wight | Boss, existing (hull, cold) | P1 | D2 Wraith unique / Drowned | Dissolve into mist; anchor drops |
| 51 | The Tallyman | Boss, side (Act I per JSON; phys/poison) | P1 | Treehead Woodfist / Coldcrow | Collapse, ledger spill |
| 52 | Ossgrind, the Reliquary Grub | Boss, Act II (cold/phys) | P1 | Duriel | Shatter (frost chitin), then dissolve |
| 53 | Ghel, the Mirthwarden | Boss, side (Act II per JSON; cold/mind) | P1 | Bishibosh / Rakanishu | Dissolve (laughter fades) |
| 54 | Civilian outfit pool (10 male, 12 female sheets) | NPC foley reference | P1 | Tristram / Rogue Camp townsfolk | n/a |
| 55 | Holt | NPC, ferryman (Briarwood / Blackwater) | P1 | Meshif / Warriv | n/a |
| 56 | Myrine | NPC, spear-hand | P1 | Kashya's rogues | n/a |
| 57 | Orithya | NPC, ex-citadel scout | P1 | Kashya | n/a |
| 58 | Sable | NPC, sly tome merchant | P1 | Gheed | n/a |
| 59 | Orlem | NPC, Qadren headman | P1 | Greiz / Lysander | n/a |
| 60 | Heska | NPC, Qadren guard | P1 | Greiz's mercs | n/a |
| 61 | Vetch | NPC, Qadren gambler | P1 | Gheed | n/a |
| 62 | Tamsin | NPC, Salt House cook-innkeeper | P1 | Atma / Ogden | n/a |
| 63 | Ayla (Phimn) | NPC, side quest | P1 | D2 Natalya register | n/a |
| 64 | Kessane, the Toll Baron | Boss, side (Act III; phys/fire) | P2 | Bonebreaker / the Countess | Collapse in plate, then ember dissolve |
| 65 | Inquisitor Halvane | Boss, Act III (lightning/mind) | P2 | Mephisto | Dissolve (lightning drains from ribcage) |
| 66 | Spire-Heart | Boss, existing (weald, poison/nature) | P2 | D2 Treehead / Thorned Hulk | Collapse (timber fall) |
| 67 | Goreth-Vaal | Boss, existing (weald, magic) | P2 | Izual / Hephasto | Shatter (obsidian), then violet dissolve |
| 68 | The Castellan | Boss, existing (castle4, phys) | P2 | Shenk the Overseer / Griswold | Collapse in plate |
| 69 | Vhorr-Akesh, the Ember Saint | Boss, Act IV (fire/lightning) | P2 | Diablo | Dissolve to embers |
| 70 | The Hollow King | Boss, existing (vault, magic) | P2 | D1 Skeleton King (Leoric) | Shatter (plate falls apart, crown drops) |
| 71 | Ysmer, Who Wrote the Plague | Boss, Act V (magic/all) | P2 | Baal | Dissolve to ink |
| 72 | Bell-Wright | Boss, Margins I (cold/time) | P2 | new (nearest: D2 Lister-style keeper) | Shatter (bell cracks, gears spill) |
| 73 | Mother Wick | Boss, Margins II (fire/mana) | P2 | new (nearest: Andariel register) | Dissolve (melts to wax and smoke) |
| 74 | The Assessor | Boss, Margins III (phys/lightning) | P2 | new (nearest: D2 Council member) | Collapse, coins spill |
| 75 | Nul-Osse | Boss, Margins IV (magic/gravity) | P2 | new (nearest: Lord De Seis) | Shatter, then implosion |
| 76 | Errata, the Copyist | Boss, Margins V (magic/copy) | P2 | new (nearest: Nihlathak / Baal clone) | Dissolve to ink, mask shatters |
| 77 | The Warm Binding | Boss, pinnacle (grief) | P2 | Uber Diablo / Tristram | Dissolve (pages fall, book closes) |
| 78 | Ysmer Unbound | Uber (magic/all) | P2 | Uber Baal | Dissolve into ink vortex collapse |
| 79 | The Unbinding (Warm Binding, Decided) | Uber (grief, ember) | P2 | Uber Diablo / Tristram | Dissolve to embers and burning pages |
| 80 | Wynn | NPC, coast gravedigger | P2 | Cain-like | n/a |
| 81 | Rusk | NPC, Bastion captain | P2 | Kashya / Larzuk | n/a |
| 82 | Sera | NPC, mud surgeon | P2 | Akara / Ormus | n/a |
| 83 | Odder | NPC, young smith | P2 | Hratli / Larzuk | n/a |
| 84 | Iskra | NPC, cliff widow | P2 | none | n/a |
| 85 | Moth | NPC, fen proverb woman | P2 | Ormus register | n/a |
| 86 | Calder | NPC, ashamed survivor | P2 | none | n/a |
| 87 | Hask | NPC, toll grandson | P2 | none | n/a |
| 88 | Kell | NPC, toll grandson | P2 | none | n/a |
| 89 | Nim | NPC, coward wit | P2 | Wirt register | n/a |
| 90 | Vellum | NPC, crypt warden | P2 | none | n/a |
| 91 | Lute | NPC, frightened diver | P2 | none | n/a |
| 92 | Brine | NPC, lamp-keeper | P2 | none | n/a |
| 93 | Jas | NPC, smuggler accountant | P2 | Gheed / Alkor | n/a |
| 94 | Piet | NPC, ex-gaoler prisoner | P2 | none | n/a |
| 95 | Ors | NPC, unfrocked priest | P2 | Ormus / Natalya | n/a |
| 96 | Cal | NPC, Highmarket parts buyer | P2 | Gheed / Anya | n/a |
| 97 | Pell | NPC, gate-crier | P2 | Warriv / Elzix | n/a |
| 98 | Hesta | NPC, Lampwick innkeeper | P2 | Ogden | n/a |
| 99 | Voss | NPC, Lampwick regular | P2 | Farnham | n/a |
| 100 | Ilen | NPC, Lampwick regular | P2 | none | n/a |
| 101 | Sarn | NPC, ash-camp boss | P2 | Qual-Kehk | n/a |
| 102 | Vesper | NPC, fence (under the castle) | P2 | Gheed | n/a |

**Counts (rows):** P0 = 21 (9 monsters, 4 classes, 8 NPCs). P1 = 42 (23 monster rows, i.e. 26 models with the 4 critters; 9 bosses; 1 civilian foley pool; 9 NPCs). P2 = 39 (16 bosses or ubers, 23 NPCs). Total 102 rows. Upcoming or undesigned models (§11) are not counted.

---

## 2. Shared sound sets (build once, reuse)

Build each **core set** once. Per-model sections then list only the **layers** added on top.

| Set | Core content | Used by |
|---|---|---|
| **S-BONE** (bone rattle) | Dry bone clacks, a joint-creak loop, jaw chatter, bone-on-stone and bone-on-dirt steps, swing effort (no voice, only a hollow skull "huff"), hit chips (6 small pieces, matching the VFX), shatter-and-scatter death (4+ variants) and a bone-pile settle tail. Plus a **reassemble** (reversed scatter) for raises. | Ossuary Footman, Bone Axeman, Swordsman, Archer, Frost-Bound Sentinel, Gravewell's Raise Bone servants, Kessane's Tabards of the Dead, Hollow Court dead, Vhorr's Reliquary Prison, Nul-Osse (bone layer) |
| **S-FLESH** (rotting dead) | Wet throat groans and moans, gurgles, slow drag-step (bare foot, rag-wrapped foot, old boot), rag-cloth flap, flesh-on-flesh slap and grab, hurt grunts with no words, wet collapse plus body thud, blood splat decal tick, corpse squelch when hit or stepped on | Grave-Risen, Shamblers, Mummified Crawler (dry variant), Plague-Spitter, Gibbet Remains, Plague Bloat, Razor/Cinder Tollman (rot layer), Saltmouth, Vessaline's briar nuns, Ysmer's risen waves |
| **S-SPECTRE** (ghost) | Breathy whispers, reversed-breath swells, a distant choir-breath bed, cloth-in-wind with no footsteps, a "phase-out" flicker (a short airy tear), a wail ring, and a dissolve death (an inhale that rises into wisps) | Rope-Shade, Bell-Wraith, Ash Wraith, Bilge-Wight, Ghel's ghost faces, the Hollow King's ghost courtiers, the Warm Binding's unwritten, Echo of You, the Errata Fair Copy |
| **S-IMP** (small demon) | Chitter, snarl, wet-teeth hiss, high squeal on hit, claw scrape, clawed-foot skitter on stone, a hop/leap whoof, and a pop-puff death (small wet burst plus a sulphur sizzle) | Fallen Spawnling, Spawn Shaman, Ledger Imp, Cinder Imp, Tallyman's Audit imps. The pitched-down, heavier version is used by Melakirniz. |
| **S-CULT** (caller / cultist) | Murmured non-word chant loops (low male and old female), robe swish, rope belt, staff butt on stone, censer-chain sway, a cast wind-up breath and release, and a robe-crumple death plus rune fizzle | Vesper Caller, Pyre Caller, Spawn Shaman (chant layer), Halvane's Council of Three, Halvane (chant layer) |
| **S-BEAR** (heavy beast) | Deep chest breathing loop, huff and snort, roar (3 sizes), fur-and-bramble rustle, padded heavy footfalls with claw clicks, swipe whoosh, jaw snap, overhead-slam impact, stagger groan, heavy fall plus dust-ring thump | Grove Mauler, Rime Bear, Scar-Eye, Spire-Heart, Goreth-Vaal (bear form) |
| **S-BRUTE** (chained hulk) | Heavy chain drag (loop), hook clinks, cleaver whoosh and chop, belly-deep effort grunts, leap whoof, ground-slam ring, thud steps, stagger, and a huge collapse with the chains settling | Razor Tollman, Cinder Tollman, Saltmouth (hooks and chains), the Castellan (chains layer) |
| **S-PLATE** (armoured undead) | Rusted plate clank per step, a joint grind loop, helm-resonant breath or growl (inside the metal), sabaton steps, shield bash, collapse in armour (pieces bounce) | Ossuary Footman (mail-only version), Frost-Bound Sentinel, Kessane, the Castellan, the Hollow King |
| **S-SERPENT** | Hiss (3 sizes), scale slide on dirt or stone, coil tighten, strike snap, recoil, a coil-down death with a slow scale slither | Blackroot Adder, Venom Asp |
| **S-MAW** (worm and chitin) | Wet maw open and close, tooth-ring grind, soil churn, burrow rumble (sub-heavy, ties to screen shake), emerge burst, squash on hit, goo-burst death | Purse-Jaw, Bile Crawler, Ossgrind (scaled up plus a chitin layer) |
| **S-LAUGH** | Laughter vocal library: giggle, breathless sprint-laugh, cackle, wheeze, choked laugh on hit, and a death laugh that breaks into a sob | Thin Laugher, Storm Laugher, Ghel, Sixth Voice revivals |
| **S-BELL** | Bronze handbell ring, cracked bell, muffled underwater toll, bell-mace impact, clock gear ticks and escapement | Bell-Wraith, Bell-Wright, Ghel's bell staff, Lute and Orrin (flavour) |
| **S-INK** (book and ink) | Page flutter, book slam, binding creak, leather-and-chain clasp, quill scratch, ink drip, slosh and splash, ink-tide wave, word whispers | Ysmer, Ysmer Unbound, Errata, the Warm Binding, The Unbinding, Halvane's confession book, the Tallyman's ledger, Quill (NPC foley), rite tome loot |
| **S-COIN** (toll, keys, scales) | Coin spill and jingle, purse, padlock, key ring, brass scale clink, abacus beads, gavel | Tallyman, Kessane, the Assessor, Purse-Jaw (swallowed coins on death), Hask and Kell |
| **S-THORN** (briar) | Thorn creak and snap, bramble drag, root rip from soil, rose-petal rot hiss | Vessaline and her briar nuns, Scar-Eye's brambles, Grove Mauler's coat, Spire-Heart, the Briar Snare and Thorn Coat rites |
| **S-WAX** | Candle gutter, wax drip and sizzle, wick whip crack, lantern creak, melting slump | Mother Wick, Tallow Saints, Brine (flavour) |

### Elemental layers (stems laid over any core set)
These follow Brian's colour rule: magic has no colour or sound of its own and takes its element's feel, always with a dark hint.

| Layer | Colour rule | Sound identity |
|---|---|---|
| **E-PHYS** | Near-invisible smoky grey | Almost no tonal layer: a dull weighty whump, dust or smoke breath and air displacement. Never sparkly. |
| **E-FIRE** | Dark realistic red | Low banked roar, ember crackle, smoulder hiss and coal tick. Dark and heavy, not a bright whoosh. |
| **E-COLD** | Dark blue with light-blue streaks | A dark low frost-groan bed (the "dark blue"), plus thin bright glassy cracks and breath-hiss tinkles on top (the "light-blue streaks"). |
| **E-LIGHT** | Pale violet-white | Dry snaps, static crackle, a short arc buzz and distant thunder tails. No sci-fi zaps. |
| **E-POIS** | Sickly green | Wet bubbling, acid fizz, spit, retch and gas hiss |
| **E-MAGIC / mind / gravity / time / copy** | Takes its element's colour | Keep it tied to a real-world texture: ink (copy), sub-pressure and stone creak (gravity), clock ticks (time), whispered words (mind). No generic arcane shimmer. |
| **E-HOLY**, **E-BLOOD**, **E-GRIEF** | Holy gold, blood red, grief ash-grey | Holy: dim bell-tone and warm air. Blood: wet pulse and heartbeat. Grief: choked breath and a desaturated choir. |

### Global per-tier and per-event hooks
- **Champion and unique packs**: a short aura bed per mod is optional (Fleet, Brutal, Knitting, Hulking, Ironhide, Spiteful, Warded, Venomous, Caustic). A unique leader adds a pitched-down vocal on aggro.
- **Night boost**: "Night. They strike harder…". Nests waking need a distant chorus cue.
- **Ambush marks**: 3 foes spring from the grass. Use a grass-burst whoosh plus a screen-shake thump.
- **Loot**: one distinct drop sound per tier (D1 lesson). Gold spill, potion bounce (two clinks), tome page flutter, key drop (violet chime), and a Boss Stone beam hum.
- **Boss shared kit**:
  - arena door seal slam and lock
  - intro roar ring plus name-plate sting
  - phase-shift white-out (1.2 s whoosh and ring)
  - enrage pulse (red heartbeat)
  - telegraph wind-up per attack shape: melee, cone, dash, line, nova, slam, zone, pull, projectile, summon, aura, special
  - death: 2.2 s hitstop with near-silence, then 3 ring booms, then a dissolve (embers or ink by theme), then the loot fountain and the Boss Stone beam
  - uber intro: 3 keys orbit and shatter, plus a violet edge hum
  - potion denied (Saint's Water): a grey smoke fizz plus a crossed-flask "denied" click

---
## 3. P0: Act I starter monsters

Each entry is keyed as: **Body**, **Character / Diablo**, then the sound list (Idle, Aggro, Attack, Special, Hit, Death, Move, Corpse/loot), then **Paths**. Animation clips are listed so cues can be tied to keyframes.

### 3.1 Grave-Risen (zombie, phys) · P0
- **Body:** man-sized (~1.8 m), gaunt grey flesh, torn tunic and old boots. Slow lurching walk, arms reaching. Attacks with a one-arm club or grab.
- **Character / Diablo:** mindless hunger, the classic first enemy. D1/D2 Zombie.
- **Sounds (S-FLESH core):**
  - Idle: low wet moan loop, occasional teeth-click.
  - Aggro: rising rasp groan.
  - Attack: effort groan plus arm whoosh plus flesh slap or grab on impact (`hit('flesh')` today).
  - Hit: wet thud plus pained grunt (3 variants).
  - Death: knees buckle, wet collapse thud, blood splat decal.
  - Move: boot drag-scuff (dirt, stone, wood).
  - Corpse/loot: soft squelch when struck again. Gravewell gains Toll from the corpse ("collect" whisper).
- **Paths:** art `ART/monsters/families/01_zombie.jpg`, rig `ART/monsters/rigpose/grave_risen_front.png`, `_back.png`. Model `ART/monsters/models3d/grave_risen.glb` (preview `models3d/previews/grave_risen.png`) and `NPC3D/monsters/grave_risen/out/grave_risen.glb` (clips idle, walk, attack, hit, death; WIP).

### 3.2 Shambler (zombie basic, 4 bodies) · P0
- **Body:** emaciated rag-wrapped dead. Man in rags, woman in a torn dress, near-bare old man. Hunched shuffle with one-arm punches.
- **Character / Diablo:** fodder in crowds (the sewer holds 38). D2 Zombie / Hungry Dead.
- **Sounds:**
  - Use S-FLESH, with a **male, female and old-man moan set** (pitch and timbre variants). Crowd-safe: short, low-volume idles, randomised so 38 don't phase.
  - Attack: punch whoosh plus flesh hit.
  - Death: collapse.
  - Move: bare-foot shuffle and rag-wrap scuff.
- **Paths:** `ART/monsters/families/12_zombie_basic_v2.jpg`, rig `rigpose/shambler_front.png`, `_back.png`. Models `ART/monsters/models3d/shambler.glb`, `NPC3D/monsters/starter/rag_zombie.glb` and `grave_old_man.glb` (clips idle, walk, attack, hit, death; previews in `starter/previews/`, lineup `starter/lineup_v2.png`). No female model yet; see §11.

### 3.3 Mummified Crawler (zombie basic) · P0
- **Body:** mud-caked, dried, prone husk on all fours. Drags itself and lunges with a bite or claw at ankle height.
- **Character / Diablo:** ambusher in mud and ash. D2 Dried Corpse, crawling.
- **Sounds (S-FLESH, dry variant):**
  - Idle: dry rattling wheeze.
  - Aggro: hiss-croak.
  - Attack: lunge scrape plus bite snap.
  - Hit: crackle of dry skin plus a puff of grave dust.
  - Death: dry crumble collapse.
  - Move: fingernail and knee drag through dirt, a mud squelch variant for the mires.
  - Corpse: dust settle.
- **Paths:** `ART/monsters/models3d/crawler.glb`, `previews/crawler.png`, rig `rigpose/crawler_front.png`. The starter README lists it as **missing** in `NPC3D/monsters/starter/`.

### 3.4 Bone Axeman (skeleton basic) · P0
- **Body:** 1.80 m, bare bone with a loin rag and leather bracer. One-handed rusty axe. Stiff, jerky gait.
- **Character / Diablo:** relentless grave guard. D1 Skeleton (axe) / D2 Skeleton.
- **Sounds (S-BONE):**
  - Idle: jaw chatter and joint creak.
  - Aggro: skull-hollow rasp plus a bone clack.
  - Attack 1, horizontal: heavy swish (`swish(true)`) plus axe bite (`hit('heavy')`).
  - Attack 2, overhead: wind-up creak plus chop.
  - Hit: bone chip clack (3).
  - Death: shatter-scatter, axe clatters on stone.
  - Move: bone-foot clicks.
  - Corpse/loot: bone pile settle. Raise and revive uses the reassemble sound.
- **Paths:** `ART/monsters/families/13_skeleton_basic.jpg`, rig `rigpose/axeman_front.png`. Models `ART/monsters/models3d/axeman.glb`, `NPC3D/monsters/axeman/out/axeman.glb` (idle, walk, attack1, attack2, hit, death) and `NPC3D/monsters/starter/bone_axeman.glb`.

### 3.5 Bone Swordsman (skeleton basic) · P0
- **Body:** 1.78 m, bone and belt, rusted sword, no shield. Same gait as the Axeman.
- **Diablo:** D1 Skeleton / D2 Returned.
- **Sounds:**
  - Use S-BONE, with a lighter blade swish and steel `cling` on contact.
  - Attack 2 is a downward cut.
  - Death: the sword rings as it hits stone.
  - Otherwise as the Axeman.
- **Paths:** `13_skeleton_basic.jpg`, rig `rigpose/swordsman_front.png`. Models `ART/monsters/models3d/swordsman.glb`, `NPC3D/monsters/swordsman/out/swordsman.glb`, `NPC3D/monsters/starter/bone_swordsman.glb`.

### 3.6 Bone Archer (skeleton basic) · P0
- **Body:** 1.84 m, rusty helm, longbow, arrow quiver. Stands off and kites.
- **Diablo:** D1 Skeleton Archer / D2 Corpse Archer.
- **Sounds:**
  - S-BONE core.
  - Bow: draw creak (old dry string), release twang, arrow whiz-by, arrow impacts (flesh, wood, stone, shield).
  - Quiver rattle on move. Helm clank on death plus the bow snaps.
- **Paths:** `13_skeleton_basic.jpg`, rig `rigpose/archer_front.png`, `archer_bow.png`, `archer_quiver.png`, `archer_helmet.png`. Model `NPC3D/monsters/starter/bone_archer.glb` only (no `models3d` glb).

### 3.7 Ossuary Footman (skeleton, phys) · P0
- **Body:** man-sized skeleton in rusted chainmail and a nasal helm. Kite shield with a cross, spear or sword. Disciplined, steady march.
- **Character / Diablo:** drilled dead soldiery, holds the line. D2 Returned / D1 Skeleton Captain.
- **Sounds (S-BONE plus S-PLATE mail-only):**
  - Idle: mail shiver and creak.
  - Aggro: shield-rim thump on bone, a hollow helm breath.
  - Attack: thrust or swing plus steel hit.
  - Special: **block**, shield wood-and-iron thud (pairs with the `ching` block). Shield-bash.
  - Hit: mail-plus-bone hit (`hit('plate')`).
  - Death: shatter while the mail slumps in a jangling heap, helm bounce, shield falls flat.
  - Move: steady mail-jingle march.
- **Paths:** `ART/monsters/families/02_skeleton.jpg`. Model `ART/monsters/models3d/ossuary_footman.glb` (preview `previews/ossuary_footman.png`). Source only in `NPC3D/monsters/ossuary_footman/` (`pick_shield`; no out).

### 3.8 Fallen Spawnling (lesser demon) · P0
- **Body:** ~3.5 ft red-scaled demon with horns, tail and a jagged notched blade. Skittering, cowardly rushes in packs.
- **Character / Diablo:** cowardly pack vermin that scatter when the shaman dies. D2 Fallen (the Fallen Spawn family).
- **Sounds (S-IMP):**
  - Idle: chittering gabble (non-word gibberish).
  - Aggro: shrill war-yelp.
  - Flee: **panicked squeal**, needed for the Fallen-style scatter.
  - Attack: small blade swish plus jagged hit.
  - Hit: yelp.
  - Death: pop-puff burst plus sulphur sizzle.
  - Move: clawed-foot skitter, tail drag.
  - Revive by a shaman: reverse puff plus a gasp.
- **Paths:** `ART/monsters/families/14_red_demon.jpg`, rig `rigpose/red_demon_spawnling_front.png`, `_back.png`. **No 3D model** (missing per the starter README).

### 3.9 Razor Tollman (brute, phys) · P0
- **Body:** huge (~2.3–2.5 m) hulking brute. Hooded, spiked iron collar. Torn, rotting, stitched skin shows raw flesh and bone in places. Chains hang from the wrists and drag at the feet. **Embers** glow in the cracks of the cleaver and wounds. Heavy cleaver in the right hand, meat hook in the left. Lumbers, then lunges.
- **Character / Diablo:** the toll-taker butcher, "fresh meat" menace. D1 Butcher / Overlord; D2 Minion of Destruction scale.
- **Sounds (S-BRUTE plus S-FLESH rot plus a faint E-FIRE ember layer):**
  - Idle: wet heavy breathing through the hood, chain sway, faint ember tick.
  - Aggro: a guttural bellow.
  - Attacks: cleaver chop (`hit('heavy')` plus a meat thunk), hook swing with a chain rattle and a flesh catch.
  - Special: **hook pull** (chain whip, hook bite, yank drag) and a ground slam that drives up embers.
  - Hit: flesh thump plus chain jangle plus a low grunt.
  - Death: groan, drops to its knees, huge collapse, dust ring, the chains settle, embers fade to a smoulder hiss.
  - Move: heavy thud steps plus a constant chain drag loop.
  - Corpse/loot: coin purse spill (toll theme).
- **Paths:** `ART/monsters/families/07_brute_v2.jpg`. Model `ART/monsters/models3d/razor_tollman.glb`, preview `previews/razor_tollman.png`. Source only in `NPC3D/monsters/razor_tollman/` (`pick_hook`, `pick_cleaver`).

---
## 4. P0: Player classes

**Model status.** No class models exist yet, and the classes have no fixed gender. The study (`research/sanctuary_and_diablo_study.md`) recommends modular light, medium and heavy armour per class with burned-out heraldry.
**Recommendation:** record a **male and a female vocal set** per class.

**Shared player kit (all classes)**, because weapons and rites are not class-locked:
- **Player vocals, per class and sex:** attack efforts (3), hurt (light, heavy), low-health breath loop, death cry, potion gulp, "can't" bark (no mana, full inventory, locked), level-up exhale.
- **Footsteps** by armour tier (light leather, medium mail, heavy plate) times surface (dirt, grass, stone, wood, mud, sand, water, snow, ash).
- **9 weapon kinds:**
  - swing, hit and miss sounds for sword, axe and mace (heavy swish), spear, dagger and staff
  - bow draw, release and arrow impacts
  - wand flick
  - shield block (`ching`) and bash
  - each needs an **equip and unequip** foley
- **Bound Rite** variants: each weapon kind adds a faint rite echo on the swing.
- **51 rites by school.** Each needs a cast, a travel or loop sound and an impact. Layer them by element per §2:

| School | Rites |
|---|---|
| Steel (E-PHYS) | Cleave, Bladedance, Execute, Rupture, Javelin, Aimed |
| Fire | Fireball, Meteor, Inferno, Cinder |
| Cold | Nova, Glacier, Hoarfrost |
| Lightning | Spark (Volt), Stormcall, Arcwhip, Elemental Consume |
| Holy | Holy, Consecrate, Smite, Starlash |
| Blood | Bloodsoaked, Mercy, Crimson |
| Bone | Bone Spear, Raise Bone (servant uses S-BONE), Graveburst, Fanbone |
| Nature | Thorn Coat, Briar, Wolf Howl (wolves: see §11), Regrowth, Locust |
| Guard | Blindrush, Bulwark, Warcry, Frostward |
| Mind | Telekinesis, Hex, Snare, Blinkstep, Veil, Dread |
| Traps | Ironjaw, Blightcask, Rimecaltrop, Thunderkiln (each needs set, arm, trigger and detonate) |
| Auras | Hearthward, Wrathbanner, Truesight, Kinship (each needs a quiet on-loop bed plus on and off) |

### 4.1 Ironvow (warrior) · P0
- **Body:** armoured melee fighter. Starts with the Rusted Iron Sword.
- **Character / Diablo:** oath-bound grinder who gets stronger the longer he fights. D2 Barbarian / Paladin.
- **Voice:** grim, low, clipped battle efforts.
- **Passive cues:**
  - Grit stack tick: a low anvil tap, rising in pitch.
  - Grit at 10 (outline glow): a steel ring plus a heartbeat.
  - **Last Stand**: a deep drum hit, then the world muffles.
  - **Iron Echo**: 3 m shockwave, dull smoky whump plus dust (E-PHYS).
- **Paths:** none yet. Kit notes are in the research study.

### 4.2 Longmark (archer) · P0
- **Body:** lightly armoured ranger. Starts with the Ashwood Short Bow.
- **Character / Diablo:** mobile hunter. D2 Amazon (bow) / D1 Rogue.
- **Voice:** tight breath, quiet focus, sharp exhale on release.
- **Passive cues:**
  - Stride stack: a soft leather patter tick.
  - **Running Shot**: a release on the move with a doppler.
  - **Slip**: phasing, cloth flick plus an air tear.
  - **Hunter's Line**: a mark, a thin taut string-hum on the target.
- **Paths:** none.

### 4.3 Cinderwake (elementalist) · P0
- **Body:** robed caster. Starts with the Gnarled Yew Wand.
- **Character / Diablo:** elemental weaver. D2 Sorceress / D1 Sorcerer.
- **Voice:** measured breath, short cast exhales, never shouted spell names.
- **Passive cues:**
  - Resonance fill: a rising element-tinted hum.
  - **Echo**: recast, a faint delayed duplicate of the cast.
  - **Prism**: three-element chord, layering fire, cold and lightning.
  - **Overflow**: barrier, a dull glassy shell plus crack on break.
  - **Triad**: a combined detonation.
- **Paths:** none.

### 4.4 Gravewell (blood and bone necromancer) · P0
- **Body:** robed, with bone fetishes. Starts with the Chipped Bone Dagger.
- **Character / Diablo:** grave-ledger keeper. D2 Necromancer.
- **Voice:** low and whispery, with dry efforts.
- **Passive cues:**
  - Toll gain: a single dull bell-tap plus a bone click.
  - **Death's Door**: heartbeat slows, choir breath.
  - **Collect**: corpse essence siphon, a wet-to-dry inhale.
  - **Ledger**: quill-scratch tick (shared with S-INK).
- **Servant:** Raise Bone servant uses S-BONE with the reassemble sound on summon.
- **Paths:** none.

---

## 5. P0: Martsirt NPCs (Act I hub)

**Voices.** Story lines may become **barks**. Record per NPC:
- greet (3)
- farewell (2)
- trade or service open and close
- "not enough gold"
- 2–3 idle mutters
- one night-variant line where the NPC has one

**Existing greeting samples:** `voice/{male,female}/*.ogg`.

**Foley.** NPC models use the civilian body bases (`NPC3D/bases/approved/`). No NPC-to-outfit mapping is documented, so footsteps default to a soft leather-shoe set plus a profession foley loop.

| NPC | Voice texture (from `voices.json`) | Idle and ambient foley |
|---|---|---|
| **Wolchen**, smith | Gruff baritone workman, warm underneath. Short declarative sentences, jokes at the customer's expense. Words: edges, rivets, hilt, coal. | Hammer on anvil, quench hiss, bellows, coal shovel; repair "ting" |
| **Ysara**, healer | Clinical, crisp imperatives, softer and slower at night. Words: arm out, stitch, thread, fever. | Mortar and pestle, bottle clink, bandage tear; heal chime |
| **Ilyra**, gate herald | Archaic, slow and formal, no contractions ("thou hast"). Words: gate, road, sisters, key. | Armour creak at rest, a key ring at the gate; waypoint and gate hum |
| **Quill**, scribe and tome-keeper | **Conflict:** `voices.json` says an anxious scholar with long self-correcting sentences and nervous jokes. `lore/quill_martsirt.md` says a soft-spoken, precise, faintly amused ex-citadel knight who speaks archaically. Record the voices.json register unless Brian decides otherwise. | Page turn, quill scratch, coffer lid creak (the unlocked tome coffer), Boss Stone socket clunk (S-INK) |
| **Bram**, logger | Rough, 2–6 word sentences, counts things. Words: blood, prints, sap, axe, six men. | Axe on wood, a **flute** (`tune()`, existing), bark rustle |
| **Mira**, taproom keeper | Teasing hospitality, rhetorical questions. Words: kettle, bench, round, stool. | Kettle whistle, mug thump, cloth wipe |
| **Orrin**, drunk ex bell-ringer | Slurred, self-mocking. Words: another, bell, rope. | Tankard slosh, hiccup, a distant bell-rope creak (S-BELL flavour) |
| **Ness**, homesick widow | Plain, quiet, repetitive. Words: next week, knife. | Knife on board, sighs |

**Shared:** the taproom room-tone (murmur, fire crackle) is ambient, not character work. It is noted only so Mira, Orrin and Ness sit inside it.

---
## 6. P1: Act I–II monsters

Families are placed in zones by `SANCTUARY_WORLD_FOR_AUDIO.md`. Each entry lists only what it adds to its core set.

### 6.1 Spawn Shaman (lesser demon caster) · P1
- **Body:** small (~3.5 ft) hooded red demon with a fang necklace and a skull staff. Hangs back and casts.
- **Diablo:** D2 Fallen Shaman (fireball, resurrects Fallen).
- **Sounds (S-IMP plus S-CULT chant):**
  - Idle: wheezy chant.
  - Aggro: a shrieked curse.
  - Attack: staff rattle (skull plus fangs) and a small fire bolt (E-FIRE: cast hiss, flight crackle, impact).
  - Special: **revive Spawnling**, a raspy incantation plus a reverse pop.
  - Hit: squeal.
  - Death: pop-puff plus the staff clattering.
  - Move: skitter plus fang-necklace jingle.
- **Paths:** `ART/monsters/families/14_red_demon.jpg`. No model.

### 6.2 Plague-Spitter (zombie, poison) · P1
- **Body:** obese, green-pustuled and hooded, in a leather apron, dripping bile. Slow waddle; spits bile at range.
- **Diablo:** D2 Plague Bearer / Gorebelly.
- **Sounds (S-FLESH plus E-POIS):**
  - Idle: bubbling belly gurgle.
  - Aggro: wet belch.
  - Attack: retch, then a spit arc and a splat puddle that hisses.
  - Hit: wet slap plus a pustule pop.
  - Death: **burst** (a green spray) then a heavy collapse.
  - Move: heavy squelch steps with apron flap.
- **Paths:** `families/01_zombie.jpg`.

### 6.3 Frost-Bound Sentinel (skeleton, cold) · P1
- **Body:** skeleton in icy plate with a longsword. Glowing blue eyes, frost mist. Slow, heavy.
- **Diablo:** D2 Horror / cold Burning Dead.
- **Sounds (S-BONE plus S-PLATE plus E-COLD):**
  - Idle: frost-groan bed with thin ice tinkles.
  - Aggro: helm rasp plus a cold breath hiss.
  - Attack: longsword cleave plus a frost crack on hit.
  - Special: possible chill on hit, a glassy crackle.
  - Death: shatter of bone **and** ice (glassy, bright-on-dark).
  - Move: plate clank on crunching frost.
- **Paths:** `families/02_skeleton.jpg`.

### 6.4 Rope-Shade (ghost, phys) · P1
- **Body:** a hovering, translucent wailing nun with a noose rope trailing. Grey wisps. Drifts and phases.
- **Diablo:** D2 Ghost / Wraith.
- **Sounds (S-SPECTRE plus E-PHYS smoke):**
  - Idle: a strangled sob loop and rope creak, as of a hanging rope.
  - Aggro: wail.
  - Attack: rope lash whoosh, a noose-tighten creak, a choke grab.
  - Hit: a breath flicker.
  - Death: dissolve with a final exhale and wisps rising; the rope drops (the only physical sound).
  - Move: none, only a cloth-in-wind drift.
- **Paths:** `families/03_ghost.jpg`.

### 6.5 Bell-Wraith (ghost, lightning) · P1
- **Body:** a hooded spectral figure ringing a handbell. Violet-white lightning.
- **Diablo:** D2 Spectre / Apparition (charged bolts).
- **Sounds (S-SPECTRE plus S-BELL plus E-LIGHT):**
  - Idle: distant handbell.
  - Aggro: a hard triple ring.
  - Attack: a bell swing that releases dry arcs.
  - Hit: a static crackle.
  - Death: the bell cracks, then a dissolve.
- **Paths:** `families/03_ghost.jpg`.

### 6.6 Ledger Imp (imp, phys) · P1
- **Body:** small, brown and gaunt, horned and clawed. Hops and swipes. Also summoned 3 at a time by the Tallyman's Audit.
- **Diablo:** D1 Imp / D2 Fallen.
- **Sounds (S-IMP plus S-INK):**
  - Idle: nasty giggle plus a page rustle.
  - Attack: claw swipes.
  - Death: pop-puff that sheds **loose pages**.
  - Move: claw-foot skitter.
- **Paths:** `families/04_imp.jpg`.

### 6.7 Cinder Imp (imp, fire) · P1
- **Body:** small and red, with a burning-coal fist and a glowing mouth.
- **Diablo:** D2 Imp (Act V).
- **Sounds (S-IMP plus E-FIRE):**
  - Idle: coal-tick and ember crackle.
  - Attack: a fire-punch whump, or a short flame spit.
  - Death: ember pop with a hiss and smoke.
- **Paths:** `families/04_imp.jpg`.

### 6.8 Vesper Caller (caller) · P1
- **Body:** a man in a black robe, swinging a censer on a chain, with a blue-glowing rune staff. Raises the dead and casts.
- **Diablo:** D2 Greater Mummy (raiser) / Fallen Shaman.
- **Element:** blue glow, so cold per the colour rule. Not confirmed; see ambiguities.
- **Sounds (S-CULT plus E-COLD):**
  - Idle: censer chain sway with low chanting.
  - Aggro: a bark of liturgy (non-words).
  - Attack: cold bolt.
  - Special: **raise dead**, a rune hum plus the S-BONE reassemble or S-FLESH rise.
  - Hit: grunt plus a censer clank.
  - Death: robe crumple, rune decal fizzle, the censer rolls.
- **Paths:** `families/05_caller.jpg`.

### 6.9 Pyre Caller (caller, fire) · P1
- **Body:** robe with red runes. Casts fire from the hand.
- **Diablo:** D2 Fallen Shaman / Zealot.
- **Sounds (S-CULT plus E-FIRE):**
  - Attack: hand-flame (dark roar) and a fire bolt.
  - Death: crumple plus the embers gutter.
- **Paths:** `05_caller.jpg`.

### 6.10 Gibbet Remains (corpse, phys) · P1
- **Body:** a rotted corpse locked in a rusted, spiked iron gibbet cage with chains. Moves slowly in a hop-drag with the cage.
- **Role:** guessed (cage-ram or slow melee).
- **Diablo:** D2 Hungry Dead, gibbet-flavoured.
- **Sounds (S-FLESH plus iron):**
  - Idle: cage creak and sway, chain clink.
  - Attack: a cage-slam ram (iron clang plus spikes).
  - Hit: iron bars ringing.
  - Death: the corpse collapses inside the cage with a rattle, then iron settles.
  - Move: iron scrape and chain drag on stone.
- **Paths:** `families/06_corpse.jpg`.

### 6.11 Plague Bloat (corpse, poison) · P1
- **Body:** a shrouded corpse covered in green boils, inside a green miasma. Waddles close and bursts.
- **Diablo:** D2 corpse-exploding bloated dead.
- **Sounds (S-FLESH plus E-POIS):**
  - Idle: gas wheeze plus bubbling.
  - Special: **swell-up** telegraph (stretching skin creak, rising gurgle).
  - Death: goo burst plus a poison-cloud hiss.
- **Paths:** `06_corpse.jpg`.

### 6.12 Cinder Tollman (brute, fire) · P1
- **Body:** bald brute with glowing ember cracks across the skin. Fire attacks.
- **Diablo:** D2 Minion of Destruction (fire).
- **Sounds:** the Razor Tollman set with a stronger E-FIRE layer.
  - Idle: a constant smoulder and crackle bed.
  - Attack: ember-burst slams.
  - Death: the body gutters out like a hearth (hiss, then collapse).
- **Paths:** `families/07_brute_v2.jpg`.

### 6.13 Grove Mauler (bear, phys) · P1
- **Body:** a large brown bear with moss and brambles; arrows and spears stick out of its hide. Charges, swipes, rears.
- **Diablo:** D2 Grizzly / Werebear.
- **Sounds (S-BEAR plus S-THORN):**
  - Idle: breathing, bramble rustle, and the stuck arrows clacking against each other.
  - Aggro: roar.
  - Attack: swipe plus claw rake, maul bite, rear-up slam.
  - Death: a heavy fall with a dust ring.
- **Paths:** `families/08_bear.jpg`. No starter model.

### 6.14 Rime Bear (bear, cold) · P1
- **Body:** a frost-furred bear with icicles, blue eyes and frost breath.
- **Sounds (S-BEAR plus E-COLD):**
  - Idle: frost-breath hiss.
  - Special: frost-breath cone.
  - Hit: icicles tinkle.
  - Death: a heavy fall with ice cracking.
- **Paths:** `08_bear.jpg`.

### 6.15 Blackroot Adder (snake, phys) · P1
- **Body:** a large, black, horned serpent with red veins, among obsidian spikes. Fast strikes; may burrow (the burrow quirk).
- **Diablo:** D2 Sand Viper / Tomb Viper.
- **Sounds (S-SERPENT):**
  - Idle: hiss plus scales on stone.
  - Attack: strike snap.
  - Death: coil-fade slither.
- **Paths:** `families/09_snake.jpg`.

### 6.16 Venom Asp (snake, poison) · P1
- **Body:** a hooded cobra in a green mist, fangs dripping.
- **Sounds (S-SERPENT plus E-POIS):**
  - Special: hood flare (a leathery snap), a spit stream (the spit quirk).
  - Hit: wet bite sound.
- **Paths:** `09_snake.jpg`.

### 6.17 Thin Laugher (raver, phys) · P1
- **Body:** a wiry humanoid in a grinning jester hood and rags, with a sickle in each hand. Sprints in packs.
- **Diablo:** D2 Flayer.
- **Sounds (S-LAUGH):**
  - Idle: giggling.
  - Aggro: a breathless sprint-laugh.
  - Attack: double sickle swish plus slice (a leap variant for the leap quirk).
  - Hit: choked laugh.
  - Death: **burst**, the laugh cut off.
  - Move: fast bare-foot slap with rags flapping.
  - Revival by Ghel's Sixth Voice: a gasp that turns into laughter.
- **Paths:** `families/10_raver.jpg`.

### 6.18 Storm Laugher (raver, lightning) · P1
- **Body:** purple, with lightning sickles and glowing eyes.
- **Sounds (S-LAUGH plus E-LIGHT):** arc-crackling sickles, dry snaps on hit, and a static burst on death.
- **Paths:** `10_raver.jpg`.

### 6.19 Purse-Jaw (worm, phys) · P1
- **Body:** a huge segmented worm with a ring-toothed maw that spills coins. Burrows and erupts.
- **Diablo:** D2 Sand Maggot.
- **Sounds (S-MAW plus S-COIN):**
  - Idle: subterranean churn.
  - Special: burrow, a rumble moving underground.
  - Attack: erupt plus maw bite.
  - Death: goo burst and **a spray of coins** (a loot gag).
- **Paths:** `families/11_worm.jpg`.

### 6.20 Bile Crawler (worm, poison) · P1
- **Body:** a green, spined worm, dripping bile.
- **Sounds (S-MAW plus E-POIS):** a bile-spit attack, spine rattle, and a bile burst on death.
- **Paths:** `11_worm.jpg`.

### 6.21 Corrupted Phimn, Winged Caster (form A) · P1
- **Body:** a 1.42 m female demon-elf with bat wings and horns; the red mon-runes are always lit. **Hovers** about 0.32 m off the ground and glides. Casts from the hand in **4 variants: fire, ice, lightning, poison**.
- **Character:** a cold, contemptuous fallen Phimn.
- **Diablo:** D2 Dark Spearwoman / Succubus.
- **Sounds:**
  - Idle: slow leathery wing beats (hover loop), a low female hiss and breath.
  - Aggro: a sharp contemptuous cry.
  - Attack: `attack_cast` (two-hand) and `attack_cast_1h`, each with a wind-up breath and an elemental release. Use the E-FIRE, E-COLD, E-LIGHT or E-POIS stem for each variant.
  - Hit: wing flinch flap plus a female pain hiss.
  - Death: wings fold, she drops from the hover with a body thud and the runes dim.
  - Move: wing-glide whoosh, no footsteps.
  - The red mon-runes have no sound by default (an optional faint hum).
- **Paths:** `ART/monsters/corrupted_phimn/` (caster sheet `corrupted_phimn_caster.jpg`). Model `NPC3D/monsters/corrupted_phimn/out/corrupted_phimn_caster.glb` (clips idle, move, attack_cast, attack_cast_1h, hit, death). Previews `.../previews/A_*`.

### 6.22 Corrupted Phimn, Feral Stalker (form B) · P1
- **Body:** the same race, moving on all fours. Feral ambusher that sniffs, pounces and claws. Same 4 element variants.
- **Diablo:** D2 Dark Stalker / Succubus.
- **Sounds (S-IMP claw layer, adult female and feral):**
  - Idle: low growl.
  - Special: **`sniff`**, an animal sniff that also works as a "found you" cue.
  - Aggro: snarl.
  - Attack: `attack_claw` rake; `attack_pounce` (leap whoof, landing thump, pin) with an elemental tint on the claws.
  - Hit: a yowl.
  - Death: collapse.
  - Move: fast four-limb padding with nail clicks, a grass rustle for the ambush.
- **Paths:** `NPC3D/monsters/corrupted_phimn/out/corrupted_phimn_feral.glb` (clips idle, run, sniff, attack_claw, attack_pounce, hit, death). Previews `.../previews/B_*`.

### 6.23 Critters · P1
Ambient and killable wildlife.

| Critter | Sounds |
|---|---|
| **Grey Hare** | Soft hop thumps, grass rustle, startle squeak, tiny death squeal |
| **Crypt Rat** | Squeaks, scurry on stone, nibbling, splat death (D1 nostalgia) |
| **Ash Crow** | Caw (dry, ashy), wing flap takeoff, perch rustle, feather-puff death |
| **Briar Hart** | Hoof steps, snort, alarm bark, bramble crash fleeing, collapse |

---
## 7. P1: Act I–II bosses

All bosses also use the **boss shared kit** (§2). Attacks are as named in `sanctuary/bosses.md`. **Every attack needs its own telegraph wind-up cue** (wind-ups run 0.35–1.5 s), and the commit sound must line up with the telegraph end. Boss art is in `ART/monsters/bosses/`. No boss has a 3D model yet.

### 7.1 The Saltmouth · P1 (existing boss, sewer, mlvl 5)
- **Body:** a bloated, salt-crusted, drowned sewer giant with an unhinged jaw, rotted smock, and hooks and chains at the belt. Wades.
- **Character / Diablo:** gluttonous drowned thing. D2 Corpsefire / D1 Butcher's den mood.
- **Sounds (S-FLESH giant plus S-BRUTE hooks plus E-POIS brine):**
  - Idle: a phlegmy gargle, water-slosh steps.
  - Attacks:
    - **Brine Spit**: throat gurgle, then a projectile spray and a splash hiss.
    - **Gulp**: a vacuum inhale pull, the jaw unhinging with a bone crack.
    - **Bite**: a huge wet chomp.
    - **Bilge Flood**: a grate gush and rising water.
  - Death: a gurgling collapse into water, then a brine-ink dissolve.
- **Paths:** `bosses/act1_01_saltmouth.jpg`.

### 7.2 Ash Wraith · P1 (existing, wild, mlvl 9)
- **Body:** a charred, hooded penitent wraith in an iron execution collar, its chain trailing into ash. Rises from a burned stake.
- **Diablo:** D2 Blood Raven, in role (an early fallen-penitent miniboss).
- **Sounds (S-SPECTRE plus E-FIRE):**
  - Idle: a smoulder bed, the collar-chain dragging through ash, a whispered penitent sob.
  - Attacks:
    - **Ash Claw**: an ember-rake hiss.
    - **Cinder Blink**: implode, then a cinder burst behind the player.
    - **Ember Ring**: a ground-flare nova roar.
  - Death: dissolve to embers, the chain drops.
- **Paths:** `bosses/act1_02_ashwraith.jpg`.

### 7.3 Melakirniz (twins) · P1 (existing, wild, mlvl 9)
- **Body:** a pair of gaunt, ram-horned feral demons in matching broken-chain iron collars. One crouches and pounces; the other howls.
- **Diablo:** a D2 Moon Clan unique pack.
- **Sounds:** S-IMP pitched down and made beefier. Each twin needs **two distinct voices** (A rasp, B howl).
  - Attacks:
    - **Rend**: hooked-claw combo.
    - **Pounce**: leap, then a pinning thud.
    - **Twin Howl**: a paired howl in harmony plus a collar-chain jangle.
  - Death: each collapses. Killing one makes the other give a grief howl.
- **Paths:** `bosses/act1_03_melakirniz.jpg`.

### 7.4 Scar-Eye · P1 (existing, root, mlvl 17)
- **Body:** a huge scarred brown bear with a milky eye, broken spears and arrows in its hide, a rusted trap and chain on its foreleg, and brambles in its fur.
- **Diablo:** a D2 Act I unique beast.
- **Sounds (S-BEAR XL plus S-THORN):**
  - Constant layer: the leg trap clanks as it walks.
  - Attacks:
    - **Maul**: a swipe.
    - **Bramble Charge**: a galloping rumble; if it hits a tree, a trunk crash and a dazed whine (stunned 1.5 s).
    - **Scar Roar**: a fear nova, the biggest roar.
  - Death: a huge collapse.
- **Paths:** `bosses/act1_04_scareye.jpg`.

### 7.5 Vessaline, the Thorn Abbess · P1 (Act I boss, mlvl 35)
- **Body:** a tall abbess in a black, rot-green habit and wimple, wearing a briar crown. Her face is stitched and pierced with thorns; briar vines run through her robes. v2 gives her greyer undead skin (pending approval). Glides.
- **Character / Diablo:** a serene, sickly-holy matriarch: "a wound is also a door". Andariel.
- **Voice:** an aged female voice, whispered-sung, with a hymnal cadence. She **sings** (Hymn of Rot). Record a dark wordless hymn plus 3–4 short lines.
- **Sounds (S-THORN plus S-FLESH plus E-POIS and E-BLOOD):**
  - Attacks:
    - **Thorn Veil**: a fan of 5 thorn needles whistling out.
    - **Sting-Step**: a glide-dash with a briar line ripping up behind.
    - **Rosary Lash**: a chain whip, hook bite and reel.
    - **Choir Crush**: a hymnbook slam (a heavy leather-and-wood boom).
    - **Hymn of Rot**: the sung zone, with a floor rot-hiss; the rose-window light sits in a slightly warmer, safer tone.
    - **Thorn Bride**: pews splinter and briar nuns rise (see §11).
  - Pews: burn and crack sounds.
  - Phases: Choir, Hymnal, Bloomrage.
  - Death: falls to her knees, the hymn breaks off, the briars wither, then a dissolve to rot-ash.
- **Paths:** `bosses/act1_05_vessaline.jpg`, `act1_05_vessaline_v2.jpg`.

### 7.6 Bilge-Wight · P1 (existing, hull, mlvl 11)
- **Body:** a frost-rimed drowned boatswain wight in a rotted sea-coat. Below the waist it turns to cold mist between broken hull planks. Carries a rusted anchor on a chain.
- **Diablo:** a drowned D2 Wraith unique.
- **Sounds (S-SPECTRE plus E-COLD plus ship timber):**
  - Idle: hull creak, dripping, a cold breath.
  - Attacks:
    - **Hull Wail**: a cone of cold breath with a wail.
    - **Through the Planks**: sinks with a water gulp, a ripple travels, then it bursts up with plank splinters.
    - **Anchor Drag**: an anchor-chain run-out and a heavy drag pull.
  - Death: dissolves into mist; the anchor thuds down.
- **Paths:** `bosses/06_bilgewight.jpg`.

### 7.7 The Tallyman of the Hollow · P1 (side, Smuggler's Hollow, mlvl 14)
- **Body:** a hunched, sickly-green smuggler's clerk in a mouldy robe and apron. Carries a quill, a ledger chained to the belt, an abacus and keys. His grafted twin-blade knife-hand belonged to Jas's brother.
- **Character / Diablo:** a muttering, counting bookkeeper. Treehead Woodfist / Coldcrow.
- **Voice:** a dry, whispery male voice that counts aloud ("…seven… eight…").
- **Sounds (S-COIN plus S-INK plus E-POIS):**
  - Attacks:
    - **Knife Count**: two knife swipes plus a bleed.
    - **Red Cask Toss**: a lob whoosh, a cask landing thud, then fire (the casks are fire, E-FIRE).
    - **Audit**: abacus clacks and a ledger slam that summon 3 Ledger Imps.
  - Arena: crates splintering, red casks exploding.
  - Death: collapses, the ledger spills pages, coins and keys scatter.
- **Paths:** `bosses/07_tallyman.jpg`.

### 7.8 Ossgrind, the Reliquary Grub · P1 (Act II boss, mlvl 50)
- **Body:** a colossal armoured grub-centipede with frost-rimed dark chitin. Saints' skulls, bones and gilded caskets are fused into its plates, with a broken golden halo, hooked legs and serrated mandibles around a toothed maw. Burrows.
- **Character / Diablo:** a ravenous relic-eater. Duriel.
- **Sounds (S-MAW XL plus chitin plus S-BONE relic rattle plus E-COLD):**
  - **Rime Brand aura**: a constant frost bed.
  - Movement: many-leg clatter on stone, with the skulls and caskets rattling on its back.
  - Attacks:
    - **Mandible Snap**: an every-third double click-chomp.
    - **Burrow Lunge**: a dust-ring rumble, then an eruption.
    - **Grave Tongue**: a wet tongue lash and pull.
    - **Mandible Frenzy**: 4 rapid bites.
    - **Relic Vomit**: a retch, bone arcs, then a shatter into frost puddles.
  - **Gorge**: eats a coffin (wood crunch, gulp, heal), interruptible.
  - Death: the chitin cracks and shatters, the halo rings as it hits the floor, then a dissolve.
- **Paths:** `bosses/09_ossgrind.jpg`.

### 7.9 Ghel, the Laugh That Stays · P1 (side, Bitter Ascent, mlvl 32)
- **Body:** a gaunt hooded pilgrim with a frozen, too-wide grin, a bell-hung staff and a pilgrim shell badge, wrapped in a storm full of ghostly laughing faces. Stands on a cliff shelf in high wind.
- **Character / Diablo:** "the wind wearing the sixth laugher". Bishibosh / Rakanishu.
- **Sounds (S-LAUGH plus S-SPECTRE plus S-BELL staff plus E-COLD plus a wind bed):**
  - Idle: laughter carried on the wind, with staff bells.
  - Attacks:
    - **Cackle**: a freezing laugh cone, with frost-crack streaks.
    - **Edge Gust**: a wind shove.
    - **Sixth Voice**: revives ravers as laughers.
    - **Hysteria**: a giddy pulse on the player.
  - Death: the laughter thins into the wind, then a final bell.
- **Paths:** `bosses/08_ghel.jpg`.

---

## 8. P1: NPCs (Briarwood, Qadren and the Salt House) and the civilian pool

| NPC | Voice texture | Foley |
|---|---|---|
| **Holt**, ferryman | Deadpan male, prices everything. Words: fare, skiff, fog, ten thousand. | Oar creak, skiff knock, rope coil |
| **Myrine**, spear-hand | Cold, grieving, clipped female voice. Words: bank, bow, spear. (No female greeting sample yet.) | Spear-butt tap, leather creak |
| **Orithya**, ex-citadel scout | Military report cadence. Words: line, plate, drill. | Plate shift, buckle |
| **Sable**, sly merchant | Sales patter, sly, fast female voice. Words: shelf, price, bargain. | Coin count, jar clink |
| **Orlem**, desert headman | Warm salesman's voice. Words: shade, water. | Water skin slosh, robe swish, sand step |
| **Heska**, guard | Few words, flat female voice. Words: stone, door. | Mail and spear at rest |
| **Vetch**, gambler | Odds talk, quick and smiling. Words: house, owe. | Dice rattle and roll, coin flip |
| **Tamsin**, cook-innkeeper | Homely female voice. Words: soup, pot, salt. | Ladle in pot, bubbling stew |
| **Ayla** (Phimn) | Not defined in `voices.json`. Suggest a quiet, wary female voice with a slight otherness (same race as the Corrupted Phimn, uncorrupted). | Soft white-leather creak, light footsteps |

- **Ayla paths:** model `NPC3D/clothing/ayla_phimn/npc_f_ayla_phimn_ayla_phimn_body.glb`; art `ART/races/ayla_phimn_final.jpg`.
- **Civilian outfit pool** (`ART/civilian_male/01–10`, `ART/civilian_female/01–12`): one generic townsfolk foley pack. It covers cloth rustle (linen, wool, leather), shoe types (bare, wrapped, leather, clog), and generic murmurs (male and female, wordless) for crowds. None of the outfits is mapped to a named NPC.

---
## 9. P2: Later-act, Margins and uber bosses

### 9.1 Kessane, the Toll Baron · P2 (side, Toll Arch, mlvl 50)
- **Body:** a towering undead gatekeeper knight in blackened plate with a slit great helm that glows ember red. Wears rotted gate tabards and a portcullis pauldron, with padlocks, a key ring, a purse and toll scales at the belt. Fights with a halberd.
- **Diablo:** Bonebreaker / the Countess (a keyed side boss).
- **Voice:** a hollow, helm-boomed voice ("Toll.").
- **Sounds (S-PLATE plus S-COIN plus E-FIRE embers):**
  - Attacks:
    - **Toll Strike**: a halberd sweep with a mana-drain siphon.
    - **Portcullis Drop**: a winch ratchet, then an iron gate slam.
    - **Brand of Debt**: a sizzling brand; a "paid" chime after 4 hits.
    - **Tabards of the Dead**: S-BONE raise ×4.
  - Death: collapses in plate, padlocks and keys rain down, the helm glow gutters.
- **Paths:** `bosses/10_kessane.jpg`.

### 9.2 Inquisitor Halvane, the Confessor-Mind · P2 (Act III boss, mlvl 57)
- **Body:** a gaunt inquisitor in a mitre and black-crimson vestments. A hollow ribcage full of lightning shows through his torn chest, and lightning comes from his mouth and hands. A gibbet cage hangs from a chain, and a chained confession book hangs at his back.
- **Diablo:** Mephisto.
- **Voice:** an inquisitor's sermon, cold, close and whispered. He speaks your rite aloud (**Dictation**), so the voice must work as a "reading aloud" overlay.
- **Sounds (S-CULT plus S-INK plus E-LIGHT plus mind whispers):**
  - Attacks:
    - **Confession Bolt**: a zig-zag snap path.
    - **Verdict**: a beam charge with a lane hum, then a discharge.
    - **Cage of Guilt**: a cage drop with an iron clang and lock.
    - **Mind Ward**: a dull glass shell, with a reflect "tick".
    - **Council of Three**: fire, cold and lightning cultists wake (§11).
  - Arena: a black-water moat lap.
  - Death: the lightning drains out of his ribcage, the book falls shut.
- **Paths:** `bosses/11_halvane.jpg`.

### 9.3 Spire-Heart · P2 (existing, weald, mlvl 72)
- **Body:** a colossal bear fused with a corrupted tree: root-woven hide, a thorned spire along the spine, green sap veins.
- **Diablo:** a Treehead or Thorned Hulk analogue.
- **Sounds (S-BEAR plus S-THORN plus timber creak plus E-POIS sap):**
  - Attacks:
    - **Root Slam**: a slam with root lines tearing through the soil.
    - **Spire Thorns**: thorn patches erupting.
    - **Graft**: a root-suck heal; a cut-root snap interrupts it.
  - Death: a timber fall with a groan-crack.
- **Paths:** `bosses/12_spireheart.jpg`.

### 9.4 Goreth-Vaal · P2 (existing, weald, mlvl 72)
- **Body:** a cracked black-obsidian demon with violet light inside, wearing a bear's hide and head as cloak and helm, chained at the back. Its second form is a jagged shard figure.
- **Diablo:** Izual (a fallen angel in borrowed flesh).
- **Sounds:**
  - Form 1: S-BEAR muffled under the hide, with glass grinding beneath.
  - Form 2: glass chime-grind, shard whistle.
  - Attacks:
    - **Wearing Bear**: swipes.
    - **Black Glass**: shards land and keep a faint ring while they stay as hazards.
    - **Say Its Name**: a glyph; a rising whisper-pressure cue counts the 1.2 s.
    - **Shed the Bear**: at 40%, a wet hide tear and the obsidian unveils.
  - Death: the obsidian shatters, then a violet dissolve.
- **Paths:** `bosses/13_gorethvaal.jpg`.

### 9.5 The Castellan · P2 (existing, castle4, mlvl 90)
- **Body:** a hulking warden in sooty plate, castle surcoat and great helm, with keys and chains. Carries a spiked mace and a tower shield.
- **Diablo:** Shenk the Overseer / Griswold.
- **Sounds (S-PLATE plus S-BRUTE chains):**
  - Attacks:
    - **Castle Mace**: a swing.
    - **Shield Rush**: a tower-shield charge with a wall-stop boom.
    - **Murder Holes**: burning oil (pour gurgle, hiss, splash fire).
  - Death: a heavy collapse in plate.
- **Paths:** `bosses/15_castellan.jpg`.

### 9.6 Vhorr-Akesh, the Ember Saint · P2 (Act IV boss, mlvl 87)
- **Body:** a colossal false saint in scorched bishop vestments and a cracked mitre, with ember-cracked skin and a burning halo. Fire pours from his mouth. He swings a chained censer crackling with lightning, with bone relics chained on his back.
- **Diablo:** Diablo.
- **Voice:** a huge, beatific, cracked preacher-roar.
- **Sounds (E-FIRE heavy plus E-LIGHT plus censer chain plus S-BONE relics):**
  - Attacks:
    - **Saint-Breath**: a channelled fire hose (a loop with sweep panning).
    - **Ash Halo**: a ring nova.
    - **Reliquary Prison**: a bone-ring eruption (Diablo's Bone Prison).
    - **Font Lightning**: forked bolts.
    - **Cinder Stomp**: a stomp with 3 cinder lines.
    - **Saint's Water**: burning holy water with the potion-denied fizz.
  - Death: dissolves to embers, the halo cracks.
- **Paths:** `bosses/14_vhorr.jpg`.

### 9.7 The Hollow King · P2 (existing, vault, mlvl 93)
- **Body:** a colossal headless king in corroded black-gold plate and an ermine mantle, with a floating spiked crown over the empty gorget. Violet starlight shows in the broken chest; he carries a greatsword, with ghost courtiers behind him.
- **Diablo:** D1 Skeleton King (Leoric).
- **Voice:** none (headless). A crown hum and a voice from the chest void.
- **Sounds (S-PLATE plus a starlight hum plus S-SPECTRE courtiers):**
  - Attacks:
    - **Crown Cleave**: a wide cleave.
    - **Hollowing**: a crown pull vortex, then the cleave.
    - **Hollow Court**: raises 4 court dead.
    - **Falling Crown**: falling star fragments (foreshadowing Nul-Osse).
  - Death: the plate falls apart, the crown drops with a long ring.
- **Paths:** `bosses/17_hollowking.jpg`, `17_hollowking_v2.jpg` (pending).

### 9.8 Ysmer, Who Wrote the Plague · P2 (Act V boss, mlvl 93)
- **Body:** a giant hooded scribe-demon on a throne of stacked tomes. His robes dissolve into ink and crawl with script. He holds a quill, grimoire and ink pot, with chained books orbiting him and a spine of books down his back.
- **Diablo:** Baal (throne waves, clone).
- **Voice:** a layered, quill-dry whisper with a deep undertone.
- **Sounds (S-INK all):**
  - Attacks:
    - **Ink Tide**: a floor wave.
    - **Errata**: a curse; 3 pip ticks, and hits heal him with an "ink drink" sound.
    - **Festering Ink**: pools that sprout tendrils.
    - **Margin Note**: a teleport to a shelf, with a page whip.
    - **Footnote**: a clone split, a doubled voice.
    - **The Last Word**: a 3 s channel, writing your name with a rising quill-scratch crescendo, then a room-wide blast. Each of the 4 glyphs makes a step-on click.
  - Throne waves: 4 waves of risen (S-FLESH and S-BONE).
  - Shelves re-shelving: wood grind.
  - Death: dissolves to ink.
- **Paths:** `bosses/16_ysmer.jpg`.

### 9.9 Margins and pinnacle

| Boss | Body | Key sounds | Death | Path |
|---|---|---|---|---|
| **Bell-Wright** (Margins I, cold/time) | A colossal drowned bell-keeper: a cracked bronze bell for a torso, gears fused into the back, a bell-mace, standing in icy water on a clock face | S-BELL, clock ticks, E-COLD. **Toll** nova, **Hour Hand** sweep (a giant gear grind with a ticking approach), **Echo of You** (a ghost replay of the player's own sounds, filtered and delayed), **Rewind** (a reversed clock spin), **Drowning Peal** (rising water per peal) | Shatter: the bell cracks, the gears spill | `bosses/18_bellwright.jpg` |
| **Mother Wick** (Margins II, fire/mana) | A towering veiled abbess dripping tallow, with a crown of burning candles, a half-melted wax face, a wick whip and a lantern | S-WAX plus E-FIRE. **Wick Lash**, **Candlefall** wax rain, **The Transposition** (a 3 s cracking-orb build, then a swap "whump"), **Snuff** (rings guttering out), **Tallow Saints** (rise, then melt into puddles that drain mana) | Dissolve: melts to wax and smoke | `bosses/19_motherwick.jpg` |
| **The Assessor** (Margins III, phys/lightning) | An undead magistrate with a lead death-mask, robes, coin chains and a brass scale | S-COIN plus E-LIGHT. **Gavel** slam, a **Levy** stack counter (a coin-stacking tick that climbs, then "Court Collects", a lightning crack), **Bailiffs** pin (iron manacles), **Final Verdict** lane beam. A "Hush" cue when stacks drop | Collapse, coins spill | `bosses/20_assessor.jpg` |
| **Nul-Osse** (Margins IV, magic/gravity) | **Legless, always hovering.** A skeletal star-corpse of meteoric iron and bone with a fused broken crown and a collapsing star in its chest | No footsteps at all; a sub-bass hover drone and an iron-bone creak. **Event Horizon** (a sub-pressure pull), **Starshed** (an outward push), **Orbitals** (5 rocks whirring, then released), **Collapse** (the disk ring cracks and falls), **Weightless** (muffled drift). Edge fall: a falling whoosh | Shatter, then a star implosion | `bosses/21_nulosse.jpg` |
| **Errata, the Copyist** (Margins V, magic/copy) | A gaunt four-armed scribe with a mirror-silver mask, quills and scraping knives | S-INK. **Fair Copy** replays the player's Bound Rite sound, ink-tinted. **Inversion**, **Plagiarism** (a buff being pulled away), **Ink Lance**. Knife-scrape vellum | Dissolve to ink, the mask shatters | `bosses/22_errata.jpg` |
| **The Warm Binding** (pinnacle, grief) | A towering hooded figure built from Quill's tome: a leather binding, page robes, a book spine and chains | S-INK plus E-GRIEF. **Grief** aura (choked breath and an ash choir), **Reading** (an eye-page turn cue), **Sentence** (a crawling word-wave of whispers), **Chapter Break** (a giant page turn), **The Nameless** (3 unwritten, §11) | Dissolve: pages fall, the book closes | `bosses/23_warmbinding.jpg` |
| **Ysmer Unbound** (uber) | Ysmer, skull-faced, with a spiked crown and robes tearing into an ink vortex | The Ysmer set plus the uber layer: ×2 Footnotes, a harsher voice, a vortex loop. Uber intro with the keys orbiting and shattering | Ink-vortex collapse | `bosses/24_ysmer_unbound.jpg` |
| **The Unbinding** (uber, Warm Binding Decided) | The tome figure glowing ember-orange, sparks rising from the pages | The Warm Binding set plus E-FIRE crackle on the pages. Summons uber copies of the 5 act bosses (a reuse of their vocals, ghost-filtered) | Dissolve to embers and burning pages | `bosses/25_warmbinding_decided.jpg` |

---

## 10. P2: NPCs (coast road, Highmarket, ash camp, castle)

| NPC | Voice texture | Foley |
|---|---|---|
| **Wynn** | Gravedigger, low and patient. Words: dig, salt. | Shovel in earth, salt pour |
| **Rusk** | Reluctant captain, wry. Words: paint, HOPE, tents. | Paintbrush, tent canvas |
| **Sera** | Mud surgeon, quick blunt jokes. Words: sew, mud. | Needle and thread, basin |
| **Odder** | Proud young smith, brags. Words: heat, hinge. | A lighter hammer than Wolchen's |
| **Iskra** | Cliff widow, quiet specifics. Words: shoes, rope. (No female greeting sample.) | Rope coil |
| **Moth** | Fen woman, at most 1 proverb in 6 lines. Words: plank, lamp, boot. (No female greeting sample.) | Boot in mud, lamp creak |
| **Calder** | Ashamed and apologetic. Words: purse, stair. | — |
| **Hask** | Toll grandson, bitter-funny and sarcastic. Words: toll, coin. | Coin flip (S-COIN) |
| **Kell** | Toll grandson, dry and flat. Words: gate, key, nineteen years. | Key ring |
| **Nim** | Coward wit who rushes. Words: laugh, wind. | Wind |
| **Vellum** | Grim crypt warden who talks to Lute *through* you. Words: chalk, slab. | Chalk on stone |
| **Lute** | Frightened diver, short and jumpy. Words: bell, ledge. | Wet drip, bell (S-BELL) |
| **Brine** | Gentle, slightly odd lamp-keeper. Words: lamp, light. | Lantern creak (S-WAX) |
| **Jas** | Smuggler accountant with gallows humour. Words: sum, cask, percent. | Cask knock, quill |
| **Piet** | Ex-gaoler, soft and careful. Words: keys, cells, organ. | Keys |
| **Ors** | Unfrocked priest who quotes liturgy and then contradicts it, at most 1 in 4 lines. Words: pews, bell. | Rosary |
| **Cal** | Mercenary parts buyer. Words: parts, pay. (Has a female greeting sample.) | Scale and parts clatter |
| **Pell** | Gate-crier with an announcer's cadence. Words: east, north, bells. | Handbell |
| **Hesta** | Lampwick innkeeper, counts things, wry. Words: list, bed. | Tankard, ledger |
| **Voss** | Drunk accountant who tells jokes. Words: audit, stool. | Mug |
| **Ilen** | Nervous. Words: lamps, door. | — |
| **Sarn** | Bitter, terse camp boss. Words: road, camp. | Ash-camp fire |
| **Vesper** | Fence who whispers, nervous. Words: loot, floor, quiet. | Sack rustle |

None of these NPCs has a model. All P2 NPCs use the civilian foley pool.

---
## 11. Upcoming and undesigned models that will need sounds

These are named in the design docs but have no sheet or model yet (or the model is missing). Plan their sound now so the shared sets cover them.

| Item | Source | Pri | Sound plan |
|---|---|---|---|
| Raise Bone servant (Gravewell / any **summon** rite) | skills, rites | P0 | S-BONE: summon reassemble, an obedient follow-step, attack, shatter on expiry |
| Wolf Howl wolves (nature rite; the Kinship perk mentions "Wolf Howl wolves") | class_passives | P0/P1 | A new small **S-WOLF** set: howl on summon, pant, snarl, bite, paw steps, a yelp death, a fade-out on expiry |
| Female Shambler model (the sheet shows a woman in a dress; no glb) | 12_zombie_basic_v2 | P1 | Already covered by the female moan set (§3.2) |
| Missing starter models: Mummified Crawler (starter), Fallen Spawnling, Spawn Shaman, Grove Mauler | starter README | P0/P1 | Covered by §3 and §6; add hooks once the clips exist |
| Briar nuns (Vessaline's Thorn Bride) | bosses.md | P1 | S-FLESH female plus S-THORN; they rise out of splintering pews and sing a fragment of the hymn |
| Ledger imps (the Tallyman's Audit) | bosses.md | P1 | The Ledger Imp set (§6.6) |
| Council of Three cultists (fire, cold, lightning) | bosses.md | P2 | S-CULT plus an elemental layer each; unique-level, so a heavier chant |
| Tabards of the Dead (gatekeepers) | bosses.md | P2 | S-BONE plus tabard cloth plus halberd |
| Hollow Court dead (4 courtiers) | bosses.md | P2 | Ghost courtiers on the art: S-SPECTRE plus a faint court whisper |
| Ysmer throne-wave risen (4 waves of 6–8) | bosses.md | P2 | S-FLESH and S-BONE with an ink layer ("risen Errata") |
| Footnote clone and Fair Copy duplicate | bosses.md | P2 | Doubled, filtered versions of the source sounds |
| Echo of You (ghost replay of the player) | bosses.md | P2 | The player's own sounds, filtered, delayed and ghosted |
| Tallow Saints | bosses.md | P2 | S-WAX: a stiff wax walk, then a melt to a puddle that drains mana (a sip loop) |
| Bailiffs | bosses.md | P2 | Undead court officers: S-BONE plus manacle chains |
| Orbitals (5 rocks) | bosses.md | P2 | A whirring stone orbit loop plus a release whoosh |
| The unwritten (Vessaline, Ossgrind, Halvane at 15%) and the uber act-boss copies | bosses.md | P2 | Reuse the bosses' vocals, ghost- and paper-filtered |
| Class armour tiers (light, medium, heavy) | study | P0 | Footstep and armour-foley tiers (§4) |
| Ambient and plague nest "spawns" (night waking) | world brief | P1 | A chorus cue for the families above |

---

## 12. Ambiguities and decisions to confirm

1. **Tallyman / Ghel act placement.** `bosses.json` says Act I and Act II, but their zones (Smuggler's Hollow, Bitter Ascent) sit on the Coast road (Act III) in the world brief. I followed the JSON: both are **P1**. Kessane is Act III, so **P2**.
2. **Bilge-Wight's act is "?"** (hull, mlvl 11). Treated as **P1**.
3. **Corrupted Phimn has no zone yet**. Treated as **P1** because both glbs are built.
4. **Spawn Shaman** was not in Brian's P0 list. Set to **P1**, but the Spawnling (P0) revive and flee behaviour depends on it.
5. **Two parallel starter pipelines.** `ART/monsters/models3d/{axeman,swordsman,grave_risen,shambler,crawler}.glb` and `NPC3D/monsters/{axeman,swordsman,grave_risen}/out/` exist alongside `NPC3D/monsters/starter/{bone_*,rag_zombie,grave_old_man}.glb`. Which is canonical is unclear; the clip names match, so the sounds apply to both.
6. **The Bone Archer** has no `models3d` glb (only rigpose images and `starter/bone_archer.glb`). **The Spawnling** has no model.
7. **Ossuary Footman and Razor Tollman** have no out/ glb in `sanctuary_npc` (source only); the art `models3d` versions exist.
8. **Bram's location.** The world brief puts him in Martsirt town; the story bible puts him in Briarwood. Treated as **P0** either way.
9. **Quill's voice conflicts.** `voices.json` says an anxious scholar; `lore/quill_martsirt.md` says a soft, precise, archaic ex-knight (and canon says only Ilyra speaks archaically). Needs Brian's call before recording.
10. **Gibbet Remains' attack role** is my guess (a cage ram).
11. **The Vesper Caller's element** is inferred as cold from the blue rune glow; the sheet calls it the base form.
12. **Class genders** are unspecified. I recommend recording male and female vocal sets.
13. **Wolf Howl wolves** exist only in the Kinship perk text; there is no design.
14. **Vessaline v2 and Hollow King v2** are pending approval. The sounds don't change.
15. **Ayla** has no location or voice entry.
16. **Coast road area levels are low** (it may be reached early), but its NPCs are left at P2 per Brian's acts rule.
17. **Diablo equivalents for the "existing" and Margins bosses** are my own reading; the docs label them "existing" or "new".
18. **The female greeting samples** are missing Myrine, Iskra and Moth (all female in `voices.json`).
19. **Uber naming.** bosses.md calls the arenas "The Index" (Ysmer Unbound) and "The Spine" (Warm Binding Decided). The art calls the second "The Unbinding" or "Warm Binding, Decided".

---

## 13. Delivery conventions (suggested)
- Stems: `sfx/mon/<set_or_family>/<event>_<nn>.ogg`, `sfx/boss/<id>/<attack_id>_<tele|commit|impact>.ogg` (attack ids from `bosses.json`), `sfx/pc/<class>/<sex>/<event>_<nn>.ogg`, `sfx/rite/<rite_id>_<cast|loop|impact>.ogg`, `voice/<male|female>/<npc>_<bark>_<nn>.ogg`.
- Variants: 3 or more for hit, death and attack effort; 4–6 for footsteps per surface; 2 or more for idle vocals.
- Loops (auras, hover, chain drag, flood) must be seamless and 4–8 s long.
- Keep the processed, organic realism. Elemental stems stay dark (§2); no generic arcane layer.
