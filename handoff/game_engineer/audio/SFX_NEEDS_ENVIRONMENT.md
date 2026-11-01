# SFX Needs — Environment & Architecture
From: New Bot · Environment and Architect builder · 2026-11-01
For: Sounds Of Sanctuary

Priorities: **P0** means the asset exists or is being integrated now. **P1** is coming soon. **P2** is later.
Seasons in the outdoor sets are spring, summer, autumn and winter, built per map. The engineer runs the sun cycle (day/night).
The design rules that affect sound are:
- The town hub is the only warm-lit place.
- Dungeons stay tight and dark.
- Elite and boss areas use dark-hinted element colours, and the audio can echo that.

---

## 1. Town: Martsirt (Tristram-style) — P0
Status: v2.2 dressing has been integrated. It has one bonfire, one smaller campfire offset in the distance, window and door glow, a few wall torches, one market stall, a creek with a footbridge, a graveyard corner, fences and sparse gothic trees.

**Ambient beds**
- Base wind: a low rural wind with occasional gusts through bare trees. Day and night versions.
- Bonfire: the main town fire, a large crackling loop with pops and ember hiss, positional with a radius of about 15 m. **P0**
- Campfire: a smaller, quieter crackle off in the distance. **P0**
- Wall torches: a small flame flutter, short radius, with only a few emitters. **P0**
- Creek: a gentle trickle that gets louder near the footbridge. In winter, use a thinner, partly iced trickle. **P0**
- Day layer: distant birds, a crow now and then, a faint stall bustle and a few cloth flaps.
- Night layer: crickets in summer and autumn, an owl, a far-off dog, and darkness that should feel heavy. **P0**
- Graveyard pocket: quieter, a cold wind tone, a creaking iron fence, and crows. **P1**
- Season changes:
  - Winter: muffled snow wind and no insects.
  - Autumn: leaf skitter.
  - Spring: rain showers.
  - Summer: insects.
- Weather: a rain bed with separate roof-drip and puddle layers near buildings, plus distant thunder. **P1**

**Interactables**
- Wooden building doors: open, close, a creak, and a locked rattle. **P0**
- Market stall: an awning flap and wood creak (ambient only). **P1**
- Hanging sign: a creaking swing in the wind. Prop: hanging_sign. **P1**
- Iron gate and iron fence (gothic): a gate creak open/close and a latch clank. **P0**
- Footbridge: a hollow wooden thump (see the footsteps section).

**Footsteps:** dirt or packed earth, cobble or stone, wood planks (the bridge), grass, mud (rain variant), and snow (winter).
**Acoustics:** open air with short early reflections between buildings. No big reverb.

---

## 2. Forest / Briarwood & outdoor wilds — P0
Status: the v5 forest with LOD trees, the per-map mountain rings, and rect border rings in all four seasons.
The mood reference is steep conifer slopes, valley fog, god rays, crows and an overcast sky.

**Ambient beds**
- Forest wind: wind through the conifer canopy, high and airy. Gusts make trunks creak. **P0**
- Birds by day: sparse and moody, mostly crows and ravens rather than songbirds. **P0**
- Night: owls, a distant wolf howl, snapping twigs, and an insect bed in the warm seasons. **P0**
- Fog areas: a dampened, softer, close-in bed with almost no birds. **P1**
- Season changes:
  - Autumn: leaf rustle and falling leaves.
  - Winter: snow-muffled wind, ice creak, and no insects.
  - Spring: rain, dripping leaves, and running streams.
  - Summer: cicadas or insects and drier wind.
- Weather: rain on the canopy (heavier, filtered), a drip layer, thunder, and a snowfall hush. **P1**
- Mountain edge / border rings: a deeper, hollow wind that blows past the ridges. **P1**

**Interactables (outdoor loot, tagged loot_low, each with a closed and an opened state)**
- rock_pile: shifting stones and a scrape, then a gravel spill. **P0**
- hollow_log: a dry wood crack, a split, and bark falling. **P0**
- rotten_stump: a soft wet rot crunch and a splinter. **P0**
- weapon_rack_wreck: a rusty metal rattle and a wood collapse. **P0**

