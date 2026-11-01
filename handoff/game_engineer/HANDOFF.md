# Sanctuary - Game Engineer handoff (Nov 1, 2026, 5:30 PM ET)

Everything the Game Engineer bot holds for Sanctuary. Live game: https://gold-iris-zippy-bird.grok.me
Brian pastes stage prompts into Grok Build on Android. No bot edits the site directly.

## Folder map (this folder)
- `prompts/`: every stage prompt sent so far (Stage 1 to 12F, A1/A3/A4 audio, P1 pathing, N1a/N1b NPCs, skill fixes).
- `design/`: NPC plan, NPC 2D audit, NPC status, Quill lines v2, skill web summary + CSV + synergy JSON, design notes, angel lore, companion demon math, live minified-name notes, Wolcen/Quill manifest.
- `audio/`: SFX needs and master lists (engine, environment, characters).
- `GLB_LIST_models.txt`: all 453 GLB paths already in this repo under `models/` (town, trees, plants, weapons, shrines, anims).

## How prompts are written (keep this format)
- RULES block, these three lines verbatim:
  - New features are 3D only. Do not touch any 2D drawing code.
  - If a step fails twice, stop and report. No retry loops. Build once, check the console, publish.
  - Be strict: change only what is listed.
- Then FACTS (verified code names, anchored by string literals), numbered STEPS, TEST, and REPORT: "One line per step: STEP n - done / failed (reason). Then console errors (if any) and files changed."
- Send the full prompt inside ~~~ fences. Keep builds short (about 6-8 steps). Never use the words "honest" or "quiet".
- Rough first, polish later. Only Brian's own words approve things.
- Asset repo commits: `git -c user.name="bdblonewolf" -c user.email="306882562+bdblonewolf@users.noreply.github.com"`, `git pull --rebase` first. Raw base: https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/

## Live build state
- Live now: index-11yoiqo-.js / routes-CG27QmQk.js = Stage 12F (v3 gnarled oaks and dark pines, models/outdoor/v3trees, ?v=12f). Clean, no console errors. Brian: trees working great.
- Earlier verified: 12D shores (no cliffs, sparse beaches, a seam; polish later), 12E plants (texture leak fixed), A3 town theme, A4 overworld theme.
- 3D view is still off by default; 2D and 3D towns use different coordinates.

## Current work: Martsirt NPCs (start town)
- N1a (`prompts/STAGE_N1_MARTSIRT_NPC_LOGIC_PROMPT.txt`, 7 steps): loaded by Brian, NOT yet published (checked at 4:50 PM). It adds invisible fire/seat/door markers in Rc(), Mira/Orrin/Ness/Ayla records, display name Wolcen (key stays Wolchen), visit rotation, inside hours, longer routes (routeOpen ?? 99 bug fix, heap, caps 9000/600), Bram re-anchor, banter rule, 3D facing and bark labels. Placeholder knight models stay.
- N1b (`prompts/STAGE_N1B_QUILL_LINES_PROMPT.txt`): Quill's ~48 line swaps. Send after N1a publishes. Anchors verified against the 12F bundle.
- After that, one 2D strip stage: step 1 makes 3D the default, then remove 2D drawing code and keep shared logic. Then drop the "do not touch 2D" rule line.
- N2 (not written): load per-NPC GLBs (one GLB per NPC: <id>_body_<region>, <id>_hair, <id>_outfit_<slot>, rigid <id>_prop_*, <id>_keepsake; hide body regions per MANIFEST slot_hides), clip states idle/walk/talk/sit/sit_talk/work/sleep, lift heels ~1 cm. Wolcen and Quill GLBs delivered by the art bot in /workspace/sanctuary_npc/martsirt/ (wolcen 1.98 m 1.39 MB; quill 1.76 m 1.24 MB). Waiting on Brian's review; the other 7 wait until then.

## NPC decisions (Brian)
- 9 NPCs: Wolcen (smith, west, 1.98 m, biggest regular NPC), Ysara (healer, east), Ilyra (gate herald, never leaves the south gate), Quill (scribe/tome keeper, scriptorium north of the square), Bram (logger, NE camp, ~1.90 m), Mira (Salted Kettle owner, inn door), Orrin (drunk ex-bell-ringer, lodge), Ness (coast widow, cottage), Ayla the Phimn (stable yard by the south gate; not a hireling; spear only if easy).
- Quill: archaic, sketchy but means well; all his lines rewritten (QUILL_LINES_V2.md). Others keep their archaic lines.
- Regulars rotate frequent short visits to the town fire (bonfire_main, tile 95.99,75.48) and the Kettle. Wolcen only forge/outside and sometimes the fire, never the inn.
- Chatter: one line every 60-90 s, only near the player (~8 m), no reply, none at night (21-6).
- Standing art rule: bare body rigged, clothing/gear as separate skinned meshes on the same skeleton.

## Balance and design locks
- No Magic Find that varies per playthrough; quest and progression XP fixed; no faction or quest buffs; no power creep.
- Factions are flavour only (quests, sidegrade uniques, lore, cosmetics, shop stock, dialogue). Faction lock steers schools only; town rep affects prices and gold, not XP. Fixed 14 skill books.
- Factions, quest pool, 14 Normal skill quests, angelic lore: ON HOLD as reference until Brian directs.
- B1 balance fix (quest XP scaling, XP shrine x3.5, fate/loot, MF on rings, regard prices): after priorities.

## Backlog (later)
- Audio stage: crypt theme (sanctuary_audio release/audio/dungeon/crypt_theme.ogg) + fix wild/* loops playing in the 'stone' mood, interior check missing root/undercroft, dread/overworld.ogg vs overworld_theme.ogg name mismatch.
- Shore polish (cliffs/headlands, beach coverage, seam). Env bot's 10 gothic trees (approved, on hold).
- Gothic props and loot containers, the boat, 3D combat visuals, fog and rain. Skill synergies: most of 153 not coded yet.
