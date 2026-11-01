# Sanctuary — Free (CC0) Prop Shortlist
_Research only, 2026-11-01. Nothing downloaded into game folders and nothing built or converted. This is waiting for Brian's approval._

**Scope:** medieval, archaic, Greek and Roman, Egyptian, mythological and religious items, plus general gothic clutter.
**Sources:** Smithsonian Open Access 3D, Poly Haven, and museum-owned CC0 uploads on Sketchfab (Cleveland Museum of Art, Minneapolis Institute of Art "Mia", The Hunt Museum, Morbase virtual museum).
**Licence rule:** CC0 only. CC-BY, CC-BY-NC and items with unclear terms were skipped.
**Thumbnails:** small previews are in `thumbs/` (`ph_*` Poly Haven, `si_*` Smithsonian, `skfb_*` Sketchfab).

## How licences were verified
- **Poly Haven:** every asset is CC0 (https://polyhaven.com/license). Polycount, dimensions and file lists were read per item from `api.polyhaven.com/info/{id}` and `/files/{id}`. Formats are always blend, glTF, FBX and USD at 1k/2k/4k(/8k) textures.
- **Smithsonian:** the item pages at si.edu returned 403 or timed out from this box. Each item's licence was checked in its Open Access API record (`api.si.edu/openaccess/api/v1.0`). In every listed item, both `online_media.media[].usage.access` and `metadata_usage.access` read `CC0`. Smithsonian 3D packages ship as GLB (around 150k faces at 4K, plus a Draco 100k/2K version), glTF zip, OBJ zip, full-res OBJ and USDZ. Links go to the Voyager viewer. **Re-check the licence on the si.edu page before downloading**, since I could only check it through the API.
- **Sketchfab:** the per-model API record (`api.sketchfab.com/v3`) gives the licence label `CC0 Public Domain` and `isDownloadable: true`. The Cleveland Museum of Art descriptions also state their Open Access terms ("copy, modify, and distribute… even for commercial purposes"). Formats: GLB, glTF, source and USDZ (Sketchfab auto-converts). Downloading needs a free Sketchfab login.

**Weight key:** OK = usable after a light texture downsize. Decimate = scanned mesh that needs decimating and baking to around 5–20k triangles. Heavy = more than 200k faces or 8K textures; needs real cleanup.

---

## TOP 10 (recommended first wave)
| # | Item | Source | URL | Why |
|---|---|---|---|---|
| 1 | Gothic statue (crowned king with sword, ruined plinth) | Poly Haven | https://polyhaven.com/a/gothic_statue | Martsirt square or Cathedral nave hero statue. 27.7k tris, 1.48×1.56×1.74 m. Ready for a game. |
| 2 | Kite shield (crusader, battered paint) | Poly Haven | https://polyhaven.com/a/kite_shield | Wall trophy, weapon-rack dressing, or a loot pedestal. 10.3k tris. |
| 3 | Large castle door (arched, iron-banded) | Poly Haven | https://polyhaven.com/a/large_castle_door | Dungeon and keep entrances, the Black Vault gate. 12.6k tris, 2.0×3.0 m. |
| 4 | Wine barrel 01, plus the wooden_barrels_01 pack | Poly Haven | https://polyhaven.com/a/wine_barrel_01 | Tavern, cellar and town clutter. 10.8k tris, about 0.9 MB glTF at 1k. |
| 5 | Mourner from the Tomb of Philip the Bold (1404–10, alabaster) | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/0d89139b17024e378f2882e575531e08 | Hooded weeping mourner. Perfect Cathedral and crypt statue; scale it up to life size. 85k faces. |
| 6 | Arm Reliquary of the Apostles (c.1190, gilt silver) | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/df98bbcd1c3b46f0a9d640e925490f4a | Relic or unique-item pedestal, shrine. 90k faces, 8K textures. |
| 7 | Kneeling winged monster (Northern Qi 550–577, limestone cave guardian) | Smithsonian (NMAA) | https://3d-api.si.edu/voyager/3d_package:0dc68216-3651-44c7-99cf-18e5d4d1eb9f | Demonic carved caryatid for dungeon pillars and Hell gates. 88 cm. |
| 8 | Kylix (Greek drinking cup, ca. 800 BC, painted earthenware) | Smithsonian (Cooper Hewitt) | https://3d-api.si.edu/voyager/3d_package:547c78d1-620b-40c4-982e-01928870fef4 | Antiquity loot and pedestal, Highmarket collector's shelf. 22 cm. |
| 9 | Egyptian false door (c.2400 BCE) | Mia / Sketchfab | https://sketchfab.com/3d-models/ffe4b699e75849d59d8efe47d3538f03 | Qadren tomb wall and a sealed-door set piece. 65k faces, 12.5 MB GLB, 4K textures. |
| 10 | Goddess Sekhmet (1320–656 BCE, faience) | Mia / Sketchfab | https://sketchfab.com/3d-models/160b5a18fa994fcdb4bef96e5c1f1c4a | Lion-headed war goddess. Qadren shrine idol or loot statuette. 62k faces. |

Licences: items 1–4 are CC0 (Poly Haven). Items 5, 6, 9 and 10 carry the CC0 Public Domain label in the Sketchfab API. Items 7 and 8 are flagged CC0 in the Smithsonian Open Access API.

---

## 1. Medieval / European (15)
| Item | Source | URL | Licence | Period / what | Sanctuary use | Formats | Size / polys | Work needed |
|---|---|---|---|---|---|---|---|---|
| Gothic statue ★ | Poly Haven | https://polyhaven.com/a/gothic_statue | CC0 | Gothic king statue on a rubble base | Town square, Cathedral, Act V throne hall | blend/gltf/fbx/usd | 1.48×1.56×1.74 m · 27.7k | OK |
| Kite shield ★ | Poly Haven | https://polyhaven.com/a/kite_shield | CC0 | Norman/crusader kite shield | Wall trophies, armoury, loot | same | 0.54×1.39 m · 10.3k | OK |
| Large castle door ★ | Poly Haven | https://polyhaven.com/a/large_castle_door | CC0 | Arched double door | Keep and dungeon entrances | same | 2.0×0.34×2.97 m · 12.6k | OK |
| Gothic cabinet | Poly Haven | https://polyhaven.com/a/GothicCabinet_01 | CC0 | Carved gothic cupboard | Interiors (Pell's, the Elder's house) | same | 1.72×1.13×2.36 m · 12.2k | OK, darken |
| Gothic bed | Poly Haven | https://polyhaven.com/a/GothicBed_01 | CC0 | Carved four-poster | Inn rooms, noble crypt dressing | same | 18.7k | OK, grime pass |
| Ornate medieval mace | Poly Haven | https://polyhaven.com/a/ornate_medieval_mace | CC0 | Flanged mace | Weapon racks, ground loot model | same | 0.63 m · 14.8k | OK, LOD for drops |
| Ornate medieval dagger | Poly Haven | https://polyhaven.com/a/ornate_medieval_dagger | CC0 | Rondel-style dagger with sheath | Loot and racks | same | 0.35 m · 6.3k | OK |
| Ornate war hammer | Poly Haven | https://polyhaven.com/a/ornate_war_hammer | CC0 | Late-medieval war hammer | Loot and racks | same | 0.71 m · 5.2k | OK |
| Antique estoc | Poly Haven | https://polyhaven.com/a/antique_estoc | CC0 | Thrusting longsword | Loot, a sword in a grave mound | same | 1.49 m · 8.2k | OK |
| Treasure chest | Poly Haven | https://polyhaven.com/a/treasure_chest | CC0 | Iron-strapped chest | Lootable chest model | same | 0.96×0.52×0.62 m · 103k | Decimate to ~10k |
| Wine barrel ★ | Poly Haven | https://polyhaven.com/a/wine_barrel_01 | CC0 | Oak barrel | Everywhere | same | 0.74×0.76×0.87 m · 10.8k | OK |
| Wooden barrels pack | Poly Haven | https://polyhaven.com/a/wooden_barrels_01 | CC0 | Barrels, kegs and broken staves | Cellars, docks, breakable debris | same | 4.4 m spread · 33k total | OK (split pieces) |
| Bronze bell (medieval) | Hunt Museum / Sketchfab | https://sketchfab.com/3d-models/6ac94462b21549ea8047228391f1239b | CC0 PD | Medieval bronze hand bell with acanthus decoration | Shrine bell, chapel dressing | glb/gltf/usdz | 250k, 2K texture | Decimate |
| Túmulo de D. Mécia de Moura | Morbase / Sketchfab | https://sketchfab.com/3d-models/78130ac3aeac405aba947b712bea02ad | CC0 PD | 16th-c. carved heraldic tomb slab (Portugal) | Crypt floor and wall tomb | glb/gltf/usdz | 500k, 8K texture, 109 MB GLB | Heavy: decimate and bake |
| Hunting horn (oliphant) | Smithsonian (NMAfA) | https://3d-api.si.edu/voyager/3d_package:ad94884b-fdd7-4fc3-a692-e53b787d78e6 | CC0 (API) | Late 15th c., carved ivory, Sierra Leone | Unique loot or quest item ("Horn of …") | glb/gltf/obj/usdz | 64 cm · ~150k | Decimate |

## 2. Greek & Roman (9)
| Item | Source | URL | Licence | Period / what | Sanctuary use | Formats | Size / polys | Work |
|---|---|---|---|---|---|---|---|---|
| Kylix ★ | Smithsonian (Cooper Hewitt chndm_1971-48-12) | https://3d-api.si.edu/voyager/3d_package:547c78d1-620b-40c4-982e-01928870fef4 | CC0 (API) | Greece, ca. 800 BC, painted earthenware | Antiquity loot, pedestal, collector shelf | glb/gltf/obj/usdz | 7.3×22×18 cm · ~150k | Decimate |
| Marble bust 01 | Poly Haven | https://polyhaven.com/a/marble_bust_01 | CC0 | Roman-style laureate bust | Highmarket villas, ruined library | blend/gltf/fbx/usd | 0.52 m · 17.5k | OK, add grime and chips |
| Torso of a Kouros | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/384326f9d7a34c14bc4641aa78c90557 | CC0 PD | Archaic Greek, c.550 BCE | Broken statue in ruins, coastal Act III | glb/gltf/usdz | 62.5 cm · 85k, 8K texture | Decimate, downsize texture |
| Torso of a Dancing Faun | Mia / Sketchfab | https://sketchfab.com/3d-models/28857593d96c4afeb580c608c74230cc | CC0 PD | Graeco-Roman, 1st c. CE marble | Ruin and garden statue fragment | glb/gltf/usdz | 64k, 4K texture, 20.6 MB | OK–Decimate |
| Head of Emperor Vespasian (recut from Nero) | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/359e48ed821544fe8cf22c3c5dbbff9d | CC0 PD | Roman, AD 64–79 | Fallen-empire head in rubble | glb/gltf/usdz | 40 cm · 65k, 8K | Decimate |
| Head of Alexander the Great | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/024889d40ffc4d209310642343a525d2 | CC0 PD | Hellenistic, 300–200 BCE | Same; pedestal loot | glb/gltf/usdz | 26.5 cm · 80k, 8K | Decimate |
| Cinerary box | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/97d4e16d56434cf5984198512737aff8 | CC0 PD | Roman, 1–100 CE marble ash chest | Crypt niches; breakable urn container | glb/gltf/usdz | 29×24 cm · 233k, 8K | Heavy |
| Two masks | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/43b984984dbc456383e3a1eda069782c | CC0 PD | Roman 3rd c. theatre-mask relief | Wall relief, Bard/Highmarket theatre | glb/gltf/usdz | 27×39 cm · 80k, 8K | Decimate |
| Torso of Venus | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/f4b4a7c34739439eae7f805b64b833ed | CC0 PD | Roman, 1–200 CE | Ruin statue | glb/gltf/usdz | 64 cm · 141k, 8K | Decimate |

## 3. Egyptian & Near Eastern (11) — mostly for Qadren (Act II)
| Item | Source | URL | Licence | Period / what | Sanctuary use | Formats | Size / polys | Work |
|---|---|---|---|---|---|---|---|---|
| False door ★ | Mia / Sketchfab | https://sketchfab.com/3d-models/ffe4b699e75849d59d8efe47d3538f03 | CC0 PD | Old Kingdom, c.2400 BCE | Tomb wall, sealed door | glb/gltf/usdz | 65k, 4K, 12.5 MB | OK–Decimate |
| Goddess Sekhmet ★ | Mia / Sketchfab | https://sketchfab.com/3d-models/160b5a18fa994fcdb4bef96e5c1f1c4a | CC0 PD | 1320–656 BCE faience | Shrine idol, loot statuette (scale up) | glb/gltf/usdz | 62k | Decimate |
| God Osiris | Mia / Sketchfab | https://sketchfab.com/3d-models/b765d64e642f4c09aeec8c4da384efca | CC0 PD | 644–30 BCE bronze | Tomb shrine | glb/gltf/usdz | 64k | Decimate |
| Canopic jar with falcon's head | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/e1e86d7848ce42089343b700c3b9c5ae | CC0 PD | Egyptian | Tomb clutter, breakable urn | glb/gltf/usdz | 45.3 cm · 90k, 8K, 88 MB GLB | Heavy textures |
| Limestone Thoth as baboon | Hunt Museum / Sketchfab | https://sketchfab.com/3d-models/ea511ed3b3b343da892b64656d0d5c21 | CC0 PD | Egyptian limestone | Temple guardian statue | glb/gltf/usdz | 178k | Decimate |
| Bronze statue of Horus | Hunt Museum / Sketchfab | https://sketchfab.com/3d-models/84542ab14ce84929b44266f1c98fae07 | CC0 PD | Egyptian bronze falcon god | Shrine and pedestal | glb/gltf/usdz | 231k | Heavy |
| Apis bull | Mia / Sketchfab | https://sketchfab.com/3d-models/8f3c2abe63754b1cbb0f4010c4215538 | CC0 PD | Egyptian bronze | Cult shrine (fits a bull-cult dungeon) | glb/gltf/usdz | 59k | Decimate |
| Udjat eye (Eye of Ra) | Mia / Sketchfab | https://sketchfab.com/3d-models/7300d219ed944585ace4b2509bef4f6e | CC0 PD | 1297–1185 BCE amulet | Amulet loot model or icon render | glb/gltf/usdz | 63k | Decimate (tiny) |
| Travertine cylindrical jar | Hunt Museum / Sketchfab | https://sketchfab.com/3d-models/f64c57d647324140add058dcbcafccf9 | CC0 PD | Egyptian stone jar | Tomb clutter | glb/gltf/usdz | 26 cm · 241k | Heavy, simple shape (easy remake) |
| Brass diya lantern | Poly Haven | https://polyhaven.com/a/brass_diya_lantern | CC0 | Pierced brass hanging lamp | Qadren bazaar lamps (light cookie) | blend/gltf/fbx/usd | 0.38 m · 12.7k | OK |
| Brass pot / brass vase | Poly Haven | https://polyhaven.com/a/brass_pot_01 · https://polyhaven.com/a/brass_vase_01 | CC0 | Hammered brass vessels | Qadren market, shrines | same | 3.8k / 21.4k | OK, age the metal |

## 4. Mythological / religious (9)
| Item | Source | URL | Licence | Period / what | Sanctuary use | Formats | Size / polys | Work |
|---|---|---|---|---|---|---|---|---|
| Mourner from the Tomb of Philip the Bold (1958.66) ★ | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/0d89139b17024e378f2882e575531e08 | CC0 PD | Burgundy 1404–10, alabaster | Cathedral and crypt mourner statues (a pair with 1958.67) | glb/gltf/usdz | 41 cm · 85k, 8K | Decimate, scale up |
| Mourner 1958.67 (companion) | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/d81c143f00a140269047c0a4619e6263 | CC0 PD | same | Variation | glb/gltf/usdz | 85k, 8K | Decimate |
| Vesperbild (Pietà) | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/aa3a38eda3c74c82baf7a019072ca368 | CC0 PD | German c.1515–20, polychrome lindenwood | Chapel altarpiece, shrine | glb/gltf/usdz | 89 cm · 125k, 8K, 120 MB | Decimate and downsize textures |
| Arm Reliquary of the Apostles ★ | Cleveland MA / Sketchfab | https://sketchfab.com/3d-models/df98bbcd1c3b46f0a9d640e925490f4a | CC0 PD | Romanesque, c.1190 | Relic pedestal, unique item | glb/gltf/usdz | 51 cm · 90k, 8K | Decimate |
| Kneeling winged monster ★ | Smithsonian (NMAA F1916.345) | https://3d-api.si.edu/voyager/3d_package:0dc68216-3651-44c7-99cf-18e5d4d1eb9f | CC0 (API) | Northern Qi, 550–577 cave guardian | Demonic pillar caryatid, Hell gate | glb/gltf/obj/usdz | 88 cm · ~150k | Decimate |
| Ritual wine ewer (gong) with taotie masks | Smithsonian (NMAA F1961.33a-b) | https://3d-api.si.edu/voyager/3d_package:d8c646aa-4ebc-11ea-b77f-2e728ce88125 | CC0 (API) | Shang, ca.1100–1050 BCE bronze | Cursed-vessel loot, demon-cult altar | same | 32 cm · ~150k | Decimate |
| Ritual container (fangyi) with taotie | Smithsonian (NMAA F1930.54a-b) | https://3d-api.si.edu/voyager/3d_package:d8c62f94-4ebc-11ea-b77f-2e728ce88125 | CC0 (API) | W. Zhou, ca.1100 BCE bronze | Altar casket, loot | same | 35 cm · ~150k | Decimate |
| Lidded incense burner (boshanlu) | Smithsonian (NMAA F1947.15a-b) | https://3d-api.si.edu/voyager/3d_package:ce850625-2cf1-4c6f-9086-0d5845d9a664 | CC0 (API) | Han, 2nd c. BCE bronze | Shrine censer with a smoke VFX socket | same | 17.9 cm · ~150k | Decimate |
| Bull head (bronze-look bust) | Poly Haven | https://polyhaven.com/a/bull_head | CC0 | Sculpted bull bust | Minotaur or bull-cult shrine, trophy | blend/gltf/fbx/usd | 17.1k | OK |

## 5. General clutter (12)
| Item | Source | URL | Licence | Use | Size / polys | Work |
|---|---|---|---|---|---|---|
| Wooden lantern | Poly Haven | https://polyhaven.com/a/wooden_lantern_01 | CC0 | Hanging and street lanterns (Martsirt) | 0.53 m · 8.3k | OK |
| Wooden candlestick | Poly Haven | https://polyhaven.com/a/wooden_candlestick | CC0 | Altars, tables | 3.3k | OK |
| Brass candleholders | Poly Haven | https://polyhaven.com/a/brass_candleholders | CC0 | Chapel and noble halls | 41.9k (set) | Split and decimate a little |
| Brass goblets | Poly Haven | https://polyhaven.com/a/brass_goblets | CC0 | Tavern tables, loot | 9.6k | OK |
| Wooden bucket | Poly Haven | https://polyhaven.com/a/wooden_bucket_01 | CC0 | Wells, stables | 5.1k | OK |
| Wooden crate (iron-bound) | Poly Haven | https://polyhaven.com/a/wooden_crate_01 | CC0 | Breakable containers | 6.6k | OK |
| Wooden stool | Poly Haven | https://polyhaven.com/a/wooden_stool_02 | CC0 | Tavern, smithy | 11.1k | OK |
| Wicker basket | Poly Haven | https://polyhaven.com/a/wicker_basket_01 | CC0 | Market stalls | 22.3k | Decimate a little |
| Ceramic pot (lidded earthenware) | Poly Haven | https://polyhaven.com/a/ceramic_pot | CC0 | Kitchens, breakable pots | 3.6k | OK |
| Stone fire pit | Poly Haven | https://polyhaven.com/a/stone_fire_pit | CC0 | Camps, Rogue-style encampment | 1.45 m · 3.9k | OK |
| Worn bookshelf | Poly Haven | https://polyhaven.com/a/wooden_bookshelf_worn | CC0 | Library / "Unread Stacks" (needs books added) | 10.1k | OK |
| Cast-iron hanging kettle cauldron | Smithsonian (NMAAHC 2011.139.1ab) | https://3d-api.si.edu/voyager/3d_package:48cbf553-df1a-47ce-9ceb-082905bda773 | CC0 (API) | Witch's or camp cauldron | 16.5×20×18 cm · ~150k | Decimate, scale up |

**Also viable, lower priority (Poly Haven CC0):**
- Furniture and tools: GothicCommode_01, wooden_bowl_01, carved_wooden_plate, wooden_axe, rusted_spade_01, spinning_wheel_01 (52k), lion_head (carved wood, 47k)
- Lights: lantern_chandelier_01 (Victorian-leaning; Highmarket only)
- Coast Act III: dutch_ship_medium (69k, wreck dressing), modular_wooden_pier (85k)
- Large set pieces: modular_fort_01 (bastion walls), dead_tree_trunk (102k, needs decimation)

**Also viable from museums (CC0):**
- Mia: Goddess Isis (https://sketchfab.com/3d-models/fef83e3711e248689702f953e02809a0), Thoth ibis (https://sketchfab.com/3d-models/394a94722862460e8cefab54b4bed7bf)
- Cleveland: Paint box of Vizier Amenemope (https://sketchfab.com/3d-models/e1e90352bbba4c56bac899deb16bf6c4)
- Smithsonian: Dire wolf skull, *Canis dirus* (https://3d-api.si.edu/voyager/3d_package:6796319b-6445-435f-994b-2f40fd8d08e4), for bone-pile dressing

**Counts:** Medieval/European 15 · Greek & Roman 9 · Egyptian & Near Eastern 11 · Mythological/religious 9 · General clutter 12 = **56 candidates**, plus the "also viable" lists above.

---

## Dropped (off-tone or problematic)
- **Poly Haven:**
  - Lantern_01: modern hurricane lamp
  - antique_ceramic_vase_01: blue-and-white chinoiserie
  - hatchet: rubber grip
  - planter_pot_clay: garden flowerpot
  - jug_01: milk jug
  - large_iron_gate: driveway gate
  - WoodenTable_01: school desk
  - horse_statue_01: porcelain
  - horse_head: reads as modern decor
- **Smithsonian:**
  - Most of the 1,937 3D records are space, aviation, natural history or American history.
  - Delft ewer and Thomas Commeraw stoneware jug: too early-modern.
  - Model of the Greek Slave: 1843, Neoclassical, American.
  - Sunstone Capital: 1840s Mormon temple.
  - Buddha pieces: off-tone for a demonic setting.
  - Jar made by "Dave" and the Colonoware pot: objects made by enslaved people, with real cultural weight. Not appropriate as dungeon clutter.
- **Sketchfab:**
  - Cleveland Table Fountain: 507k faces and a 212 MB GLB.
  - Hunt Museum Medieval Gilded Donkey: 1M faces, 8 cm.
  - Världskulturmuseerna Bronze cat: 1.3M faces.
  - Faroe Islands site scans: landscapes, not props.
  - danielpett uploads (sarcophagus lid, lion): CC0 but not museum-owned, with unfinished sides.
  - Ganesha: off-tone.

## Notes for production (after approval)
- Every museum scan needs decimating to game budget (about 5–20k triangles for hero props, 1–3k for clutter), a normal-map bake and textures cut to 1K–2K. They are the fidelity reference for the hand-made "battle-worn" look, and they will need grime and damage passes to sit in Sanctuary's palette.
- Sketchfab downloads need a free account; Smithsonian and Poly Haven need none.
- CC0 means no attribution is legally required, but crediting the museums in the game credits is good practice.