**Footsteps:** grass, forest floor (needles and leaves), mud, rock, snow, and shallow water.

---

## 3. Coast, islands and mires — P0
Status: the border and coast kit (sloped sea cliffs, end caps, height steps, dunes, shelves), the shore foam and rocks, and Islands v2 (isle and mires).

**Ambient beds**
- Sea: two layers. A distant swell bed, and positional wave breaks against the cliff toes, which hit heavier against the tall cliffs (h8). **P0**
- Shore: lapping and wash over sand and pebbles at the beach and dune edges. **P0**
- Sea wind: a strong, salty, buffeting wind, and gulls by day. **P0**
- Night: quieter swell, distant buoy-less emptiness, and the odd far-off bell (optional). **P1**
- Mires (the swamp island): frogs, bubbling mud, insects, still air, and a creepy wet ambience. In winter, frozen mud creaks and the insects drop out. **P0**
- Storm weather: crashing surf, rain hitting the sea, and thunder. **P1**

**Interactables**
- **Rideable longship** (boat_longship_ride_v1). It has player-stand and boarding nodes, six NPC seats, a sail and two oar banks. **P0**
  - Boarding: wood thump and a hull shift.
  - Rowing: an oar stroke loop for each side, with a creak and a splash.
  - Sailing: sail flap and fill, plus rigging creak.
  - Hull: water slap against the hull, a beaching grind on sand, and a dock thud.
- **Wreck at the cave entrance** (boat_wreck_cave_v1): ambient timber groans, water sloshing inside the hull, and a hollow wind through the hull and ribs. **P0**
- Cave mouth transition: the sea bed fades into a dripping cave tone. **P0**

**Footsteps:** sand, wet sand, pebble or shingle, rock, wood deck (the boat), mud and bog (mires), and shallow water splash.

---

## 4. Desert: Qadren & the walled desert city — P1 / P2
Status: Qadren is the next town in my queue (P1). The walled desert city comes later (P2).
Each will be built from its own local materials (sandstone and so on). Expect braziers in place of a bonfire, and one warm hub.

- Ambient beds:
  - Hot dry wind and sand hiss blowing over the dunes.
  - By day: a heat-shimmer drone, and a sparse hawk or buzzard.
  - At night: cold wind, insects and jackals.
  - A sandstorm weather bed.
- Town: braziers (an oily crackle), cloth awnings flapping, a well with a rope and bucket, wind chimes, and a single market stall.
- Interactables: heavy wooden gates on sandstone walls, a stone slab grind, and pots and urns breaking.
- Footsteps: sand, sandstone, packed earth, and wood.
- Acoustics: dry, with almost no reverb outdoors. Courtyards slap back from the walls.

---

## 5. Crypts & dungeons — P0
Status: the gothic prop pack batch 1 has been integrated. It has dungeon loot containers, a gibbet cage, chains and shackles, a carved sarcophagus, an iron maiden and cobwebs. There is also the older KayKit dungeon and the hell gates.

**Ambient beds**
- Cave or crypt tone: low sub rumble, still air, and far-off dripping. **P0**
- Tight tunnels: close and dry, with almost no tail. **P0**
- Big burial halls: long, dark reverb, with distant stone settles and faint whispers or moans (sparse). **P0**
- Water caves: drips, a pool trickle, and echo. **P1**
- Torches and sconces: small flame loops, with very few emitters to keep it dark. **P0**
- Hanging chains and the gibbet cage: slow creaking sway, and a chain clink when you're near. **P0**
- Elite and boss areas: a tonal swell layer per element: fire roar, cold hiss/crackle, poison bubbling, lightning buzz. **P1**

