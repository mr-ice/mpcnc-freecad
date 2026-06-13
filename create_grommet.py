from math import cos, pi, sin

import FreeCAD as App
import Part


def create_grommet(
    diameter,
    depth,
    rim_width,
    thickness,
    friction_embed_percent=50,
    cut_width=None,
    taper_percent=10,
):
    """
    Create a grommet with specified parameters

    Args:
        diameter (float): Outer diameter of the grommet body
        depth (float): Total height of the grommet
        rim_width (float): Width of the rim extending from the body
        thickness (float): Wall thickness of the grommet
        friction_embed_percent (float): How far the friction cylinders are embedded
                                      into the wall (0-100%, where 50% means centered)
        cut_width (float): If provided, splits the grommet into two parts using a cube of this width
        taper_percent (float): Percentage to reduce cylinder diameter at top (0-100)
    """
    # Convert to mm if inputs are in inches
    inch_to_mm = 25.4

    # Calculate key dimensions
    radius = diameter / 2
    inner_radius = radius - thickness
    rim_end_thickness = thickness * 0.75  # rim tapers to 1/4 of original thickness

    # Create the main cylindrical body (outer)
    outer_cylinder = Part.makeCylinder(radius, depth)
    inner_cylinder = Part.makeCylinder(inner_radius, depth)

    # Create the hollow cylinder by subtracting inner from outer
    body = outer_cylinder.cut(inner_cylinder)

    # Create friction cylinders
    friction_cylinders = []
    cylinder_radius = thickness / 2
    cylinder_height = depth - thickness
    top_radius = cylinder_radius * (1 - taper_percent / 100)  # Reduced radius at top

    # Calculate cylinder position
    embed_distance = thickness * friction_embed_percent / 100
    # Adjust so 50% means center is at outer edge (radius)
    cylinder_center_radius = radius + (thickness / 2) - embed_distance

    # # Create four cylinders at 90-degree intervals
    # for i, angle in enumerate([0, 90, 180, 270]):
    #     # Calculate position for this cylinder
    #     angle_rad = angle * pi / 180
    #     x = cylinder_center_radius * cos(angle_rad)
    #     y = cylinder_center_radius * sin(angle_rad)
    #
    #     # Create the tapered cylinder (cone)
    #     pos = App.Vector(x, y, thickness/2)
    #     dir = App.Vector(0, 0, 1)
    #     cylinder = Part.makeCone(cylinder_radius, top_radius, cylinder_height, pos, dir)
    #
    #     # Create fillet at the top
    #     edges_to_fillet = []
    #     for edge in cylinder.Edges:
    #         if abs(edge.CenterOfMass.z - (cylinder_height + thickness/2)) < 0.1:  # Top edge
    #             edges_to_fillet.append(edge)
    #
    #     # Apply fillet
    #     cylinder = cylinder.makeFillet(top_radius/2, edges_to_fillet)
    #
    #     friction_cylinders.append(cylinder)
    #
    # # Fuse all friction cylinders together
    # combined_cylinders = friction_cylinders[0]
    # for cyl in friction_cylinders[1:]:
    #     combined_cylinders = combined_cylinders.fuse(cyl)
    #
    # # Fuse friction cylinders with the main body
    # body = body.fuse(combined_cylinders)

    # Create threading
    thread_pitch = 4.0  # Distance between threads (larger for thicker threads)
    thread_depth = thickness * 0.8  # Deep threads
    thread_width = thread_pitch * 0.6  # Width of thread
    num_segments = 36  # Number of segments per revolution

    # Create the thread by making a series of helical cuts
    for i in range(int((depth - thread_pitch) / (thread_pitch / num_segments))):
        angle = (i * 360 / num_segments) % 360
        z_pos = i * thread_pitch / num_segments

        # Create a box for each thread segment
        thread_box = Part.makeBox(thread_depth, thread_width, thread_pitch / 2)

        # Position and rotate the box
        thread_box.translate(App.Vector(radius - thread_depth, -thread_width / 2, z_pos))
        thread_box.rotate(App.Vector(radius, 0, z_pos), App.Vector(0, 0, 1), angle)

        # Cut the thread into the body
        body = body.cut(thread_box)

    # Create the rim
    outer_rim_radius = radius + rim_width

    # Create points for the rim profile, all points are at y=0
    p1 = App.Vector(radius, 0, 0)
    p2 = App.Vector(radius, 0, thickness)
    p3 = App.Vector(outer_rim_radius, 0, thickness)
    p4 = App.Vector(outer_rim_radius, 0, rim_end_thickness)

    # Create a Bezier curve for the taper
    edge1 = Part.makeLine(p1, p2)
    edge2 = Part.makeLine(p2, p3)
    edge3 = Part.makeLine(p3, p4)
    edge4 = Part.makeLine(p4, p1)

    # Create wire and face from edges
    wire = Part.Wire([edge1, edge2, edge3, edge4])
    rim_profile = Part.Face(wire)

    # Temporarily add wire to document for visualization
    # doc = App.activeDocument()
    # temp_wire = doc.addObject("Part::Feature", "TempWire")
    # temp_wire.Shape = wire
    # doc.recompute()

    # Rotate the rim profile to create the full rim
    rim = rim_profile.revolve(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 360)

    # Temporarily add rim to document for visualization
    # doc = App.activeDocument()
    # temp_rim = doc.addObject("Part::Feature", "TempRim")
    # temp_rim.Shape = rim
    # doc.recompute()

    # Combine body and rim
    grommet = body.fuse(rim)

    # After creating the complete grommet, split it if cut_width is provided
    if cut_width is not None:
        outer_rim_radius = radius + rim_width

        # Create points for the wedge profile
        inner_cut_width = 5  # Fixed inner width
        outer_cut_width = 30  # Fixed outer width
        p1 = App.Vector(-inner_cut_width / 2, 0, 0)
        p2 = App.Vector(inner_cut_width / 2, 0, 0)
        p3 = App.Vector(outer_cut_width / 2, outer_rim_radius, 0)
        p4 = App.Vector(-outer_cut_width / 2, outer_rim_radius, 0)

        # Create the wedge face
        wedge_wire = Part.makePolygon([p1, p2, p3, p4, p1])
        wedge_face = Part.Face(wedge_wire)

        # Extrude the wedge to create the cutting shape
        wedge = wedge_face.extrude(App.Vector(0, 0, depth))

        # Rotate the wedge 45 degrees
        wedge.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), -45)

        # Create the two parts
        part1 = grommet.common(wedge)  # Intersection
        part2 = grommet.cut(wedge)  # Remainder

        # Create a friction cylinder at the center of the cut face
        center_cylinder_radius = thickness / 2
        center_cylinder_height = depth - thickness

        # Calculate position - at outer radius, rotated 90 degrees from the cut face
        center_x = radius * cos(45 * pi / 180)  # 45 degrees (90 degrees from -45)
        center_y = radius * sin(45 * pi / 180)

        # Create the center cylinder
        center_pos = App.Vector(center_x, center_y, thickness / 2)
        center_cyl = Part.makeCylinder(
            center_cylinder_radius, center_cylinder_height, center_pos, App.Vector(0, 0, 1)
        )

        # Create fillet at the top
        edges_to_fillet = []
        for edge in center_cyl.Edges:
            if (
                abs(edge.CenterOfMass.z - (center_cylinder_height + thickness / 2)) < 0.1
            ):  # Top edge
                edges_to_fillet.append(edge)
        center_cyl = center_cyl.makeFillet(center_cylinder_radius / 2, edges_to_fillet)

        # Add center cylinder to part1 and subtract from part2
        part1 = part1.fuse(center_cyl)
        part2 = part2.cut(center_cyl)

        # Show the cutting wedge (but hide it)
        doc = App.activeDocument()
        temp_wedge = doc.addObject("Part::Feature", "TempCuttingWedge")
        temp_wedge.Shape = wedge
        temp_wedge.Visibility = False

        # Create separate objects for the two parts
        part1_obj = doc.addObject("Part::Feature", "Grommet_Part1")
        part1_obj.Shape = part1

        part2_obj = doc.addObject("Part::Feature", "Grommet_Part2")
        part2_obj.Shape = part2

        doc.recompute()

        return part1, part2

    return grommet


