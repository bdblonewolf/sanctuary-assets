// natural_flow_wire.ts  (add-only, nothing live until wired)
// 1) real trees instead of placeDress cone/box placeholders
// 2) visible bonfire model on every `bonfire` prop
// 3) per-instance variety for decorative props (VISUAL ONLY: colliders/positions in data untouched)
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const BASE = 'https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/';
export const DRESS_TREES: Record<string, string[]> = {
  summer: ['models/outdoor/trees_gothic_v6/tree_v6_pine_healthy_summer.glb','models/outdoor/trees_gothic_v6/tree_v6_pine_mangy_straight_summer.glb','models/outdoor/trees_gothic_v6/tree_v6_decid_gothic_weeping_summer.glb','models/outdoor/trees_gothic_v6/tree_v6_oak_healthy_summer.glb','models/outdoor/v5/trees/tree_conifer_a_v5.glb','models/outdoor/v5/trees/tree_decid_a_v5.glb'],
  autumn: ['models/outdoor/trees_gothic_v6/tree_v6_decid_gothic_crooked_autumn.glb','models/outdoor/trees_gothic_v6/tree_v6_pine_mangy_lean_autumn.glb','models/outdoor/trees_gothic_v6/tree_v6_decid_gothic_weeping_autumn.glb','models/border_trees_v1/btree_oak_autumn.glb','models/border_trees_v1/btree_gothic_tall_autumn.glb'],
  winter: ['models/outdoor/v3trees/tree_pine_dark_snow.glb','models/outdoor/trees_gothic_v6/tree_v6_pine_mangy_droop_winter.glb','models/ashen_v1/gtree_twisted_winter_lod0.glb','models/ashen_v1/gtree_weeping_winter_lod0.glb'],
  dead:   ['models/outdoor/v5/plants/tree_dead_a_v5.glb','models/outdoor/v5/plants/tree_dead_b_v5.glb','models/ashen_v1/gtree_crooked_winter_lod0.glb','models/ashen_v1/gtree_twisted_winter_lod0.glb','models/town/martsirt_v2/props/prop_tree_dead_a.glb'],
};
export const DRESS_BUSHES = ['models/outdoor/v5/plants/plant_scrub_bush_a_v5.glb','models/border_trees_v1/bscrub_a_v5_512.glb'];
export const BONFIRE_GLB = 'models/town/martsirt_v2/props/prop_bonfire_main.glb';
export const CAMPFIRE_GLB = 'models/town/martsirt_v2/props/prop_campfire.glb';

export const hash = (x: number, y: number) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };
const cache = new Map<string, Promise<THREE.Object3D>>();
const loader = new GLTFLoader();
export function loadModel(path: string) {
  if (!cache.has(path)) cache.set(path, loader.loadAsync(BASE + path).then(g => { g.scene.traverse((o: any) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g.scene; }));
  return cache.get(path)!;
}

/** Replace placeDress: call with the same tile list placeDress gets. Each spot picks a random real tree
 *  (or bush 30%), random yaw, scale 0.75-1.35, +-0.4 tile jitter, small lean. Skip `this.cone(...)` instancing. */
export async function placeRealDress(group: THREE.Object3D, spots: {x: number; z: number; y?: number}[], season: string) {
  const trees = DRESS_TREES[season] ?? DRESS_TREES.summer;
  for (const s of spots) {
    const h = hash(s.x + 3.1, s.z + 7.7);
    const list = h < 0.3 ? DRESS_BUSHES : trees;
    const src = await loadModel(list[Math.floor(hash(s.x, s.z) * list.length) % list.length]);
    const m = src.clone();
    m.position.set(s.x + (hash(s.x + 1, s.z) - 0.5) * 0.8, s.y ?? 0, s.z + (hash(s.x, s.z + 1) - 0.5) * 0.8);
    m.rotation.set((hash(s.x + 5, s.z) - 0.5) * 0.12, hash(s.x + 9, s.z + 2) * Math.PI * 2, (hash(s.x, s.z + 5) - 0.5) * 0.12);
    m.scale.setScalar(0.75 + hash(s.x + 2, s.z + 4) * 0.6);
    group.add(m);
  }
}

/** Visible fire pit under every bonfire prop (the flame + light the engine already makes stay as they are). */
export async function placeBonfireModels(group: THREE.Object3D, props: {kind: string; x: number; y: number; style?: string}[], heightAt?: (x: number, z: number) => number) {
  for (const p of props) {
    if (p.kind !== 'bonfire') continue;
    const m = (await loadModel(p.style === 'ash' ? CAMPFIRE_GLB : BONFIRE_GLB)).clone();
    m.position.set(p.x, heightAt ? heightAt(p.x, p.y) : 0, p.y);
    m.rotation.y = hash(p.x, p.y) * Math.PI * 2;
    group.add(m);
  }
}

const DECOR = new Set(['rock', 'bush', 'bones', 'skull', 'debris', 'grass', 'plant', 'stump', 'log', 'crate', 'barrel']);
/** Per-instance variety for repeated decorative meshes. Apply to the rendered object only. */
export function varyDecor(obj: THREE.Object3D, kind: string, x: number, y: number) {
  if (!DECOR.has(kind)) return;
  obj.rotation.y = hash(x + 11, y + 3) * Math.PI * 2;
  const s = 0.7 + hash(x + 4, y + 13) * 0.65; obj.scale.multiplyScalar(s);
  if (kind === 'rock' || kind === 'bones' || kind === 'debris') { obj.rotation.x = (hash(x, y + 21) - 0.5) * 0.25; obj.rotation.z = (hash(x + 21, y) - 0.5) * 0.25; }
  obj.position.x += (hash(x + 6, y) - 0.5) * 0.3; obj.position.z += (hash(x, y + 6) - 0.5) * 0.3;
}
/** Visual thinning: hide ~45% of a decorative prop when 2+ of the same kind+style sit within 1.6 tiles. Collider unchanged. */
export function thinDecor(props: {kind: string; x: number; y: number; style?: string}[]) {
  const hide = new Set<number>();
  props.forEach((p, i) => {
    if (!DECOR.has(p.kind) || p.kind === 'crate' || p.kind === 'barrel') return;
    let n = 0; for (let j = 0; j < i; j++) { const q = props[j]; if (!hide.has(j) && q.kind === p.kind && q.style === p.style && Math.hypot(q.x - p.x, q.y - p.y) < 1.6) n++; }
    if (n >= 2 && hash(p.x + 17, p.y + 29) < 0.45) hide.add(i);
  });
  return hide;
}
