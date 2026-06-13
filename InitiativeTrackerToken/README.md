# Initiative Tracker Token

A round tabletop-game initiative token generated with FreeCAD. The Python
script builds a 50 mm diameter, 3 mm thick cylinder with filleted top/bottom
edges and extruded "GO" text, producing a 3D-printable STL.

## Files
- `initiativeToken.py` — defines `create_token()` (filleted cylinder) and `create_text()` (extruded "GO" text)
- `init.FCMacro` — FreeCAD macro that reloads the module and rebuilds the `initiativeToken` document
- `initiativeToken-InitiativeToken.stl` — exported token mesh
- `__pycache__/` — compiled Python cache

## Usage
Open `init.FCMacro` in FreeCAD 1.0.2 and run it. It creates a fresh
`initiativeToken` document, reloads `initiativeToken.py`, and builds the token
and "GO" text. Edit the `radius`, `height`, and font size in
`initiativeToken.py` to adjust dimensions.
