# Robo Rally 30th Anniversary Insert

A parametric 3D-printable insert for the Robo Rally 30th Anniversary edition. The design is split across several FreeCAD documents covering the main big-box tray, card-deck holders, maps/boards, per-player kits, and assorted small parts. Dimensions are driven by a shared `Config` class in `BigBox.py`.

## Files
- `BigBox.py` — Python script that builds the main tray: a wedge-shaped outer box with filleted card slots, an upgrade/damage card slot, reboot-token slots, flag cubbies, a priority-token cutout, and a misc compartment. All sizes come from the `Config` class. Run inside FreeCAD to build the `BigBox` document.
- `BigBox.FCStd` / `.FCStd1` — FreeCAD document for the big-box tray.
- `BigBox-BoxVolume.stl` — Exported tray mesh; `BigBox-BoxVolume_*.bgcode` is a sliced Prusa job for it.
- `CardDecks.FCStd` (`.FCBak` backup) — Card-deck holder(s).
- `Maps.FCStd` — Map/board storage tray.
- `PlayerKit.FCStd` — Per-player component holder.
- `Extras.FCStd` — Additional/optional insert parts.
- `MiscParts.FCStd` — Miscellaneous small parts.
- `Config.FCStd` — Shared configuration/parameters document.

## Usage
Open the relevant `.FCStd` in FreeCAD 1.0.2 and recompute. For the main tray, open/run `BigBox.py` (creates the `BigBox` document) and export the resulting `Box` solid to STL for slicing.
