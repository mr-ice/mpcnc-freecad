"""
Configuration for THXX drawer bin inserts (FreeCAD).
Constants from THXXPROJECT.md; used by project Python modules.
"""

# Unit conversion
IN_TO_MM = 25.4

# Drawer dimensions (inches from THXXPROJECT.md)
DRAWER_DEPTH_IN = 12.0
DRAWER_WIDTH_IN = 8.0 + 7.0 / 8.0
DRAWER_HEIGHT_IN = 2.0 + 1.0 / 2.0

# Drawer dimensions (mm), calculated
DRAWER_DEPTH_MM = DRAWER_DEPTH_IN * IN_TO_MM
DRAWER_WIDTH_MM = DRAWER_WIDTH_IN * IN_TO_MM
DRAWER_HEIGHT_MM = DRAWER_HEIGHT_IN * IN_TO_MM

# Tolerance (mm)
OUTSIDE_TOLERANCE_MM = 1.0  # around the outside
BETWEEN_BIN_TOLERANCE_MM = 0.2  # between bins

# Insert envelope (after outside tolerance), calculated
INSERT_DEPTH_MM = DRAWER_DEPTH_MM - (2 * OUTSIDE_TOLERANCE_MM)
INSERT_WIDTH_MM = DRAWER_WIDTH_MM - (2 * OUTSIDE_TOLERANCE_MM)
INSERT_HEIGHT_MM = DRAWER_HEIGHT_MM - (2 * OUTSIDE_TOLERANCE_MM)

# Corner radii (mm)
CORNER_RADIUS_VERTICAL_MM = 9.0
CORNER_RADIUS_HORIZONTAL_MM = 3.0

# Label surface minimum (mm)
LABEL_MIN_WIDTH_MM = 6.0
LABEL_MIN_LENGTH_MM = 40.0

# Walls (mm)
WALL_MIN_MM = 1.5

# Max fillet radius is limited by wall thickness (BRep fails if radius > adjacent material).
# Fillets are capped to WALL_MIN_MM * FILLET_MAX_FRAC_OF_WALL.
FILLET_MAX_FRAC_OF_WALL = 0.99

# Bin height (configurable; inches, then converted)
BIN_HEIGHT_IN = 1.75
BIN_HEIGHT_MM = BIN_HEIGHT_IN * IN_TO_MM

# Bin layout fractions (of insert width/depth/height)
# Bin 1: full width, 1/4 depth
BIN1_WIDTH_FRAC = 1.0
BIN1_DEPTH_FRAC = 1.0 / 4.0

# Bin 2: 1/3 width, 3/4 depth
BIN2_WIDTH_FRAC = 1.0 / 3.0
BIN2_DEPTH_FRAC = 3.0 / 4.0

# Bin 3: 1/3 width, full depth
BIN3_WIDTH_FRAC = 1.0 / 3.0
BIN3_DEPTH_FRAC = 1.0

# Bin 4: 2/3 width, full height, 1/2 depth
BIN4_WIDTH_FRAC = 2.0 / 3.0
BIN4_DEPTH_FRAC = 1.0 / 2.0

# Bottom connectors (bowtie): on interior grid edges where bins meet (1/3 × 1/4)
CONNECTOR_GRID_COLS = 3  # 1/3 width -> interior x at 1/3, 2/3
CONNECTOR_GRID_ROWS = 4  # 1/4 depth -> interior y at 1/4, 1/2, 3/4
# Bowtie = two trapezoids joined at short edge. Length along connector axis.
BOWTIE_LENGTH_MM = 8.0
BOWTIE_WIDTH_MM = 6.0  # full width at the two ends
BOWTIE_NARROW_FRAC = 0.3  # narrow width at center = BOWTIE_WIDTH_MM * this
# Hole in bin floor is bowtie outline expanded by this (mm) so connector fits
CONNECTOR_HOLE_TOLERANCE_MM = 0.2
