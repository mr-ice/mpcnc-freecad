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

def inch_to_mm(inches):
    """
    Convert inches to millimeters.

    Args:
        inches (float): Length in inches

    Returns:
        float: Length in millimeters
    """
    return float(inches) * 25.4

# These are the h x w of the margin between the front/back and the corners
triangle = 3  ## mm
# these are the gaps between the ends and spine
gap = 6  ## mm
# This is the wrap around area (along the outside)
margin = 20  ## mm
# This is the thickness of the 3d model to print, enough to make it rigid but not too thick.
thickness = 3  ## mm

font_size = "15 mm"  ## font size as string

label_x_offset = 15  # mm from left edge of inner plates

# Pin/hole parameters
pin_radius = 5.0  # mm radius of circular part
slot_width = 5.0  # mm width of slot
slot_length = 9.0  # mm length of slot
pin_hole_tolerance = 0.2  ## mm

max_printer_dimension = 345  # mm

"""Configuration elements for the terrain generator"""

class Config:
    square_size = 1.25 * 25.4 # 1.25 inches in mm

config = Config()
