/**
 * Sanctuary campfire fire — ShaderMaterial + particle script (v2).
 *
 * Additive, depthWrite: false, flipbook billboard.
 * Implements Brian's pass-2 spec:
 *   1. No linear alpha fade. Tight smoothstep clamp on texture alpha
 *      (default smoothstep(0.25, 0.45, texAlpha)), uniforms uLo / uHi.
 *   2. Soft-particle depth fade: alpha → 0 within 0.1 world units of any
 *      solid mesh or the ground.
 *   3. Grit-dissolve at the apex of lifetime (and/or uv.y tips): fine hash
 *      noise vs a rising threshold, sharp flickering micro-embers, no blur-out.
 *   4. Dark gothic palette: tint + capped intensity, keep blacks, no bloom wash.
 *      Flickering point light notes are in the particle script below.
 *
 * Linear filtering on the flipbook. Premultiplied PNG (RGB already * alpha;
 * where alpha is 0, RGB is 0).
 *
 * GLSL is NOT COMPILED and this file is NOT TESTED in three.js or in the game.
 * Syntax-checked only with `node --check`.
 *
 * three.js: written against r150+ style APIs (ShaderMaterial, DepthTexture,
 * WebGLRenderTarget, AdditiveBlending). Adjust if your engine revision differs.
 */
/* eslint-disable no-undef */

const DEFAULTS = {
  cols: 4,
  rows: 4,
  fps: 16,
  // Billboard world size, metres. Pivot at the BOTTOM CENTER.
  width: 1.2,
  height: 1.3,
  uLo: 0.25,
  uHi: 0.45,
  softDistance: 0.1,
  // For the looping campfire billboard the tip dissolve is already baked
  // into campfire_flame_flipbook_v2.png. Leave dissolveStrength at 0 so
  // the shader does not double-eat the tips. Raise it for short-lived
  // flame particles that should grit-dissolve at the end of their life.
  dissolveStrength: 0.0,
  dissolveStart: 0.65,
  intensity: 1.0,
  intensityCap: 1.35,
  tint: [1, 1, 1],
};

function hash2(p) {
  // Used in JS for the point-light flicker (CPU). GLSL has its own hash.
  const n = Math.sin(p[0] * 127.1 + p[1] * 311.7) * 43758.5453;
  return n - Math.floor(n);
}

/**
 * Create a ShaderMaterial for one additive fire flipbook billboard.
 *
 * @param {object} THREE
 * @param {THREE.Texture} map  campfire_flame_flipbook_v2.png (or _b_v2)
 * @param {object} [opts]
 * @returns {THREE.ShaderMaterial}
 */
function createCampfireFireMaterial(THREE, map, opts) {
  const o = Object.assign({}, DEFAULTS, opts || {});

  // Authored as a premultiplied PNG. Linear filtering keeps the tightened
  // edge from stair-stepping; the tight smoothstep is what makes it crisp,
  // not a nearest-neighbor lookup (which would look pixelated).
  map.generateMipmaps = false;
  map.minFilter = THREE.LinearFilter;
  map.magFilter = THREE.LinearFilter;
  map.wrapS = THREE.ClampToEdgeWrapping;
  map.wrapT = THREE.ClampToEdgeWrapping;
  if ('colorSpace' in map && THREE.LinearSRGBColorSpace) {
    // Additive fire is authored in linear-ish values; do not apply sRGB decode
    // on top or the heart will wash. If your pipeline is sRGB-only, test it.
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
    uDepthIsLinear: { value: 1 }, // 1 = color texture holding linear view distance
    uResolution: { value: new THREE.Vector2(1, 1) },
    uCameraNear: { value: 0.1 },
    uCameraFar: { value: 500 },
    uLogDepthBufFC: { value: 0 },
    uAge: { value: 0.0 },
    uDissolveStrength: { value: o.dissolveStrength },
    uDissolveStart: { value: o.dissolveStart },
    uTint: { value: new THREE.Vector3(o.tint[0], o.tint[1], o.tint[2]) },
    uIntensity: { value: Math.min(o.intensity, o.intensityCap) },
    uIntensityCap: { value: o.intensityCap },
    uTime: { value: 0 },
    uMapSize: { value: new THREE.Vector2(map.image?.width || 1024, map.image?.height || 1024) },
  };

  const material = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: CAMPFIRE_FIRE_VERT,
    fragmentShader: CAMPFIRE_FIRE_FRAG,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    depthTest: true,
    transparent: true,
    toneMapped: false, // keep blacks; do not let tone-map / bloom lift the edges
    side: THREE.DoubleSide,
  });
  material.userData.campfireFire = true;
  return material;
}

