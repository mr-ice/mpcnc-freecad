# Belt Tensioner

A pair of belt-grip parts that clamp onto a G2 (10 mm) toothed belt to tension it.
The grip is two semicylinders bolted together around the belt: one half has tracks
that engage the belt teeth, and a base that engages a tensioner holder. Output is
OpenSCAD (`.scad`), generated from Python via the openpyscad library.

## Files
- `belt_grip.py` — generator script; emits a `.scad` file for the `top` or `bottom` half, using `MetricBolt` and `semicylinder` helpers.
- `belt-tensioner.config` — parameters (grip length/depth/radius, belt width, M3 bolt grip, corner-bracket mounting/spacing, table/wood offsets).
- `belt_tensioner_upper.scad` — generated OpenSCAD output (currently only the `$fn` header).

## Usage
Run the generator and choose which half to make:

```
python belt_grip.py --part top    [--out top.scad]
python belt_grip.py --part bottom  [--out bottom.scad]
```

Output `.scad` is rendered to STL in OpenSCAD. Edit `belt-tensioner.config` to
change dimensions. Requires `openpyscad` and the repo-level `Config`, `MetricBolt`,
and `semicylinder` modules.
