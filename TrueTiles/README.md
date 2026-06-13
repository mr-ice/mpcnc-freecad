# TrueTiles Water Tile

Python scripts that generate a small 3D-printable "water"-themed tile in
FreeCAD: a 30.75mm square base with a parabolic wave profile cut into the top
surface. Output is saved as `30.75mm_square_with_wave_top_surface.FCStd`.

## Files
- `water1.py` — empty placeholder.
- `water2.py` — builds the square base, defines a parabolic wave wire, extrudes and cuts it from the base, saves the FCStd.
- `water3.py` — variant of `water2.py` using an open polygon wire and an explicit `Base.Vector` extrusion direction.

## Usage
Run `water2.py` (or `water3.py`) inside FreeCAD 1.0.2 (FreeCAD Python console or
as a macro). Each creates a new document, builds the tile, recomputes, and saves
`30.75mm_square_with_wave_top_surface.FCStd`. Export to STL/3MF to print.
