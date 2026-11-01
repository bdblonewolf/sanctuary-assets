# NPC 2D → 3D Audit (Martsirt) — live_12e/r.js

Read-only audit, 2026-11-01. Nothing in the game has been edited.
Line numbers refer to `/workspace/sanctuary/live_12e/r.js`, the formatted Vite bundle, so the minified names will change on each build.

**Coordinates.** v2.2 town tile = metres + origin [81, 76], and 1 tile = 1 m. The sim runs in tiles (e.x, e.y). The 3D renderer places NPCs at `(x, 0, y)`.

**Legend.** **3D** = already affects the 3D view. **2D-only** = drawn only by the canvas renderer. Verdict = **REUSE** (as-is) / **ADAPT** / **MISSING**.

> Big picture: the NPC *sim* is renderer-agnostic and mostly reusable. Two things make it nearly inert in 3D Martsirt:
> 1. `Rc()` builds the v2.2 town with **no props** except the angel shrine, so there are no bonfire, bench, bar or building props for posts, needs or doorsteps to use.
> 2. The 3D renderer only teleports tinted knight models: idle clip only, no rotation, no poses.

---

## 1. Town fire location (v2.2)

| What | Placement | Metres (x, z) | Tile (sim) | Notes |
|---|---|---|---|---|
| **Main town fire** | `bonfire_main` / `prop_bonfire_main.glb`, rotY 0.2967 | **(14.99, −0.52)** | **(95.99, 75.48)** | About 15 m east of the square (0, 0). FX: `fx_fire_bonfire_main` + `fx_embers`. Matches the `bon:true` light in martsirt_world.json. |
| Gate campfire | `campfire_gate` / `prop_campfire.glb` | (−9.0, 59.1) | (72.0, 135.1) | Small fire just inside the south gate. |

- **Other bon:true lights (tile):**
  - inn-area fires (49.82, 84.09) and (63.28, 86.9)
  - forge (25.86, 53.76)
  - Ysara (124.65, 92.25)
  - gate brazier (82.7, 143.75)
  - Ness (47.9, 124.92)
  - Orrin/Bram camp (139.24, 18.45)
  - watch-house (82.0, 19.41) and (83.81, 16.68)
- **Rc() lights are lighting only.** `Rc()` turns them into `{x, y, r:90, warm}`. No `bonfire` prop is created, so `townPyre()` returns undefined in 3D and every fire behaviour is off.
- **Distances from the fire** (tiles):
  - Wolcen home (26.43, 61.04): about 71
  - Quill (93.25, 50.85): about 25
  - Ysara (119.5, 97.5): about 32
  - Bram (144.71, 23.04): about 72
  - Ilyra (84, 136): about 62
  - Inn door (≈58.4, 94.6): about 42

## 2. NPC records

| Item | Where | Status |
|---|---|---|
| Town NPCs `gc()` (Wolchen, Ysara, Ilyra, Quill, Bram): name/x/y/homeX/homeY/lines/role/roam/quest/wander | 29243–29334 | REUSE. Roles: smith, healer, herald, scribe, quest. roam is 5.6/5.8/6.2/3.2/1.4 tiles, tuned for the 40×34 town. |
| `Rc()` re-homes them from `gs.npcs` by **name** | 30957–30961 | ADAPT. The json only has those 5 names. Mira, Orrin, Ness and Ayla do not exist in the 3D town. |
| Taproom NPCs: `kc()` → `wc(name, x, y, lines, roam)` builds Mira (8, 2.95), Orrin (5.5, 5.7), Ness (10.5, 5.55) | 30216–30300 (`wc` 30127) | REUSE for record shape. They live only in the taproom area. |
| "About themselves" bark pool `var es` / `cs()` talk sub-menu (self / news / this place) | 27093, 27441 | REUSE |
| LW interaction one-liners `Wn` (`wolchen_i01`…) | 14147–14541 | REUSE |
| Ayla | — | MISSING. No record, lines, LW entries or json home. |

- **Name hazard.** The display rename is Wolcen, but the code uses `Wolchen` in:
  - gc
  - martsirt_world.json `npcs`
  - LW ids `wolchen_*`
  - quest `wol1/wol2.who`
  - banter `Jn`
  - `postFor` (`e.name === 'Wolchen'`)
  - the `Cr()` night bonus
  - the taproom Orrin line

  Rename only via a display-name field, or rename everything at once.

