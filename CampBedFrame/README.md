# Camp Bed Frame

3D-printable feet for a camp bed frame. The main part is a hollow,
quarter-cylinder corner foot: a filleted base plus a curved leg wall with
embedded grip cylinders for friction. The foot is built parametrically with
FreeCAD's `Part` API in Python.

## Files
- `feet.py` — main generator; builds the corner foot (base + hollow leg + grip cylinders) as FreeCAD `Part::Feature` objects. Parameters (radii, thicknesses, wall thickness) are constants at the top.
- `load_feet_macro.FCMacro` — FreeCAD macro that `cd`s into this dir and (re)loads `feet.py`.
- `test_chevron.py` — standalone test that builds a single chevron rib profile.
- `Unnamed.FCStd` — FreeCAD document (binary).
- `Unnamed-foot.stl` — printable foot output.
- `Dice Tower-BottomSection.stl`, `Dice Tower-TopSection.stl` — unrelated dice-tower STLs that also live in this directory.

## Usage
Open `load_feet_macro.FCMacro` in FreeCAD 1.0.2 and run it to load/reload
`feet.py`, which builds the foot in a new document. Adjust the parameter
constants at the top of `feet.py` to resize. Note: the macro hard-codes this
directory path.
