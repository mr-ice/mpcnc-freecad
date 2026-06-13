# import FreeCAD as App
import math

import Part

# Configuration variables
BASE_WIDTH = 120.0  # mm
TOP_WIDTH = 30.0  # mm
HEIGHT = 240.0  # mm
THICKNESS = 6.0  # mm

# Hinge configuration
HINGE_RADIUS = 2.5  # mm
HINGE_TOLERANCE = 0.3  # mm
HINGE_NUMBER = 5  # how many hinge parts to create, should be odd
HINGE_END_OFFSET = 3.0  # mm

EDGE_LENGTH = math.sqrt(HEIGHT**2 + ((BASE_WIDTH - TOP_WIDTH) / 2) ** 2)

HINGE_LENGTH = (EDGE_LENGTH - 2 * HINGE_END_OFFSET) / HINGE_NUMBER - HINGE_TOLERANCE

REINFORCE_SIZE = HINGE_RADIUS * 2  # Size of reinforcement box

# Calculate the exact offset needed for hinge alignment
HINGE_CENTER_OFFSET = (HINGE_LENGTH + HINGE_TOLERANCE) / 2


def create_base_shape():
    """Creates the basic truncated pyramid side shape"""
    # Calculate points for the trapezoid
    points = [
        App.Vector(0, 0, 0),  # Bottom left
        App.Vector(BASE_WIDTH, 0, 0),  # Bottom right
        App.Vector((BASE_WIDTH - TOP_WIDTH) / 2 + TOP_WIDTH, HEIGHT, 0),  # Top right
        App.Vector((BASE_WIDTH - TOP_WIDTH) / 2, HEIGHT, 0),  # Top left
    ]

    # Create the 2D shape
    wire = Part.makePolygon(points + [points[0]])
    face = Part.Face(wire)

    # Extrude to create 3D
    return face.extrude(App.Vector(0, 0, THICKNESS))


def create_hinge_positive():
    """Creates a positive hinge

    - cylinder with truncated codes at both ends
    - reinforcement to connect cylinder to base shape
    """
    # Create reinforcement box
    box_length = HINGE_LENGTH
    box = Part.makeBox(
        box_length, REINFORCE_SIZE, THICKNESS / 2, App.Vector(0, -REINFORCE_SIZE, -THICKNESS / 4)
    )

    # Create main cylinder
    cylinder = Part.makeCylinder(
        HINGE_RADIUS, HINGE_LENGTH, App.Vector(0, 0, 0), App.Vector(1, 0, 0)
    )

    # Create truncated cone at end
    cone_length = HINGE_RADIUS
    top_cone = Part.makeCone(
        HINGE_RADIUS,
        HINGE_TOLERANCE,
        cone_length,
        App.Vector(HINGE_LENGTH, 0, 0),
        App.Vector(1, 0, 0),
    )
    bottom_cone = Part.makeCone(
        HINGE_RADIUS, HINGE_TOLERANCE, cone_length, App.Vector(0, 0, 0), App.Vector(-1, 0, 0)
    )
    # Fuse parts together
    hinge = cylinder.fuse(top_cone)
    hinge = hinge.fuse(bottom_cone)
    hinge = hinge.fuse(box)
    if False:
        temp = App.activeDocument().addObject("Part::Feature", "Hinge000")
        temp.Shape = hinge
    return hinge


def create_hinge_negative():
    """Creates a negative hinge (with truncated cone cavities and reinforcement)"""
    # Create reinforcement box
    box_length = HINGE_LENGTH
    box = Part.makeBox(
        box_length,
        REINFORCE_SIZE,
        THICKNESS / 2,
        App.Vector(-HINGE_LENGTH, -REINFORCE_SIZE, -THICKNESS / 4),
    )

    # Create main cylinder
    cylinder = Part.makeCylinder(
        HINGE_RADIUS, HINGE_LENGTH, App.Vector(-HINGE_LENGTH, 0, 0), App.Vector(1, 0, 0)
    )

    # Create truncated cones for cavities
    # The negative has to be much taller to avoid fusing.  The truncated cone is wider
    r0 = HINGE_RADIUS + HINGE_TOLERANCE
    r1 = HINGE_TOLERANCE
    h = HINGE_RADIUS + HINGE_TOLERANCE * 2
    top_cone = Part.makeCone(
        r0, r1, h, App.Vector(-HINGE_LENGTH - HINGE_TOLERANCE, 0, 0), App.Vector(1, 0, 0)
    )
    bottom_cone = Part.makeCone(r0, r1, h, App.Vector(HINGE_TOLERANCE, 0, 0), App.Vector(-1, 0, 0))

    # Create the final shape
    hinge = box.fuse(cylinder)  # must be first so that cones are cut out of both
    hinge = hinge.cut(top_cone)
    hinge = hinge.cut(bottom_cone)
    if False:
        temp = App.activeDocument().addObject("Part::Feature", "Cylinder000")
        temp.Shape = cylinder
        temp = App.activeDocument().addObject("Part::Feature", "Box000")
        temp.Shape = box
        temp = App.activeDocument().addObject("Part::Feature", "TopCone000")
        temp.Shape = top_cone
        temp = App.activeDocument().addObject("Part::Feature", "BottomCone000")
        temp.Shape = bottom_cone
        temp = App.activeDocument().addObject("Part::Feature", "Hinge000")
        temp.Shape = hinge
    return hinge


