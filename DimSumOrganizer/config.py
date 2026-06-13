"""Configuration constants for Dim Sum Organizer insert."""

# Circle token dimensions
CIRCLE_TOKEN_HEIGHT = 6.2 + 3  # mm 2mm extra space
CIRCLE_TOKEN_DIAMETER = 40.7  # mm .5mm tolerance
CIRCLE_TOKEN_RADIUS = CIRCLE_TOKEN_DIAMETER / 2.0  # mm

# Oval token dimensions
OVAL_TOKEN_HEIGHT = 12.2 + 3  # mm 2mm extra space
OVAL_TOKEN_LENGTH = 39  # mm (major axis)
OVAL_TOKEN_WIDTH = 31  # mm (minor axis)
OVAL_TOKEN_MAJOR_RADIUS = OVAL_TOKEN_LENGTH / 2.0  # mm
OVAL_TOKEN_MINOR_RADIUS = OVAL_TOKEN_WIDTH / 2.0  # mm

# Container cylinder dimensions
CONTAINER_DIAMETER = 63.0  # mm
CONTAINER_RADIUS = CONTAINER_DIAMETER / 2.0  # mm
CONTAINER_HEIGHT = 13.0  # mm

# Number of stacks
NUM_OVAL_STACKS = 2
NUM_CIRCLE_STACKS = 1

BASKET_DIAMETER = 68.0
BASKET_SEPARATION = 74.5
BASKET_HEIGHT = 26.0

# Lid dimensions
LID_THICKNESS = 3.0  # mm
TOKEN_PROTRUSION_HEIGHT = 1.0  # mm - how much tokens protrude above lid surface
