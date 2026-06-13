# LFG Sign

A three-panel folding sign generated in FreeCAD. Each panel is a chamfered
truncated-pyramid (trapezoid) plate, and adjacent panels are joined by
interlocking printed pin hinges (alternating positive/negative) so the assembly
can fold. Produces 3D-printable STL/3MF output.

## Files
- `LFG.FCMacro` — FreeCAD macro: resets the `LFG1` document, reloads `lfg`, and calls `create_sign()`.
- `lfg.py` — geometry module; builds the trapezoid panels, hinges, and the three-panel layout. Dimensions (widths, height, thickness, hinge sizing) are constants at the top of the file.
- `LFG1.stl` — exported full sign mesh.
- `LFG1.3mf` — exported full sign in 3MF.
- `LFG1-SignSide.stl` — exported single sign side/panel mesh.

## Usage
Open `LFG.FCMacro` in FreeCAD 1.0.2 and run it. The macro rebuilds the `LFG1`
document from `lfg.py`. Adjust the configuration constants (`BASE_WIDTH`,
`TOP_WIDTH`, `HEIGHT`, `THICKNESS`, and the `HINGE_*` values) in `lfg.py`, then
re-run the macro. Export the resulting solids to STL/3MF for printing.
