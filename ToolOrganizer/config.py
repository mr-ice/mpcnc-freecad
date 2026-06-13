"""
Configuration file for Tool Organizer FreeCAD model
Contains all dimensions, wall thicknesses, and compartment layout
"""

# Base dimensions (mm)
# X (width): 297mm, Y (depth): 25mm, Z (height): 130mm
BASE_LENGTH = 297.0  # X dimension (width)
BASE_WIDTH = 25.0    # Y dimension (depth)
BASE_HEIGHT = 130.0 - 25.0  # Z dimension (height) (leave a bit at the top)

# Wall thicknesses (mm)
OUTER_WALL_THICKNESS = 1.6
INNER_WALL_THICKNESS = 0.8

# Fillet radius for outside corners (mm)
CORNER_FILLET_RADIUS = 2.0

# Internal dimensions (calculated)
# Internal dimensions after accounting for outer walls
INTERNAL_LENGTH = BASE_LENGTH - (2 * OUTER_WALL_THICKNESS)  # X
INTERNAL_WIDTH = BASE_WIDTH - (2 * OUTER_WALL_THICKNESS)    # Y
# Z dimension (bottom wall thickness)
INTERNAL_HEIGHT = BASE_HEIGHT - OUTER_WALL_THICKNESS

# Compartment layout configuration
# Each compartment is defined by: {x, y, width, depth}
# - x, y: position relative to internal front-bottom corner
#   (accounting for outer wall thickness)
# - width: size in X dimension (along the 297mm width)
# - depth: size in Y dimension (along the 25mm depth)
#   typically spans full depth
# All compartments extend downward in Z (toward bottom)
# They open to the top
# All dimensions in mm
COMPARTMENTS = [
    # Small compartments for screwdrivers and utility knives
    # the shortest are first, as they are over the voltmeter.
    [
        ["screwdriver", "screwdriver"], 12
    ],
    [
        ["utility knife", "utility knife"], 12
    ],
    [
        ["pliers", "pliers"], 30
    ],
    [
        ["scissors", "scissors"], 25
    ],
    ["large", 40],
    ["small", 10],
    ["large", 40],
    ["small", 10],
    ["large", 40],
    ["large", 40],
    ["medium", 26.8],
    ]

# Calculate remaining length for more compartments
# Total used: sum of widths + walls between slots
_used_length = sum(
    slot[1] for slot in COMPARTMENTS
) + (len(COMPARTMENTS) - 1) * INNER_WALL_THICKNESS
_REMAINING_LENGTH = INTERNAL_LENGTH - _used_length
# Remaining length available for more compartments: 114.0mm
print(f"Remaining length available for more compartments: {_REMAINING_LENGTH}mm")
