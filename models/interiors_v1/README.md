# interiors_v1 - data for the Martsirt interiors (stage I2)

inn.json -> world `taproom` (The Salted Kettle). church.json -> world `church1` (Chapel of St. Noll).

The interior uses the same building GLB and transform as the town (placements.json). So every window, door,
hearth and chimney seen from inside is the same mesh you see from the street, and the walkable floor is the
inside of the building's own col_ walls.

Fields
- coords: all x,y are town tiles (placements pos + origin 81,76). The interior world is the rectangle offset..offset+size.
  The loader converts: local = town - offset.
- pieces: GLBs to load at their town transform.
- hide.prefix: node-name prefixes to hide (roof skin, upper storey, yard, col_/nav_/fx_ helpers). hide.minYAbove hides meshes that sit wholly above that height (inn upper floor).
- cutaway: the camera-side wall fades to fadeOpacity.
- walk: rect_local (building-local, metres, with centre and rotY) or poly (town tiles). Tiles whose centre is outside are solid.
- spawn, exits, locked: locked entries are closed doors with a lore key (the crypt hatch stays locked, so church1 has no basement exit).
- props: extra existing GLBs (repo path, or bundle path for game assets3d) or code-built items (candle, stool).
- seats: N3 seat props. Pews use the chapel's own col_pew boxes.
- lights: warm point lights (2700 K is about 0xffa957). shafts: built at the GLB's fx_lightshaft_* nodes and coloured from the nearest window material.
- npcSpots / visits: where NPCs stand inside and which NPCs visit the church at which hours.
- lore: tap spots; keys are in lore/martsirt_lore.json `lines`.
