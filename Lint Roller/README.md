# Lint Roller

A model of a lint-roller roll, sized to a measured roller (8 mm pin diameter,
53.75 mm roll diameter, 102 mm roll length). Currently the OpenSCAD model draws
only the roll cylinder.

## Files
- `handle.scad` — OpenSCAD source. Defines `pin_radius`, `roll_radius`, and `roll_length`, and renders the roll as a cylinder.
- `handle.py` — notes file recording the measured dimensions (107 mm, 8.5 mm, 55 mm) as comments.

## Usage
Open `handle.scad` in OpenSCAD, adjust the radius/length parameters as needed,
and render/export to STL for printing.