const CAMPFIRE_FIRE_VERT = /* glsl */ `
  varying vec2 vUv;
  varying float vViewZ;      // three.js view space: negative in front of the camera
  varying vec4 vClipPos;

  void main() {
    vUv = uv;
    vec4 viewPos = modelViewMatrix * vec4(position, 1.0);
    vViewZ = viewPos.z;
    vClipPos = projectionMatrix * viewPos;
    gl_Position = vClipPos;
  }
`;

const CAMPFIRE_FIRE_FRAG = /* glsl */ `
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
  uniform float uLogDepthBufFC;
  uniform float uAge;
  uniform float uDissolveStrength;
  uniform float uDissolveStart;
  uniform vec3 uTint;
  uniform float uIntensity;
  uniform float uIntensityCap;
  uniform float uTime;
  uniform vec2 uMapSize;

  varying vec2 vUv;
  varying float vViewZ;
  varying vec4 vClipPos;

  // --- hash / value noise (fine grit) ---------------------------------
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
    float nxy0 = mix(nx00, nx10, f.y);
    float nxy1 = mix(nx01, nx11, f.y);
    return mix(nxy0, nxy1, f.z);
  }

  // Perspective window-depth [0,1] -> view Z (NEGATIVE in front, three.js).
  // Standard (non-logarithmic) perspective projection.
  float perspectiveDepthToViewZ(const in float depth, const in float near, const in float far) {
    float zNdc = depth * 2.0 - 1.0;
    return (2.0 * near * far) / (zNdc * (far - near) - far - near);
  }

  vec2 flipbookUV(vec2 uv, float frame, float cols, float rows) {
    float f = floor(mod(frame, cols * rows));
    float col = mod(f, cols);
    float row = floor(f / cols);
    // Sheet is row-major, left-to-right, top-to-bottom. Frame 0 = top-left.
    // three.js UV origin is bottom-left, so the row is flipped.
    vec2 cell = vec2(1.0 / cols, 1.0 / rows);
    vec2 origin = vec2(col, rows - 1.0 - row) * cell;
    // Inset a half texel to reduce UV bleed across the 3 px authored pad.
    vec2 texel = 0.5 / uMapSize;
    vec2 uvPad = clamp(uv, texel / cell, 1.0 - texel / cell);
    return origin + uvPad * cell;
  }

  void main() {
    vec2 uv = flipbookUV(vUv, uFrame, uCols, uRows);
    vec4 tex = texture2D(map, uv);

    // Premultiplied PNG: rgb is already * alpha, and true-black at alpha 0.
    // Recover a colour for the clamp, then re-premultiply at the end.
    float texAlpha = tex.a;
    vec3 unpremul = tex.rgb / max(texAlpha, 1e-5);

    // (1) Tight alpha contrast. Not a linear fade. Tunable uLo / uHi.
    // Linear filtering of the texture keeps this from pixelating; the
    // smoothstep is only a contrast curve, not a binary cut.
    float alpha = smoothstep(uLo, uHi, texAlpha);

    // (3) Grit-dissolve at the apex of lifetime (and along the tip, uv.y).
    // Disabled when uDissolveStrength is 0 (looping campfire billboard —
    // dissolve is already baked into the v2 sheet).
    if (uDissolveStrength > 1e-5) {
      float age = clamp(uAge, 0.0, 1.0);
      // Also tighten near the top of the quad so tongues break apart.
      float tip = smoothstep(0.55, 0.92, vUv.y);
      float apex = max(smoothstep(uDissolveStart, 1.0, age), tip * 0.65);
      float thresh = 0.18 + 0.82 * apex;
      float grit = vnoise(vec3(vUv * 42.0, uTime * 3.0 + age * 7.0));
      grit = mix(grit, vnoise(vec3(vUv * 90.0, uTime * 5.5)), 0.45);
      // Narrow transition: sharp fragments, not a blur-out / muddy mist.
      float keep = smoothstep(thresh - 0.07, thresh + 0.02, grit);
      float edge = smoothstep(thresh - 0.10, thresh - 0.01, grit)
                 * (1.0 - smoothstep(thresh - 0.01, thresh + 0.06, grit));
      alpha *= mix(1.0, keep, apex * uDissolveStrength);
      // Ember-colour boost on the dissolve edge (amber, not red).
      unpremul += vec3(1.0, 0.48, 0.08) * edge * apex * uDissolveStrength * 0.8;
    }

    // (2) Soft-particle depth fade. Fades to 0 within uSoftDistance (0.1 m)
    // of any solid already in the depth / linear-depth pre-pass.
    if (uUseDepth > 0.5) {
      vec2 screenUv = (vClipPos.xy / max(vClipPos.w, 1e-6)) * 0.5 + 0.5;
      float sceneViewDist;
      if (uDepthIsLinear > 0.5) {
        // Recommended path: a color texture written with positive view distance
        // (-viewPos.z) from a solid-only pre-pass. Avoids log-depth issues.
        sceneViewDist = texture2D(uDepth, screenUv).r;
      } else {
        // Alternative: a DepthTexture from a NON-logarithmic perspective camera.
        // See SHADER_v2.md for the unpack and why log-depth should use the
        // linear color pre-pass instead.
        float d = texture2D(uDepth, screenUv).r;
        float sceneViewZ = perspectiveDepthToViewZ(d, uCameraNear, uCameraFar);
        sceneViewDist = -sceneViewZ;
      }
      float fragViewDist = -vViewZ;
      // scene is farther away than the fragment → positive gap.
      float gap = sceneViewDist - fragViewDist;
      alpha *= smoothstep(0.0, uSoftDistance, gap);
    }

    // (4) Dark gothic palette: authored colour, a white tint only, capped
    // intensity. Do not add a gray lift or a bloom wash — keep blacks.
    vec3 color = unpremul * uTint * min(uIntensity, uIntensityCap);
    color = max(color, vec3(0.0));

    // Re-premultiply for AdditiveBlending (One, One). RGB already holds
    // the energy to add; alpha is informative only under pure additive.
    gl_FragColor = vec4(color * alpha, alpha);
  }
`;

