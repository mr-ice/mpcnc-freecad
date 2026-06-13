# QuickPump Adapter

A parametric, 3D-printable adapter ("Adapter1") generated in FreeCAD 1.0.2 by
Python. The part is a stacked, tapered tubular adapter made of five sections
(base, first ridge, middle, second ridge, top), with two filleted ridges and a
pair of mirrored L-shaped bayonet slots cut into the base.

## Files
- `parameters.py` — all dimensions (mm): section heights, ODs/IDs, ridge fillets, slot geometry.
- `Adapter1.py` — builds the adapter from `parameters.py` via the FreeCAD `Part` API (tapered sections, fillets, swept slots).
- `LoadAdapter1.FCMacro` — reloads `parameters`/`Adapter1`, rebuilds a fresh `Adapter1` document, and fits the view.
- `__pycache__/` — compiled Python cache.

## Usage
Open `LoadAdapter1.FCMacro` in FreeCAD 1.0.2 and run it. It closes/recreates the
`Adapter1` document and regenerates the model. Adjust dimensions in
`parameters.py` and re-run the macro. Export the resulting `Adapter1` solid to
STL/3MF for printing.
