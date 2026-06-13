# MPCNC Parts

A collection of 3D-printable parts for an MPCNC (Mostly Printed CNC) machine,
authored/edited in FreeCAD 1.0.2. Most parts include a `.FCStd` source, a
printable `.stl` (some also `.3mf`), and a couple of pre-sliced `.gcode` files.
This is a parts library rather than a single model; the notable groups:

## Files
- **Z endstop assembly** (~37 endstop-related files) — the bulk of the collection: switch actuators, adjust block, connector, corner, upright, vertical frame/holder, endstop bars, and X/Y/Z/YZ endstop bodies (e.g. `X Endstop`, `Y Endstop`, `Z Endstop`, `Z ENDSTOP SWITCH ACTUATOR`, `Z Endstop Adjust Block`, `YZ Endstop`).
- **Belt mounting** — `Belt Mounting Bracket` (plus mirrored variant) and `belt_grip_top`/`belt_grip_bottom v1.3mf` belt grips.
- **Pen holder** — `New PenHolder Upright Base`, `New PenHolder Friction Ring`, `New PenHolderCaddy`, `PenHolderAdapter` for a pen/plotter tool.
- **Slider** — `Unnamed2-SliderAssembly.stl`.
- Pre-sliced gcode — `Z ENDSTOP SWITCH ACTUATOR_*.gcode` (PETG, Prusa MK3S/MMU2S).

## Usage
Open any `.FCStd` in FreeCAD 1.0.2 to edit a part. Print the matching `.stl` /
`.3mf` files; the `.gcode` files are pre-sliced for a Prusa MK3S. No build
scripts or macros are present.
