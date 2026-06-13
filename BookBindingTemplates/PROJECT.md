# BookBindingTemplates

Python-driven FreeCAD models that generate 3D-printable **bookbinding templates** at
several configurable sizes. General FreeCAD coding rules live in the repository-root
`CLAUDE.md`; this file captures the design intent for this project.

The templates are thin, rigid plates used to mark out the front/back covers, spine, and
corner wrap when binding a book. See `Diagram.jpeg` for the layout, `sizes.py` for the
set of book sizes, and `template.py` for the geometry.

## Current design parameters

Defined in `config.py` (millimeters unless noted):

- **Triangle margin** (between front/back and the corners): `triangle = 3`
- **Gap** (between the ends and the spine): `gap = 6`
- **Margin** (wrap-around area along the outside): `margin = 20`
- **Thickness** (of the printed plate — rigid but not too thick): `thickness = 3`
- **Label:** `font_size = "15 mm"`, `label_x_offset = 15` (from the left edge of the inner plates)
- **Pin/hole registration:** `pin_radius = 5.0`, `slot_width = 5.0`, `slot_length = 9.0`,
  `pin_hole_tolerance = 0.2`
- **Printer limit:** `max_printer_dimension = 345`

Sizes are expressed in inches and converted with `inch_to_mm()`; designs must stay within
`max_printer_dimension`.
