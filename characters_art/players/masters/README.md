# Player masters (uncompressed)
These are the full-resolution sources for the mobile files one folder up. The skin textures are 2048 WebP and none of these files went through mobile_compress. Use them for rebuilds and re-compression. Do not load them in the mobile client.

| Master | Mobile copy |
|---|---|
| `player_<class>.glb` | `../player_<class>.glb`: skin texture downsized to 1024, then mobile_compress.sh (no meshopt/Draco) |
| `player_<class>_hair.glb` | `../player_<class>_hair.glb`: texture already 1024, so only mobile_compress.sh was run |
| `player_necromancer_piercings.glb` | `../player_necromancer_piercings.glb`: no textures, only mobile_compress.sh was run |
| `player_<class>_hair_v2.glb` | `../player_<class>_hair_v2.glb`: hair refitted and shortened to clear the plates; texture already 1024, so only mobile_compress.sh was run |

Classes: archer, elementalist, necromancer, warrior. The geometry, vertex order and rig are identical between each master and its mobile copy.
