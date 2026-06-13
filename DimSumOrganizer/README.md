# DimSumOrganizer

A 3D-printable insert that sits inside a bamboo steamer ("dim sum") basket and holds vertical stacks of circular and oval game tokens, with a lid the tokens protrude through. See [PROJECT.md](PROJECT.md) for the full design spec and parameters.

## Files
- `DimSumOrganizer.FCMacro` — FreeCAD macro: reloads `config` and `create_insert`, rebuilds the `DimSumOrganizer` document via `create_insert.create_insert()`.
- `create_insert.py` — geometry for the main organizer insert.
- `BasketInsert.FCMacro` — alternate macro that builds the basket-insert variant via `create_basket_insert`.
- `create_basket_insert.py` — geometry for the basket-insert variant.
- `DimSumOrganizer-Insert.stl` / `.3mf` — exported insert meshes.
- `BasketInsert-Insert*.stl` — exported basket-insert meshes (v2, v3 base, v3 lid).
