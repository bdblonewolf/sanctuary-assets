# LOCATION_PLAN v1 (planning only; every slot is HOLD for Brian)

Machine-readable: `poi_slots.json` (84 slots). Each slot has zone, local_uv (0–1 in the zone's later grid), continent_m, tag, faction, skill_quest, on_road, footprint, reuse list, new-asset list and status. Map icons are in `continent_map_v1.png`.

Tags: faction 19, quest 42, remnant 6, explore-only 17.

Rules:
- Slots never sit on a road corridor. Off-road slots connect by goat path or hidden approach, and terrain and props never block a road.
- Faction homes reuse each faction's existing district or zone.
- Each skill quest gets 3 variation spots in different zones: same reward, different spot and opposition.
- The 13 new zones are HOLD as well (see PLAN.md).

## Faction home ground (F01–F10)
| id | slot | zone | tag | access | reuse | new |
|---|---|---|---|---|---|---|
| F01 | Fallen Parish home: St Noll undercroft + ruined chapel row | town | faction | road | martsirt_v2_2/chapel_st_noll/bld_chapel_st_noll_shared.glb; martsirt_v2_2/chapel_st_noll/bld_chapel_st_noll_tower_shared.glb; martsirt_v2_2/graveyard/bld_gravey | floorboard-hide trapdoor prop |
| F02 | Halvane's Inquisition: quarantine village + sealed ovens | n_quarantine | faction | road | martsirt_v2_2/cottage_ness/bld_cottage_ness_shared.glb; martsirt_v2_2/watchhouse_gibbet/bld_watchhouse_gibbet_shared.glb; martsirt_v2_2/gatehouse_south/seg_pali | sealed brick oven; chimney cap w/ iron grate; quarantine X-door decal |
| F03 | Open Eye knights: sealed iron citadel (outer wards only) | n_citadel | faction | road | martsirt_v2_2/gatehouse_south/seg_curtain_wall_4m_shared.glb; martsirt_v2_2/gatehouse_south/bld_gatehouse_south_shared.glb; border_kit/glb/bk_mountain_{season}. | citadel keep impostor (unenterable); drainage grate; bell-rope gap in wall |
| F04 | Toll families: toll houses on the gorge bridges | n_tollgorge | faction | road | martsirt_v2_2/gatehouse_south/bld_gatehouse_south_shared.glb; martsirt_v2_2/stable/bld_stable_shared.glb; martsirt_v2_2/gatehouse_south/seg_palisade_4m_shared.g | rope/plank bridge 12 m + 24 m; toll-house booth |
| F05 | Hollow smugglers: ridge path + cove (Jas) | n_hollowridge | faction | road | martsirt_v2_2/props/prop_crate_stack.glb; martsirt_v2_2/props/prop_barrel_group.glb; border_kit/glb/bk_coast_land_{season}.glb; interior hull; interior den | cut-page drop niche |
| F06 | Ash-camp of the Touched: ash pits + outer rings | n_ashcamp | faction | road | martsirt_v2_2/props/prop_bonfire_main.glb; martsirt_v2_2/props/prop_campfire.glb; martsirt_v2_2/gatehouse_south/seg_palisade_4m_shared.glb; models/outdoor/v5/pl | ash-pit decal + ash mound |
| F07 | Survivors: sinkhole shrines + river stones | n_sinkholes | faction | road | martsirt_v2_2/shrines/shrine_weeping_angel.glb; martsirt_v2_2/dressing/creek.glb; martsirt_v2_2/dressing/dress_rocks.glb; martsirt_v2_2/dressing/dress_trees.glb | sinkhole collapse mesh (reusable 3 sizes) |
| F08 | Quiet Choir: safe-cellar network under Martsirt | town | faction | road | interior choir; interior sewer; interior vault; martsirt_v2_2/dressing/dress_clutter.glb | bricked-hearth wall piece; cellar hatch prop |
| F09 | Ashen Covenant: burn-circles | n_burn | faction | road | martsirt_v2_2/props/prop_bonfire_main.glb; martsirt_v2_2/dressing/dress_rocks.glb; border_kit/glb/bk_desert_{season}.glb; models/outdoor/v5/plants/tree_dead_a_v | standing-stone ring (8 stones, instanced); scorched ground decal |
| F10 | Tidebound: night coves, kelp floats, leeward cairns | n_tidecoves | faction | road | border_kit/glb/bk_sea_{season}.glb; border_kit/glb/bk_coast_land_{season}.glb; martsirt_v2_2/dressing/dress_rocks.glb; interior hull | kelp float; cairn (instanced stones); tidal-cave mouth piece |

## Skill quests: 14 × 3 variation spots (SQ01–SQ14 are PLACEHOLDER ids; the faction/skill-quest file is ON HOLD)
| id | slot | zone | tag | access | reuse | new |
|---|---|---|---|---|---|---|
| SQ01_v1 | Parish wells - variation 1 | town | quest | road | existing spot props of the zone | - |
| SQ01_v2 | Parish wells - variation 2 | coast | quest | road | existing spot props of the zone | - |
| SQ01_v3 | Parish wells - variation 3 | wild | quest | road | existing spot props of the zone | - |
| SQ02_v1 | Parish fonts - variation 1 | town | quest | road | existing spot props of the zone | - |
| SQ02_v2 | Parish fonts - variation 2 | bluffs | quest | road | existing spot props of the zone | - |
| SQ02_v3 | Parish fonts - variation 3 | n_manor_bluffs | quest | road | existing spot props of the zone | - |
| SQ03_v1 | Parish lofts - variation 1 | town | quest | road | existing spot props of the zone | - |
| SQ03_v2 | Parish lofts - variation 2 | briarE | quest | road | existing spot props of the zone | - |
| SQ03_v3 | Parish lofts - variation 3 | mires | quest | road | existing spot props of the zone | - |
| SQ04_v1 | Inquisitor cottages - variation 1 | n_quarantine | quest | road | existing spot props of the zone | - |
| SQ04_v2 | Inquisitor cottages - variation 2 | gaol | quest | road | existing spot props of the zone | - |
| SQ04_v3 | Inquisitor cottages - variation 3 | bastion | quest | road | existing spot props of the zone | - |
| SQ05_v1 | Inquisitor ovens & chimneys - variation 1 | n_quarantine | quest | road | existing spot props of the zone | - |
| SQ05_v2 | Inquisitor ovens & chimneys - variation 2 | lut | quest | road | existing spot props of the zone | - |
| SQ05_v3 | Inquisitor ovens & chimneys - variation 3 | wild | quest | road | existing spot props of the zone | - |
| SQ06_v1 | Citadel approaches - variation 1 | n_citadel | quest | road | existing spot props of the zone | - |
| SQ06_v2 | Citadel approaches - variation 2 | iron | quest | road | existing spot props of the zone | - |
| SQ06_v3 | Citadel approaches - variation 3 | ascent | quest | road | existing spot props of the zone | - |
| SQ07_v1 | Toll bridges - variation 1 | n_tollgorge | quest | road | existing spot props of the zone | - |
| SQ07_v2 | Toll bridges - variation 2 | n_tollgorge | quest | road | existing spot props of the zone | - |
| SQ07_v3 | Toll bridges - variation 3 | chasm | quest | road | existing spot props of the zone | - |
| SQ08_v1 | Smuggler ridges - variation 1 | n_hollowridge | quest | road | existing spot props of the zone | - |
| SQ08_v2 | Smuggler ridges - variation 2 | ridge | quest | road | existing spot props of the zone | - |
| SQ08_v3 | Smuggler ridges - variation 3 | hollow | quest | road | existing spot props of the zone | - |
| SQ09_v1 | Ash pits - variation 1 | n_ashcamp | quest | road | existing spot props of the zone | - |
| SQ09_v2 | Ash pits - variation 2 | waste | quest | road | existing spot props of the zone | - |
| SQ09_v3 | Ash pits - variation 3 | market | quest | road | existing spot props of the zone | - |
| SQ10_v1 | Survivor sinkholes - variation 1 | n_sinkholes | quest | road | existing spot props of the zone | - |
| SQ10_v2 | Survivor sinkholes - variation 2 | sink | quest | road | existing spot props of the zone | - |
| SQ10_v3 | Survivor sinkholes - variation 3 | mires | quest | road | existing spot props of the zone | - |
| SQ11_v1 | Survivor rivers - variation 1 | wild | quest | road | existing spot props of the zone | - |
| SQ11_v2 | Survivor rivers - variation 2 | briarE | quest | road | existing spot props of the zone | - |
| SQ11_v3 | Survivor rivers - variation 3 | desert | quest | road | existing spot props of the zone | - |
| SQ12_v1 | Choir cellars - variation 1 | town | quest | road | existing spot props of the zone | - |
| SQ12_v2 | Choir cellars - variation 2 | n_quarantine | quest | road | existing spot props of the zone | - |
| SQ12_v3 | Choir cellars - variation 3 | lut | quest | road | existing spot props of the zone | - |
| SQ13_v1 | Covenant circles - variation 1 | n_burn | quest | road | existing spot props of the zone | - |
| SQ13_v2 | Covenant circles - variation 2 | waste | quest | road | existing spot props of the zone | - |
| SQ13_v3 | Covenant circles - variation 3 | duneW | quest | road | existing spot props of the zone | - |
| SQ14_v1 | Tidebound coves & cairns - variation 1 | n_tidecoves | quest | road | existing spot props of the zone | - |
| SQ14_v2 | Tidebound coves & cairns - variation 2 | flotsam | quest | road | existing spot props of the zone | - |
| SQ14_v3 | Tidebound coves & cairns - variation 3 | coast | quest | road | existing spot props of the zone | - |

## The 7 new locations (NL1–NL7)
| id | slot | zone | tag | access | reuse | new |
|---|---|---|---|---|---|---|
| NL1 | Choir safe-cellar network (entrances) | town | faction | road | interior choir; interior sewer | cellar hatch prop |
| NL2 | Tidebound tidal caves | n_tidecoves | faction | road | interior den; border_kit/glb/bk_sea_{season}.glb | tidal-cave mouth piece |
| NL3 | Covenant burn-circles (outer ring) | waste | faction | road | martsirt_v2_2/props/prop_bonfire_main.glb; martsirt_v2_2/dressing/dress_rocks.glb | standing-stone ring |
| NL4 | Outer Citadel drainage wards | n_citadel | faction | road | interior sewer; martsirt_v2_2/gatehouse_south/seg_curtain_wall_4m_shared.glb | drainage grate |
| NL5 | Toll undercrofts | n_tollgorge | faction | road | interior undercroft | - |
| NL6 | Single untouched-cache ruin (far off-road) | n_ruin | remnant | OFF-road | martsirt_v2_2/chapel_st_noll/bld_chapel_st_noll_shared.glb; martsirt_v2_2/dressing/dress_rocks.glb; border_kit/glb/bk_mountain_{season}.glb | broken chapel ruin variant (cut chapel) |
| NL7 | Survivor sinkhole shrines (deep water) | n_sinkholes | faction | road | martsirt_v2_2/shrines/shrine_weeping_angel.glb; martsirt_v2_2/dressing/creek.glb | sinkhole collapse mesh |

## Flagged sites (X)
| id | slot | zone | tag | access | reuse | new |
|---|---|---|---|---|---|---|
| X01 | Fallen Parish church ruin (Briarwood) | wild | faction | road | martsirt_v2_2/chapel_st_noll/bld_chapel_st_noll_shared.glb; martsirt_v2_2/graveyard/bld_graveyard_st_noll_shared.glb; interior church1/church2 | - |
| X02 | Fallen Parish church ruin (Mourning Bluffs) | bluffs | faction | road | martsirt_v2_2/chapel_st_noll/bld_chapel_st_noll_shared.glb; martsirt_v2_2/dressing/dress_graveyard.glb; interior nave | - |
| X03 | Ash-camp outer ring (Cinder Barrens edge) | waste | faction | road | martsirt_v2_2/props/prop_campfire.glb; martsirt_v2_2/gatehouse_south/seg_palisade_4m_shared.glb | - |

## Villages (V)
| id | slot | zone | tag | access | reuse | new |
|---|---|---|---|---|---|---|
| V01 | Kettle Ford (coast-road village) | bastion | explore-only | road | martsirt_v2_2/cottage_ness/bld_cottage_ness_shared.glb; martsirt_v2_2/mill/bld_mill_shared.glb; martsirt_v2_2/props/prop_fence_wattle_2m.glb; martsirt_v2_2/herb | - |
| V02 | Greywater (Briarwood road village) | briarE | explore-only | road | martsirt_v2_2/cottage_ness/bld_cottage_ness_shared.glb; martsirt_v2_2/lodge_orrin/bld_lodge_orrin_shared.glb; martsirt_v2_2/stable/bld_stable_shared.glb; martsi | - |
| V03 | Hightarn (ridge switchback hamlet) | ridge | explore-only | road | martsirt_v2_2/cottage_ness/bld_cottage_ness_shared.glb; martsirt_v2_2/v2/bld_forge_wolchen_v2_shared.glb; martsirt_v2_2/gatehouse_south/seg_palisade_4m_shared.g | - |
| V04 | Saltmere (Qadren basin village) | lut | explore-only | road | martsirt_v2_2/props/prop_market_stall_c.glb; martsirt_v2_2/props/prop_crate_stack.glb; martsirt_v2_2/cottage_ness/bld_cottage_ness_shared.glb; interior house | desert reskin of cottage (material swap) |

## Hidden oasis (ONE; no road, secret quest)
| id | slot | zone | tag | access | reuse | new |
|---|---|---|---|---|---|---|
| H01 | Hidden oasis (secret quest) | n_oasis | remnant | OFF-road | martsirt_v2_2/dressing/creek.glb; martsirt_v2_2/dressing/dress_trees.glb; martsirt_v2_2/dressing/dress_rocks.glb; border_kit/glb/bk_desert_{season}.glb | palm/date tree (1 asset) |

## Gothic manors with interiors (M)
| id | slot | zone | tag | access | reuse | new |
|---|---|---|---|---|---|---|
| M01 | Vael Manor (Briarwood, gothic, interior) | n_manor_briar | explore-only | road | martsirt_v2_2/chapel_st_noll/bld_chapel_st_noll_shared.glb; martsirt_v2_2/chapel_st_noll/bld_chapel_st_noll_tower_shared.glb; martsirt_v2_2/dressing/dress_grave | manor shell from chapel+tower kitbash (one new facade) |
| M02 | Ossery Hall (Mourning Bluffs, gothic, interior) | n_manor_bluffs | explore-only | road | martsirt_v2_2/chapel_st_noll/bld_chapel_st_noll_shared.glb; martsirt_v2_2/gatehouse_south/seg_curtain_wall_4m_shared.glb; interior castle1-4; interior nave | same manor facade, winter/dead season |
| M03 | Drowned House (sea cliff W of Martsirt, gothic, interior) | n_manor_coast | explore-only | road | martsirt_v2_2/chapel_st_noll/bld_chapel_st_noll_tower_shared.glb; border_kit/glb/bk_sea_{season}.glb; interior house; interior vault | same manor facade |

## Explore-only spaces (E)
| id | slot | zone | tag | access | reuse | new |
|---|---|---|---|---|---|---|
| E01 | Cliff overlook above the sea | coast | explore-only | road | zone kit + dressing | - |
| E02 | Wreck shallows | flotsam | explore-only | road | zone kit + dressing | - |
| E03 | Fog hollow with standing stones | wild | explore-only | road | zone kit + dressing | - |
| E04 | Fallen watchtower | bluffs | remnant | road | zone kit + dressing | - |
| E05 | Bog lights boardwalk | mires | explore-only | road | zone kit + dressing | - |
| E06 | Hairpin shrine ledge | ascent | explore-only | road | zone kit + dressing | - |
| E07 | Flooded crypt gallery | crypts | remnant | road | zone kit + dressing | - |
| E08 | Obsidian spire field | weald | remnant | road | zone kit + dressing | - |
| E09 | Dune ship skeleton | desert | explore-only | road | zone kit + dressing | - |
| E10 | Glass flats | waste | explore-only | road | zone kit + dressing | - |
| E11 | Blackwater shore ruin | isle | remnant | road | zone kit + dressing | - |
| E12 | Gorge waterfall cave | n_tollgorge | explore-only | road | zone kit + dressing | - |
| E13 | Highmarket rooftops | market | explore-only | road | zone kit + dressing | - |
| E14 | The Narrow cliff shelf | duneW | explore-only | road | zone kit + dressing | - |
