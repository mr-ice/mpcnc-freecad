# Pickleball Scoreboard

A 3D-printable pickleball scoreboard, modeled in FreeCAD 1.0.2. It produces a
frame (with a body fillet) and a separate back, exported as STL/3MF for printing.

## Files
- `Frame.FCStd` — FreeCAD model of the scoreboard frame.
- `Frame.FCStd1` — FreeCAD backup of the frame document.
- `Back.FCStd` — FreeCAD model of the scoreboard back panel.
- `Frame-BodyFillet001.stl` / `Frame-BodyFillet001.3mf` — printable frame body (filleted) export.
- `Frame-FrameFillet001.stl` — printable frame export (frame fillet variant).

## Usage
Open the `.FCStd` files in FreeCAD 1.0.2 to edit the model. Print the exported
`Frame-*.stl` / `.3mf` files. No build scripts or macros are present.
