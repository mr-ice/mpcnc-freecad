# BookBindingTemplates

Python-driven FreeCAD models that generate thin, rigid 3D-printable bookbinding templates at several configurable book sizes (used to mark out the front/back covers, spine, and corner wrap). See [PROJECT.md](PROJECT.md) for the full design spec and parameters.

## Files
- `BookBindingTemplates.FCMacro` — FreeCAD macro: reloads `sizes`, `config`, and `template`, rebuilds the `Templates` document, and calls `template.main()`.
- `template.py` — geometry generation for the templates.
- `sizes.py` — list of book sizes (x, y, spine) in inches.
- `Diagram.jpeg` — reference layout for the template.
- `Template*.stl` — exported template meshes (e.g. `Template5.5x8.5x1.5.stl`).
- `FirstThreeSizes.3mf` — exported 3MF of the first three sizes.
