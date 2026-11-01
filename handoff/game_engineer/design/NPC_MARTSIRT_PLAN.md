# Martsirt NPC plan (stage 1: Martsirt only)

Written 2026-11-01 (ET). This is prep only: no game or asset files were changed and nothing was pushed.

**Inputs:**
- Brian's answers of Nov 1:
  - Quill's v2 voice is canon.
  - The other NPCs keep their archaic lines.
  - Mira, Orrin and Ness get outdoor homes and an evening taproom walk.
  - Banter is muted.
  - Ayla joins Martsirt.
- `sanctuary_env/martsirt_v2_2` (world, placements and solid grid).
- `live_12d/r.js` (`dutyOf`, `postFor`, `maybeBanter`, `Rc()`).
- `sanctuary_npc` (bodies, clothing and the anim test).
- Story bible, voices.json and `lore/quill_martsirt.md` v2.

**Conventions:**
- Coordinates are in **metres** (the square is at 0,0; −z is north), with the matching **tile** in brackets (tile = metre + [81, 76]).
- Every spot below was checked against the v2.2 solid grid. Each is walkable and reachable from the spawn.
- The new spots are Mira, Ness, Orrin and Ayla. The five existing homes are unchanged (Brian: keep the v2.2 homes).

**Clock:** `daySeconds = 21600`, so one game hour is 15 real minutes.
- The longest walk to the taproom (Orrin, ~100 tiles) takes about 70–80 s of real time.
- Base `dutyOf`: sleep 21–6, meal 6–8, work 8–17, leisure 17–21. The schedules below refine the evening and night.

---

## 0. Engine facts this plan depends on
1. **The v2.2 town has no NPC props.** `Rc()` only adds the shrine, so `postFor`/`nearestProp` find nothing and every NPC stands on its home tile. Each post below needs either invisible prop markers (`bench`, `table`, `bed`, `log`, `hearth`…) or explicit post points.
2. **Mira, Orrin and Ness are not in `martsirt_world.json → npcs`.** They exist only in the taproom (`kc()`). They need outdoor entries and a schedule gate, so that the taproom copy shows only while the NPC is "inside".
3. **Ayla is not in code.** She needs an NPC record (name, role, lines, home), a 3D model hook and her quest hooks.
4. **The 3D NPC renderer plays the tinted knight's `idle` only.** See §3 for what the engine stage must add.

---

## 1. Per-NPC plan

The triangle target covers body, outfit and hair in one decimated GLB. Textures are 1024² webp: basecolor, normal and ORM.

### Wolcen (smith), west
- **Home/post:** forge door (−54.57, −14.96) [26.43, 61.04]. The forge hearth (bonfire light) is at about (−55.1, −22.2) and the door torch at (−53.1, −16.4).
- **Day:** 8–17 at the anvil (profession idle: hammering).
- **Evening:** 17–20 sits on a bench at the forge mouth by the dying coals, polishing or whetting (sit idle).
- **Night:** 20:30 banks the fire and goes inside; hidden 21–6.
- **Props at post:**
  - anvil on stump, quench barrel, grindstone
  - coal bin, tool rack
  - bench (the `bench` marker for the evening sit)
- **Body / outfit:** `male_brute_heavy`, kept at the full 1.98 m and broad-shouldered (Brian: the largest regular NPC in the game). Concept `civilian_male/06_blacksmith`: scorched leather apron, rolled linen sleeves, soot on the forearms, heavy boots.
- **Keepsake:** Odder's small apprentice hammer, hung through his apron loop. Wolcen never uses it. (Optional extra: a cold-iron offcut on a cord, the last of Quill's bands. That is a secret only Quill would recognise.)
- **Tris:** ~22k (big frame).

### Ysara (healer), east
- **Home/post:** herb-garden gateway (38.5, 21.5) [119.5, 97.5]. The garden fire/kettle light is at (43.65, 16.25).
- **Day:** 8–17 at the herb bench (profession idle: mortar and pestle).
- **Evening:** 17–20 at the garden kettle (sit or stand).
- **Night:**
  - 21–23 she is inside, hidden.
  - **Optional secret beat:** at 23:00 she walks to Noll's salt statue in the square (nearest walkable is about (−1.5, 2.5); confirm the statue node). She stands there for 20 game-minutes with no line, then goes home.
  - This is her bible secret ("talks to it at night"). If the player is near, it can be one LW bark at most.
