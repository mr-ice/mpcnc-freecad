# Photosynthesis Dividers

Card/component dividers for the board game *Photosynthesis*, modeled in FreeCAD.
The box-with-chamfered-cutout geometry is driven by a spreadsheet of dimensions
plus a helper script that computes matching inner/outer chamfer lengths. Produces
3D-printable STL output.

## Files
- `ChamferCalc.py` — FreeCAD macro/script: reads thickness and chamfer-height from the document `Spreadsheet`, computes outer and inner chamfer lengths, applies two `Part::Chamfer` features (box and hole), and cuts the hole from the box.
- `Photosynthesis Dividers.FCStd` — main FreeCAD document.
- `Photosynthesis Dividers.FCStd1` — backup of the previous save of the main document.
- `Photosynthesis Dividers v1.FCStd` — version 1 document.
- `Photosynthesis Dividers v2.FCStd` — version 2 document.
- `Photosynthesis Dividers v1.stl` — exported mesh, version 1.
- `Photosynthesis Dividers-Fusion002.stl` — exported mesh of a fused/cut result.
- `.idea/` — IDE project metadata.

## Usage
Open a `.FCStd` document in FreeCAD 1.0.2, set the dimensions in the embedded
`Spreadsheet`, then run `ChamferCalc.py` to apply the chamfers and cut. Export
the resulting solid to STL for printing.
