/**
 * Sanctuary campfire SMOKE — ShaderMaterial + particle script (v2).
 *
 * NORMAL blend (not additive), depthWrite: false.
 * Flipbook: campfire_smoke_flipbook_v2.png (preferred) or the softer
 * fireball_smoke_flipbook.png as a fallback.
 *
 * Brian's rules:
 *   1. BASE: where smoke is born it is highly transparent — only a subtle
 *      faint heat-tint over the fire, no cloud clutter. A smooth ease keeps
 *      the smoke near-invisible for the first 25 % of its vertical ascent.
 *   2. SOOT INVERSION: in the upper 50–75 % of lifetime a strict colour
 *      ramp shifts to deep matte soot black at the tips (not gray, not
 *      flat / geometric). Tight tunable smoothstep on alpha so the soot
 *      tendrils stand out crisply against a dark foggy environment.
 *   3. TRAIL: strictly upward vertical velocity + subtle wind-driven
 *      horizontal turbulence (noise sway, small amplitude). At the end, a
 *      high-frequency noise mask dissipates the soot into sharp microscopic
 *      wisps (rising threshold by normalized age). No blur-out.
 *
 * Soft-particle depth fade is the same 0.1 world-unit fade as the fire
 * shader (reuse the same linear-depth pre-pass).
 *
 * Premultiplied PNG, no gray wash, KEEP BLACKS.
 *
 * GLSL is NOT COMPILED and this file is NOT TESTED in three.js or in the game.
 * Syntax-checked only with `node --check`.
 */
/* eslint-disable no-undef */

const SMOKE_DEFAULTS = {
  cols: 4,
  rows: 4,
  fps: 12,               // a little slower than the 16 fps flame reads more like smoke
  width: 1.1,            // metres
  height: 1.6,
  // Alpha contrast (tighter than a linear fade). Tunable.
  uLo: 0.18,
  uHi: 0.42,
  softDistance: 0.1,
  // Lifetime (seconds) and motion
  life: 2.8,
  rise: 2.2,             // metres of vertical travel over a full life
  // Spawn just above the flame apex (flames are 1.0–1.3 m, pit 1.2 m).
  spawnY: 1.25,
  spawnJitter: 0.18,
  windAmp: 0.16,         // metres of horizontal sway (small)
  windFreq: 0.35,
  // Visibility curve
  invisibleUntil: 0.25,  // first 25 % of ascent / life almost invisible
  sootStart: 0.50,
  sootEnd: 0.75,
  dissolveStart: 0.78,
  maxAlpha: 0.72,
  heatTint: [0.16, 0.07, 0.03],
  sootColor: [0.025, 0.016, 0.012], // deep matte warm black, NOT gray
  count: 6,
};

function hash2(p) {
  const n = Math.sin(p[0] * 127.1 + p[1] * 311.7) * 43758.5453;
  return n - Math.floor(n);
}