- **Props at post:**
  - herb table with mortar, drying rack with bundles, kettle on a tripod, basket
  - stool (`table` / `hearth` markers)
- **Body / outfit:** `female_medium` (1.65 m). Concept `civilian_female/01_long_dress`: plain wool dress, linen apron with herb pouches and thread spools, sleeves pinned up, a hair kerchief.
- **Keepsake:** a strip of Father Noll's parish stole tied round her left wrist.
- **Tris:** ~20k.

### Ilyra (gate herald), south gate
- **Home/post:** south gatehouse (3, 60) [84, 136]. The gate brazier is at (1.7, 67.75); the gate torches are at (2.6/−2.6, 65.7).
- **Day:** 6–21 at the gate (standing idle, an occasional look-around).
- **Evening:** 17–21 the same.
- **Night:**
  - 21–6 she sits by the gate brazier (sit idle) and is **never hidden**. Her vow keeps her at the gate.
  - The difficulty-gate function keeps working at night (as now, with a moodLine).
- **Props at post:**
  - brazier (exists)
  - a stone mounting block or bench for the night sit, a lantern
  - a small lectern or post with the road board
- **Body / outfit:** `female_skinny` (1.60 m). Concept `civilian_female/09_cloak`: grey Open Eye habit under a travel cloak, cord belt, bare head.
- **Keepsake:** a cracked Open Eye lens on a cord at her throat. The cold-iron postern key hangs beside it, half hidden under the cloak. Only an observant player should notice it.
- **Tris:** ~20k.

### Quill (scribe, tome-keeper, Boss Stones), north of the square
- **Home/post:** scriptorium door (12.25, −25.15) [93.25, 50.85]. The window and candle lights are at (11.3, −33.3), (12.6, −27.9) and (8.9, −29.9).
- **Leash:** keep the existing scribe leash (post radius 1.6, roam 2.4–3.6).
- **Day:** 6–21 at his writing desk in the scriptorium doorway (profession idle: writing). Shelf/tome/Boss Stone duties are unchanged.
- **Evening:** the same.
- **Night:**
  - 21–23:30 inside, hidden (candle on).
  - **Optional lore beat:** "the pages go somewhere at night". At about 23:30 he walks north with a bundle under his arm to the watch-house by the north gate (south face (3.5, −55.5) [84.5, 20.5], about 30 m), pauses 10 game-minutes, then returns and is hidden by 01:00.
  - If the player sees him there, play one bark: "Thou didst not see me here…" (see QUILL_LINES_V2.md).
  - He is never interactable on that walk.
- **Props at post:**
  - writing desk with a chained book, the **unlocked coffer** (the warm tome), paper stacks
  - ink pots and quills, candle stubs, a stool
  - a page pinned to the door (`table` marker)