## 3. Schedules / duty (day-night)

| Function | Lines | What | Status |
|---|---|---|---|
| `dutyOf(e)` | 86733+ | Returns sleep/meal/work/leisure by hour. Default: sleep 21–6, meal 6–8, work 8–17, leisure 17–21. Amazon/ferry always work; gambler and guard have their own tables. | REUSE. Add per-NPC tables (Ayla: work 7–19, sit 19–22, hidden at night; Wolcen). |
| `dutyBlurb`, `moodLine`, `wake` | 87386, 86860s | Talk-menu flavour by duty, role and regard. Talk menu at 80365. | REUSE |
| Regard/duty readout | 91955, 92143 | Debug overlay | REUSE |

## 4. Posts / props / markers

| Function | Lines | What | Status |
|---|---|---|---|
| `postFor(e)` | 87407–87542 | Picks a post by duty and role. Sleep → bed; meal → table/hearth/pot, else bonfire/well/bar; leisure → bar/bonfire/well/chair/bench/log within roam+2.4; inn role → bar. Special cases: Vesper, Bram, and Wolchen (barrel/table within 6). | ADAPT. The logic is fine, but **3D has no props**. It needs marker props injected in `Rc()`. |
| `nearestProp(e, kinds, r)` | 87366 | Nearest prop of a kind | REUSE |
| `dockBeside(prop, e)` | 87096 | Hash-seeded ring slot around a prop, wider for bonfire and hearth. This gives the circle around the fire. | REUSE |
| `spotTaken`, `clampPost` | 87120, 87376 | Avoid stacking; scribe leash 2.2–3.5 | REUSE |
| `holdPost`, `faceProp` | 87296, 87279 | Stand at the post and face the prop (sets `e.facing`) | REUSE |
| `doorstep(x, y)` | 88661 | Door tile in front of a `building` prop | ADAPT. Needs `building` props (w/d) in `Rc()`. |

The v2.2 placements.json has 14 buildings: inn (−24.5, 9.5) m, forge (−50.5, −21.5) m, stable (41, 41) m, and others. It has barrel groups, a market stall and a crate stack. It has **no** bench, log, well, table or bed props, so marker props must be authored.

## 5. Walking / pathing

| Function | Lines | Status |
|---|---|---|
| `routeOpen(e, tx, ty)`: A* over `npcBlocked` | 87144 | **ADAPT.** Capped at **240 expansions / 80 steps**, sized for 40×34. v2.2 trips are 25–100 tiles, so long routes fail silently and NPCs fall back to direct steering. Raise the caps, or add waypoint and road-graph legs. |
| `losOpen` | 87135 | REUSE |
| `aimNpc`, `advancePath`, `stepNpc`, `stepToward`, `stepAside`, `separateNpcs` | 87219, 87229, 87254, 87574, 87700, 88614 | REUSE |
| `npcBlocked` | ~88680 | REUSE. Uses `world.solid`, which `Rc()` fills from the json bitmask. |
| `faceNpc(e, dx, dy)` sets `e.facing = atan2(dx+dy, dx−dy)` (iso convention) | 88700 | REUSE. The 3D conversion `IE()` (75072) already exists and is used for mobs. |
| `watchNpc` stuck detector (shim) | 84512 | REUSE |
| `stroll`, home leash | 87312, wanderNpc | ADAPT. The roam values are small; retune per NPC for the bigger town. |

## 6. Living-world routine loop

| Function | Lines | What | Status |
|---|---|---|---|
| `wanderNpc(dt)` main loop | 88340–88612 | Calls maybeBanter and tickRumors; unsticks NPCs; dispatches ferry → `tickHolt`, amazon → `tickAmazon`, Bram → `tickBram`, everyone else → `lifeBeat`. Leisure includes a 16% chance to enter a building (hidden 3.2–5.6 s). Visits another NPC within roam; home leash at roam+0.8. | REUSE as the skeleton |
| `lifeBeat(e)` | 88155–88277 | Order: needs → hang → pose timers → guard/herald `stepBeat` → quest chores → go to post via `postFor`/`aimNpc`/`holdPost` | REUSE. This is where a visit rotation should slot in. |
| `stepBeat` | 87543 | Guard/herald patrol beats (Ilyra) | ADAPT. The beat points come from props and home. |
| `tickBram` | 87650 | Labor → haul → flute at **hard-coded legacy 2D coords** (26.2, 11.2), (30.6, 10.15), (28, 12.15) | **ADAPT (broken in v2.2).** Bram would walk to the wrong place, 70+ tiles away. |
| `tickHolt`, `tickAmazon` | 87594 | Not Martsirt | n/a |
| `busyWith` | — | Player-talk freeze | REUSE |

