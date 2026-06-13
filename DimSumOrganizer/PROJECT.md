# DimSumOrganizer

A 3D-printable **insert that sits inside a bamboo steamer ("dim sum") basket** and holds
stacks of game tokens. General FreeCAD coding rules live in the repository-root
`CLAUDE.md`; this file captures the design intent for this project.

The insert holds **circular** and **oval** tokens in vertical stacks, with a lid through
which the tokens protrude slightly so they can be picked out. See `create_insert.py` /
`create_basket_insert.py` for the geometry and `DimSumOrganizer.FCMacro` to build it.

## Current design parameters

Defined in `config.py` (millimeters):

- **Circle tokens:** diameter `40.7` (0.5 mm tolerance), pocket height `6.2 + 3` (2 mm extra space)
- **Oval tokens:** length `39`, width `31`, pocket height `12.2 + 3` (2 mm extra space)
- **Container cylinder:** diameter `63.0`, height `13.0`
- **Stacks:** `2` oval stacks, `1` circle stack
- **Basket:** diameter `68.0`, separation `74.5`, height `26.0`
- **Lid:** thickness `3.0`, token protrusion above the lid surface `1.0`

The insert must fit within the basket diameter; token pockets include the extra space /
tolerance noted above so tokens seat and release cleanly.