- **Body / outfit:** `male_skinny` (1.75 m). A long scholar's coat, faded; it was once fine cloth from the iron citadel. **Ink-stained cuffs past the wrists**, soft boots, a satchel. Concept: mix `civilian_male/09_cloak` and `01_noble`, washed out.
- **Keepsake:**
  - the **cold-iron bands** on both wrists (Wolcen's work)
  - a citadel signet ring worn turned inward
  - a burned sleeve edge (from the tome)
- **Tris:** ~20k.

### Bram (logger, quest `groves`), NE camp outside the wall
- **Home/post:** camp by Orrin's lodge (63.71, −52.96) [144.71, 23.04]. The camp and lodge lights are at about (58.2, −57.6), (64.1, −58.5) and (58.5, −54.3).
- **Day:** 8–17 at the chopping block (the existing `tickBram` log/labor post; profession idle: axe chop and haul).
- **Evening:** 17–21 at the campfire (sit on a log).
- **Night:** 21–6 asleep on a bedroll by the fire (sleep pose, or hidden if there is no sleep clip).
- **Props at post:**
  - chopping block with an axe, a split-log pile
  - a campfire ring, log seats (`log` markers), a bedroll
  - a saw on a trestle
- **Body / outfit:** `male_brute_muscular`, scaled to ~1.88 m. Concept `civilian_male/04_laborer`: wool shirt, leather jerkin, braces, sawdust, a wrapped forearm.
- **Keepsake:** six notches cut in his axe haft, one per man of his crew. He counts things.
- **Tris:** ~22k.

### Mira (Salted Kettle owner): NEW outdoor spot
- **Home/post (outdoor):** beside the inn door, off the threshold (−22.6, 18.6) [58.4, 94.6].
  - The taproom exit is at (−24.7, 17.16) and the door torch at (−23.4, 16.0).
  - The spot is 2 tiles from the door, so she never blocks the exit.
- **Day:** 8–17 outdoors at the inn door. She sweeps the step, airs the cloths and greets passers-by (profession idle: sweeping or wiping a tankard).
- **Evening:** at 17:00 she steps inside (despawn at the door) and works the bar in the taproom interior until 23:00.
- **Night:** 23–8 she sleeps upstairs, hidden. She is not outdoors at night.
- **Props at post (outdoor):**
  - a bench by the door, a barrel (the barrel group at (−32.6, 18.4) is close)
  - a mop and bucket, a chalk menu board on an easel (`bench` marker)
- **Body / outfit:** `female_curvy` (1.68 m). Concept `civilian_female/07_cook`: rolled sleeves, apron with a tap key and rag at the waist, a kerchief, a sturdy skirt.
- **Keepsake:** her father's brass tap key on a chain at her belt.
- **Tris:** ~20k.

### Orrin (drunk ex-bell-ringer): NEW outdoor home
- **Home/post:** the west side of `lodge_orrin`, facing the chapel bell tower (55.5, −55.0) [136.5, 21.0].
  - The lodge is at (60.5, −57.5) and the bell tower at (31.3, −38.6).
  - This spot is 8 m from Bram's camp, so the two share the NE corner.
- **Day:** 8–17 in a chair with a blanket by the lodge door. He sits turned *half away* from the tower and keeps glancing at it (sit idle plus a look-around fidget). He drinks from a bottle.
- **Evening walk:**
  - 17:45 he gets up and walks to the taproom door (~100 tiles, about 75 s real). Despawn at the door.
  - He is in the taproom 18:00–23:00.
  - 23:00 he walks home at ~0.8× speed (optional sway).
- **Night:** at the lodge, hidden, 23:30–8.
- **Props at post:**
  - a chair with a blanket (`bench`/`chair` marker), empty bottles under the window
  - a tankard on an upturned crate
  - the frayed bell rope coiled on a hook by the door
- **Body / outfit:** `male_regular` (1.78 m), soft and tired; the body has no beer-gut variant. Concept `civilian_male/03_casual` worn shabby: a stained tunic, an open waistcoat, a scarf.
- **Keepsake:** a length of frayed bell rope knotted as his belt, plus a leather bell-ringer's wrist guard.
- **Tris:** ~20k.

### Ness (homesick coast widow): NEW outdoor home
- **Home/post:** by her cottage door (−31.6, 53.6) [49.4, 129.6].
  - `cottage_ness` is at (−33.5, 49.0).
  - **Note:** the "Cottage" exit at (−34.34, 52.43) is the *player's stash*. Keep Ness off the exit tile, about 3 m east, so a click on the door never lands on her.
- **Day:** 8–17 by the door, mending nets or sharpening her knife on a whetstone (profession idle: whetting). She faces south toward the coast gate.
- **Evening walk:** 17:45 she walks to the taproom (~35 tiles), stays 18:00–22:30, then walks home.
- **Night:** at the cottage, hidden, 22:30–8.
- **Props at post:**
  - a fish drying rack, a net with floats, an oar over the door
  - an upturned boat used as a lean-to seat (`bench` marker), gull feathers
  - a whetstone on a stump
- **Body / outfit:** `female_thick` (1.73 m; a sturdy fisherwoman). Widow's dark wool dress, an oilskin shawl, a kerchief and salt-stained boots. Concepts `civilian_female/09_cloak` + `01_long_dress`, dark.
- **Keepsake:** her late husband's gutting knife, always on her belt (it is the knife she sharpens).
- **Tris:** ~20k.

### Ayla the Phimn: NEW (see §2)
- **Home/post:** the stable's coaching yard, in the open bay between the stable and the yard fence (45.5, 41.5) [126.5, 117.5]. The stable is at (41, 41) and the south gate is about 25 m south-west.
- **Day:** 7–19 in the yard. She stands at the bay mouth watching the coast road and the south gate (idle plus look-around), and sometimes whets a spear or checks the lame horse.
- **Evening:** 19–22 she sits on a hay bale in the bay (sit idle).
- **Night:** 22–6 up in the hayloft, hidden. She never goes to the taproom; a wary outsider.
- **Props at post:**
  - hay bales (`bench` marker), a trough, a lantern on a hook
  - her bedroll and pack visible in the bay
  - (optional, Brian to decide) a pale bone-and-steel Phimn spear leaning on a stall post, the mirror of the Feral Stalker's bone spear
- **Body / outfit:** the **existing** approved Ayla (`bodies_fit/ayla_phimn_body.glb` 1.42 m + `clothing/ayla_phimn` outfit + hair). Decimate from ~67k (27k body + 40k outfit) to ~22k and cut the textures from 2048² to 1024².
- **Keepsake:** the silver charm with the pale-blue crystal (the Phimn identifier), already modelled. Keep it readable after decimation (do not merge it away).
- **Tris:** ~22k.

---

## 2. Ayla: proposed home and role

**Home:** the stable's coaching yard and hayloft (45.5, 41.5) [126.5, 117.5].
- The stable is the "coast-road traffic stopped; one lame horse left" building, and it is otherwise unused.
- It is out of the square's eye, and its hayloft gives a wary outsider shelter without the inn's crowd.
- It is close to the south gate she would have come in by. Ilyra keeps that gate, so the two "last of their kind" women are neighbours.
- **Alternative** (if the Corrupted Phimn quests live in Briarwood): the empty north watch-house (3.5, −55.5), watching the Briarwood road.

**Role:** *Ayla, the last free Phimn, a hunter of her own kin.*
- She tracks the **Corrupted Phimn**, the demon-turned Winged Casters and Feral Stalkers (locked by Brian).
- She is a **side-quest giver**, not a vendor. Her chain: "find where they nest → put down N Stalkers/Casters → bring back a corrupted charm". The last step ends with her deciding what to do with a crystal that went red.
- Optional later: she reads the red rune markings on corrupted drops, which is a natural hook for an identify-style service or a hireling. That is out of scope for stage 1.
- **Voice:** per SFX_NEEDS_CHARACTERS, a "D2 Natalya register": quiet, wary, short sentences with a slight otherness. She keeps the archaic form like the other Martsirt NPCs (Brian: keep archaic in game).
- **Relations (suggested):**
  - Ilyra is courteous and the only one Ayla trusts.
  - Quill knows more about the Phimn than he says (a "sketchy" hook).
  - Wolcen once tried to buy her crystal.
- **Lines needed (writer task, not drafted here):** 5–7 static lines, 2–3 rumours, a quest offer/progress/done/after and 2 banter lines.

---

## 3. Banter rule (Brian, Nov 1)
- NPC-to-NPC banter fires **at most once every 60–90 s town-wide** (`banterWait = 60 + rand·30`).
- It fires **only when the player is within ~8 m** of the speaker.
- It is **one line with no reply**: drop `banterReply` and play `la` only.
- There is **none at night** (21–6), and none from hidden NPCs.
- The same rule applies inside the taproom. Indoors the pair radius stays 8 tiles, and the player-distance check still applies.
- Note: in v2.2 the outdoor homes are 25–100 m apart, so outdoor pairs within 3.1 tiles mostly happen on the evening walks (Orrin passing Wolcen's road, etc.). Most banter will happen in the taproom 18–23. That fits "alive but muted".
- Player-facing greetings and LW barks are unchanged.

---

## 4. Who delivers what

### NPC/art bot delivers (assets; push only with Brian's OK)
1. **9 NPC GLBs:** Wolcen, Ysara, Ilyra, Quill, Bram, Mira, Orrin, Ness, Ayla.
   - Body + outfit + hair, merged and **decimated to ~20k tris** (22k for Wolcen, Bram and Ayla).
   - One skinned mesh (or ≤3), with the keepsake modelled and kept readable.
   - **1024² webp** basecolor, normal and ORM. Target **≤1.5 MB per GLB**.
   - Forward +Z, metres, feet at y=0, the real height from the body (no runtime rescale).
2. **Outfits** per §1. Six new concept-to-outfit builds are needed; Ayla's exists.
3. **Baked clips in each GLB**, retargeted from the hero's town clips or from the Mixamo FBX set (method: `npc_test/README.md`):
   - `idle`, `walk`, a **standing** `talk` (Talking.fbx; the hero's `town_talk` is seated) and `sit_talk`/`sit` (from `town_talk`)
   - **one profession idle**: hammer, mortar, writing, axe, sweep, drink, whet, watch
   - optional `sleep`
   - with a **relaxed finger pose** baked in, because the source has no finger bones
4. A small shoulder/deltoid weight fix if it is still visible at the game camera.
5. **Post props** listed in §1 that are not already in the town kit (net rack, upturned boat, chair with blanket, bedroll, writing desk with coffer…). These go to the env/town bot if that bot owns town props.
6. Manifest: name → GLB path, height, clip names and the keepsake node name.

### Engine stage does (r.js; not done here)
1. **Per-NPC model loading** in `fillNpc` by name, with a fallback to the tinted knight.
2. **Clip state machine:** idle, walk, talk, sit, profession and sleep. It is driven by speed, talk state, `pose` and duty, with crossfades.
3. **Facing:** toward the movement direction, and toward the player while talking.
4. **Homes and posts:**
   - Add Mira, Orrin, Ness and Ayla to the Martsirt NPC set with the homes above.
   - Add post markers or props near each home so `postFor` works in v2.2.
   - Keep the scribe leash and add a return-to-home leash for everyone.
5. **Schedules:**
   - per-NPC overrides of `dutyOf` (§1)
   - the evening taproom walk for Orrin and Ness (Mira steps inside)
   - taproom presence gated by schedule
   - night `hide` at the home door
   - optional night beats (Quill to the watch-house, Ysara to the statue)
6. **Banter retune** per §3.
7. **Ayla integration:** NPC record, lines, side-quest chain hooks, voice table entry.
8. **Lore text:** Quill's line rewrites (QUILL_LINES_V2.md), including the "southwest corner" fixes in the static lines, bark table, arrival texts and help-panel strings.
9. Performance budget: 9 × 20k = ~180k tris and ~13 MB total. Load the NPC GLBs lazily and share them between the outdoor and taproom copies.

### Open items for Brian
- Ayla: the stable (proposed) or the north watch-house; the spear prop yes or no; whether she later becomes a hireling.
- The optional night beats (Quill's paper walk, Ysara at the statue): in or out for stage 1?
- Bodies: Wolcen stays at the full 1.98 m with a broad build, the largest regular NPC (Brian, 2026-11-01). Bram is scaled to ~1.90 m.

## 5. Brian decisions (2026-11-01, 3:58 PM)
- Ayla: NOT a hireling. She stays in the stable yard (proposed spot kept). The spear prop is optional and only added if it's easy.
- Homes and posts: keep them as planned (Brian likes them).
- Rotation: regulars often rotate visits to the town fire, the Salted Kettle and similar social spots during the day and evening (short visits, then back to their post).
- Wolcen: only goes between his home/forge and the outside of it, plus the fire sometimes. He never goes to the inn.
