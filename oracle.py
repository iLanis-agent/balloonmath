#!/usr/bin/env python3
"""Independent oracle for Balloon math. Mirrors engine.js float ops exactly."""
import json, math

FILL = {"23": 7, "28": 14, "40": 42}
FLOAT = {"latex": 10, "foil": 120}
CLUSTERS_PER_M = 4
PER_CLUSTER = 4

def r1(x): return math.floor(x * 10 + 0.5) / 10

def num(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)

def tank_balloons(tank_l, size):
    if not (isinstance(tank_l, (int, float)) and math.isfinite(tank_l) and tank_l > 0):
        return {"error": "tank size must be positive"}
    vol = FILL.get(size)
    if vol is None:
        return {"error": "unknown balloon size"}
    n = math.floor(tank_l / vol)
    if n < 1:
        return {"error": "tank is too small for one balloon"}
    return {"tankL": r1(tank_l), "size": size, "vol": vol, "balloons": n,
            "leftover": r1(tank_l - n * vol)}

def render_tank(r):
    if "error" in r: return r["error"]
    return (f"{num(r['tankL'])} L of helium fills {r['balloons']} balloons of {r['size']} cm "
            f"({r['vol']} L each) - {num(r['leftover'])} L left over (labeled fill volumes).")

def arch_balloons(length_m):
    if not (isinstance(length_m, (int, float)) and math.isfinite(length_m) and length_m > 0):
        return {"error": "arch length must be positive"}
    clusters = math.ceil(length_m * CLUSTERS_PER_M)
    return {"lengthM": r1(length_m), "clusters": clusters, "balloons": clusters * PER_CLUSTER}

def render_arch(r):
    if "error" in r: return r["error"]
    return (f"{num(r['lengthM'])} m of arch takes about {r['clusters']} clusters of {PER_CLUSTER} = "
            f"{r['balloons']} balloons (labeled cluster every 25 cm).")

def float_window(hours_until, kind):
    if not (isinstance(hours_until, (int, float)) and math.isfinite(hours_until) and hours_until > 0):
        return {"error": "hours must be positive"}
    float_h = FLOAT.get(kind)
    if float_h is None:
        return {"error": "unknown balloon kind"}
    if hours_until <= float_h:
        return {"kind": kind, "hoursUntil": r1(hours_until), "floatH": float_h, "ok": True}
    return {"kind": kind, "hoursUntil": r1(hours_until), "floatH": float_h, "ok": False,
            "waitFor": r1(hours_until - float_h)}

def render_float(r):
    if "error" in r: return r["error"]
    if r["ok"]:
        return (f"Inflate any time from now - {r['kind']} floats about {r['floatH']} h and the event is "
                f"{num(r['hoursUntil'])} h away (labeled float estimate).")
    return (f"Wait {num(r['waitFor'])} h before inflating - {r['kind']} floats about {r['floatH']} h "
            f"and the event is {num(r['hoursUntil'])} h away (labeled float estimate).")

cases = []
for t, s in [(200, "28"), (420, "40"), (5, "28"), (50, "23"), (100, "28"), (1000, "40"),
             (14, "28"), (7.5, "23"), (0, "28"), (-3, "23"), (100, "66"), (300.5, "28")]:
    res = tank_balloons(t, s)
    cases.append({"fn": "tankBalloons", "args": [t, s], "result": res, "render": render_tank(res)})
for m in [5, 2.3, 1, 0.5, 8.75, 3.25, 12, 0.2, 0, -1, 4.4, 6.1]:
    res = arch_balloons(m)
    cases.append({"fn": "archBalloons", "args": [m], "result": res, "render": render_arch(res)})
for h, k in [(6, "latex"), (30, "latex"), (200, "foil"), (10, "latex"), (120, "foil"),
             (2.5, "latex"), (48, "foil"), (0, "latex"), (-2, "foil"), (15, "mylar"),
             (10.5, "latex"), (119, "foil")]:
    res = float_window(h, k)
    cases.append({"fn": "floatWindow", "args": [h, k], "result": res, "render": render_float(res)})

with open("expected.json", "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print(len(cases), "cases written")
