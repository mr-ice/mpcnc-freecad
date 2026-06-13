# Dog Gate Latch

A Python-driven FreeCAD model of a 3D-printable gate latch: a hollow base mount that slips over a gate post and a pivoting lever/handle latch that hinges on it via tapered cone pins. The handle has a finger indent and the latch carries a wedge that holds the gate closed.

## Files
- `gatelatch.FCMacro` — FreeCAD macro: reloads `latch` and calls `latch.main()` to build the `GateLatch` document.
- `latch.py` — geometry and parameters; `create_base_mount()` builds the post mount, `create_latch_mechanism()` builds the lever/handle/wedge, and `main()` assembles them into `Base` and `Latch` objects.
- `GateLatch-Base.stl` — exported base mount.
- `GateLatch-Latch.stl`, `GateLatch-Latch5mm.stl`, `GateLatch-Latch6mm.stl` — exported latch variants.
- `GateLatch-Lever.stl` — exported lever.
- `GateLatch.stl`, `GateLatch.3mf` — exported full assembly.

## Usage
Open `gatelatch.FCMacro` in FreeCAD 1.0.2 and run it. It rebuilds the model from `latch.py`; edit the parameters at the top of `latch.py` (dimensions, clearances, hinge cone sizes) to retune the fit, then export the `Base` and `Latch` objects as STL/3MF for printing.
