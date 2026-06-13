"""Configuration constants for the bookbinding templates."""


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
