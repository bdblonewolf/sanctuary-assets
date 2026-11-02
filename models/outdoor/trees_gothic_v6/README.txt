trees_gothic_v6 - close-range gothic forest trees for Sanctuary (replace glb_v5 tree_conifer_a/b/c + tree_decid_a/b in-map; far rings untouched)
Files: tree_v6_<archetype>_<summer|autumn|winter>.glb  (10 archetypes x 3 seasons). Scene root node sway_<stem> -> children <stem>_LOD0/1/2.
Manifest: trees_gothic_v6.json (tris, bytes, heights, mix weights, v5->v6 swap rules, atlas layout, sources/licences).
Sway: TEXCOORD_1.x = weight (0 root..1 tip), TEXCOORD_1.y = phase.  COLOR_0 = AO/tint multiply.
Rebuild: cd src_trees_v6 && python3 atlas.py && python3 build.py && python3 previews.py && python3 manifest.py
Sources: procedural geometry/foliage; bark CC0 Poly Haven (pine_bark, island_tree_02 branches, bark_willow_02).
