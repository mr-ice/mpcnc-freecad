# Utilities

Shared FreeCAD helper macros and scripts reused across projects in this repo. These are general-purpose building blocks rather than a single printable model.

## Files
- `mountkeyhole.py` — Python module that builds a keyhole-style wall-mount cutout (screw-head cylinder, shaft slot, end cylinder, and a filleted backing T-slot) via `create_keyhole(...)`. When run inside FreeCAD it adds a `Keyhole` `Part::Feature` to the active document.
- `loadkeyhole.FCMacro` — FreeCAD macro that closes/recreates the `mountkeyhole` document, imports and `reload`s `mountkeyhole`, then sets a top view and fits the view. (Paths reference `/Users/michael/3dp/WallHangers/`; adjust the `os.chdir` if running elsewhere.)

## Usage
Open `loadkeyhole.FCMacro` in FreeCAD 1.0.2 and run it to (re)build the keyhole geometry from `mountkeyhole.py`. The `create_keyhole()` parameters (head diameter/height, shaft diameter, backing plate height, corner radius) can be edited to tune the mount.