def create_matching_nut(diameter, depth, thickness, thread_pitch=4.0):
    """Create a matching nut for the threaded grommet"""
    # Nut dimensions
    nut_height = depth * 0.4  # Make nut shorter than grommet
    nut_outer_dia = diameter * 1.8  # Make nut substantially larger
    nut_inner_dia = diameter - thickness * 0.2  # Slightly smaller for good fit
    thread_depth = thickness * 0.8
    thread_width = thread_pitch * 0.6
    num_segments = 36

    # Create basic hexagonal nut
    hex_nut = Part.makeCylinder(nut_outer_dia / 2, nut_height)
    hex_nut = hex_nut.makeHexa()

    # Create central hole
    hole = Part.makeCylinder(nut_inner_dia / 2, nut_height)
    hex_nut = hex_nut.cut(hole)

    # Create internal threads
    for i in range(int((nut_height - thread_pitch) / (thread_pitch / num_segments))):
        angle = (i * 360 / num_segments) % 360
        z_pos = i * thread_pitch / num_segments

        # Create thread segment
        thread_box = Part.makeBox(thread_depth, thread_width, thread_pitch / 2)

        # Position and rotate
        thread_box.translate(App.Vector(nut_inner_dia / 2, -thread_width / 2, z_pos))
        thread_box.rotate(App.Vector(nut_inner_dia / 2, 0, z_pos), App.Vector(0, 0, 1), angle)

        # Add thread to nut
        hex_nut = hex_nut.fuse(thread_box)

    return hex_nut


def main():
    # Example usage
    diameter = 55  # mm
    depth = 30  # mm
    rim_width = 12  # mm
    thickness = 3  # mm
    cut_width = 20  # mm

    result = create_grommet(
        diameter,
        depth,
        rim_width,
        thickness,
        friction_embed_percent=50,
        cut_width=cut_width,
        taper_percent=80,
    )

    # Create matching nut
    nut = create_matching_nut(diameter, depth, thickness)

    # Add nut to document
    doc = App.activeDocument()
    nut_obj = doc.addObject("Part::Feature", "Matching_Nut")
    nut_obj.Shape = nut
    nut_obj.Placement.Base = App.Vector(diameter * 1.5, 0, 0)  # Place nut beside grommet

    # If cut_width was provided, result is a tuple of (part1, part2)
    if isinstance(result, tuple):
        part1, part2 = result
    else:
        # Create a FreeCAD document and add the shape
        doc = App.activeDocument()
        part = doc.addObject("Part::Feature", "Grommet")
        part.Shape = result
        doc.recompute()


if __name__ == "__main__":
    main()
