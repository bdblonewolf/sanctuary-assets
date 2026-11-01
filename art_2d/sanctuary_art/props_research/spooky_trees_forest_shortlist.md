# Sanctuary – Spooky / Diablo-style trees & dark-forest assets (CC0 shortlist)
Researched 2026-11-01. **Models first** (per Brian: env builder needs real 3D models it can tweak). CC0 only; anything CC-BY / NC / unclear is rejected (see bottom).
Tri counts marked (m) were measured from the downloaded 1k glTF; others from source metadata. Thumbnails: `trees_thumbs/ph_<id>.png`.
**Raw downloads of the Top 10:** `/workspace/sanctuary_art/props/trees/raw/<id>/` (untouched, not converted; see `raw/SOURCES.md`).

## Already owned by the env builder (do not re-download)
- `/workspace/sanctuary/assets3d/overworld/polyhaven/` (1k GLB): dead_tree_trunk (~102k tris), dead_tree_trunk_02 (~83k), dry_branches_medium_01, root_cluster_01, tree_stump_01/02, fir_tree_01 (~7M), pine_tree_01 (~17M), tree_small_02 (~2M), fern_02, moss_01, shrub_01/02/04, nettle_plant, grass_medium_01, rock_moss_set_01/02, boulder_01, rock_07, rock_face_01, namaqualand_cliff_01.
- `sanctuary_env/outdoor`: procedural tree_oak_* (lush/gnarled/autumn/bare/winter), tree_dead_blighted(_spiky) with noose/crow perches, tree_pine_dark(_snow), far billboards tree_far_*, v5 cone backdrop trees, grass clumps; planned burnt-stump set & decimated fir/pine.
- Textures already used: bark_brown_02, forest_leaves_02, brown_mud_leaves_01, moss_wood, rough_wood, rock_pitted_mossy, mossy_stone_wall etc. No HDRIs (procedural sky by design).
- `ENV_SHORTLIST.md` had already *suggested* pine_roots (not downloaded) – now in raw/.

## Top 10 (downloaded raw → props/trees/raw/)
| # | Asset | Source / URL | Licence | What it is | Tris / textures | Format avail. (downloaded) | Game-readiness | Use |
|---|---|---|---|---|---|---|---|---|
| 1 | dead_quiver_trunk | Poly Haven https://polyhaven.com/a/dead_quiver_trunk | CC0 | Bleached, split, gnarled dead trunk/snag | 18k (m); 1k–8k PBR | blend/gltf/fbx/usd (gltf 1k) | Near game-ready; darken albedo; LOD1 ~5k | Hero dead snag / Dark Wood landmark, hang noose/crows |
| 2 | dead_quiver_branch_01 | https://polyhaven.com/a/dead_quiver_branch_01 | CC0 | Dead forked branch | 14.8k (m) | same (gltf 1k) | Good; kitbash onto trunks | Kitbash crowns for dead trees, ground debris |
| 3 | dead_quiver_branch_02 | https://polyhaven.com/a/dead_quiver_branch_02 | CC0 | Dead twisted branch | 14.4k (m) | same (gltf 1k) | Good | Kitbash / fallen limbs |
| 4 | pine_roots | https://polyhaven.com/a/pine_roots | CC0 | Mossy exposed root mound | 163k (m) | same (gltf 1k) | Decimate to ~10–20k | Giant-tree bases, Dark Wood ground set-dressing |
| 5 | root_cluster_02 | https://polyhaven.com/a/root_cluster_02 | CC0 | Tangle of roots (complements owned _01) | 340k (m) | same (gltf 1k) | Decimate hard (~15k) | Root walls, cave/forest edges |
| 6 | single_root | https://polyhaven.com/a/single_root | CC0 | Single arching root | 61k (m) | same (gltf 1k) | Decimate to ~5k; instance | Trip-roots, path borders, kitbash under trees |
| 7 | island_tree_02 | https://polyhaven.com/a/island_tree_02 | CC0 | Gnarled twisted trunk with leaf canopy | 1.07M (m) | same (gltf 1k, 45 MB) | Heavy: strip leaf mesh → bare gnarled tree, decimate, LOD+billboard | Hero gnarled "Tristram oak" once leaves removed |
| 8 | fir_sapling | https://polyhaven.com/a/fir_sapling | CC0 | Dark young fir | 433k (m) | same (gltf 1k) | Needs LOD/impostor; cards ok | Dark conifer understory filler |
| 9 | shrub_03 | https://polyhaven.com/a/shrub_03 | CC0 | Sparse, dead-looking twig shrub | 8.3k (m) | same (gltf 1k) | Game-ready | Dead brush ground cover |
| 10 | 3DTreeStump001 | ambientCG https://ambientcg.com/a/3DTreeStump001 | CC0 | Photoscanned stump | ~5k faces; 1K–4K color/normal/AO | OBJ + USDC zip (LQ-1K-JPG) | Game-ready | Realistic stump variety (vs PH stumps owned) |

Note: Poly Haven has **no standing realistic dead tree**; #1+#2/#3 kitbash or #7-without-leaves are the best realistic route. Procedural tree_dead_blighted already covers the archetype.

