# Sanctuary and Diablo 1/2: design study (art and monster lead's reference)

Compiled 2026-11-01, about 3 AM ET. I only read the sources and did not change any of them.
**Sources read:** `sanctuary/story/story_bible.md` (canon), `story/extract.md` (headers and class strings), `monster_levels.md`, `WORLD_PROMPT_ONE.md` (boss rules and index), `balance_review.md` §1, §7, §11, §13, `starting_book.md`, `skills_and_rites.md`, `uniques/v2/spec.md` (head), `living_world_roadmap.md` §0, `sanctuary_art/{monsters,races,environment}/LOG.md`, `sanctuary_art/lore/quill_martsirt.md`, `sanctuary_env/CLEANUP_v4_2_PROGRESS.md`, `sanctuary_env/statues_angels/PROGRESS.md`, and the bot's memory of Brian's rules.
**Missing or flagged:** `sanctuary/` has no README or top-level design doc. `sanctuary_art/monsters/bosses/` has no LOG.md; the boss entries are in `monsters/LOG.md`. I found no doc on music or audio direction, and nothing that says whether dungeon layouts are randomly generated.

---

## 1. Sanctuary at a glance

**Premise (story bible §1).** A parish burned its register of the drowned. The copyist Ysmer then wrote all the names into a book bound in his own skin, called **the Warm Binding**. The book rewrites whatever it reads: the dead come home "wrong" and the living start to sound like the page. The player came out of a lost battle at the north trench with their name burned away, so the book can't read them.
**Theme:** what we owe the dead, and when holding on turns into the disease. Every survivor holds onto an object: shoes, a key, a ledger, a bell, a ribbon, a lamp.
**Tone:** "D2 Act I. Bleak, grounded, terse, dread." Horror comes from specific details ("a ring with skin in the band"), not from adjectives.

**Backstory timeline.**
- Y-60: the clock-mages crack the Glass Sky, which leaves the Cinder Barrens. The Hollow King seals himself under the Black Vault.
- Y-40: the Open Eye becomes the iron citadel and shuts its gates. Ilyra is left outside.
- Y-6: the ferry *Ninth Bell* sinks with 212 aboard.
- Y-3: Father Noll's fire from Zhera turns his flock into a garden of salt statues.
- Y-2: Abbess Vessaline burns the register, and Ysmer binds the book.
- Y-1: the Inquisition (Halvane) arrives.
- This spring: the tome reaches Quill, and Orithya walks you to Martsirt.