def add_hinges(shape):
    """Adds hinges to the basic shape"""
    doc = App.activeDocument()
    angle = math.atan2(HEIGHT, (BASE_WIDTH - TOP_WIDTH) / 2)
    edge_length = math.sqrt(HEIGHT**2 + ((BASE_WIDTH - TOP_WIDTH) / 2) ** 2)

    result = shape

    # Add hinges to right side, skipping the bottom-most hinge
    pos = HINGE_END_OFFSET * 2 + HINGE_LENGTH
    for i in range(HINGE_NUMBER):
        x = BASE_WIDTH - ((pos / edge_length) * (BASE_WIDTH - TOP_WIDTH) / 2)
        y = (pos / edge_length) * HEIGHT
        pos += HINGE_LENGTH + HINGE_TOLERANCE

        if i % 2 == 0:
            continue

        hinge = create_hinge_positive()
        hinge.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), -math.degrees(angle))

        # Adjust offset to move hinge away from base by radius plus 2*tolerance
        dx = HINGE_RADIUS * math.cos(angle)
        dy = HINGE_RADIUS * math.sin(angle)
        offset_x = (HINGE_RADIUS + 2 * HINGE_TOLERANCE) * math.sin(angle)
        offset_y = -(HINGE_RADIUS + 2 * HINGE_TOLERANCE) * math.cos(angle)

        hinge.translate(App.Vector(x + dx + offset_x, y - dy + offset_y, THICKNESS / 2))
        result = result.fuse(hinge)

    pos = HINGE_END_OFFSET * 2 + HINGE_LENGTH
    # Add negative hinges to left side
    for i in range(HINGE_NUMBER):
        x = (pos / edge_length) * (BASE_WIDTH - TOP_WIDTH) / 2
        y = (pos / edge_length) * HEIGHT
        pos += HINGE_LENGTH + HINGE_TOLERANCE

        if i % 2 != 0:
            continue

        hinge = create_hinge_negative()
        hinge.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), math.degrees(angle))

        dx = HINGE_RADIUS * math.cos(angle)
        dy = HINGE_RADIUS * math.sin(angle)
        offset_x = -(HINGE_RADIUS + 2 * HINGE_TOLERANCE) * math.sin(angle)
        offset_y = (HINGE_RADIUS + 2 * HINGE_TOLERANCE) * math.cos(angle)

        hinge.translate(App.Vector(x - dx + offset_x, y - dy + offset_y, THICKNESS / 2))
        result = result.fuse(hinge)

    return result


def find_longest_edges(shape):
    """Find the four longest edges of the shape"""
    # Get all edges and their lengths
    edges = [(edge, edge.Length) for edge in shape.Edges]

    # Sort edges by length in descending order
    edges.sort(key=lambda x: x[1], reverse=True)

    # Get the four longest edges
    longest_edges = [edge[0] for edge in edges[:4]]

    # Create visualization objects
    # doc = App.activeDocument()
    # for i, edge in enumerate(longest_edges):
    #     temp = doc.addObject("Part::Feature", f"LongEdge_{i}")
    #     # Create a shape from the edge
    #     edge_shape = Part.Shape([edge])
    #     temp.Shape = edge_shape

    return longest_edges


def create_panel():
    """Creates one side of the sign and adds it to the current document"""
    # Create basic shape
    base = create_base_shape()

    # Find the four longest edges and apply chamfer
    longest_edges = find_longest_edges(base)
    chamfer_size = THICKNESS / 3  # Make chamfer 1/3 of thickness to leave room for hinges
    base = base.makeChamfer(chamfer_size, chamfer_size, longest_edges)

    # Add hinges
    final_shape = add_hinges(base)

    return final_shape


def create_sign():
    """Creates one side of the sign and adds it to the current document"""
    doc = App.activeDocument()

    panel1 = create_panel()
    panel2 = create_panel()
    panel3 = create_panel()

    # Panel spacing based on hinge dimensions plus extra tolerance
    spacing = 2 * (HINGE_RADIUS + 2 * HINGE_TOLERANCE)  # Increased to match new hinge offsets

    # Calculate corner angle from trapezoid dimensions
    corner_angle = math.degrees(math.atan2(HEIGHT, (BASE_WIDTH - TOP_WIDTH) / 2))
    print(f"{corner_angle=}")
    rotation_angle = 2 * (90 - corner_angle)

    # Panel 2 stays at origin
    obj = doc.addObject("Part::Feature", "Panel2")
    obj.Shape = panel2

    # Panel 1 to the left, rotated around its lower right corner
    panel1.translate(App.Vector(-BASE_WIDTH - spacing, 0, 0))  # Removed 1.5 y-offset
    panel1.rotate(
        App.Vector(-HINGE_END_OFFSET - HINGE_TOLERANCE - HINGE_CENTER_OFFSET, 0, 0),
        App.Vector(0, 0, 1),
        -rotation_angle,
    )

    # Fine adjustment for panel1 alignment
    # panel1.translate(App.Vector(1.459, 8.380, 0))
    panel1.translate(App.Vector(0.104 + 1.768, 9.420 + HINGE_TOLERANCE, 0))
    obj = doc.addObject("Part::Feature", "Panel1")
    obj.Shape = panel1

    # Panel 3 to the right
    panel3.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), rotation_angle)
    panel3.translate(App.Vector(BASE_WIDTH + spacing - 0.1747, 0, 0))
    obj = doc.addObject("Part::Feature", "Panel3")
    obj.Shape = panel3

    doc.recompute()
    return obj
