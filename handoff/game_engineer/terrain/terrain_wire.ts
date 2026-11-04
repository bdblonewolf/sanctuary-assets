// Drop-in terrain heights for every zone (data: handoff/game_engineer/terrain/<zone>.json, Martsirt = martsirt.json).
// corners = (w+1)*(h+1) heights in metres, row-major by y; tile (x,y) spans world x..x+1, z..z+1 (three.js x east, z south).
// Usage:
//   await loadTerrain(world.id)                      // on zone load (cached)
//   heightAt(world.id, x, z)                         // ground y for hero, monsters, NPCs, loot, props, camera target
//   displaceGeometry(world.id, planeGeometry)        // after building the ground plane (world-space XZ vertices) -> sets Y
//   isCliff(world.id, tx, ty)                        // treat as solid for pathing (drop edges > 1.2 m)
// Coast and Martsirt are flat at 0 by design, so they are safe first; Bastion/Mires/Iron/Ascent were regraded to <=30 deg on every walkable tile.
const BASE = 'https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/handoff/game_engineer/terrain/';
type T = { w: number; h: number; c: Float32Array; cliff: Set<number>; base: number };
const cache = new Map<string, T | null>();
const fileFor = (id: string) => (id === 'town' ? 'martsirt' : id);

export async function loadTerrain(id: string): Promise<T | null> {
  if (cache.has(id)) return cache.get(id)!;
  let t: T | null = null;
  try {
    const d = await (await fetch(BASE + fileFor(id) + '.json')).json();
    const [w, h] = d.size;
    t = { w, h, c: Float32Array.from(d.corners), base: d.base ?? 0,
      cliff: new Set((d.cliff_tiles ?? []).map((p: number[]) => p[1] * w + p[0])) };
  } catch { t = null; }               // no file (interiors/caves) -> flat 0
  cache.set(id, t);
  return t;
}

export function heightAt(id: string, x: number, z: number): number {
  const t = cache.get(id); if (!t) return 0;
  const fx = Math.max(0, Math.min(t.w, x)), fz = Math.max(0, Math.min(t.h, z));
  const x0 = Math.min(t.w - 1, Math.floor(fx)), z0 = Math.min(t.h - 1, Math.floor(fz));
  const u = fx - x0, v = fz - z0, W = t.w + 1;
  const a = t.c[z0 * W + x0], b = t.c[z0 * W + x0 + 1], c = t.c[(z0 + 1) * W + x0], d = t.c[(z0 + 1) * W + x0 + 1];
  return (a * (1 - u) + b * u) * (1 - v) + (c * (1 - u) + d * u) * v;
}

export function displaceGeometry(id: string, g: { attributes: any; computeVertexNormals(): void }, keepExistingY = true) {
  const p = g.attributes.position;
  for (let i = 0; i < p.count; i++) p.setY(i, (keepExistingY ? p.getY(i) : 0) + heightAt(id, p.getX(i), p.getZ(i)));
  p.needsUpdate = true; g.computeVertexNormals();
}

export const isCliff = (id: string, tx: number, ty: number) => !!cache.get(id)?.cliff.has(ty * (cache.get(id)!.w) + tx);