/**
 * Recommended linear-view-distance pre-pass material (solids only).
 * Renders -viewPos.z into a float / RGBA color target; bind that texture
 * as uDepth and set uDepthIsLinear = 1, uUseDepth = 1.
 *
 * GLSL is NOT COMPILED / NOT TESTED.
 */
function createLinearDepthMaterial(THREE) {
  return new THREE.ShaderMaterial({
    vertexShader: /* glsl */ `
      varying float vViewDist;
      void main() {
        vec4 viewPos = modelViewMatrix * vec4(position, 1.0);
        vViewDist = -viewPos.z;
        gl_Position = projectionMatrix * viewPos;
      }
    `,
    fragmentShader: /* glsl */ `
      varying float vViewDist;
      void main() {
        gl_FragColor = vec4(vViewDist, 0.0, 0.0, 1.0);
      }
    `,
    toneMapped: false,
  });
}

/**
 * Flipbook frame (0-based) from time and a per-billboard random offset.
 */
function frameAt(timeSec, fps, frameCount, offset) {
  return Math.floor(timeSec * fps + (offset || 0)) % frameCount;
}

/**
 * Build the two crossed upright fire billboards (XY and ZY planes), a
 * flickering gothic point light, plus optional ember and smoke hooks.
 *
 * The group is placed at `origin` (world). Each fire plane is pivoted at
 * its bottom center, so origin should be the top-center of the log pile
 * (inside the teepee, not in front of the near logs).
 *
 * NOT TESTED in the game.
 */
