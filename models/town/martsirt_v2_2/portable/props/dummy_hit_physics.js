/**
 * dummy_hit_physics.js — engine-agnostic damped angular spring for a training dummy.
 * Pivot at dummy_root base (ground). Apply impulse on hit; integrate each frame.
 *
 * three.js usage:
 *   import { DummyHitPhysics } from './dummy_hit_physics.js';
 *   const phys = new DummyHitPhysics(dummyRoot, { stiffness: 28, damping: 6, maxAngle: 0.35 });
 *   phys.applyHit(hitDir, force);   // hitDir world xz (or xyz), force ~1..8
 *   // in animate(): phys.update(dt);
 *
 * Tunables (defaults match a heavy straw/burlap dummy on a timber post):
 *   stiffness  — spring return strength (rad/s^2 per rad)
 *   damping    — velocity decay
 *   maxAngle   — clamp lean (radians) ~20 deg default
 *   mass       — impulse divisor
 *   secondary  — optional head/straw lag (0..1), applied if a child named 'dummy' exists
 */
export class DummyHitPhysics {
  constructor(root, opts = {}) {
    this.root = root;
    this.stiffness = opts.stiffness ?? 28;
    this.damping = opts.damping ?? 6;
    this.maxAngle = opts.maxAngle ?? 0.35;
    this.mass = opts.mass ?? 1.0;
    this.secondary = opts.secondary ?? 0.15;
    this.ax = 0; // rotation about X (lean in Z)
    this.az = 0; // rotation about Z (lean in X)
    this.vx = 0;
    this.vz = 0;
    this.secX = 0;
    this.secZ = 0;
    this._baseQuat = root.quaternion ? root.quaternion.clone() : null;
  }

  /** Apply a hit. direction is a 3-vector (x,y,z); y is ignored for lean. force > 0. */
  applyHit(direction, force = 2.5) {
    let dx = direction.x ?? direction[0] ?? 0;
    let dz = direction.z ?? direction[2] ?? 0;
    const len = Math.hypot(dx, dz) || 1;
    dx /= len; dz /= len;
    const impulse = force / this.mass;
    // Hit from +Z pushes lean toward -X rotation (pitch back)
    this.vx += -dz * impulse;
    this.vz += dx * impulse;
  }

  update(dt) {
    if (dt <= 0 || dt > 0.1) dt = Math.min(Math.max(dt, 0), 0.05);
    // spring-damper: a'' = -k*a - d*a'
    this.vx += (-this.stiffness * this.ax - this.damping * this.vx) * dt;
    this.vz += (-this.stiffness * this.az - this.damping * this.vz) * dt;
    this.ax += this.vx * dt;
    this.az += this.vz * dt;
    const m = this.maxAngle;
    if (this.ax > m) { this.ax = m; this.vx *= -0.2; }
    if (this.ax < -m) { this.ax = -m; this.vx *= -0.2; }
    if (this.az > m) { this.az = m; this.vz *= -0.2; }
    if (this.az < -m) { this.az = -m; this.vz *= -0.2; }

    if (this.root.rotation) {
      this.root.rotation.x = this.ax;
      this.root.rotation.z = this.az;
      this.root.rotation.y = 0;
    }

    // Optional secondary lag for visual "soft" feel (does not move a separate bone;
    // consumers can read secX/secZ to nudge a child or shader).
    const k = 1 - Math.pow(1 - this.secondary, Math.max(1, dt * 60));
    this.secX += (this.ax - this.secX) * k;
    this.secZ += (this.az - this.secZ) * k;
  }

  reset() {
    this.ax = this.az = this.vx = this.vz = this.secX = this.secZ = 0;
    if (this.root.rotation) {
      this.root.rotation.x = 0;
      this.root.rotation.z = 0;
    }
  }
}

export default DummyHitPhysics;