function createCampfireSmokeMaterial(THREE, map, opts) {
  const o = Object.assign({}, SMOKE_DEFAULTS, opts || {});

  map.generateMipmaps = false;
  map.minFilter = THREE.LinearFilter;
  map.magFilter = THREE.LinearFilter;
  map.wrapS = THREE.ClampToEdgeWrapping;
  map.wrapT = THREE.ClampToEdgeWrapping;
  if ('colorSpace' in map && THREE.LinearSRGBColorSpace) {
    map.colorSpace = THREE.LinearSRGBColorSpace;
  }
  map.needsUpdate = true;

  const uniforms = {
    map: { value: map },
    uCols: { value: o.cols },
    uRows: { value: o.rows },
    uFrame: { value: 0 },
    uLo: { value: o.uLo },
    uHi: { value: o.uHi },
    uSoftDistance: { value: o.softDistance },
    uUseDepth: { value: 0 },
    uDepth: { value: null },
    uDepthIsLinear: { value: 1 },
    uResolution: { value: new THREE.Vector2(1, 1) },
    uCameraNear: { value: 0.1 },
    uCameraFar: { value: 500 },
    uAge: { value: 0.0 },
    uInvisibleUntil: { value: o.invisibleUntil },
    uSootStart: { value: o.sootStart },
    uSootEnd: { value: o.sootEnd },
    uDissolveStart: { value: o.dissolveStart },
    uMaxAlpha: { value: o.maxAlpha },
    uHeatTint: { value: new THREE.Vector3(o.heatTint[0], o.heatTint[1], o.heatTint[2]) },
    uSootColor: { value: new THREE.Vector3(o.sootColor[0], o.sootColor[1], o.sootColor[2]) },
    uTime: { value: 0 },
    uMapSize: { value: new THREE.Vector2(map.image?.width || 1024, map.image?.height || 1024) },
  };

  const material = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: CAMPFIRE_SMOKE_VERT,
    fragmentShader: CAMPFIRE_SMOKE_FRAG,
    blending: THREE.NormalBlending, // NOT additive
    depthWrite: false,
    depthTest: true,
    transparent: true,
    toneMapped: false, // keep blacks — do not lift soot into gray
    side: THREE.DoubleSide,
    // Premultiplied PNG: tell three.js so NormalBlending uses One, OneMinusSrcAlpha.
    premultipliedAlpha: true,
  });
  material.userData.campfireSmoke = true;
  return material;
}

const CAMPFIRE_SMOKE_VERT = /* glsl */ `
  varying vec2 vUv;
  varying float vViewZ;
  varying vec4 vClipPos;

  void main() {
    vUv = uv;
    vec4 viewPos = modelViewMatrix * vec4(position, 1.0);
    vViewZ = viewPos.z;
    vClipPos = projectionMatrix * viewPos;
    gl_Position = vClipPos;
  }
`;

