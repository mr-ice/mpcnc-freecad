# Water Terrain

Procedurally generated 3D-printable water terrain tiles. Each tile is a base plate topped with a rippled NURBS water surface (sine/cosine waves plus a random component), then scored with rounded channel cuts along the grid lines so the surface reads as separate squares. Tile dimensions are driven by `config.square_size` from the repo's shared config.

## Files
- `terrain_generator.py` — Core module. `create_water_tile(width_squares, length_squares, thickness_mm, wave_amplitude)` builds a tile; `create_channel_cutter(...)` makes the rounded edge-channel tool. Produces a `WaterTerrain` solid in a new FreeCAD document.
- `water_terrain_macro.FCMacro` — Driver macro. Reloads `terrain_generator` and loops over sizes `(1,1), (1,2), (2,2), (3,3), (1,3)`, generating 20 random variants each (`wave_amplitude=0.8`) and exporting STLs.
- `*v2-NN-WaterTerrain.stl` — Generated tiles, named `<W>x<L>v2-<NN>-WaterTerrain.stl` (e.g. `1x1v2-01`, `2x2v2-15`, `3x3v2-20`); 20 numbered variants per size.
- `WaterTerrainXL*.3mf`, `2x 2x2 WaterTerrainXL.3mf` — Pre-arranged/sliced 3MF plates of larger tiles for printing.

## Usage
Open `water_terrain_macro.FCMacro` in FreeCAD 1.0.2 and run it to (re)generate the tile set and export STLs to this folder. Edit the size list, `wave_amplitude`, or variant count in the macro to change output. Each run reseeds randomness, so geometry varies.
