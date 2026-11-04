// Drop-in ground haze wiring for fog_zones.json. Add-only module; call initHaze() once before the first render,
// and setHazeZone(world.id, game.fog, isNight) on zone change / each frame (cheap: only writes 6 uniforms).
// Works on every stock material with fog=true. Materials with a custom onBeforeCompile simply keep density 0 (no haze) unless
// they call applyHazeUniforms(shader) inside their own hook (one line).
import { Color, Material, ShaderChunk } from 'three';

const URL = 'https://raw.githubusercontent.com/bdblonewolf/sanctuary-assets/main/handoff/game_engineer/fog/fog_zones.json';
export const haze = {
  uHazeColor: { value: new Color(0xa3aebc) }, uHazeDensity: { value: 0 },
  uHazeBase: { value: 0 }, uHazeTop: { value: 1.6 }, uHazeFall: { value: 1.6 }, uHazeRange: { value: 30 },
};
let data: any = null; let target = 0;
export function applyHazeUniforms(s: { uniforms: Record<string, any> }) { Object.assign(s.uniforms, haze); }

export async function initHaze() {
  ShaderChunk.fog_pars_vertex += '\nvarying vec3 vHazeWp;';
  ShaderChunk.fog_vertex += `
#ifdef USE_INSTANCING
vHazeWp = (modelMatrix * instanceMatrix * vec4(transformed, 1.0)).xyz;
#else
vHazeWp = (modelMatrix * vec4(transformed, 1.0)).xyz;
#endif`;
  ShaderChunk.fog_pars_fragment += `
varying vec3 vHazeWp;
uniform vec3 uHazeColor; uniform float uHazeDensity; uniform float uHazeBase; uniform float uHazeTop; uniform float uHazeFall; uniform float uHazeRange;`;
  ShaderChunk.fog_fragment += `
if (uHazeDensity > 0.0) {
  float hzH = pow(clamp((uHazeTop - vHazeWp.y) / max(uHazeTop - uHazeBase, 0.01), 0.0, 1.0), uHazeFall);
  float hzD = 1.0 - exp(-length(vHazeWp - cameraPosition) / uHazeRange);
  gl_FragColor.rgb = mix(gl_FragColor.rgb, uHazeColor, min(uHazeDensity * hzH * hzD, 0.35));
}`;
  const base = Material.prototype.onBeforeCompile;
  Material.prototype.onBeforeCompile = function (s: any, r: any) { applyHazeUniforms(s); base.call(this, s, r); };
  try { data = await (await fetch(URL)).json(); } catch { data = null; }
}

function zoneCfg(id: string) {
  if (!data) return null;
  let z = data.zones?.[id] ?? data.default;
  if (z?.inherit) z = data[z.inherit] ?? data.default;
  return z;
}
// Call on zone change and every frame (dt in seconds). weather = game.fog (0..1); night = true at night.
export function setHazeZone(id: string, weather: number, night: boolean, dt = 1 / 60) {
  const z = zoneCfg(id); if (!z) return;
  const m = data.model;
  target = (z.density ?? 0) * (1 + 1.5 * Math.min(1, Math.max(0, weather))) * (night ? m.night_mul ?? 0.8 : 1);
  const k = Math.min(1, dt / (m.transition_s ?? 2.5));
  haze.uHazeDensity.value += (target - haze.uHazeDensity.value) * k;
  if (z.color) haze.uHazeColor.value.lerp(new Color(z.color), k);
  if (z.height) { haze.uHazeBase.value = z.height.base; haze.uHazeTop.value = z.height.top; haze.uHazeFall.value = z.height.falloff_exp; }
  haze.uHazeRange.value = m.range_m ?? 30;
}
