# env_extra/interactables - final chest + doors (batch1 interactables v2)

Latest finished versions (v2 grit/realism revision; v3/v4 only changed the shrine).
Plain GLB, embedded JPEG textures, no extensions, 1 u = 1 m, +Y up, origin at base centre. gltf-validator: 0 errors.

| File | Size | Tris | Nodes |
|---|---|---|---|
| chest.glb | 1.84 MB | 24,050 | chest_root > body, lid, col_chest |
| door.glb | 1.98 MB | 25,658 | door_root > frame, door (> col_door_leaf), col_door_jamb_l, col_door_jamb_r |
| door_gothic.glb | 2.21 MB | 27,468 | door_gothic_root > same as door |

- Chest lid pivot (0, 0.42, -0.30): `lid.rotation.x = -1.8` opens it.
- Door leaf pivot on the hinge edge (-0.6, 0, 0): `door.rotation.y = +θ` swings inward, `-θ` outward. Opening 1.2 m wide; square door 2.4 m high, gothic apex ~2.49 m. Wall 0.5 m deep.
- `col_*` are box colliders: hide them (`visible=false`) and use for physics. `col_door_leaf` rotates with the leaf, so the doorway is passable when open.

Shrines: the final v4 shrines (shrine_basic.glb, shrine_weeping_angel.glb) are already at models/shrines/ (byte-identical). Their FX data is here:
- `shrine_fx.json`: point lights, candle/glow emitters, weeping-angel cure + `angel_regen` buff (1% max HP/s for 30 s).
- `heal_motes_8x8.png`: 1024 px sprite sheet, 8x8 = 64 frames, additive, 24 fps.

Preview: preview_chest_doors.jpg.
