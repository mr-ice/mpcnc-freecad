# ToolOrganizer

Parametric 3D-printable drawer bin inserts (with optional bow-tie locking clips), plus a separate voltmeter-hole organizer variant. See [PROJECT.md](PROJECT.md) for the full design spec and parameters.

## Files
- `ToolOrganizer.FCMacro` — FreeCAD macro: reloads the modules, builds the voltmeter hole, then the organizer (subtracting the hole), into the `ToolOrganizer` document.
- `tool_organizer.py` — main organizer bin geometry (`build_model`).
- `config.py` — organizer dimensions and tolerances.
- `voltmeter.py` / `voltmeter_config.py` — voltmeter cutout geometry and its config.
- `Voltmeter.FCMacro` — macro to build the voltmeter model on its own.
- `txhh_organizer.py` / `configtxhh.py` / `TXHHOrganizer.FCMacro` — a TXHH organizer variant and its config/macro.
- `Organizer.stl`, `1stRevOrganizer.3mf` — exported meshes.