function createCampfireFireRig(THREE, opts) {
  const o = Object.assign({
    origin: new THREE.Vector3(0, 0, 0),
    mapA: null, // campfire_flame_flipbook_v2.png
    mapB: null, // campfire_flame_flipbook_b_v2.png
    width: 1.2,
    height: 1.3,
    fps: 16,
    cols: 4,
    rows: 4,
    // B is 5–10 % smaller so the cross does not lock into a perfect plus.
    scaleB: 0.92,
    // Random frame offsets (0..15). Pass explicit values to keep them stable.
    offsetA: Math.floor(Math.random() * 16),
    offsetB: Math.floor(Math.random() * 16),
    lightColor: 0xffa24a, // warm orange, not red, not white
    lightIntensity: 1.6,  // LOW — gothic, high-contrast, not a flood fill
    lightDistance: 6.0,   // metres; decay is physically meaningful inside this
    lightDecay: 2.0,
    lightCastShadow: false, // set true only if the scene is set up for it
    softDistance: 0.1,
  }, opts || {});

  const group = new THREE.Group();
  group.position.copy(o.origin);

  const matA = createCampfireFireMaterial(THREE, o.mapA, {
    cols: o.cols, rows: o.rows, fps: o.fps,
    width: o.width, height: o.height,
    softDistance: o.softDistance,
  });
  const matB = createCampfireFireMaterial(THREE, o.mapB, {
    cols: o.cols, rows: o.rows, fps: o.fps,
    width: o.width, height: o.height,
    softDistance: o.softDistance,
  });

  function makePlane(mat, w, h, rotY) {
    const geo = new THREE.PlaneGeometry(w, h);
    // Pivot at the bottom center: shift the geometry up by half height.
    geo.translate(0, h * 0.5, 0);
    const mesh = new THREE.Mesh(geo, mat);
    mesh.rotation.y = rotY;
    mesh.frustumCulled = false;
    mesh.renderOrder = 2; // after solids, with the other additive FX
    return mesh;
  }

  const planeA = makePlane(matA, o.width, o.height, 0);
  const planeB = makePlane(matB, o.width * o.scaleB, o.height * o.scaleB, Math.PI * 0.5);
  group.add(planeA, planeB);

  // High-contrast cobblestone lighting: a SMALL, warm, decaying point light.
  // Low intensity, tight distance, warm orange. Do not flood the scene.
  // Optional shadow-casting is off by default (cost + Peter-panning on
  // the soft particles); enable only with a tight shadow camera.
  const light = new THREE.PointLight(
    o.lightColor,
    o.lightIntensity,
    o.lightDistance,
    o.lightDecay,
  );
  light.position.set(0, o.height * 0.35, 0);
  light.castShadow = !!o.lightCastShadow;
  if (light.castShadow && light.shadow) {
    light.shadow.mapSize.width = 512;
    light.shadow.mapSize.height = 512;
    light.shadow.camera.near = 0.15;
    light.shadow.camera.far = o.lightDistance;
    light.shadow.bias = -0.003;
  }
  group.add(light);

  const state = {
    group,
    planeA,
    planeB,
    matA,
    matB,
    light,
    offsetA: o.offsetA,
    offsetB: o.offsetB,
    fps: o.fps,
    frameCount: o.cols * o.rows,
    baseIntensity: o.lightIntensity,
    time: 0,
  };

  /**
   * Advance flipbook frames and the gothic flicker.
   * Flicker is a cheap CPU hash, quantized to the same 16 fps as the sheet
   * so the light and the flame read as one fire, not two clocks.
   */
  function update(dt, depthSetup) {
    state.time += dt;
    const t = state.time;
    const fA = frameAt(t, state.fps, state.frameCount, state.offsetA);
    const fB = frameAt(t, state.fps, state.frameCount, state.offsetB);
    state.matA.uniforms.uFrame.value = fA;
    state.matB.uniforms.uFrame.value = fB;
    state.matA.uniforms.uTime.value = t;
    state.matB.uniforms.uTime.value = t;

    if (depthSetup) {
      bindDepth(state.matA, depthSetup);
      bindDepth(state.matB, depthSetup);
    }

    // Quantize flicker to 16 fps so it matches the flipbook cadence.
    const tick = Math.floor(t * state.fps);
    const n1 = hash2([tick * 0.17, 3.1]);
    const n2 = hash2([tick * 0.07 + 1.7, 8.9]);
    const flicker = 0.82 + 0.22 * n1 + 0.08 * (n2 - 0.5);
    state.light.intensity = state.baseIntensity * flicker;
  }

  return { group, update, state };
}