const CAMPFIRE_SMOKE_FRAG = /* glsl */ `
  uniform sampler2D map;
  uniform float uCols;
  uniform float uRows;
  uniform float uFrame;
  uniform float uLo;
  uniform float uHi;
  uniform float uSoftDistance;
  uniform float uUseDepth;
  uniform sampler2D uDepth;
  uniform float uDepthIsLinear;
  uniform vec2 uResolution;
  uniform float uCameraNear;
  uniform float uCameraFar;
  uniform float uAge;
  uniform float uInvisibleUntil;
  uniform float uSootStart;
  uniform float uSootEnd;
  uniform float uDissolveStart;
  uniform float uMaxAlpha;
  uniform vec3 uHeatTint;
  uniform vec3 uSootColor;
  uniform float uTime;
  uniform vec2 uMapSize;

  varying vec2 vUv;
  varying float vViewZ;
  varying vec4 vClipPos;

  float hash13(vec3 p) {
    p = fract(p * 0.1031);
    p += dot(p, p.yzx + 33.33);
    return fract((p.x + p.y) * p.z);
  }

  float vnoise(vec3 p) {
    vec3 i = floor(p);
    vec3 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    float n000 = hash13(i);
    float n100 = hash13(i + vec3(1.0, 0.0, 0.0));
    float n010 = hash13(i + vec3(0.0, 1.0, 0.0));
    float n110 = hash13(i + vec3(1.0, 1.0, 0.0));
    float n001 = hash13(i + vec3(0.0, 0.0, 1.0));
    float n101 = hash13(i + vec3(1.0, 0.0, 1.0));
    float n011 = hash13(i + vec3(0.0, 1.0, 1.0));
    float n111 = hash13(i + vec3(1.0, 1.0, 1.0));
    float nx00 = mix(n000, n100, f.x);
    float nx10 = mix(n010, n110, f.x);
    float nx01 = mix(n001, n101, f.x);
    float nx11 = mix(n011, n111, f.x);
    return mix(mix(nx00, nx10, f.y), mix(nx01, nx11, f.y), f.z);
  }

  float perspectiveDepthToViewZ(const in float depth, const in float near, const in float far) {
    float zNdc = depth * 2.0 - 1.0;
    return (2.0 * near * far) / (zNdc * (far - near) - far - near);
  }

  vec2 flipbookUV(vec2 uv, float frame, float cols, float rows) {
    float f = floor(mod(frame, cols * rows));
    float col = mod(f, cols);
    float row = floor(f / cols);
    vec2 cell = vec2(1.0 / cols, 1.0 / rows);
    vec2 origin = vec2(col, rows - 1.0 - row) * cell;
    vec2 texel = 0.5 / uMapSize;
    vec2 uvPad = clamp(uv, texel / cell, 1.0 - texel / cell);
    return origin + uvPad * cell;
  }

  void main() {
    vec2 uv = flipbookUV(vUv, uFrame, uCols, uRows);
    vec4 tex = texture2D(map, uv);
    float texAlpha = tex.a;

    // Tight contrast — distinct soot tendrils, not a soft gray puff.
    // Linear filtering + a smoothstep (not a binary cut) keeps the edge
    // crisp but non-pixelated.
    float alpha = smoothstep(uLo, uHi, texAlpha);

    float age = clamp(uAge, 0.0, 1.0);

    // (1) BASE: near-invisible for the first 25 % of life / ascent.
    // Smooth ease, not a pop. A faint heat-tint may remain, but no clutter.
    float riseVis = smoothstep(uInvisibleUntil, uInvisibleUntil + 0.18, age);
    alpha *= riseVis;

    // Peak in the mid/soot window, then the dissolve takes over.
    float mid = smoothstep(uInvisibleUntil, 0.45, age)
              * (1.0 - smoothstep(0.90, 1.0, age));
    alpha *= mix(0.15, 1.0, mid);
    alpha = min(alpha * uMaxAlpha, uMaxAlpha);

    // (2) SOOT INVERSION: 50–75 % of life ramps from a faint heat-tint to
    // deep matte soot black. Not gray. Not a flat geometric fill — the
    // texture tendrils + tight alpha give the shape.
    float soot = smoothstep(uSootStart, uSootEnd, age);
    // Deep matte soot, not gray. No fill light, no lift.
    vec3 color = mix(uHeatTint, uSootColor, soot);

    // (3) End-of-life grit-dissolve. Rising noise threshold by age.
    // Sharp microscopic wisps, not a blur-out / muddy mist.
    float apex = smoothstep(uDissolveStart, 1.0, age);
    if (apex > 1e-5) {
      float thresh = 0.12 + 0.88 * apex;
      float grit = vnoise(vec3(vUv * 48.0, uTime * 1.6 + age * 5.0));
      grit = mix(grit, vnoise(vec3(vUv * 110.0, uTime * 2.4)), 0.5);
      float keep = smoothstep(thresh - 0.06, thresh + 0.02, grit);
      alpha *= mix(1.0, keep, apex);
    }

    // Soft-particle depth fade, same 0.1 m contract as the fire shader.
    if (uUseDepth > 0.5) {
      vec2 screenUv = (vClipPos.xy / max(vClipPos.w, 1e-6)) * 0.5 + 0.5;
      float sceneViewDist;
      if (uDepthIsLinear > 0.5) {
        sceneViewDist = texture2D(uDepth, screenUv).r;
      } else {
        float d = texture2D(uDepth, screenUv).r;
        float sceneViewZ = perspectiveDepthToViewZ(d, uCameraNear, uCameraFar);
        sceneViewDist = -sceneViewZ;
      }
      float fragViewDist = -vViewZ;
      float gap = sceneViewDist - fragViewDist;
      alpha *= smoothstep(0.0, uSoftDistance, gap);
    }

    // Premultiplied output for NormalBlending with premultipliedAlpha: true
    // (One, OneMinusSrcAlpha). RGB stays dark — no gray wash.
    vec3 pre = color * alpha;
    gl_FragColor = vec4(pre, alpha);
  }
`;