## Further candidates (not downloaded)
### Models
| Asset | Source / URL | Licence | Notes (tris, format) | Use |
|---|---|---|---|---|
| island_tree_03 | https://polyhaven.com/a/island_tree_03 | CC0 | Very twisted trunk, 4.76M tris, 85 MB 1k gltf; blend/gltf/fbx/usd | Alt hero gnarled tree (strip leaves) |
| island_tree_01 | https://polyhaven.com/a/island_tree_01 | CC0 | Gnarled, 3.7M tris | Alt hero |
| bark_debris_01 | https://polyhaven.com/a/bark_debris_01 | CC0 | 363k tris, 8 MB | Forest-floor debris (decimate) |
| fir_sapling_medium | https://polyhaven.com/a/fir_sapling_medium | CC0 | 2.3M tris, 78 MB | Bigger dark fir (impostor) |
| pine_sapling_small | https://polyhaven.com/a/pine_sapling_small | CC0 | 398k tris, sparse | Sparse pine filler |
| searsia_burchellii | https://polyhaven.com/a/searsia_burchellii | CC0 | 1.43M tris, sparse twiggy | Thorny scrub-tree |
| wild_rooibos_bush | https://polyhaven.com/a/wild_rooibos_bush | CC0 | 76k tris | Scrub ground cover |
| 3DStick001 | https://ambientcg.com/a/3DStick001 | CC0 | OBJ/USDC, low poly | Twig scatter |
| CC0 Japanese Black Pine (ffishAsia) | https://sketchfab.com/3d-models/cc0-japanese-black-pine-p-thunbergii-c834dd713c384e60b1b943b82cd8d8a7 | CC0 (API-verified) | 327k tris scan; Sketchfab login to download | Twisted dark pine hero (scan) |
| CC0 Japanese Red Pine (ffishAsia) | https://sketchfab.com/3d-models/cc0-japanese-red-pine-pinus-densiflora-a21a0843495a4235882873c121512a94 | CC0 (API-verified) | 1.42M tris; login | Gnarled pine |
| CC0 Sawtooth Oak (ffishAsia) | https://sketchfab.com/3d-models/cc0-sawtooth-oak-quercus-acutissima-cb9130b2028b4a2db439962e49d87990 | CC0 (API-verified) | 387k tris; login | Oak reference/hero |
| Stump – Low Poly Medieval | https://sketchfab.com/3d-models/stump-low-poly-medieval-cc0-11acb1c3ca694c0984cdf264f97de83e | CC0 (API-verified) | 1,248 tris; login | Cheap stump (stylised-ish) |
| Tree Trunk with Moss (3DTexel) | https://3dtexel.com/product/photogrammetry-tree-3d-assets/ | CC0 (page) | Realistic mossy trunk; download via site/Blender addon, format unconfirmed | Mossy trunk |
| Grab3D Dead Tree | https://grab3d.com/models/nature/dead-tree/ | CC0 | 13.8k tris, 2K tex, GLB/FBX/BLEND, no login | Standing dead tree — **stylised "cozy"**, needs restyle |
| Quaternius Ultimate Nature (Dead Birch/Common/Willow ×5) | https://quaternius.com/packs/ultimatenature.html | CC0 | ~0.8–1.6k tris, FBX/OBJ/blend | **Too stylised**; silhouettes / far-LOD only |
| Kenney Nature Kit | https://kenney.nl/assets/nature-kit | CC0 | low-poly GLB/FBX | **Too stylised** |
| Toolbench Low-poly Forest Kit (dead tree 142 tris) | https://toolbenchdev.com/gamedev/cc0-game-assets/low-poly-forest-kit/ | CC0 | flat colour, no UVs | **Too stylised** |
| OpenGameArt Big LowPoly Env Pack (3 dead trees) | opengameart.org | CC0 | low-poly | Too stylised |

### Bark / ground materials (CC0, 1k–8k) – for re-texturing models darker
Poly Haven: bark_brown_01, bark_willow, bark_willow_02, pine_bark, knotted_pine_bark, tree_bark_03, jolcham_oak_bark_01, chinese_cedar_bark; forest_floor, forest_ground_04/05/06, forrest_ground_01/03, leaves_forest_ground, mud_forest, dry_decay_leaves, roots, winter_leaves, mossy_rock. ambientCG: Bark008/011/013 (mossy), Ground028 (dead), Ground070/076/084 (roots), Moss001–004, PineNeedles001.
### HDRIs (only if procedural sky is ever dropped – low priority)
Poly Haven misty_pines, mossy_forest, muddy_autumn_forest, snowy_forest; ambientCG DayEnvironmentHDRI039 (foggy forest).

## Checked & rejected
- Smithsonian 3D Open Access: CC0 search "tree" = 17 results, none usable trees/wood.
- Sketchfab items whose API licence is **CC-BY** (despite "CC0" in title/description): "CC0 - Dead Wood 2" (plaggy), "Cut down tree" (3DLandskap), "Scan of fallen tree" (sterlingcrispin), "Gnarly Dead Trees" (MattMakesSwords), "Mossy tree stump"(+fungi) (ZiemniaQ), "Dead Tree Trunk" (ngooi1397), "Dead Tree" (MaX3Dd), "Bare/Leafless tree" (Darxkl05). widthRider "dead tree log" = CC-BY. Paid store items skipped.
- Poly Haven quiver_tree_01/02, othonna, jacaranda: too exotic/African.
- Archade "Dead Tree Trunk 2" = mirror of PH dead_tree_trunk_02 (already owned).
