# gen_border.py

This regenerates a zone's border layout (`out/layout_<zone>.json`). Re-run it whenever a zone's bounds change; that is the standing rule.

It needs `border_styles.json` and `kit_manifest.json` next to it (copies are included here). Its world/placement inputs are hard-coded box paths near lines 85–97 (the coast world after the 3907d8e cleanup, plus martsirt_world.json and placements.json). Point those at the repo's world and placement JSONs before running.

Usage: `python3 gen_border.py coast|martsirt`