## 7. Needs system ("living world")

| Function | Lines | Status |
|---|---|---|
| `seedNeeds`: hunger, fatigue, boredom, entertained, cold, fear, happy, sad (hash-seeded) | 87739 | REUSE |
| `tickNeed`: hide/eat/ash/warm/rest/feed/play/wash/bar. Excludes Bram, Vesper, ferry and amazon. | 87775 | REUSE. **Warm** and **bar** are the "short social visit" behaviours Brian wants. |
| `needPost`: props within **9.5 tiles of home** (1.8 for the scribe) | 87902 | **ADAPT.** With the fire 25–72 tiles from homes, it will never be chosen. Add per-NPC allowed social spots instead of a radius. |
| `needLine`, `serveNeed` | 87991, 88010 | REUSE (bark text) |
| `townPyre`, `nearHeat`, `pyreTender` (herald → guard → nearest) | 87720–87753 | REUSE once a `bonfire` prop exists. `hc()` (~29055) auto-converts a town bonfire to `style:'town'`, fuel 0.6. |
| `tickSmart`: pyre fuel decay, "down to coals" bark, light radius by fuel, arches barred at night | 88095 | REUSE. Check that the 3D fire FX/light follows fuel; the 3D bonfire is a static GLB. |

## 8. Barks / chatter / banter

| System | Where | Status |
|---|---|---|
| `bark(e, line, secs)` floating line | 88278 | 2D-only render. ADAPT: needs a 3D speech label (`project()` at ~75480 can position HTML). |
| `maybeBanter`: generic pairs `DD` (78796) + `ls` (27471); every 11–21 s; radius 3.1 tiles (8 indoors); reply | 88284–88339, state at 79016/79018 | ADAPT. Brian's rule is once per 60–90 s town-wide, player within ~8 m, no reply, none 21–6. Scribe excluded. |
| LW named banter `Jn` (ban_00…), `Yr()`, called from `storyBeat()` | 14551, 15326, 81864–81893 | REUSE. Gap 90 s, NPCs within 12 tiles of the player, 24 h per-pair cooldown, B replies after 2.5 s. **Two banter systems run together**; pick one for town. |
| Fire rumours `OD` / `tickRumors`: needs a pyre with 2+ NPCs within 3.5; every 16–30 s | 78807, 88126 | REUSE once the bonfire prop exists. Good "people at the fire" flavour. |
| Town-fire flavour text | 78694, 90930 | REUSE |

## 9. Regard

| Function | Lines | Status |
|---|---|---|
| `regardOf`, `noteRegard` (theft/aid/trade/gift memory), `witness` (r 6.5), `grantFavor` (≥55 → 20 g), `tip` (40 g → +12), `vendorMul` (≥45 ×0.88, ≤−20 ×1.22, asleep ×1.12), `shopShut` (≤−40) | 86733–86909 | REUSE. Pure data on `player.regard` (init 21935/22124). |
| LW condition evaluator `vr()` with `regard`, `hour`, `wx`, `boss`, `quest`, `help`, `recent`, `act`, `diff` and `flag` keys | 14983–15045 | REUSE |

## 10. Dialogue trees and quest hooks

