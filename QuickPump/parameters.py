import math

# Parameters for Adapter1 (all dimensions in mm)

# This is a stack of 5 parts, the base, the first ridge, the middle, the second ridge, and the top.

# Base cylinder parameters
BASE_HEIGHT = 13.0
BASE_ID = 24.0
BASE_OD = 29.6

# Middle cylinder parameters
RIDGE_HEIGHT = 2.0
FIRST_RIDGE_ID = 21.0
FIRST_RIDGE_OD = 31.6

# Middle cylinder parameters
MID_HEIGHT = 15.0  # Adjust as needed
MID_OD = 25.2
MID_ID = 18.0
MID_WALL_BOTTOM = 2.0
MID_WALL_TOP = 1.2

# Second ridge parameters
SECOND_RIDGE_OD = 24.3
SECOND_RIDGE_ID = 18.9

# Both ridges have an outside fillet radius of ridge_height / 2 - 0.01
RIDGE_FILLET = RIDGE_HEIGHT / 2 - 0.01

# Top cylinder parameters
TOP_HEIGHT = 9.8
TOP_OD = 19.0
TOP_ID = 18.0
TOP_FILLET = 0.99
TOP_UPPER_OD = 17.0
TOP_UPPER_ID = 15.0

# OVERALL HEIGHT = BASE_HEIGHT + MID_HEIGHT + TAPER_HEIGHT + TOP_RIDGE_HEIGHT
# OVERALL HEIGHT = 49.6

SLOT_WIDTH = 3.9
SLOT_DEPTH = 8.5 - SLOT_WIDTH / 2
SLOT_LENGTH = 15.0
SLOT_ANGLE = math.sqrt(15**2 + 0.2**2)
