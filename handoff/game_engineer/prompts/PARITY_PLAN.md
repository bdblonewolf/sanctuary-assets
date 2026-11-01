# Sanctuary 2D -> 3D Parity Audit + Staged Plan
Build audited: routes-Cc6gVP-T.js (live 2026-10-30 23:30 EDT). 3D renderer class: `dT` (was LT). Zone data probed live via window.__eng.enter(id) for all 39 zones (raw: /workspace/sanctuary/probe/zones.json, zones.txt).

## How 3D works now (baseline)
- The game loop calls `this.room.frame(dt,{world,player,speed,mode,heading,enemies,loot,projs})`. The 2D `paint()` is skipped entirely in 3D, and the 2D canvas is opacity 0. **Everything drawn only by paint() is missing in 3D**, including vfx (`this.vfx.drawGround/drawOver`), floats/damage numbers, labels, bubbles, health bars, the minimap and weather.
- dT methods: buildZone (chunk of radius `Kw` around the player; floor/wall/rock/water instanced, banners), placeLights, poseHero, poseMobs/makeMob/fillMob/foeMat, poseNpcs/fillNpc, syncLoot, syncBolts/boltColor, pick, project.
- Prop kinds 3D handles: torch, lamp, bonfire, pillar, barrel, crate, chest, arch, stairs. **All other kinds are skipped.**
- Mob models: `skeleton` -> skeleton model, `guard` (boss/rare) -> armored_guard_knight, and a `simple` fallback for other kinds (with special cases for ghost/wraith/king). NPCs use a tinted knight. Not passed to 3D at all: `this.allies` (summons), `world.critters`, `this.patches`, traps.

## 1. Zones, buildings, props
39 zones (Ec): town, wild, briarE, duneW, den, church1, church2, desert, lut, isle, market, waste, vault, cottage, taproom, inn, house, castle1-4, root, coast, bastion, bluffs, mires, sink, ridge, ascent, crypts, chasm, iron, flotsam, hollow, gaol, weald, hull, sewer, nave.
Towns/hubs: town "Martsirt", lut "Qadren", market "Highmarket", bastion "Bastion of Hope". Interiors (16x13): cottage, taproom, inn "Lampwick Inn", house "Salt House". The player's home is the **cottage** (bed, hearth, chest/stash, mark/chart); inn and house also have chest/stash. I found no separate "roster" area in the code.

