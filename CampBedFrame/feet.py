import math

import FreeCAD as App
import FreeCADGui as Gui
import Part

# Parameters
corner_radius = 2
outer_radius = 46
outer_side_length = outer_radius
base_thickness = 4
leg_thickness = 18
leg_radius = 43.75  # different from leg length
leg_side_length = (outer_radius - leg_radius) / 2  # the leg is offset by the difference in radius
wall_thickness = 2.4


def points(edge):
    return [v.Point for v in edge.Vertexes]


def fillet_vertical_edges(part, corner_radius):
    for edge in part.Edges:
        if (
            abs(edge.Vertexes[0].Point.x - edge.Vertexes[1].Point.x) < 0.01
            and abs(edge.Vertexes[0].Point.y - edge.Vertexes[1].Point.y) < 0.01
        ):
            part = part.makeFillet(corner_radius, [edge])
    return part


def make_arc_extrude(radius, height, corner_radius, end_angle):
    arc = Part.makeCircle(radius, App.Vector(0, 0, 0), App.Vector(0, 0, 1), 0, end_angle)
    line1 = Part.LineSegment(arc.Vertexes[-1].Point, App.Vector(0, 0, 0))
    line2 = Part.LineSegment(arc.Vertexes[0].Point, App.Vector(0, 0, 0))
    wire = Part.Wire([arc, line1.toShape(), line2.toShape()])
    part = Part.Face(wire).extrude(App.Vector(0, 0, height))
    for edge in part.Edges:
        if (
            abs(edge.Vertexes[0].Point.x - edge.Vertexes[1].Point.x) < 0.01
            and abs(edge.Vertexes[0].Point.y - edge.Vertexes[1].Point.y) < 0.01
        ):
            # This is a vertical edge
            print(f"Filleting vertical edge {points(edge)}")
            part = part.makeFillet(corner_radius, [edge])
    return part


def make_arc_cut(radius, edge_length, height, end_angle):
    arc = Part.makeCylinder(radius, height, App.Vector(0, 0, 0), App.Vector(0, 0, 1), end_angle)

    plane1 = Part.makeBox(radius, radius, height, App.Vector(-edge_length, 0, 0))
    plane2 = Part.makeBox(radius, radius, height, App.Vector(0, -edge_length, 0))

    part = arc.cut(plane1).cut(plane2)

    for edge in part.Edges:
        if (
            abs(edge.Vertexes[0].Point.x - edge.Vertexes[1].Point.x) < 0.01
            and abs(edge.Vertexes[0].Point.y - edge.Vertexes[1].Point.y) < 0.01
        ):
            # This is a vertical edge
            print(f"Filleting vertical edge {points(edge)}")
            part = part.makeFillet(corner_radius, [edge])

    return part


def make_curved_chevron_rib(radius=leg_radius, angle_span=15):
    # Dimensions
    width = 3  # Width of the rib
    height = 1.5  # Height of the chevron
    thickness = 0.8  # Thickness of the walls

    # Create chevron profile (same as before)
    outer_points = [
        App.Vector(thickness, 0, 0),
        App.Vector(width / 2, height - thickness, 0),
        App.Vector(width - thickness, 0, 0),
        App.Vector(width, 0, 0),
        App.Vector(width / 2, height, 0),
        App.Vector(0, 0, 0),
    ]

    # Create profile wire
    profile = Part.makePolygon(outer_points + [outer_points[0]])

    # Create sweep path (arc)
    path = Part.makeCircle(radius, App.Vector(0, 0, 0), App.Vector(0, 0, 1), 0, angle_span)

    # Sweep profile along path
    pipe = Part.BRepOffsetAPI.MakePipe(path, profile)
    return pipe.Shape


def make_chevron_rib(length=15):
    # Dimensions
    width = 3  # Width of the rib
    height = 1.5  # Height of the chevron
    thickness = 0.8  # Thickness of the walls

    # Create outer chevron profile
    outer_points = [
        App.Vector(thickness, 0, 0),
        App.Vector(width / 2, height - thickness, 0),
        App.Vector(width - thickness, 0, 0),
        App.Vector(width, 0, 0),
        App.Vector(width / 2, height, 0),
        App.Vector(0, 0, 0),
    ]

    # Create wire and face
    wire = Part.makePolygon(outer_points + [outer_points[0]])
    face = Part.Face(wire)

    # Extrude along Y axis
    return face.extrude(App.Vector(0, 0, length))


def add_grip_cylinders(leg, leg_radius, leg_side_length, leg_thickness):
    # Cylinder dimensions
    cyl_radius = 1
    protrusion = 0.7
    # offset from the edge of the foot is the leg_side_length plus the cyl_radius
    # to be centered on the wall, then subtract the protrusion to embed the cylinders in the wall
    straight_offset = (
        leg_side_length + cyl_radius + (cyl_radius - protrusion)
    )  # protrude in the negative direction
    print(f"straight_offset: {straight_offset}")

    total_radius = leg_radius + protrusion
    chamfer_size = 0.5
    FIRST_OFFSET = outer_radius / 3
    SECOND_OFFSET = FIRST_OFFSET * 2

    # Positions for straight sides (2 per side)
    straight_positions = [
        (leg_radius - FIRST_OFFSET, straight_offset),  # First straight side
        (leg_radius - SECOND_OFFSET, straight_offset),
        (straight_offset, leg_radius - FIRST_OFFSET),  # Second straight side
        (straight_offset, leg_radius - SECOND_OFFSET),
    ]

    # Positions for curved side (4 cylinders) should be at 90/5 degree intervals
    curve_angles = [18, 36, 54, 72]  # degrees
    curved_positions = [
        (
            (total_radius - cyl_radius) * math.cos(math.radians(angle)),
            (total_radius - cyl_radius) * math.sin(math.radians(angle)),
        )
        for angle in curve_angles
    ]

    # Combine all positions
    all_positions = straight_positions + curved_positions

    # Create and position cylinders
    for x, y in all_positions:
        # Create cylinder
        cyl = Part.makeCylinder(cyl_radius, leg_thickness, App.Vector(x, y, 0))

        # Chamfer top edge
        top_edge = next(
            edge
            for edge in cyl.Edges
            if abs(edge.Length - 2 * math.pi * cyl_radius) < 0.01
            and edge.Vertexes[0].Point.z > leg_thickness / 2
        )
        cyl = cyl.makeChamfer(chamfer_size, [top_edge])

        # Fuse to leg
        leg = leg.fuse(cyl)

    return leg


# Create a new document
doc = App.newDocument()


# Create base
base = make_arc_extrude(outer_radius, base_thickness, corner_radius, 90)

# Create leg (cylinder quadrant).  the leg is already offset by the difference in radius
leg = make_arc_cut(leg_radius, leg_radius - leg_side_length * 2, leg_thickness, 90)

# Apply grip cylinders
leg = add_grip_cylinders(leg, leg_radius, leg_side_length, leg_thickness)

# Create hollowing for the leg.  This is also offset by the difference in radius
hollow_cut = make_arc_cut(
    leg_radius - wall_thickness,
    leg_radius - 2 * (leg_side_length + wall_thickness),
    leg_thickness,
    90,
)

# Add the hollow cut
leg = leg.cut(hollow_cut)


# Create FreeCAD part objects
foot = doc.addObject("Part::Feature", "foot")
foot.Shape = base.fuse(leg)

leg_obj = doc.addObject("Part::Feature", "leg")
leg_obj.Shape = leg


# Refresh the view
doc.recompute()

# Set up the view
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewIsometric()
