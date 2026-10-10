// Balloon math engine - pure arithmetic, shared by the page and the tests.
// Every borrowed number is a labeled party norm, not a rule.
(function (root) {
"use strict";

// Labeled norms:
// - Helium fill volumes: 23 cm (9 in) balloon about 7 L, 28 cm (11 in) about 14 L, 40 cm (16 in) about 42 L.
// - Garland/arch: a 4-balloon cluster every 25 cm, so about 16 balloons per meter.
// - Float time: latex about 10 h, foil about 120 h (5 days) - labeled estimates, altitude and temperature shift them.
var FILL = { "23": 7, "28": 14, "40": 42 };
var FLOAT = { latex: 10, foil: 120 };
var CLUSTERS_PER_M = 4;
var PER_CLUSTER = 4;

function r1(x) { return Math.round(x * 10) / 10; }
function positive() {
  for (var i = 0; i < arguments.length; i++) {
    var v = arguments[i];
    if (typeof v !== "number" || !isFinite(v) || v <= 0) return false;
  }
  return true;
}

function tankBalloons(tankL, size) {
  if (!positive(tankL)) return { error: "tank size must be positive" };
  var vol = FILL[size];
  if (!vol) return { error: "unknown balloon size" };
  var n = Math.floor(tankL / vol);
  if (n < 1) return { error: "tank is too small for one balloon" };
  return { tankL: r1(tankL), size: size, vol: vol, balloons: n, leftover: r1(tankL - n * vol) };
}

function renderTank(r) {
  if (r.error) return r.error;
  return r.tankL + " L of helium fills " + r.balloons + " balloons of " + r.size + " cm (" + r.vol +
    " L each) - " + r.leftover + " L left over (labeled fill volumes).";
}

function archBalloons(lengthM) {
  if (!positive(lengthM)) return { error: "arch length must be positive" };
  var clusters = Math.ceil(lengthM * CLUSTERS_PER_M);
  var balloons = clusters * PER_CLUSTER;
  return { lengthM: r1(lengthM), clusters: clusters, balloons: balloons };
}

function renderArch(r) {
  if (r.error) return r.error;
  return r.lengthM + " m of arch takes about " + r.clusters + " clusters of " + PER_CLUSTER + " = " + r.balloons +
    " balloons (labeled cluster every 25 cm).";
}

function floatWindow(hoursUntil, kind) {
  if (!positive(hoursUntil)) return { error: "hours must be positive" };
  var floatH = FLOAT[kind];
  if (!floatH) return { error: "unknown balloon kind" };
  if (hoursUntil <= floatH) {
    return { kind: kind, hoursUntil: r1(hoursUntil), floatH: floatH, ok: true };
  }
  return { kind: kind, hoursUntil: r1(hoursUntil), floatH: floatH, ok: false, waitFor: r1(hoursUntil - floatH) };
}

function renderFloat(r) {
  if (r.error) return r.error;
  if (r.ok) {
    return "Inflate any time from now - " + r.kind + " floats about " + r.floatH + " h and the event is " +
      r.hoursUntil + " h away (labeled float estimate).";
  }
  return "Wait " + r.waitFor + " h before inflating - " + r.kind + " floats about " + r.floatH +
    " h and the event is " + r.hoursUntil + " h away (labeled float estimate).";
}

var api = {
  tankBalloons: tankBalloons,
  archBalloons: archBalloons,
  floatWindow: floatWindow,
  renderTank: renderTank,
  renderArch: renderArch,
  renderFloat: renderFloat
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.BalloonMath = api;
})(typeof window !== "undefined" ? window : globalThis);