| Piece | Where | Status |
|---|---|---|
| Talk menu: `talk()` → `Ir()` (quest progress) + `Cr()` (best LW line by pri/cd/when/mood), `rumors()` → `wr()`, `hearHelp()` → `Dr()/Er()` offer | 90380–90440; Cr 15067, wr 15099 | REUSE (renderer-free) |
| `Gn` talk lines: 192 total (Wolchen 15, Ysara 13, Ilyra 11, Quill 12, Bram 12, Mira 11, Orrin 2, Ness 2) | 14543 | REUSE. Ayla has none. |
| `Kn` rumours: 96 total (6 each for the town five and Mira; 1 each Orrin/Ness) | 14546 | REUSE |
| `qn` quests: 30 total. Town ones: wol1 Millrace Stone, wol2 Thirty-One Irons, ysa1, ysa2, ily1, ily2, qui1, qui2, bra1, bra2 (deliver → Mira), mir1, mir2 | 14549 | REUSE. **Cross-area hooks:** `bra2` delivers to Mira, `qui1/mir2` deliver to Hesta, and `wol2` delivers to Piet. Mira must be reachable. |
| Boss-reaction lines `lr` | 14864 | REUSE |
| `Hr()`: Ness is hidden permanently (`hide = 1e6`) 72 h after the `ness_home` flag | 15291, 81874 | REUSE. Note for scheduling: Ness can vanish by story. |

## 11. Visits to the fire / inn / taproom