**Interactables (dungeon loot, tagged loot_low, closed and opened states)**
- bone_pile: a dry bone clatter and spill. **P0**
- skull_heap: skulls rolling and a hollow knock. **P0**
- burial_urn: a ceramic crack, a shatter, and an ash puff. **P0**
- sarcophagus_small, and sarcophagus_carved (a dressing prop): a heavy stone lid scraping and grinding, then a thud. **P0**
- sack_pile: a cloth rip and grain spill. **P0**
- remains_heap: a wet cloth-and-bone shift. **P0**
- rubble_cache: shifting rock and a small collapse. **P0**
- Iron maiden: a heavy hinge creak (dressing, optional interaction). **P2**
- Chest and doors (batch1_interactables): a chest lid with a lock click, and a wooden door and a gothic door, each with an open, close, creak and locked sound. **P0**
- Shrine: an activation hum or chime, a short magic swell, and a used-up dull sound. **P0**
- Hell gates / portals: an idle portal loop (a fiery roar with a low drone), plus an activate sound and a step-through whoosh. **P0**
- Future: levers, pressure plates, collapsing walls, portcullis, spike traps and secret stone doors. **P1** (planned)

**Footsteps:** stone, wet stone, bone and gravel, dirt, wood (scaffold and bridges), and shallow water.

---

## 6. Churches & chapels — P1
Status: the gothic props for these exist (pews, an altar cloth, a lectern with a book, a tall candelabra, wall sconces, a gargoyle, a saint niche, a heraldic tapestry). Full church and castle architecture kits are queued.

- Ambient beds: a large stone nave reverb with a long tail, faint drafts, a guttering candle sound, an occasional distant bell, and a choir-ish pad (only if it doesn't fight the music, and only for desecrated areas).
- Interactables: the lectern book (page turn and a "read" cue), candle lighting and snuffing, heavy oak church doors, and a tapestry rustle.
- Footsteps: flagstone, and wood (pew aisles, choir loft).

---

## 7. Cellars & interiors — P1
- Cellars: a close, damp room, dripping, a rat skitter, and a low creak overhead.
- Building interiors: a hearth fire, creaking floorboards, rain on the roof (the weather link), wind whistling at the shutters, and a muffled version of the outdoor bed.
- Tavern and smithy props (anvil_stump, cauldron_tripod, hanging_sign):
  - Anvil: hammer strikes in a loop, used near the smith NPC.
  - Cauldron: a bubbling loop.
  - Tavern: a muffled tavern murmur.
- Interactables: barrels (hit, break, and roll), crates (break), trapdoors, and stairs.
- Footsteps: wood floor, stone floor, and straw.

---

## 8. Footstep surface master list
| Surface | Where | Priority |
|---|---|---|
| Dirt / packed earth | town, paths, dungeons | P0 |
| Cobble / flagstone | town, church, crypt | P0 |
| Wood plank | bridge, boat deck, interiors | P0 |
| Grass | forest, town edges | P0 |
| Forest floor (needles/leaves) | forest | P0 |
| Mud / bog | rain, mires | P0 |
| Sand / wet sand | coast, desert | P0 |
| Shingle / pebble | coast | P1 |
| Rock / gravel | mountains, caves | P0 |
| Shallow water | creek, caves, shore | P0 |
| Snow | winter seasons | P0 |
| Bone / rubble | crypts | P1 |
| Straw | stables, cellars | P2 |

## 9. Reverb / acoustic zones
| Zone | Character |
|---|---|
| Outdoor open | Dry, with a short slap from nearby walls |
| Town between buildings | Short early reflections |
| Forest | Soft, diffuse, slightly absorbed |
| Fog banks | Damped highs, close |
| Coast cliffs | An open slap-back off the cliff faces |
| Tight tunnel / cellar | Small, boxy, almost no tail |
| Crypt hall / cave chamber | Large, dark, long tail |
| Church nave | Large, bright stone, longest tail |
| Building interior | Small wood room, warm |
| Desert courtyard | Dry, with a hard slap-back |

## 10. Coming soon (P1/P2)
- Qadren town (desert, sandstone): P1.
- Castle and gothic architecture kits: P1.
- Possible "side-quest kit" of event set-pieces: notice boards, ambushed carts, cursed altars, levers and pressure plates. P1, if Brian picks it.
- The walled desert city, and the hell-gate statues: P2.

## Integration hooks
- The loot containers all share the interactable tag `loot_low`, and each has a closed and an opened GLB. One "open" sound per type covers it.
- On the longship, the nodes `oars_L`, `oars_R`, `sail` and `player_board` are the natural places to attach sound emitters.
- The fire emitters should sit on the bonfire, the campfire, the torches and the braziers. The engineer owns their placement.
