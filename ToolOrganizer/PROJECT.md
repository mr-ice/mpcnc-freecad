# ToolOrganizer — Drawer Bin Inserts

Organizer bin inserts for several drawers. General FreeCAD coding rules live in the
repository-root `CLAUDE.md`; this file captures the design intent for this project.

## Drawer

- Drawer interior: **12" depth × 8 7/8" width × 2 1/2" height**.
- Tolerances: ~**1 mm** of clearance around the outside of the bins (against the drawer),
  and **0.2 mm** between adjacent bins.

## Bins

- **Rounded corners:** vertical corners use a **9 mm** radius; horizontal corners use a
  **3 mm** radius.
- **Label surface:** each bin has a mostly-horizontal surface for a label, minimum
  **6 mm × 40 mm**. *(The original spec sentence was truncated here — confirm the intended
  maximum / placement before relying on it.)*
- **Walls:** **1.5 mm** minimum, but increase as needed so other features work.
- **Height:** configurable; start with **1.75 in**.

### Bin layout

| Bin | Width      | Depth     |
|-----|------------|-----------|
| 1   | full width | 1/4 depth |
| 2   | 1/3 width  | 3/4 depth |
| 3   | 1/3 width  | full depth|
| 4   | 2/3 width  | 1/2 depth |

## Locking

- Optional **locking clips** hold adjacent bins together.
- Locking **slots and clips** are placed on all bins to lock to their neighbors.
- Slots are accessible from the **bottom only**.
- Clips lock two adjacent bins together in a **bow-tie** shape.