- **Fire.** This happens only through the needs system: `warm` → bonfire via `needPost`, rumours, and `pyreTender` feeding. In 3D everything is off, because there is no bonfire prop and the radius is 9.5.
- **Inn/taproom.** Taproom NPCs are fixed copies in `kc()`. There is no NPC transfer between areas, and no schedule decides who is inside. The `bar` need targets `bar` props in the current area only.
- **Building visits.** The leisure "enter building" hide (16%, 3.2–5.6 s) is the only "go inside" behaviour.
- **MISSING** (per Brian's decisions):
  - a visit rotation for regulars (short trip to the fire, the Kettle door or social spots, then back to post)
  - Wolcen restricted to forge ↔ outside ↔ fire, never the inn
  - Ayla kept inside the stable-yard area
  - schedule-gated taproom presence: whoever is "in the Kettle" in town should appear in `kc()`

## 12. 3D spawning and animation

| Piece | Lines | Status |
|---|---|---|
| `poseNpcs(state)` | 77110–77134 | **3D.** Creates a group per NPC and hides it if `hide > 0`. Position `(x, 0, y)`, `actor.update(0.016)` at a fixed dt. **No rotation, no walk/idle switch, no poses.** |
| `fillNpc` | 77135–77146 | **3D.** `rT(fs.heroModelUrl → plated_knight_rigged.glb, us, {tint: 0x3A2418, targetHeight: 1.8})`, plays `idle`. Every NPC is the same brown-tinted knight. `us` maps idle/walk/run/attack/hit/death to Idle/Walk/Run… (27539). |
| Actor class `nT` (`bind`, `playState`, crossfade 0.15) | 72302–72435 | REUSE for the NPC anim state machine. |
| Mob precedent: `poseMobs` sets `rotation.y = IE(a.facing)` and detects movement via lx/ly | ~77005 | REUSE the pattern: copy it into poseNpcs. |
| Hero town clips (`jE.peace`: town_idle, unarmed_walk, fidget town_look_around / town_weight_shift) from `knight_anim_v10b.glb` via `buildKnight()` (`PE` strips hip root motion) | 74988, 75685 | ADAPT. A source of talk/wave/argue/sit-like clips for NPCs. Needs a retarget/bind onto the NPC rig. |
| 2D pose vocabulary: sit, sleep, eat, drink, cook, read, labor, haul, flute, fish, perch, ground, water | various | MISSING in 3D. Map each to a clip or a fallback (idle). |
| Interiors in 3D: taproom and inn render through the generic modular kit `buildZone()` | 76781 | ADAPT. Only floors, walls, torches, bonfire, barrel/crate/chest and arches render. **Bar, stools, tables, hearth and bed are invisible in 3D**, so NPC posts point at nothing. |
| Area switch: `enter()` uses `gs.arrive[prevArea]` for Martsirt | 81162 | REUSE. The taproom OUT arch's legacy sx/sy (14.7, 27.2) is overridden by `gs.arrive.taproom`. |
| `fs.view3d` defaults off (27574); `zc('town')` uses `Rc()` only when `townMartsirt && view3d && gs` (30990) | — | Risk: the 2D and 3D towns are different worlds with different coordinates. Toggling calls `retown()`. |

---

## Reuse plan for the NPC engine stage

1. **Inject marker props in `Rc()`.** Add these from placements.json and new marker data:
   - `{kind:'bonfire'}` at tile (95.99, 75.48). `hc()` makes it the town pyre, which turns on `townPyre`, `pyreTender`, `tickRumors`, `nearHeat` and `tickNeed` warm.
   - a plain `bonfire` at the gate campfire (72.0, 135.1)
   - `building` props (x, y, w, d) for the inn/Salted Kettle, forge, stable and houses, for `doorstep` and leisure hides
   - `bench`/`log`/`barrel`/`table`/`bar`-kind markers at the forge yard, the Kettle door, the stable yard and the square

   Mark the new props non-rendering in 3D, since the GLBs already draw them.
2. **Add NPCs to `Rc()`.** Extend `gc().npcs` / `gs.npcs` with Mira, Orrin and Ness as town presences, plus **Ayla**: role `stable`, home (126.5, 117.5), roam ~4, `wander:true`, lines and LW `Gn`/`Kn` entries. Keep the internal key `Wolchen` and add `display:'Wolcen'` (rendered in talk, bark and menu).
3. **Per-NPC duty tables in `dutyOf`.** Ayla: work 7–19 (stable yard), sit 19–22, hidden 22–7 (hayloft = `hide`). Wolcen: work at the forge/outside, and leisure at the fire only.
4. **Build `visitSpots` + a rotation inside `lifeBeat`.** Insert before the `postFor` step. Every N minutes (hash-staggered per NPC), a regular picks one spot (fire ring via `dockBeside`, the Kettle doorstep, the square), walks there with `aimNpc`, holds 20–60 s with `holdPost`/`faceProp`, then returns to the `postFor` post. Allow-lists:
   - Wolcen = forge, forge-outside, fire
   - Ayla = stable yard only
   - Quill = his corner, plus the fire (if Brian wants)
   - Bram = camp, plus the fire rarely
5. **Fix `needPost`.** Replace the 9.5-tile home radius with the per-NPC allow-list from step 4, so `warm` and `bar` needs reach the fire and the Kettle.
6. **Fix `routeOpen`.** Raise the caps (e.g. 4000 expansions / 300 steps) or add a coarse road-node graph (square, fire, Kettle door, forge, stable, gates) and run A* per leg. Keep `losOpen`, `advancePath`, `stepNpc` and `watchNpc` unchanged.
7. **Re-anchor `tickBram`.** Replace the hard-coded (26.2, 11.2) / (30.6, 10.15) / (28, 12.15) with offsets from his v2.2 home (144.71, 23.04) / camp light (139.24, 18.45).
8. **Upgrade `poseNpcs`/`fillNpc` in 3D:**
   - `group.rotation.y = IE(n.facing)` (copy `poseMobs`)
   - walk/idle switch from position delta → `actor.playState('walk'|'idle')`
   - map `n.pose` (sit/eat/drink/read/labor/haul/flute/sleep…) to clips, falling back to idle
   - real dt instead of 0.016
   - per-NPC model/tint table, with the knight as the fallback
9. **3D speech.** Render `bark()` lines in 3D via `KE.project()` → HTML label over the head (2D bark is canvas-only today).
10. **Single banter path for town.** Keep LW `Yr()`/`Jn` (named pairs, 90 s gap, 12-tile radius). Tune it to Brian's rule: 60–90 s town-wide, player ≤ 8 m, no reply, none 21–6. Disable `maybeBanter` (`DD`) in Martsirt. Keep `tickRumors` at the fire.
11. **Reuse unchanged:** `regardOf`/`noteRegard`/`witness`/`vendorMul`/`shopShut`/`tip`/`grantFavor`; `Cr`/`wr`/`Dr`/`Er`/`Ir` dialogue; `qn` quests; `moodLine`/`dutyBlurb`/`wake`; `seedNeeds`/`tickNeed`/`serveNeed`/`needLine`; `dockBeside`/`spotTaken`/`nearestProp`/`clampPost`; `separateNpcs`/`stepAside`.
12. **Taproom consistency (later).** Gate `kc()` NPC presence on the town schedule (Mira always, Orrin and Ness at leisure). Add 3D bar, stool, table and hearth meshes to `buildZone()` (currently invisible) before relying on interior posts in 3D.