**Acts and route (story bible §3, monster_levels zone ladder).**
| Act | Hub | Main zones | Act boss |
|---|---|---|---|
| I | **Martsirt** (square, cottage, taproom) | Sealed Nave, Salt Cellar, Briarwood (north), logging camp, Blackroot Cavern, Chapel, Underchapel / Thorn Choir | Vessaline, the Thorn Abbess |
| II | **Qadren** (desert town, reached by Holt's skiff across Blackwater) | The Narrow, the Isle, the Sands, Dry Reliquary | Ossgrind |
| III ("Coast road", out the south gate) | Bastion of Hope (field camp) | Ashen Coast, Mourning Bluffs, Bleak Flotsam, Silt Mires, Putrid Sink, Razor Ridge, Bitter Ascent, Sunken Crypts, Drowned Chasm, Iron Bastion Pass / Toll Arch, Smuggler's Hollow, Inquisitor's Gaol, Weald Edge, Obsidian Spires, Spire Roots | Inquisitor Halvane (Goreth-Vaal is the "prince") |
| IV | **Highmarket** (plaza, Lampwick Inn) | Highmarket Undercroft, Castle Gate, Burning Gallery, the Fence, Cinder Barrens, Ash-Camp Ruins, Ashen Font, the Castellan | Vhorr-Akesh, the Ember Saint |
| V | (none listed) | Vault Antechamber, Unread Stacks, Black Vault | Ysmer, Who Wrote the Plague (and the Hollow King) |
| Hell only | the Margins | Tide-Clock, Tallow Cathedral, Toll Court, Hollow Star, Mirror Scriptorium, the Last Page | Pinnacle: the Warm Binding |

- The difficulty tiers are part of the story. Normal: the book is reading. Nightmare: it has read you, and NPCs misremember your first walk. Hell: you walk in the margins.
- **Flag:** Act III's coast zones begin at danger 3 (Bastion and Ashen Coast are area level 3 on Normal) and are mixed in with Act I zones, so "Act III" works as a parallel side road, not a strict third act. This should be confirmed with Brian.
- **Flag:** the code's list of towns (`inTown()`) is town, lut (Qadren), market (Highmarket), cottage and taproom. I found no Act V town.
- The bible says to drop "Lut Gholein": the desert town is Qadren everywhere.

**Towns: art state.**
- **Martsirt:** an outdoor kit exists (v4.2 cleanup, Oct 31): Voronoi flagstone square, stable, lodge, salt statues (the hood gap was fixed), a cliff and gorge with waterfall, and `plan/martsirt_town_overview.png`. Noll's salt garden is canon set dressing.
- **Qadren:** environment sheets 01a through 08 exist. It's a small walled town of sandstone and mud-brick with a Free Well plaza, the domed Dry Reliquary (stairs down), a watchtower, black-glass dunes, eight building fronts (Tamsin's kitchen-inn, Orlem's house, Vetch's dice house, Heska's watch post, the well house, the Reliquary, the caravanserai, the coppersmith), interiors, a parchment layout map and 16 clutter props. A larger walled desert city has no name yet (sheets 02a and 02b, including a clock-mage observatory ruin).
- Kits: castle (walls, portcullis, guardian-knight statues), gothic (ironwork, stained glass, buttresses), 12 material swatches running from filthy to holy, and four hell-gate statue designs.
- **Statues:** a D2-style "Epic Angels and Sad Souls" brief (grave faces, rain stains, lichen, dulled gilt). The hero bust v2 GLB was approved. The kneeling knight is next, but statues come after characters and monsters.

**Key NPCs (the bible's cast).**
- Martsirt:
  - **Wolchen**, the smith. He forged the Inquisition's irons and the cold-iron bands on Quill's coffer.
  - **Ysara**, the healer and Noll's sister. She visits his salt statue at night.
  - **Ilyra**, the gatekeeper. She is the only NPC who speaks archaic English, because of an Open Eye vow.
  - **Quill**, the scribe and tome-keeper. He was Noll's clerk, helped Ysmer with the binding knife, and burns his sleeves on the warm tome. He keeps the First Reading and Boss Stone duties.
  - **Bram**, the logger. He ran when Scar-Eye took Aldo.
  - **Mira**, the taproom keeper.
  - **Orrin and Ness**, regulars.
- Field: Orithya, Sable, Holt, Myrine, Wynn, Rusk and Sera, Odder, Iskra, Moth and Calder, Hask and Kell, Nim, Vellum and Lute, Brine, Jas, Piet, Ors.
- Qadren: Orlem, Heska, Vetch, Tamsin. Highmarket: Hesta, Voss, Ilen, Cal, Pell. Cinder Barrens: Sarn. Under the castle: Vesper.
- Unique race: **Ayla, the Phimn** (approved). The Phimn are a people thought extinct, with grey-blue skin and a height of always 4'8". She wears red ancient runes and a pale-blue crystal charm.
- **Conflict to resolve (Quill):** `lore/quill_martsirt.md` writes Quill as a former high-seat member of the iron citadel who speaks archaic English ("Thou askest…"). The canon bible says he was Noll's clerk, that he speaks plainly ("precise, a little pedantic"), and that archaic speech belongs to Ilyra alone. The bible is canon, so the lore file probably needs Brian's ruling or a rewrite.

## 2. Stats, classes and progression (as documented)

**Attributes:** five level-up cards: **Brawn** (melee and steel), **Vigor**, **Mark** (bow and javelin), **Reverie** (other rites, ×2/3) and **Fortune** (+0.5% rite damage, crit capped at +20%). Returns diminish: `Te(x)=0.03x·60/(x+60)`. Sources: desc/audit.md and DESC_WORDING_FIX_PROMPT.md.
**Level and difficulty:** Normal area levels run 2 to 93, Nightmare 95 to 130, Hell 132 to 185. Sims run to L185.

**Four classes.** Nothing is class-locked, and there is no penalty for off-class weapons. Each class gets one passive that scales with level (§13, approved 2026-10-26).
| Class | Archetype | Base | Passive |
|---|---|---|---|
| **Ironvow** | warrior | 130 hp, +6 def, 8% DR, Rusted Iron Sword | **Unbroken / Grit**: grows stronger when hit. Last Stand at L80, Iron Echo shockwave at L120 |
| **Longmark** | archer | 90 hp, +12 IAS, Ashwood Short Bow | **Stride**: moving builds speed and dodge. Running Shot, Slip. Keen Eye halves enemy defense |
| **Cinderwake** | elementalist | 90 hp, largest mana pool, Gnarled Yew Wand | **Resonance**: spent mana echoes the next rite. Prism, Overflow barrier, Triad |
| **Gravewell** | blood and bone necromancer | 110 hp, 8% leech, Chipped Bone Dagger | **Toll**: nearby deaths heal you. Death's Door, Collect. Blood rites cost life |

- **Rites and tomes:** there are 51 rites, each taught by a "<Rite> Tome" (legendary, 10,000 gold). Schools: fire, cold, lightning, holy, blood, bone, nature, steel, guard and mind, plus traps (Ironjaw, Blight Cask, Rime Caltrop, Thunderkiln) and auras (Hearthward, Wrathbanner, Truesight, Kinship). Learning some rites **permanently seals others** (the Synergy Web v3/v4).
- **Bound Rite:** a rite is socketed into the basic attack, with a variant for each weapon kind (sword, axe, spear, mace, dagger, bow, wand, staff, shield).
- **Starting book:** every character starts with one seeded random rank-1 tome from a class pool. Quill's First Reading offers a choice of 1 from 6.
- **Talents:** 37 talents in branches (Flesh, Blood, Bone, Element, Steel, Guard, Mind, Orbit), each with max rank 12.
- **Scorecard:** 6 build archetypes (All-Rounder, Glass Cannon, Speed, Tank, Safe, Sustain), with 3 different archetypes per class.
- **Items:**
  - Rarities in code are common, uncommon, rare, epic and legendary (base chances 15% / 3.4% / 0.8% / 0.24%). These differ from D2's names.
  - Uniques: 93 existing, with 50 more planned (v2 spec "The Ninth Bell"). The spec adds rolled ranges, +Rites, procs, auras and fixed sockets.
  - Sockets come only on epic items (20%).
  - Ethereal: a 5% roll when ilvl > 10. It gives +40% base and cannot have sockets.
  - Affix tiers are gated by ilvl in six bands (T1 1–20 through T6 150–185).
  - Potions are tiered by monster level.
- **Not found:** set items, runewords or a rune system, a horadric-cube-style crafting system, trade, and a ladder or seasons.
- **Living world (roadmap, partly live):** NPC regard and memory, a day/night cycle, rain and fog, town schedules, and plans for named foes, nemesis and "seekers".

## 3. Monsters: roster, level bands, bosses, colour rules

**Level rules (monster_levels.md):** mlvl = area level. Magic (champion, blue) packs get +2, and rare (unique, gold) leaders and bosses get +3. Drop ilvl = mlvl. Resists rise by +0/+20/+40 per difficulty, capped at 75. In Hell there is a 20% chance of one immunity, modelled as "resist 100, breakable to 95". The XP gap penalty follows D2.
**Pack mods:** Fleet, Brutal, Knitting, Hulking, Ironhide and Spiteful, plus Warded, Venomous and Caustic from Nightmare up. Champions have 1 mod, and unique leaders have 2 (3 in Nightmare and Hell) plus minions that share the first mod.
**Bosses:** TTK targets are 40 to 150 s depending on tier. Arenas seal, attacks are telegraphed, and no untelegraphed hit deals more than 30% eHP. The first kill per difficulty drops a **Boss Stone**.

**Families (locked by Brian 2026-10-31).** Each has a physical form and an elemental form.
| # | Family (life/dmg ratio vs zombie) | Physical | Elemental |
|---|---|---|---|
| 01 | zombie (1.0/1.0) | Grave-Risen | Plague-Spitter (poison) |
| 02 | skeleton (0.41/0.63) | Ossuary Footman | Frost-Bound Sentinel (ice) |
| 03 | ghost (0.36/0.71) | Rope-Shade | Bell-Wraith (lightning) |
| 04 | imp (0.25/0.51) | Ledger Imp | Cinder Imp (fire) |
| 05 | caller (0.63/0.47) | Vesper Caller | Pyre Caller (fire) |
| 06 | corpse (0.51/0.63) | Gibbet Remains | Plague Bloat (poison). Its role was a guess |
| 07 | brute (1.34/1.29) | Razor Tollman (v2: torn hide, sinew, hooks, chains) | Cinder Tollman (fire) |
| 08 | bear (1.67/1.4) | Grove Mauler | Rime Bear (ice) |
| 09 | snake (0.52/0.93) | Blackroot Adder | Venom Asp (poison) |
| 10 | raver (0.2/0.85) | Thin Laugher | Storm Laugher (lightning) |
| 11 | worm (1.7/1.24) | Purse-Jaw | Bile Crawler (poison) |
- Act I starter basics (approved): 12 Shamblers (v2, weathered by rain and mud), 13 bone axemen, swordsmen and archers, and 14 the "Fallen Spawn" small red demons (Spawnling and Spawn Shaman).
- Special: the **Corrupted Phimn** (locked), in two forms: a Winged Caster and a Feral Stalker, each with fire, ice, lightning and poison variants.
- Boss templates: wraith (2.84 life), melakir (1.27), king (5.01).

**Bosses with mlvl (Normal / NM / Hell) and element.**
- Saltmouth 5/98/135 (poison)
- Ash Wraith 9/102/139 (fire)
- Melakirniz, a twin pair, 9/102/139 (physical)
- Bilge-Wight 11/104/141 (cold)
- Tallyman 14/105/143 (physical and poison)
- Scar-Eye 17/106/144 (physical)
- Ghel 32/111/153 (cold and mind)
- **Vessaline** 35/112/154 (poison and blood; v2 has greyer undead skin)
- **Ossgrind** 50/117/163 (cold and physical)
- Kessane 50/117/163 (physical and fire)
- **Halvane** 57/120/166 (lightning)
- Spire-Heart and Goreth-Vaal 72/125/175 (physical and poison; magic)
- **Vhorr-Akesh** 87/130/183 (fire and lightning)
- Castellan 90/130/185 (physical)
- **Ysmer** and the Hollow King 93/130/185 (magic; v2 of the Hollow King is the pick)
- Margins: Bell-Wright (cold and time), Mother Wick (fire), Assessor (lightning), Nul-Osse (gravity; stays legless and hovering), Errata (copy)
- Pinnacle: the Warm Binding (grief: desaturated ash-grey). Ubers: Ysmer Unbound and the Warm Binding, Decided.
- All 25 boss sheets are done and sent. Brian said to hold off on 3D, with the split pipeline as the plan.

**Colour rules (Brian; the newest rule wins):**
1. **Magic has no colour of its own.** It takes its damage element's colour **with a dark hint**:
   - fire: dark, realistic fiery red
   - physical: almost invisible dark smoky grey
   - cold: dark blue with light-blue streaks
   - by extension, poison is sickly green and lightning is pale violet-white
   This replaced the earlier violet placeholder for magic.
2. **Element hue shifts on skin or body apply only to monsters Brian names**, not to every monster (clarified 2026-10-31). Violet is used only where it fits.
- **Stale rule to fix:** `monsters/LOG.md` still opens with "Global monster rule: hue ALWAYS shifts", which contradicts rule 2. Several boss entries also still describe "arcane violet" (Goreth-Vaal, Ysmer, Errata, Nul-Osse, the Hollow King's starlight). Under rule 1, the magic VFX on those bosses should be re-read with the element-plus-dark-hint rule, or confirmed as places where violet fits.

## 4. What made Diablo 1 and Diablo 2 great

- **Kill and reward, with a goal always close.** "There's always a quest that is almost finished, a waypoint almost reached, an experience level almost achieved." Monsters die "like piñatas", and every action, inventory clicks included, makes a satisfying sound. ([Schaefer, D2 Postmortem, Game Developer 2000](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-))
- **Randomness makes the run your own.** Levels, monsters and treasure were random, so "each player's game [is] his or her own" and walkthroughs don't solve it. D1 had **16 random levels under one town**: church, catacombs, caves, Hell. Reviews praised the random dungeons and the "moody musical score". ([D2 Postmortem](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-); [Wikipedia: Diablo](https://en.wikipedia.org/wiki/Diablo_(video_game)))
- **Simple controls.** The "Mom test": left-click to move, attack, talk, open and loot. ([D2 Postmortem](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-))
- **Real time with roguelike tension.** D1 began as a turn-based roguelike (Angband was "the real template"). Brevik converted it to real time but kept the "sweaty palms" of being one hit point from death. ([Brevik GDC 2016 postmortem](https://www.gdcvault.com/play/1023469/Classic-Game-Postmortem); [transcript](https://gameindustrylibrary.com/documents/diablo-a-classic-game-postmortem); [Uelmen, PureDiablo](https://www.purediablo.com/matt-uelmen-interview-from-condor-to-torchlight-2))
- **Darkness and lighting came from the palette.** D1 split a 256-colour palette into 128 background and 128 character/FX colours, ordered by hue and brightness so that lighting tables could darken everything. The torch-radius darkness was built into the art itself. ([Brevik GDC 2016](https://gameindustrylibrary.com/documents/diablo-a-classic-game-postmortem))
- **The town is a safe hub, and the music sets its mood.** Uelmen aimed Tristram's 12-string theme at an early-70s folk-rock "medieval" vibe, "the ideal vibe for a safety/shopping/quest zone". It "never really goes anywhere", which is why it works under a slot-machine loop. Glenn Stafford did much of D1's monster and death audio. ([Dread Central](https://www.dreadcentral.com/news/261440/stay-listen-interview-diablo-composer-matthew-uelmen/); [Shacknews](http://www.shacknews.com/article/60997/from-tristram-to-torchlight-an))
- **Loot colours and loot sounds.**
  - Colours: grey for trash, blue for magic (1–2 affixes), yellow for rare (3–4), green for set, gold for unique. Blue came first "because blue is the colour of magic". Gold was used for uniques "because it looked more important".
  - Sound: rare rings were hard to see, but players heard them land.
  - Schaefer deliberately avoided flat balance. He wanted temporary "too good" spikes, which sets, uniques and runewords provided.
  - Sources: [Kotaku interview with Schaefer and Brevik](https://kotaku.com/why-video-game-loot-is-so-addictive-according-to-the-c-1846695147); [PureDiablo: Schaefer on items](https://www.purediablo.com/erich-schaefer-on-item-design-and-story)
- **Item art itself.** D2's inventory art (Bob Steele) was painted meticulously, with many visual variants for each item type. Heroes had modular light, medium and heavy armour. ([Craddock, "Why Diablo 2 holds up"](https://medium.com/@dlcraddock/why-diablo-2-holds-up-almost-20-years-later-df4be1a5b740); [D2 Postmortem](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-))
- **Skill trees.** D2 dropped D1's shared spellbooks for class skill trees with prerequisites. That allowed specialisation, for example a poison-dagger Necromancer next to a summoner. ([D2 Postmortem](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-))
- **Random uniques and packs.** D2 generated "thousands" of random unique bosses with special abilities. The team also planned **multiple death sounds and attack animations per monster**, because players kill the same monster so often. ([D2 Postmortem](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-))
- **Four towns, five acts, one story.** D2 has four towns (five with LoD), each act bookended by cinematics. Its architecture mixes cultures (Act III draws on Maya and Aztec) so that no area copies a single real culture too closely. ([D2 Postmortem](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-))
- **Long-tail systems.** Gem sockets came from a programmer's suggestion. Patch 1.10 added runewords (20 new ones, some ladder-only), synergies, tougher Hell, more Hell uniques and cube recipes. LoD added immunities in Hell. Ladder resets kept the economy fresh. ([Diablo Wiki: Patch 1.10](https://diablo.fandom.com/wiki/Patch_1.10_(Diablo_II)); [Ladder Runewords](https://diablo2.diablowiki.net/Ladder_Runewords))
- **Waypoints and the no-save-scum design.** Games reset to town, and waypoints are a small reward in their own right. ([D2 Postmortem](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-))

## 5. Where Sanctuary matches, gaps and risks, suggestions

**Where it already matches D1 and D2.**
- Tone and voice are explicitly "D2 Act I". The bible's "D2 test" holds NPC lines to Charsi, Akara and Gheed brevity. The horror comes from specific details.
- The structure follows D2: hub towns (Martsirt, Qadren, Highmarket), 5 acts, act bosses inspired by Andariel, Duriel, Mephisto, Diablo and Baal but with original names, Normal/NM/Hell, D2 XP penalties, champion (blue) and unique (gold) packs with D2-style mods, and Hell immunities. Ubers and a pinnacle stand in for Uber Tristram.
- The difficulty tiers are tied to the story (the book reading you), which is stronger than D2's.
- Grounded and real: salt statues, gibbets, toll families, inquisition, plague. The monsters are rotting peasants, bone soldiers, bears and imps, close to D1's cathedral bestiary. The Fallen Spawn plays the Fallen role.
- Items carry D2's DNA: ilvl drops, affix tiers, ethereal, sockets, +skills on uniques, procs, MF with diminishing returns, Town Portal Scrolls.

**Gaps and risks.**
1. **Rarity names and colours.** The code uses common, uncommon, rare, epic and legendary (WoW-style), but players read D2's grey/white/blue/yellow/green/gold. I found no documented colour table.
2. **No sets, runewords or crafting** in the docs. D2's long-term "spikes" came largely from sets, uniques and runewords.
3. **Book-learned rites echo D1, a model D2 dropped.** The Synergy Web's permanent locks bring back tree-like choice, but a lock is a heavy, final decision, so the UX in §9.6 matters.
4. **Random layouts aren't documented.** The roadmap mentions `rememberArea()` but says nothing about random generation. If maps are fixed, that is the biggest difference from D1 and D2.
5. **No audio or music direction** was found. Only VFX sound-hook names exist. In D1 and D2, sound was half the atmosphere: the town theme, loot-drop sounds, multiple death sounds.
6. **Lore contradictions:** the Quill lore file and the bible disagree. The monster hue rule in LOG.md is outdated. Violet still appears as a magic colour on boss sheets.
7. **Act III ordering is ambiguous.** The coast zones start at level 3 even though they're labelled Act III.
8. **Unnamed places:** the big desert city and the Act V hub have no names. Highmarket has no environment sheets yet.
9. **Darkness:** the env work is moonlit and fog-heavy, which is good. I found no torch-radius or light-radius gameplay spec, although "Light Radius" is an affix on Sun-Eater.

**Suggestions (art, monsters and characters first).**
1. **Lock a loot-colour table in D2 order** and map it to the code's rarities: grey/white for common, blue for uncommon, yellow for rare, green for epic (or a future set tier), dark gold for legendary/unique. Dull the colours slightly so they fit the battle-worn palette, and add a distinct drop sound for each tier.
2. **Give every regular family 2 or 3 death variants and a hit-react pose** (D2's lesson: you kill the same monster thousands of times). Put these on the rig and pose sheets before the 3D pass, starting with the Act I Shamblers, bone soldiers and Fallen Spawn.
3. **Make champion and unique packs readable without recolouring the skin** (hue shifts are only for monsters Brian names). Use a dark-hinted elemental aura, rim light or ground decal in the mod's element colour, plus small physical tells: Ironhide gets rusted plates, Hulking +15% scale, Fleet a leaner silhouette. This keeps the realism and stays inside Brian's rule.
4. **Clean up the colour canon in the art logs.** Replace the "ALWAYS shifts" line in `monsters/LOG.md` with Brian's two current rules. For each violet-magic boss (Goreth-Vaal, Ysmer, Errata, Nul-Osse, Hollow King, Halvane's mind), list whether violet stays (Brian approves) or becomes element-plus-dark-hint. This is a doc fix for the art bot to do, after asking Brian.
5. **Settle Quill.** Rewrite `lore/quill_martsirt.md` in the canon voice: Noll's clerk, plain and pedantic speech, sleeves burned by the tome, the binding-knife secret. Keep the "keeping the shape" idea if Brian likes it, but put it in plain speech. Then design his model: ink-stained, sleeves scorched, wrists bandaged, with the warm coffer and Wolchen's cold-iron bands as props.
6. **A unique silhouette for each town, from one local material:** Martsirt is salt, slate and wet timber. Qadren is sandstone and black glass. Highmarket should get its own sheet next: lamps, bells (Pell) and a market under the castle. Like D2's Act III, mix real-history references (Flemish and English parish towns, Andalusian and Maghrebi caravan towns) so none of them copies one culture.
7. **Make the town feel safe.** Light Martsirt warmly (taproom glow, Wolchen's forge) against the cold moonlit fields. The D1 trick: the hub is the only warm-coloured place. Add a music brief for Martsirt in the Tristram spirit, a sparse, looping acoustic theme that "never goes anywhere", and flag that audio direction is missing.
8. **Plan darkness for the dungeons.** Use a tight warm light radius around the hero with near-black falloff in the crypts, cellars and the Underchapel, as D1's palette lighting did. Make Light Radius gear actually widen it. Art should paint texture values for that falloff (mid-dark albedo, strong normal detail).
9. **Characters wear their burden.** Each named NPC's model shows the object they hold onto (Iskra's shoes, Wynn's blue ribbon, Brine's lamp, Jas's ledger, Lute's bell, Holt's hook). The bible's theme then reads in silhouette, and the Margins bosses (Bell-Wright, Mother Wick, the Assessor) visually echo the NPCs they came from.
10. **Lay out the player kit the way D2 did:** modular light, medium and heavy armour per class (Ironvow, Longmark, Cinderwake, Gravewell), with battle damage on every tier. The nameless-hero premise suggests a burned-out or scraped heraldry slot on every chest piece. That is a cheap, strong story tell.
11. **Systems to raise with Brian (not art):** a set or runeword-like layer (for example "bindings" of rite-inscribed relics, which fits the book theme), random or semi-random dungeon layouts for the crypt, cellar and chasm zones, and a seasons or ladder plan.