| Prop kind/style (examples) | Where | 3D now |
|---|---|---|
| building/stone, wood, brick, sand | town 4+1, market 4, lut 3, wild, bastion | MISSING |
| fence/picket, fence/stone | town 84, bastion 72 | MISSING |
| arch/stone, cave, trees, gap, road, sand, sealed, wood (exits/gates) | all zones | placeholder glow marker |
| well, well/heal | town, market 2, lut, desert, bastion | MISSING |
| cart, boat, boat/hulk, boat/ribs | town, market, lut, wild, isle, coast, flotsam | MISSING |
| bonfire, bonfire/town, bonfire/ash | many | done (brazier) |
| torch, torch/wall, torch/fade, lamp, lamp/flicker/dead/fallen | dungeons, interiors | done (torch/flame); lamp styles ignored |
| pillar | church, castle, iron, nave, weald | done |
| barrel, barrel/fire, barrel/anvil, crate, chest, chest/stash, chest/super | everywhere | done (generic; fire/anvil/stash/super not distinguished) |
| tomb, tomb/crypt | 30+ | MISSING |
| body, body/kin (corpses) | almost all zones | MISSING |
| pew, pew/stone, pew/wreck, organ, bookshelf | church1/2, gaol, nave, crypts, interiors | MISSING |
| bed, hearth/g1-3, table, table/smith, chair, stool, bench, bar, pot, pot/pan | interiors, town | MISSING |
| shrine/(xp, speed, might, magic, cold, fire, lightning, curse, heal) | ~25 placed | MISSING (gameplay object!) |
| stairs/(trap, hatch, ladder, deep) | many | placeholder marker |
| folio/* (lore books), mark/chart, mark/ambush (invisible) | most zones | MISSING (folio is interactable) |
| log, log/seat, rock, rock/bone, rock/print, rock/stain, rock/dune, rock/cache | outdoor | MISSING |

## 2. Terrain
- Tile enum W: Grass, Grass2, Dirt, Road, Water, Bridge, Sand, Sand2, Stone, Cave, Blood, Wall, Plaza, Plank, Rug. **3D now:** floor variants from the dungeon kit (or "dark" floors), water plane, walls/rocks from solid. No per-tile material, so grass, road, sand, plaza, plank, rug and blood all look the same, and bridges are missing. MISSING: per-tile materials.
- Trees: tree (town 47, wild 200, market 52, briarE 75...), tree/far (backdrop), tree/dead (waste 42, flotsam 41, weald 39...), tree/blackroot 32 + tree/giant 3 (weald), palm 12 (lut), cactus, bush/thorn, flower(/white/glow/shroom). **MISSING.**
- Mountains: mountain, mountain/peak (backdrop ring, 30-66 per outdoor zone), mountain/sand, mountain/shelf. **MISSING.**
- Atmosphere: this.fog, this.rain (weather), this.clock/hours (day/night phase), world.lights, vfx.torchEmbers, the `quiet`/haze layer (drawHaze). **3D:** fixed moon plus torches; no day/night, rain or fog. MISSING.

## 3. Characters
- Classes (player.classId): ironvow, longmark, gravewell, cinderwake.
- Weapon types: sword, axe, mace, dagger, spear, staff, wand, bow, javelin, hammer, orb, plus shield. The 2D look comes from `Td(e,t,n,r)`, which reads eq.armor/weapon/helm/shield via `bd()` (gear changes colors and silhouette), and `Wu(...)`, which draws the weapon by type. The swing uses player.swing/swingT (drawSwing). **3D:** one plated knight with no weapon, and gear doesn't change the look. MISSING.
- Attack anim types: melee swing, bow draw/release (longmark), cast (gravewell/cinderwake staff/wand), throw (javelin), plus skill shapes in V (melee, cone, blink, buff, heal, summon, projectile, aura...). **3D:** one Attack clip.
- NPCs (role): town: Wolchen smith, Ysara healer, Ilyra herald, Quill scribe, Bram quest. lut: Orlem mage, Heska guard, Vetch gambler. market: Cal, Pell guard. bastion: Rusk, Sera healer, Odder smith. Inns: Mira, Orrin, Ness, Hesta, Voss, Ilen, Tamsin. Wild: Holt ferry, Myrine/Orithya guards, Sable scribe. Quest-givers in each later zone: Sarn, Wynn, Iskra, Moth, Calder, Hask, Nim, Vellum, Lute, Kell, Brine, Jas, Piet, Ors. Also Vesper mage (castle3). **3D:** generic tinted knight, no names or role look.
- Companions: `this.allies` (summoned skeletons/hex minions from gravewell summon, plus a pet). I found no named "Companion Demons" feature in the code. **3D:** MISSING (allies aren't passed to frame).
- Critters (world.critters: rat, rabbit, deer, crow, bird). MISSING.

## 4. Monsters (makeEnemy kinds seen in zones)
skeleton, zombie, corpse, ghost, wraith (Ash Wraith), imp, caller (summoner), raver, brute, bear (incl. bosses Spire-Heart, Scar-Eye), snake (hidden ambusher), worm (burrow), king (Black Vault boss), melakir (boss), boss variants (bossId e.g. halvane "Inquisitor Halvane"). Elite packs: rarity magic/rare with mods (Fleet, Brutal, Ironhide, Venomous...), and variants spit/leap/burrow tinted with CSS filters. Projectiles: bone (fan), arrows/spit.
**3D:** only skeleton has a real model. guard knight is used for boss/rare, and everything else uses a simple mesh. No telegraphs (vfx.telegraph), no hit flash colors per element, and no death bursts. Rarity tint is partial.

## 5. Effects
vfx system (`this.vfx`: cast, impact, emit, telegraph, number, shed, torchEmbers, drawGround/drawOver; arrays rings, arcs, bolts, decals, nums, parts). drawArcs, drawAuras, drawBolts, drawSwing, drawTraps, drawStatus, drawHaze. Also blood decals, shrines glow, exit glows, loot beams by rarity, gold piles.
**3D:** syncBolts (projectiles as colored spheres) and syncLoot (glowing markers) only. Everything else is MISSING.

## 6. Screen-anchored UI
Damage numbers (this.float / vfx.number / nums), item labels on the ground, enemy name and health bars (title, rarity), boss bar, NPC names and bark/speech bubbles (this.bark, skipBubble), the toast/caption, the minimap (lf / onMapTap, mapOpen), and the hero long-press potion zone. These are drawn in paint() with xo(). **3D:** they're not drawn. `this.toScreen()` now exists, so they can be drawn on a 2D overlay canvas above the 3D canvas using toScreen/room.project. React HUD (orbs, belt, skill bar, menus) is unaffected and works.

## STAGED PLAN (one small strict Grok Build prompt each)
0. **Stick fix** (STICK_FIX_PROMPT.txt). Assets: none.
6. **World-anchored UI overlay**: a transparent 2D canvas above the 3D canvas, redrawn each frame by reusing the existing 2D label/number/bar/bubble/minimap draw functions with positions from toScreen. Assets: none.
7. **Shrines, exits, interactables**: shrine (by style color), folio, stairs variants, arch/exit gates, well, chest/stash/super, body corpses, tomb/crypt. Assets we have: dungeon_props.glb, modular_dungeon_kit (Pillar, Barrel, Braiser, Rock), /assets3d/dungeon/* (wall_arched, wall_gated, stairs, wall_doorway, pillar_decorated). Need to source: tomb/sarcophagus, shrine/altar, corpse. Candidates: KayKit Halloween Bits (gravestones, crypt, coffins), Broken Stone Slab, Large Iron Gate, Treasure Chest (PH).
8. **Town and homes**: building/stone|wood|brick|sand, fence/picket|stone, cart, boat, interiors (bed, hearth, table, chair, stool, bench, bar, bookshelf, pew, organ, pot). Have: nothing that fits beyond barrels and crates. Need: houses, walls, towers, well (KayKit Medieval Hexagon, retextured dark), Large Castle Door, Wooden Lantern/Bucket/Barrels, Stone Fire Pit (PH), GothicCabinet/GothicBed (PH), plus a pew, organ, bar and a cart/boat (gap, not on the shortlist).
9. **Terrain and nature**: per-tile materials (grass, road, sand, plaza, plank, rug, blood, bridge), trees (normal, dead, blackroot, giant, palm, far), bushes, flowers, cactus, rocks/bone piles, mountains/peaks as backdrop, logs, plus day/night, fog and rain. Have: kit Rock pieces. Need: PH Dead Tree Trunk 02, Tree Stump, Root Cluster/Pine Roots, Rock Moss sets, Rock Face, Mountainside, Namaqualand Cliff, and ground textures (PH textures). Gaps: living leafy tree, palm, cactus, flowers.
10. **Monsters by kind**: skeleton (have skeleton_animated + KayKit Skeleton_Minion/Warrior in /assets3d/kaykit), zombie/corpse, ghost/wraith (shader on a skeleton or knight), imp, caller, raver, brute, bear, snake, worm, king, melakir, plus telegraphs and death bursts. Need sourcing for zombie, imp, bear, snake, worm, brute/ogre and demon bosses (big gap; animated CC0 creatures are scarce. Try the Quaternius Ultimate Monsters pack manually, or Mixamo for humanoids).
11. **Hero gear and weapon anims**: weapon meshes by type (sword, axe, mace, dagger, spear, staff, wand, bow, javelin, hammer, orb, shield) attached to the right-hand bone, armor/helm tint from Td/bd colors, and per-type attack clips (slash, thrust, bow, cast, throw). Have: Kite Shield (PH, shortlist) and the knight rig. Need: a CC0 weapon pack (e.g. KayKit Adventurers/Weapons, Quaternius) and Mixamo clips for bow/cast/throw on the Mixamo-boned knight. NPC models by role can come from the same pack.
12. **Skills and VFX**: port vfx (cast, impact, rings, arcs, bolts, auras, telegraphs, decals, embers, blood) to 3D sprites/particles, plus allies (summons) and critters. Assets: sprite sheets (none yet; generate or source CC0 particle textures).
13. **Final**: remove 2D (paint, xo/So use, draw*), making 3D the only view.
Not now: statues in /workspace/sanctuary/assets3d/statues (statue_barbarian_queen, dark_archer, holy_knight, priest_king) are reserved for later.

## Big asset gaps
1. Gothic town buildings, walls and fences (only stylized KayKit candidates).
2. Monster models beyond skeletons: zombie, imp, bear, snake, worm, brute, demon bosses.
3. Weapon meshes plus bow/cast/throw animations.
4. Trees/foliage that aren't dead (leafy, palm, cactus) and ground textures per tile type.
5. Tombs, shrines, corpses, church furniture (pews, organ).
