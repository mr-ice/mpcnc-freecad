# Wispwood Tile Holder (custom)

A two-stack tile rack for **Wispwood**, derived from the community
*wispwood-tile-holder* by **gepesso** (reference STLs in `gepesso/`), redesigned with a
**two-part sliding/dispensing lid** and an **integrated folding stand**.

General FreeCAD coding rules live in the repository-root `CLAUDE.md`; this file captures
the design intent for this project.

## Source model (reverse-engineered from the reference STLs)

Measured from `gepesso/wispwood-tile-holder/*.stl` (binary STL bounding boxes + wall planes):

- **Outer tray:** 86 (X) × 182 (Y) × 42 (Z) mm.
- **Walls:** long sides **4 mm**, end walls **2 mm**, floor **~3 mm**, centre divider **2 mm**.
- **Two pockets:** **38.0 mm** wide × **~177 mm** long × **~39 mm** deep, split by the divider.
- **Lid:** ~80.5 × 180 × **2 mm**, slide-in.
- Original has finger scoops cut into the long walls.

## Tiles

- **160 square tiles** total, **80 per pocket** (two side-by-side stacks).
- **35 × 35 mm square, 2.133 mm thick** (measured). A stack of 80 is **~170.6 mm**.
- Fit **comfortably / low-friction** in the **38 mm** pocket (1.5 mm/side clearance),
  with ~8 mm of slack along the stack length.

## New design

### Tray
- Two side-by-side pockets, 80 tiles each, comfortable low-friction fit on the tile
  width and free sliding along the stack length.
- **Two equal-height end walls** (`END_WALL_HEIGHT`), front and back, both rising to the
  lid underside (full pocket depth) so the lid can slide out **either end**.
- Full-length lid rails, **beveled** (45° lip underside) so the tray prints without
  support; **rail friction** holds the lid in place during play and storage.

### Two-part sliding / dispensing lid
- A **flat** plate (no walls closing off the columns), split into **two parts** that
  share the rails and have **beveled top sliding edges** for clean printing/entry:
  - **Large part (game use):** covers the front through **~tile 65**.
  - **Small part (storage):** seals the remaining **~65 → 80** region.
- During play, sliding the large lid **back** by one tile (`DISPENSE_GAP`) opens a gap at
  the **top-front**. With the rack tilted/suspended, the front tile **slides up and out
  through that gap, over the front wall, into the operator's hand**.
- **Single-source fit:** the lid cross-section is defined once; the tray's lid slot is the
  *same* section grown by `LID_SLIDE_CLEARANCE` and cut from the tray, so the fit is exact
  and edited in one place. The slot cutter is emitted as a hidden `LidSlotCutter` object
  for inspection. The chamfer spans the full groove depth (45°) so the tray's retaining
  lip prints without support.
- **Friction tuning:** the printed lid slid well but did not stay put, so the **lid only**
  is widened in X by `LID_WIDTH_FRICTION` (0.4 mm total, 0.2 mm/side) — the slot is left
  unchanged, dropping the side clearance from 0.3 → 0.1 mm/side for a tighter friction grip
  while keeping the (good) vertical fit. Tune `LID_WIDTH_FRICTION` against the next print.

### Finger scoops
- On **both short ends** (front and back walls), one per pocket, **~80% of the pocket
  depth** (`SCOOP_DEPTH_FRACTION`) for easy tile access from either end.
- **Not on the long sides** — that area is reserved for the folding stand.

### Folding stand
- Two **legs** (each **half the tray length**) with **rounded free ends**, centred
  vertically on the box, joined by a **front base panel** made **a little wider than the
  box front so it covers the legs**, with **chamfered gussets** at the leg/base junctions.
- Each leg carries a **substantial oval peg** (`STAND_PEG_LENGTH`×`STAND_PEG_WIDTH`) at the
  **back of the leg, equal top/bottom/back margins**, riding a slot in the wall's outer
  face (blind — does not breach the pocket).
- Slot path (hinge toward the **front**, constant-width channels, **no keyhole**):
  - **parallel arm** — horizontal, the folded peg rest, length `STAND_SLOT_ARM_LEN`;
  - **jog** — a short vertical lift of `STAND_JOG_FRAC` × peg width (≈50%) at the vertex;
  - **top arm** — short tilted lock arm, `STAND_ARM2_FRAC` × peg length (≈150%), at
    `STAND_V_ANGLE_DEG`. The jog + short arm form the lock detent.
- Slot position **derived from the leg** (margins stay equal). Modelled **folded** —
  kinematics still to be tuned against a print.
- **Anti-fuse gap:** each leg's inner face is offset from the tray's outer wall by
  `STAND_BODY_GAP` (0.2 mm) so the folded-modelled legs do not print fused to the tray
  body; the oval pegs are lengthened to bridge the gap and still seat fully in the slot.

### Finger-scoop chamfers
- The scoops' **outer-face and top edges** are chamfered (`SCOOP_CHAMFER`) for finger
  comfort. Applied by geometric edge selection (best-effort) — verify in FreeCAD.

## Decisions

- Tiles **35 × 35 × 2.133 mm** (measured); pocket **38 mm** wide (1.5 mm/side clearance).
- Dispense at the **front** short end: lid slides back, the front tile slides up and out
  through the **top-front gap** (over the tall front wall) into the operator's hand, with
  the tray tilted/suspended.
- Folding stand uses **oval pegs riding V-slots** in the long side walls (not a pin
  hinge): down → swing → up to lock.
- Lid split at **tile 65**.

## Assumptions (to confirm by printing)

- Stand deployed tilt angle **~15°**; suspension height ≈ one-tile drop clearance.
- Dispensing clearances: `DISPENSE_GAP`, `LID_SLIDE_CLEARANCE`, `GATE_FLOOR_GAP`,
  `STAND_HINGE_CLEARANCE` — empirical, tune after a test print.

## Print-tuning log

- **Print 1:** lid slid freely but would not hold position; legs printed fused to the tray
  body. **Fixes:** `LID_WIDTH_FRICTION = 0.4` (tighter lid friction, slot unchanged) and
  `STAND_BODY_GAP = 0.2` (leg-to-wall clearance). Re-print to confirm both.

## Build status

- [x] Reverse-engineer reference dimensions
- [x] `PROJECT.md` spec + `config.py` parameters
- [x] Core parametric tray (pockets, walls, divider, lid rails) — `.FCMacro` + Python
- [x] Two-part sliding/dispensing lid + short-end finger scoops
- [x] Folding stand: V-slot + oval-peg legs + base bar (folded; kinematics need tuning)
- [x] Print 1 fit fixes: lid friction width + leg anti-fuse gap (config-driven)
- [ ] Re-print to confirm lid holds position and legs separate cleanly
