"""Configuration constants for the Wispwood tile holder (custom design).

All dimensions are in millimetres and all angles in degrees unless noted. Values
reverse-engineered from the reference model in ``gepesso/`` are tagged ``SOURCE``;
values that are design assumptions pending confirmation are tagged ``ASSUMED``.

The public API of this module is the set of module-level constants below; downstream
modeling code imports them and must not hard-code measured coordinates (see the
repository ``CLAUDE.md``: always calculate offsets).
"""

# --- Tiles -------------------------------------------------------------------
TILE_COUNT_TOTAL = 160  # tiles in the game
STACKS = 2  # two side-by-side pockets
TILES_PER_STACK = TILE_COUNT_TOTAL // STACKS  # 80
TILE_SIZE = 35.0  # MEASURED square tile edge length
TILE_THICKNESS = 2.133  # MEASURED single-tile thickness

# --- Fit / clearances --------------------------------------------------------
TILE_SIDE_CLEARANCE = 1.5  # per side on tile width: keeps the 38 mm comfortable fit
STACK_LENGTH_SLACK = 8.0  # extra length so a full 80-tile stack slides freely
TILE_DEPTH_CLEARANCE = 1.0  # extra pocket depth above the tile height

# --- Pockets (derived) -------------------------------------------------------
POCKET_WIDTH = TILE_SIZE + 2 * TILE_SIDE_CLEARANCE  # -> 38.0 (matches SOURCE)
POCKET_LENGTH = (
    TILES_PER_STACK * TILE_THICKNESS + STACK_LENGTH_SLACK
)  # ASSUMED tile_thk
POCKET_DEPTH = TILE_SIZE + TILE_DEPTH_CLEARANCE  # ~37; SOURCE interior depth ~39

# --- Walls / structure -------------------------------------------------------
WALL_LONG = 4.0  # SOURCE: long-side outer walls
WALL_END = 2.0  # SOURCE: end walls
FLOOR_THICKNESS = 3.0  # SOURCE
DIVIDER_THICKNESS = 2.0  # SOURCE: centre divider between the two pockets

# --- Lid ---------------------------------------------------------------------
LID_THICKNESS = 2.0  # SOURCE
LID_SPLIT_TILE = (
    65  # large lid covers tiles 1..LID_SPLIT_TILE; small lid covers the rest
)
DISPENSE_GAP = TILE_THICKNESS + 0.6  # how far the lid slides back to release one tile
RAIL_DEPTH = 1.5  # how far the lid edge sits into the side rail groove
# The lid cross-section is defined once (in wispwood.py); the tray slot is that same
# section grown by LID_SLIDE_CLEARANCE and cut from the tray, so the fit is exact and
# defined in one place. LID_BEVEL spans the full groove depth (45 deg), making the tray's
# retaining lip a clean 45 deg overhang that prints without support. The lid's outer tip
# is then LID_THICKNESS - LID_BEVEL thick (~0.5 mm) -- raise LID_THICKNESS if too fragile.
LID_BEVEL = (
    RAIL_DEPTH  # 45 deg chamfer on the lid's top sliding edges (== groove depth)
)
LID_SLIDE_CLEARANCE = (
    0.3  # tolerance grown around the lid to cut the tray slot (the fit)
)
LID_TOP_LIP = 1.0  # wall lip above the lid that retains it from lifting

# End walls (front and back) are identical: both rise to the lid underside (full pocket
# depth) so the flat lid can slide out either end and is held only by rail friction.
# Going higher would block the lid from sliding over them.
END_WALL_HEIGHT = POCKET_DEPTH  # top flush with the lid underside (~36 mm)

# --- Finger scoops (both end walls, one per pocket) -------------------------
SCOOP_WIDTH = 24.0  # ASSUMED: width of the thumb scoop (pocket is POCKET_WIDTH wide)
SCOOP_DEPTH_FRACTION = 0.8  # scoop reaches ~80% of the pocket depth from the top down
SCOOP_CHAMFER = 1.0  # chamfer on the scoop's outer-face and top edges (finger comfort)

# --- Folding stand -----------------------------------------------------------
# Two legs (rounded free ends) joined by a front base panel a little wider than the box
# front so it covers the legs; the leg/base junction is chamfered. Each leg carries a
# substantial oval peg that rides a complex slot in the tray's outer side wall. Modelled
# FOLDED; the path/lock still need tuning vs a print.
STAND_THICKNESS = 3.0  # leg and base-panel thickness
STAND_LEG_LENGTH_FRAC = 0.5  # legs span half the tray length
STAND_LEG_WIDTH = 16.0  # leg width (Z extent), centred on the peg
STAND_BASE_DEPTH = 8.0  # base-panel thickness along Y (the foot)
STAND_CHAMFER = 5.0  # chamfer/gusset at the leg-to-base junction

# Oval / bar peg on each leg (rides the slot) -- substantial, centred on the leg:
STAND_PEG_LENGTH = 10.0  # oval major axis, along the leg
STAND_PEG_WIDTH = 5.0  # oval minor axis (sets the slot channel width)
STAND_PEG_DEPTH = 2.5  # how far the peg projects into the wall slot (< WALL_LONG)
STAND_SLOT_CLEARANCE = 0.4  # slot-vs-peg running clearance

# Slot path in the outer wall face, DERIVED from the leg so the oval sits at the back of
# the leg with equal margins. The hinge is toward the FRONT. Path: along the horizontal
# "parallel" arm to its end, a short vertical jog up (so the peg lifts before locking),
# then a short tilted "top" arm to the lock. This jog+short-arm is the lock detent.
STAND_SLOT_ARM_LEN = 24.0  # length of the horizontal (parallel) arm
STAND_V_ANGLE_DEG = 20.0  # tilt of the top arm above horizontal
STAND_JOG_FRAC = 0.5  # vertical jog at the vertex = this * peg width (the lift)
STAND_ARM2_FRAC = (
    1.5  # top (lock) arm length = this * peg length (significantly shorter)
)

# --- Tolerances / print ------------------------------------------------------
GENERAL_CLEARANCE = 0.2  # default fit clearance for mating printed parts
MAX_PRINTER_DIMENSION = 256.0  # ASSUMED build-plate limit; keep parts within this
