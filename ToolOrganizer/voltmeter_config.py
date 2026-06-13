"""
Configuration file for Voltmeter FreeCAD model
Contains all dimensions for the voltmeter shape
"""

# Main body dimensions (mm)
# X (width): 111mm, Y (depth): 25.4mm, Z (height): 42mm
VOLTMETER_LENGTH = 111.0  # X dimension (width)
VOLTMETER_WIDTH = 25.4  # Y dimension (depth)
VOLTMETER_HEIGHT = 42.0  # Z dimension (height)

# Extra bits on top edge (at one end)
# First extra bit: 24 x 20 with fillet
EXTRA_BIT_1_WIDTH = 24.0  # X dimension
EXTRA_BIT_1_HEIGHT = 20.0  # Z dimension (extends upward)
EXTRA_BIT_1_FILLET = 9.0  # Fillet radius

# Second extra bit: 20 x 8
EXTRA_BIT_2_WIDTH = 20.0  # X dimension
EXTRA_BIT_2_HEIGHT = 8.0  # Z dimension (extends upward)

# Third extra bit: 20 x 12
EXTRA_BIT_3_WIDTH = 20.0  # X dimension
EXTRA_BIT_3_HEIGHT = 12.0  # Z dimension (extends upward)

# Tolerance for cutting hole (mm)
# This will be added to all dimensions to create clearance
DEFAULT_TOLERANCE = 0.25

# Finger cutout translation distance
EXTRA_BIT_2_TRANSLATE = -2.0
