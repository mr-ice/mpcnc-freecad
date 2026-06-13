# Grommet4David

A Python-driven FreeCAD model of a 3D-printable threaded grommet (hollow cylindrical body with helical-cut threads and a tapered rim), optionally split into two interlocking halves by a wedge cut with a friction pin, plus a matching hex nut.

## Files
- `load_grommet.FCMacro` — FreeCAD macro: reloads `create_grommet` and calls `create_grommet.main()` to build the `create_grommet` document.
- `create_grommet.py` — geometry and parameters loaded by the macro; `create_grommet()` builds the threaded body/rim (with optional wedge split), `create_matching_nut()` builds the hex nut, and `main()` assembles them.
- `grommet1.py` — earlier variant of the grommet (adds four tapered friction cylinders around the body; no matching nut).

## Usage
Open `load_grommet.FCMacro` in FreeCAD 1.0.2 and run it. It rebuilds the grommet and matching nut from `create_grommet.py`; edit the values in `create_grommet.main()` (diameter, depth, rim width, thickness, cut width, taper) to resize, then export the resulting objects as STL/3MF for printing.