function bindDepth(mat, setup) {
  mat.uniforms.uUseDepth.value = 1;
  mat.uniforms.uDepth.value = setup.texture;
  mat.uniforms.uDepthIsLinear.value = setup.linear ? 1 : 0;
  mat.uniforms.uResolution.value.set(setup.width, setup.height);
  mat.uniforms.uCameraNear.value = setup.near;
  mat.uniforms.uCameraFar.value = setup.far;
}

/**
 * Depth pre-pass helper.
 *
 * Recommended: render solids only with createLinearDepthMaterial() into a
 * float (or half-float) color target, then pass { texture, linear: true,
 * width, height, near, far } into update().
 *
 * Alternative: attach a DepthTexture to a WebGLRenderTarget, render the
 * solid scene with the real materials, and pass { texture: target.depthTexture,
 * linear: false, ... }. Only correct when logarithmicDepthBuffer is FALSE.
 *
 * NOT TESTED.
 */
function createFireDepthTarget(THREE, renderer, width, height, linear) {
  const w = Math.max(1, width | 0);
  const h = Math.max(1, height | 0);
  if (linear) {
    return new THREE.WebGLRenderTarget(w, h, {
      format: THREE.RGBAFormat,
      type: THREE.FloatType,
      depthBuffer: true,
      stencilBuffer: false,
      minFilter: THREE.NearestFilter,
      magFilter: THREE.NearestFilter,
    });
  }
  const depthTexture = new THREE.DepthTexture(w, h);
  depthTexture.format = THREE.DepthFormat;
  depthTexture.type = THREE.UnsignedIntType;
  return new THREE.WebGLRenderTarget(w, h, {
    depthTexture,
    depthBuffer: true,
    stencilBuffer: false,
    minFilter: THREE.NearestFilter,
    magFilter: THREE.NearestFilter,
  });
}

/**
 * Tiny rising ember sprites. Uses the existing Fireball sheet
 * `characters_art/fx_rites/fireball/fireball_sparks_embers.png` (additive).
 * Spawn a handful above the heart, short life, grit-like flicker.
 * NOT TESTED.
 */
function createEmberParticles(THREE, opts) {
  const o = Object.assign({
    map: null,
    count: 14,
    origin: new THREE.Vector3(0, 0.7, 0),
    rise: 0.55,          // metres over a lifetime
    life: 0.7,           // seconds
    size: 0.06,          // metres
  }, opts || {});

  const mat = new THREE.SpriteMaterial({
    map: o.map,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    color: 0xffc56a,
    toneMapped: false,
  });

  const sprites = [];
  const seeds = [];
  for (let i = 0; i < o.count; i++) {
    const s = new THREE.Sprite(mat.clone());
    s.scale.set(o.size, o.size, 1);
    s.position.copy(o.origin);
    s.renderOrder = 3;
    sprites.push(s);
    seeds.push({
      phase: Math.random(),
      x: (Math.random() - 0.5) * 0.35,
      z: (Math.random() - 0.5) * 0.35,
    });
  }

  function update(t, parent) {
    for (let i = 0; i < sprites.length; i++) {
      const life = ((t / o.life) + seeds[i].phase) % 1;
      const y = o.origin.y + life * o.rise;
      sprites[i].position.set(o.origin.x + seeds[i].x, y, o.origin.z + seeds[i].z);
      const fade = life < 0.12 ? life / 0.12 : (life > 0.75 ? 1 - (life - 0.75) / 0.25 : 1);
      sprites[i].material.opacity = Math.max(0, fade);
      sprites[i].visible = fade > 0.02;
    }
  }
  return { sprites, update };
}

// UMD-style export for both module and plain script tags.
const CampfireFireV2 = {
  DEFAULTS,
  createCampfireFireMaterial,
  createLinearDepthMaterial,
  createCampfireFireRig,
  createFireDepthTarget,
  createEmberParticles,
  frameAt,
  bindDepth,
  CAMPFIRE_FIRE_VERT,
  CAMPFIRE_FIRE_FRAG,
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = CampfireFireV2;
}
if (typeof window !== 'undefined') {
  window.CampfireFireV2 = CampfireFireV2;
}