/**
 * A small stack of rising smoke cards, spawned just above the flame apex.
 *
 * Motion (CPU): strictly upward velocity, plus a small noise-driven
 * horizontal wind sway. Per-particle age and a random flipbook offset.
 *
 * NOT TESTED in the game.
 */
function createCampfireSmokeRig(THREE, opts) {
  const o = Object.assign({}, SMOKE_DEFAULTS, opts || {});
  if (!o.map) {
    throw new Error('createCampfireSmokeRig: opts.map (smoke flipbook texture) is required');
  }

  const group = new THREE.Group();
  if (o.origin) group.position.copy(o.origin);

  const particles = [];
  for (let i = 0; i < o.count; i++) {
    const mat = createCampfireSmokeMaterial(THREE, o.map, o);
    const geo = new THREE.PlaneGeometry(o.width, o.height);
    geo.translate(0, o.height * 0.5, 0); // pivot bottom-center
    const mesh = new THREE.Mesh(geo, mat);
    // Alternate a slight yaw so a stack of cards does not z-fight as one plane.
    mesh.rotation.y = (i / o.count) * Math.PI * 0.35;
    mesh.renderOrder = 1; // under the additive fire, over solids
    mesh.frustumCulled = false;
    group.add(mesh);
    particles.push({
      mesh,
      mat,
      // Stagger births so the column is always populated.
      age: i / o.count,
      life: o.life * (0.85 + 0.3 * hash2([i * 1.17, 4.4])),
      offset: Math.floor(hash2([i * 3.7, 1.1]) * o.cols * o.rows),
      seed: hash2([i * 9.1, 2.2]),
      x0: (hash2([i * 2.3, 0.4]) - 0.5) * o.spawnJitter,
      z0: (hash2([i * 4.9, 0.8]) - 0.5) * o.spawnJitter,
    });
  }

  function update(dt, depthSetup) {
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.age += dt / p.life;
      if (p.age >= 1) {
        p.age = p.age % 1;
        p.offset = (p.offset + 3) % (o.cols * o.rows);
      }
      const age = p.age;
      // (3) TRAIL: strictly upward + small wind sway (CPU, noise-driven).
      const y = o.spawnY + age * o.rise;
      const wind = o.windAmp * Math.sin((age * o.rise + p.seed * 10.0) * o.windFreq * Math.PI * 2);
      const wind2 = o.windAmp * 0.6 * Math.sin((age * 1.7 + p.seed * 6.0) * (o.windFreq * 1.4) * Math.PI * 2 + 1.3);
      p.mesh.position.set(p.x0 + wind, y, p.z0 + wind2);

      // Slight scale-up as it rises (a thin birth, a wider soot head).
      const sc = 0.72 + 0.45 * age;
      p.mesh.scale.set(sc, 0.9 + 0.25 * age, 1);

      p.mat.uniforms.uAge.value = age;
      p.mat.uniforms.uTime.value = (p.mat.uniforms.uTime.value || 0) + dt;
      const frame = Math.floor(age * p.life * o.fps + p.offset) % (o.cols * o.rows);
      p.mat.uniforms.uFrame.value = frame;

      if (depthSetup) {
        p.mat.uniforms.uUseDepth.value = 1;
        p.mat.uniforms.uDepth.value = depthSetup.texture;
        p.mat.uniforms.uDepthIsLinear.value = depthSetup.linear ? 1 : 0;
        p.mat.uniforms.uResolution.value.set(depthSetup.width, depthSetup.height);
        p.mat.uniforms.uCameraNear.value = depthSetup.near;
        p.mat.uniforms.uCameraFar.value = depthSetup.far;
      }
    }
  }

  return { group, update, particles };
}

const CampfireSmokeV2 = {
  SMOKE_DEFAULTS,
  createCampfireSmokeMaterial,
  createCampfireSmokeRig,
  CAMPFIRE_SMOKE_VERT,
  CAMPFIRE_SMOKE_FRAG,
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = CampfireSmokeV2;
}
if (typeof window !== 'undefined') {
  window.CampfireSmokeV2 = CampfireSmokeV2;
}
