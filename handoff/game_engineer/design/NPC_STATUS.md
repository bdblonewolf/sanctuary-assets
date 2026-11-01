# NPC status: Martsirt NPC & town stage (3D)

Written 2026-11-01 (ET) from: live build `live_12d/r.js` (same hashes as https://gold-iris-zippy-bird.grok.me), `sanctuary-assets` @ 04e3fe1,
`sanctuary_env/martsirt_v2_2`, `sanctuary_art` (lore, races, audio notes), `sanctuary_npc` (3D bodies, outfits, anim tests),
`story/story_bible.md`, `story/data/voices.json`, `design/DESIGN_NOTES.md`, `living_world_roadmap.md`, `port_audit_2d_to_3d.md`.
Read-only survey: no game or asset files changed, nothing pushed.

Scope (Brian): this stage covers **Martsirt only**. Other towns come later if this works.
Brian's rules for smart NPCs: keep the new v2.2 home spots. NPCs drift but always return home, keep their daily routines,
talk to each other much less (D2-style: alive but muted), and keep their dialogue with lore tweaks.

---

## 1. Martsirt roster (8 NPCs)

Home spots are the v2.2 values (`martsirt_world.json` tile → metres from `REPORT_v2.md`; the square is at 0,0).
"Live code" means the NPC exists in r.js. All of them use the 2D legacy town unless `view3d` is on (see §3).

| NPC | Role (code role) | Zone | Home spot v2.2 | Model file (art / pushed?) | Rig & animations | Lore / voice note | In live code? |
|---|---|---|---|---|---|---|---|
| **Wolcen** | Smith, vendor (`smith`) | Martsirt, west | Forge door, (−54.6, −15.0) m, tile [26.43, 61.04] | **None.** No body or outfit assigned. Concept sheets `civilian_male/06_blacksmith` exist, not mapped. Repo: none. | 3D: tinted hero knight, `idle` only | voices.json: gruff workman, *not archaic*. Live static lines are archaic ("an thou hast the coin"). Secret: he made Quill's cold-iron bands (bible + Quill v2 agree). | Yes. `gc()` town plus LW lines `wolchen_t01…`, `_r01`, `_i01-03`, quest `wol1` |
| **Ysara** | Healer, vendor (`healer`) | Martsirt, east | Herb-garden gateway, (38.5, 21.5) m, tile [119.5, 97.5] | **None** | same | Clinical, not archaic. Feeds Quill. | Yes, plus LW `ysara_t01…` |
| **Ilyra** | Gate herald (`herald`) | Martsirt, south gate | South gatehouse, (3, 60) m, tile [84, 136] | **None** | same | The *only* canon archaic speaker (KJV). | Yes, plus LW `ilyra_t01…` |
| **Quill** | Scribe, tome-keeper, Boss Stones (`scribe`, quest `firstread`) | Martsirt, NNE of the square | Scriptorium door, (12.25, −25.15) m, tile [93.25, 50.85] | **None** | same; leashed (roam 2.4–3.6, post radius 1.6) | **Lore v2 changed today (art bot, 2:36 PM ET):** archaic, sketchy but good, hiding something, ex-high seat in the iron citadel, buys Holt's spare paper, pages go somewhere at night. Voice: low near-whisper, dry chuckle, never menacing. | Yes. Static lines (archaic) plus LW `quill_t01–t12`, `quill_r01` (anxious, modern) |
| **Bram** | Logger, quest giver (`quest`, quest `groves`) | Martsirt "Camp", NE outside the wall | Near Orrin's lodge, (63.7, −53.0) m, tile [144.71, 23.04] | **None** (a `male_brute_*` base would fit) | same; special `tickBram` (log/labor post) | Few words, counts things. Courting Mira. | Yes, plus LW `bram_t02…` |
| **Mira** | Taproom owner (`inn`) | Salted Kettle **interior only** | Interior (8, 2.95), roam 2.2. **No v2.2 outdoor spot.** | **None** (civilian_female `07_cook` concept, not mapped) | same | Teasing hospitality. Waters the ale for Ysara's thread. | Yes, taproom `kc()` |
| **Orrin** | Drunk ex-bell-ringer (`inn`) | Taproom interior | Interior (5.5, 5.7). The v2.2 town has `lodge_orrin` (60.5, −57.5), but Bram stands there, not Orrin. | **None** | same | Self-mocking; avoids the chapel bell. | Yes, taproom |
| **Ness** | Homesick widow (`inn`) | Taproom interior | Interior (10.5, 5.55). v2.2 has `cottage_ness` (−33.5, 49.0), but the "Cottage" exit leads to the player's stash. | **None** | same | Sharpens her knife at the table; wants the coast. | Yes, taproom |

Shared schedule (`dutyOf`) for all eight: sleep 21–6, meal 6–8, work 8–17, leisure 17–21. Posts come from `postFor`
(bed, table/hearth/well/bar, sit props; Bram uses logs).

### Other towns' NPCs (brief, out of this stage's scope)
- **Wilds / Briarwood / Blackwater:** Holt (ferry), Myrine and Orithya (guards), Sable (rival tome seller).
- **Qadren:** Orlem (mage), Heska (guard), Vetch (gambler).
- **Highmarket:** Cal (quest), Pell (guard).
- **Cinder:** Sarn. **Castle:** Vesper (fence).
- **Generic `To()`/`wc()` townsfolk:** Wynn, Rusk, Sera, Odder, Iskra, Moth, Calder, Hask, Nim, Vellum, Lute, Kell, Brine, Jas, Piet, Ors, Hesta, Voss, Ilen, Tamsin.
- **Ayla (Phimn)**, side-quest NPC: the **only NPC with a finished dressed model** (approved 2026-10-31). She is not in code and her zone is not defined.

---

## 2. New from the art / NPC bots vs what's live

**New (last ~3 days, none of it in the repo or the game):**
- `sanctuary_npc/approved/`: **12 base bodies** (MPFB2/MakeHuman, Blender 4.2).
  - 7 female: curvy 1.68, medium 1.65, hourglass_a/b 1.65, skinny 1.60, thick 1.73, tiny 1.47 m.
  - 5 male: brute_heavy 1.98, brute_muscular 1.98, regular 1.78, skinny 1.75, vshape 1.85 m.
  - Each is 27,036 tris, ~0.95 MB, one mesh `base`, materials skin / linen_undergarment / eye, untextured.
  - **Skin: 52-bone `mixamorig:` skeleton** (fingers included). No animation clips.
- `sanctuary_npc/animtest/*_anim.glb`: male_regular, female_medium v7–v9b, female_tiny and male_brute_heavy.
  - Clips are **Idle (8.3 s) and Looking Around (6.3 s) only**.
  - Mixamo FBX already in `animtest/anims/`, not baked: Walking, Talking, Waving, Weight Shift, Bored, Standing Arguing, plus combat and death clips.
- `sanctuary_npc/clothing/`: a modular outfit system (`manifest.json` v1).
  - One skinned GLB per piece, with per-body vertex masks so the body is hidden under worn pieces; forward +Z.
  - Outfit `11_leather_bikini_white` (hourglass_a): 73.7k tris, 3.25 MB.
  - Outfit `12_leather_bikini_redbrown` (hourglass_b): 76.5k tris, 3.23 MB.
  - Ayla: `npc_f_ayla_phimn_ayla_phimn_body.glb` (9 outfit meshes, 39.9k tris, 2.47 MB, 3 × 2048² webp: normal, basecolor, orm), plus `bodies_fit/ayla_phimn_body.glb` (1.42 m, skin 3 × 2048² webp), plus hair.
  - None of these are Martsirt characters.
- Concept sheets: `sanctuary_art/civilian_male/01–10` and `civilian_female/01–12`, including a blacksmith, cook, merchant and laborer. **No NPC-to-outfit mapping exists.**
- Lore: `lore/quill_martsirt.md` **v2** (today). See §3.
- `audio/SFX_NEEDS_CHARACTERS.md`: the list of character voice and SFX needs. Martsirt NPCs are P0. It notes that no NPC has a model.
- `quests/HOLD_story_factions_skillquests.md`: **ON HOLD per Brian. Not to be used.**
- Monsters `sanctuary_npc/monsters/starter/*` use mixamorig too (54–65 bones). They are not NPCs.

**Live today:**
- Every NPC, in both 2D sprites and 3D, renders as `plated_knight_rigged.glb` tinted `0x3A2418` at 1.8 m (`fillNpc`, r.js ~76836).
- It plays `idle` only, with no walk, no facing (yaw never set), no sit/sleep/labor poses, and no per-NPC model.
- The town GLBs (martsirt v2.2, 165 placements) and the Martsirt theme are pushed.
- NPC voice audio: **none** in `sanctuary_audio` or the repo.

**Rig compatibility (good news):**
- The hero anim file `knight_anim_v10b.glb` (27-joint `mixamorig:`, no fingers) **already contains town clips**: `town_idle`, `town_walk`, `town_talk`, `town_wave`, `town_argue`, `town_bored`, `town_look_around`, `town_weight_shift`, `unarmed_walk/run`.
- The hero already uses them in its `peace` set (r.js ~74701).
- The new 52-bone bodies share the same `mixamorig:` bone names. Retargeting by name should work, with fingers staying in bind pose.
- So NPCs can probably use the hero's town clips with no new anim baking. This needs a quick in-engine check of bind-pose and scale differences between MPFB and the knight.

---

## 3. Gaps & mismatches (Martsirt)

1. **No named Martsirt NPC has a model.** There are only bare bases, two non-Martsirt outfits and Ayla. Nothing NPC-related is in `sanctuary-assets`.
2. **The renderer can't do NPCs yet.** `fillNpc` hard-codes the hero GLB. There's no per-NPC URL, no `walk`/`talk` state switch, no rotation toward movement or the player, and no pose clips.
3. **v2.2 home spots only apply in 3D.**
   - `zc('town')` uses `Rc()` only when `fs.townMartsirt && fs.view3d && gs`. Since `fs.view3d` defaults to false, the 2D game uses the legacy 40×34 `gc()` coordinates.
   - Also, `postFor` looks for `bed/table/well/bench…` props near each home. Those props need to exist near the v2.2 homes, or NPCs will just stand on the home tile.
4. **Quill's home contradicts lore.** The v2 lore and his live line ("I keep to the southwest corner of the square…") say SW of the square. The v2.2 home (keep, per Brian) is the scriptorium, about 28 m **NNE** of the square. The lore/line needs a tweak, e.g. "I keep to my scriptorium, north of the square."
5. **Quill's voice and backstory have three versions.**
   - voices.json and the story bible: anxious, modern scholar; Noll's clerk who copied the book of names with Ysmer.
   - Lore v2: archaic, sketchy, an ex-high seat of the iron citadel.
   - Live: static lines are archaic, but LW lines `quill_t01–t12` are modern and anxious ("Ysara brought bread. I ate the bread…").
   - The bible also says only Ilyra speaks archaically, but in live code most static lines (Wolcen, Ysara, Bram…) are archaic too.
   - DESIGN_NOTES still lists "Quill's voice" as waiting on Brian.
6. **Bram's home.** The bible says "Briarwood camp". The v2.2 town puts him at a camp by Orrin's lodge, outside the NE wall of Martsirt (keep, per Brian). Two bible lines need a tweak.
7. **Mira, Orrin and Ness have no outdoor presence.** They only exist inside the taproom. `cottage_ness` and `lodge_orrin` are built but empty, and the "Cottage" exit is the player's stash, not Ness's home.
8. **Banter is too chatty for Brian's rule.**
   - `maybeBanter` fires every 11–21 s for any `bD` pair within 3.1 tiles (8 indoors), and the second NPC answers.
   - Ambient `bark`s and LW lines also fire, though they are less frequent.
9. **Model budget.**
   - A dressed NPC is about 100k tris and 3–4 MB with 3–6 × 2048² textures (Ayla: 27k body + 40k outfit).
   - Eight of them is ~800k tris and ~30 MB, more than the whole town.
   - They need LOD/decimation to ~15–25k tris and 1024² textures for the isometric camera.
10. **Keepsakes.** DESIGN_NOTES asks that "each NPC's keepsake is visible on their model". No keepsake list exists per NPC.
11. **No NPC voice audio** (voices.json has text direction only). This is a later audio task, not 3D.

---

## 4. Questions (for Brian / art bot)

1. **Quill's voice and past.** Lore v2 makes him archaic and an ex-high seat of the citadel, but the bible and voices.json say anxious modern scholar and Noll's clerk. Is v2 canon? If so, should his 12 live LW lines be rewritten archaic, and should the bible and voices.json be updated?
2. **Archaic speech in general.** Canon says only Ilyra (now plus Quill?) is archaic, but most live static lines for Wolcen, Ysara, Bram and Mira are archaic. Should their lines be modernised to match voices.json, or should voices.json follow the game?
3. **Look per NPC.** Which base body and outfit/concept sheet goes to each of the 8 Martsirt NPCs, and what is each one's visible keepsake? Is the art bot building their outfits next? Only bikini/leather outfits and Ayla exist so far.
4. **Mira, Orrin and Ness outdoors.** Should they get v2.2 outdoor homes (Ness → `cottage_ness`, Orrin → `lodge_orrin`, Mira → inn door) with routines that walk them to the taproom in the evening, or stay taproom-only for this stage?
5. **How muted is "muted"?** Proposal: NPC-to-NPC banter at most once every 60–90 s town-wide, only when the player is within ~8 m, a single line with no reply chain, and none at night. Should player-facing greetings and barks stay as they are?
6. **Ayla.** Is she in Martsirt for this stage, or later? Where is her home spot?

---

## 5. Suggested scope for the Martsirt NPC & town stage (3D only, in order)

1. **Rig check (small).** In a scratch build, load `approved/male_regular.glb` and play `town_idle` and `town_walk` from `knight_anim_v10b.glb` by bone name. Check bind pose, scale and foot sliding. If it fails, bake Walking/Talking/Idle from the `animtest/anims` FBX the way the animtest files were made.
2. **Character mapping (art bot plus Brian).** Assign body, outfit and keepsake for Wolcen, Ysara, Ilyra, Quill, Bram, Mira, Orrin and Ness (Q3).
3. **Build the 8 NPC GLBs (art/NPC bot).** Merge body and outfit, decimate to ~20k tris, use 1024² webp textures, and target about 1.5 MB each.
   - Clips: town_idle, town_walk, town_talk, plus one profession idle each (Wolcen hammering, Ysara mortar, Quill writing, Bram axe/haul, Mira wiping the bar). Sit and sleep are optional.
4. **Push** under `models/npc/martsirt/<name>.glb` (needs Brian's OK; not done here).
5. **Renderer.**
   - Give `fillNpc` an NPC-model map by name with a fallback to the tinted knight. Use per-NPC `targetHeight` from the base heights.
   - Switch between `idle`, `walk` and `talk` from movement speed and talk state, with crossfades.
   - Face the movement direction, or the player while talking.
   - Map poses (sit/labor/read/sleep) to clips where they exist.
6. **Homes and leash.** Use the v2.2 `gs.npcs` homes (unchanged). Keep `dutyOf`/`postFor`, and add the bench/table/well props each post needs near each home. Wander radius should be ~2–4 m around home, with a hard return-to-home leash.
7. **Mute chatter.** Retune `maybeBanter` per Q5, with no reply chains and night silence.
8. **Lore tweaks.** Change Quill's "southwest corner" line to the scriptorium. Apply the Q1/Q2 voice decisions to LW lines, and fix the Bram camp text. Keep all dialogue content otherwise.
9. **(Optional)** Outdoor homes and routines for Mira, Orrin and Ness (Q4), and a 3D taproom interior with all three.
10. **(Later stages)** NPC voice barks (audio), Ayla placement, other towns.
