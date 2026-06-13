import math

import FreeCAD as App
import FreeCADGui as Gui
import Part


class Config:
    box_width = 320.0
    box_top_width = 313.0
    box_top_delta = (box_width - box_top_width) / 2
    box_depth = 130.0
    card_height = 91.0
    card_width = 59.0
    card_thickness = 12.0  # per 20
    map_width = 312
    map_thickness = 30  # per 13
    player_length = 305  # player boards
    player_width = 150  # player boards
    player_thickness = 4  # player boards
    mini_width = 19.85  # mini base width
    mini_length = 22.85  # base length
    mini_height = 27.85  # mini height
    base_height = 3.5  # base height
    mini_overall_width = 28.25  # mini overall width
    mini_overall_height = 30  # mini overall height
    bitbox_length = 129  # bitbox length
    bitbox_width = 68  # bitbox width
    bitbox_height = 22  # bitbox height
    clearance = 2  # slot clearances
    reboot_thickness = 4.125  # reboot thickness 33mm / 8
    reboot_width = 21.5  # reboot width
    flag_side = 25.56  # flag side width
    flag_thickness = 2.2  # flag thickness  13.2 / 6
    flag_x_thickness = math.sqrt(
        flag_thickness**2 + flag_thickness**2
    )  # flag x thickness is offset to have thickness at our 45 deg angle
    flag_height = 20.05  # flag height
    flag_width = 16.3  # flag width
    flag_pole = 3.7  # flag pole
    bottom_thickness = 2  # bottom thickness
    space_between_slots = bottom_thickness * 3
    tolerance = 0.01
    priority_token_radius = 38.3 / 2
    priority_token_height = 3.0
    general_fillet_radius = 1
    top_fillet_radius = 0.3


test = __name__
test = "__main__"

if test == "__main__":
    # Create a new document
    doc = App.newDocument("BigBox")

    # Create outer box
    # outer_box = Part.makeBox(Config.box_width, Config.box_width, Config.card_width + Config.bottom_thickness + Config.player_thickness * 4)

    outer_box_object = doc.addObject("Part::Wedge", "OuterBox")
    outer_box_object.Xmin = 0
    outer_box_object.Ymin = 0
    outer_box_object.Zmin = 0
    outer_box_object.Xmax = Config.box_width
    outer_box_object.Ymax = (
        Config.card_width + Config.bottom_thickness + Config.player_thickness * 4
    )
    outer_box_object.Zmax = Config.box_width
    outer_box_object.X2min = Config.box_top_delta
    outer_box_object.Z2min = Config.box_top_delta
    outer_box_object.X2max = Config.box_top_width + Config.box_top_delta
    outer_box_object.Z2max = Config.box_top_width + Config.box_top_delta
    outer_box_object.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(90, 0, 90))

    outer_box = outer_box_object.Shape

    # Create inner box (smaller in all dimensions by wall_thickness * 2, and extra padding on bottom)
    inner_box = Part.makeBox(
        Config.player_length + Config.clearance,  # width
        Config.player_length + Config.clearance,  # depth
        Config.box_depth - Config.bottom_thickness - Config.card_width,  # height
    )

    # Fillet the vertical-ish edges of outer box
    outer_edges = []
    for edge in outer_box.Edges:
        # Get edge vertices
        v1 = edge.Vertexes[0]
        v2 = edge.Vertexes[1]

        # Calculate direction vector of edge
        dx = v2.Point.x - v1.Point.x
        dy = v2.Point.y - v1.Point.y
        dz = v2.Point.z - v1.Point.z

        # Calculate angle with vertical (Z) axis in degrees
        length = math.sqrt(dx * dx + dy * dy + dz * dz)
        if length > Config.tolerance:  # Avoid division by zero
            angle = math.degrees(math.acos(abs(dz) / length))

            # If angle is less than 10 degrees from vertical
            if angle < 10:
                outer_edges.append(edge)

    outer_box = outer_box.makeFillet(10, outer_edges)

    # Fillet the vertical edges of inner box
    inner_edges = []
    for edge in inner_box.Edges:
        if abs(edge.tangentAt(0).z) == 1:
            inner_edges.append(edge)

    inner_box = inner_box.makeFillet(3, inner_edges)

    wall_thickness = (Config.box_width - inner_box.BoundBox.XLength) / 2

    # Position inner box (centered, raised by bottom padding)
    inner_box.translate(
        App.Vector(wall_thickness, wall_thickness, Config.bottom_thickness + Config.card_width)
    )

    # Create hollow box by subtracting inner from outer
    hollow_box = outer_box.cut(inner_box)

    # Hide the original outer box object
    outer_box_object.ViewObject.hide()

    # Calculate dimensions with clearance
    slot_height = Config.card_height + Config.clearance
    slot_width = Config.card_width + Config.clearance
    slot_thickness = Config.card_thickness * 1.25
    slot_spacing = Config.card_thickness

    x_offset = wall_thickness * 2
    y_offset = wall_thickness * 2
    z_offset = Config.bottom_thickness

    # make a hollow for the cards about 2/3 of the way up
    hollow_top_card_slot = Part.makeBox(
        slot_height, Config.box_width - (x_offset * 2), slot_width / 3
    )
    hollow_top_card_slot.translate(
        App.Vector(x_offset, y_offset, z_offset + slot_width - slot_width / 3)
    )

    hollow_box = hollow_box.cut(hollow_top_card_slot)

    slots_count = 8

    # Create and position each card slot
    for i in range(slots_count):
        # Create slot box
        slot = Part.makeBox(slot_height, slot_thickness, slot_width)

        # Position slot:
        # x: wall_thickness (from left side)
        # y: wall_thickness + Config.card_width + (i * (slot_thickness + slot_spacing)) (from front)
        # z: wall_thickness (above bottom padding)
        slot.translate(
            App.Vector(
                x_offset, y_offset + slot_spacing + (i * (slot_thickness + slot_spacing)), z_offset
            )
        )

        # Cut slot from hollow box
        hollow_box = hollow_box.cut(slot)

    upgrade_slot = Part.makeBox(slot_height, Config.card_thickness / 20 * 80 * 1.25, slot_width)
    upgrade_slot.translate(
        App.Vector(
            x_offset + slot_height + (Config.space_between_slots), y_offset + slot_spacing, z_offset
        )
    )

    hollow_box = hollow_box.cut(upgrade_slot)

    # Create damage slot (7/8 size of upgrade slot)
    damage_slot = Part.makeBox(
        slot_height,
        Config.card_thickness / 20 * 80 * 1.25 * 0.875,  # 7/8 of upgrade slot
        slot_width,
    )
    damage_slot.translate(
        App.Vector(
            x_offset,
            y_offset + slot_thickness + (slots_count * (slot_thickness + slot_spacing)),
            z_offset,
        )
    )

    hollow_box = hollow_box.cut(damage_slot)

    # Add hollow top for damage slot
    hollow_top_damage_slot = Part.makeBox(
        slot_height, y_offset + upgrade_slot.BoundBox.YLength + slot_spacing, slot_width / 3
    )
    hollow_top_damage_slot.translate(
        App.Vector(
            x_offset + slot_height + (Config.space_between_slots),
            y_offset,
            z_offset + slot_width - slot_width / 3,
        )
    )

    hollow_box = hollow_box.cut(hollow_top_damage_slot)

    cylinder_radius = Config.card_width / 2
    cylinder_length = Config.box_width - (x_offset * 2)
    # Add cylinder for damage slot
    damage_cylinder = Part.makeCylinder(
        cylinder_radius,
        y_offset + upgrade_slot.BoundBox.YLength + slot_spacing,
        App.Vector(0, 0, 0),
        App.Vector(0, 1, 0),  # Align along Y axis
    )

    damage_cylinder.translate(
        App.Vector(
            x_offset + slot_height + (Config.space_between_slots) + Config.card_height / 2,
            y_offset,
            Config.bottom_thickness + Config.card_width,
        )
    )

    hollow_box = hollow_box.cut(damage_cylinder)

    # Create cylinder for top cutout
    card_cylinder = Part.makeCylinder(
        cylinder_radius,
        cylinder_length,
        App.Vector(0, 0, 0),
        App.Vector(0, 1, 0),  # Align along Y axis
    )

    # Position cylinder:
    # x: same as card slots
    # y: offset by 4 * wall_thickness and half the card height
    # z: wall_thickness + card_width + (card_width/2)
    # because the cylinder is aligned along Y, we need to offset the x by half the card height
    card_cylinder.translate(
        App.Vector(
            x_offset + Config.card_height / 2, y_offset, Config.bottom_thickness + Config.card_width
        )
    )

    # Cut cylinder from hollow box
    hollow_box = hollow_box.cut(card_cylinder)

    # Create reboot token slots
    reboot_slot_width = Config.reboot_width + Config.clearance
    reboot_slot_thickness = Config.reboot_thickness * 8 + Config.clearance
    sphere_radius = reboot_slot_width * 0.4  # 80% of width for sphere cutouts

    # Position offset from damage slot
    reboot_x_offset = x_offset + Config.card_height * 2 + Config.bottom_thickness * 8

    reboot_slot = Part.makeBox(reboot_slot_width, reboot_slot_thickness, reboot_slot_width)

    # Position slot
    reboot_slot.translate(
        App.Vector(
            reboot_x_offset,
            y_offset + sphere_radius,
            z_offset + Config.card_width - reboot_slot_width,
        )
    )

    # Create spherical cutouts at ends
    front_sphere = Part.makeSphere(sphere_radius)
    back_sphere = Part.makeSphere(sphere_radius)

    # Position spheres at ends of slot
    front_sphere.translate(
        App.Vector(
            reboot_x_offset + (reboot_slot_width / 2),
            y_offset + sphere_radius,
            z_offset + Config.card_width - (Config.bottom_thickness / 2),
        )
    )

    back_sphere.translate(
        App.Vector(
            reboot_x_offset + (reboot_slot_width / 2),
            y_offset + reboot_slot.BoundBox.YLength + sphere_radius,
            z_offset + Config.card_width + (Config.bottom_thickness / 2),
        )
    )

    # Cut slots and spheres from box
    hollow_box = hollow_box.cut(reboot_slot)
    hollow_box = hollow_box.cut(front_sphere)
    hollow_box = hollow_box.cut(back_sphere)

    # Create staggered cube cutouts for flag side
    flag_cutout_width = Config.flag_side + Config.clearance
    flag_cutout_depth = Config.flag_side + Config.clearance
    flag_cutout_height = Config.flag_height + Config.clearance

    flag_cutout_spacing = Config.flag_thickness * 6 + Config.clearance
    flag_start_x = (
        reboot_x_offset
        + reboot_slot_width
        + Config.space_between_slots * 2
        + Config.priority_token_radius
        - Config.space_between_slots
    )
    flag_x_offset = flag_start_x
    flag_y_offset = y_offset

    # Create and position 6 overlapping cubes
    for i in range(6):
        # Create cube
        flag_cube = Part.makeBox(flag_cutout_height, flag_cutout_width, flag_cutout_depth)

        # Calculate diagonal distance from corner to center (using Pythagorean theorem)
        corner_to_center = (flag_cutout_width * math.sqrt(2)) / 2

        # Rotate 45 degrees counter-clockwise around Z axis
        flag_cube.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 45)

        # Position cube with offset
        flag_cube.translate(
            App.Vector(
                flag_x_offset + corner_to_center,  # offset by corner_to_center distance
                flag_y_offset,
                z_offset + Config.card_width - flag_cutout_depth,
            )
        )

        # Cut cube from box
        hollow_box = hollow_box.cut(flag_cube)

        # flag_x_offset -= Config.clearance + Config.flag_thickness
        flag_x_offset += Config.flag_x_thickness

    flag_sphere = Part.makeSphere(Config.flag_side * 0.55)
    flag_sphere.translate(
        App.Vector(
            flag_start_x + Config.flag_side / 2,
            flag_y_offset + corner_to_center,
            z_offset + Config.card_width,
        )
    )

    hollow_box = hollow_box.cut(flag_sphere)

    # THe priority token needs a cutout with a raised center so that it can be lifted from the box
    token_height = (
        Config.priority_token_height * 1.5 + Config.clearance
    )  # Reduced from *2 to *1.5 (25% reduction)
    torus_z = (
        Config.bottom_thickness
        + Config.card_width
        - (Config.priority_token_height + Config.clearance) * 2
    )  # Store torus Z

    priority_token = Part.makeCylinder(
        Config.priority_token_radius + Config.clearance / 2,  # applied twice for diameter
        token_height,
    )

    # Position token to maintain same max Z height
    priority_token.translate(
        App.Vector(
            reboot_x_offset
            + reboot_slot_width
            + Config.space_between_slots
            + Config.priority_token_radius,
            y_offset
            + sphere_radius
            + reboot_slot_thickness
            + Config.priority_token_radius / 2
            + Config.space_between_slots,
            Config.bottom_thickness
            + Config.card_width
            - token_height,  # Adjusted to keep top at same Z
        )
    )

    hollow_box = hollow_box.cut(priority_token)

    # Create torus for priority token
    torus_radius = Config.priority_token_radius / 2  # half the diameter of priority token
    tube_radius = Config.priority_token_height * 2  # Keep original tube radius

    # Create torus
    torus = Part.makeTorus(
        torus_radius,  # major radius (center to middle of tube)
        tube_radius,  # minor radius (tube thickness)
        App.Vector(0, 0, 0),
        App.Vector(0, 0, 1),  # normal vector (pointing up)
        0,  # angle1 (start angle)
        360,  # angle2 (end angle)
    )

    # Position torus at original Z position
    torus.translate(
        App.Vector(
            priority_token.Placement.Base.x,
            priority_token.Placement.Base.y,
            torus_z,  # Use stored original Z position
        )
    )

    # Fuse (add) torus to box instead of cutting
    hollow_box = hollow_box.fuse(torus)

    # Miscellaneous go in the top right corner in a larger box
    misc_box_height = (
        inner_box.BoundBox.XLength - (x_offset + slot_height) - Config.space_between_slots * 2
    )
    misc_box_width = (
        inner_box.BoundBox.YLength
        - (y_offset + upgrade_slot.BoundBox.YLength + slot_spacing * 2)
        - Config.space_between_slots * 2
    )

    misc_box = Part.makeBox(misc_box_height, misc_box_width, slot_width + Config.clearance * 2)

    misc_box.translate(
        App.Vector(
            x_offset + slot_height + (Config.space_between_slots),
            y_offset
            + upgrade_slot.BoundBox.YLength
            + slot_spacing * 2
            + Config.space_between_slots,
            Config.bottom_thickness,
        )
    )

    hollow_box = hollow_box.cut(misc_box)

    ## FILLETS ONLY BELOW HERE, NO MORE CUTS

    def is_value(value, target):
        """Check if two values are equal within a small tolerance"""
        return abs(value - target) < Config.tolerance  # Allow small tolerance for floating point

    def are_value(*args):
        """Check if all values are equal within a small tolerance"""
        target = args[-1]
        values = args[:-1]
        return all(is_value(value, target) for value in values)

    def exclude_reboot_short_walls(edge):
        """Exclude short walls that are a transition between the reboot slot and the finger grooves.

        The fillet here causes some problems breaking the part and the stl can't be printed.
        """
        # 68.8, 61.0  y, z
        # 20.4, 61.0  x, z
        v1 = edge.Vertexes[0]
        v2 = edge.Vertexes[1]
        if (
            are_value(v1.Point.z, v2.Point.z, 61.0)
            and (
                are_value(v1.Point.y, v2.Point.y, y_offset + sphere_radius)
                or are_value(
                    v1.Point.y, v2.Point.y, y_offset + sphere_radius + reboot_slot_thickness
                )
            )
            and (abs(v1.Point.x - v2.Point.x) < 5.0)
        ):
            # print(f"Found reboot excluded edge at z={v1.Point.z}: Edge{i + 1}")
            # print(f"  Coordinates: ({v1.Point.x}, {v1.Point.y}) to ({v2.Point.x}, {v2.Point.y})")
            return True
        return False

    def fillet_top_edges_at_height(shape, target_z, fillet_radius):
        # Fillet the top edges of the hollow box
        top_edges = []
        top_edge_indices = []
        for i, edge in enumerate(shape.Edges):
            # Get the vertices of the edge
            if len(edge.Vertexes) < 2:  # circles have only one vertex
                # The priority token needs a fillet
                if is_value(edge.Vertexes[0].Point.z, target_z):
                    top_edges.append(edge)
                continue
            if exclude_reboot_short_walls(edge):
                continue

            v1 = edge.Vertexes[0]
            v2 = edge.Vertexes[1]

            # Check if edge is at the top height (comparing Z coordinates)
            if is_value(v1.Point.z, v2.Point.z):  # is horizontal
                if is_value(v1.Point.z, target_z):  # and at the target height
                    top_edges.append(edge)
                    top_edge_indices.append(i + 1)

        return hollow_box.makeFillet(fillet_radius, top_edges)

    # Fillet edges at these heights
    top_points = (
        (0, Config.general_fillet_radius),
        (
            Config.card_width + Config.bottom_thickness + Config.player_thickness * 4,
            Config.top_fillet_radius,
        ),
        (inner_box.Placement.Base.z, Config.general_fillet_radius),
    )

    for top_height, fillet_radius in top_points:
        hollow_box = fillet_top_edges_at_height(hollow_box, top_height, fillet_radius)

    ##
    ## Fillet the edges at the top of the card slots
    ##
    # some edges are remnants of cut boxes and should not be filleted
    target_z = z_offset + slot_width - slot_width / 3  # fillet the top of the card slots

    # These coordinates lie on the edges that need to be excluded from filleting
    # Define specific coordinates to look for
    x_coords = [13.0, 106.0, 112.0, 205.0]
    y_coords = [13.0, 98.0, 307.0]

    # Get all edges at the specified Z height
    edges_at_z = []
    edges_index_at_z = []
    for i, edge in enumerate(hollow_box.Edges):
        # Skip circles at this level
        if len(edge.Vertexes) < 2:
            continue

        v1 = edge.Vertexes[0]
        v2 = edge.Vertexes[1]

        # Skip edges that are too short
        if edge.Length < Config.tolerance:
            continue

        # Check if both vertices are at the target Z height
        if (
            abs(v1.Point.z - target_z) < Config.tolerance
            and abs(v2.Point.z - target_z) < Config.tolerance
        ):
            # Check if edge contains any of our specific coordinates
            edge_has_target_coord = False
            for x in x_coords:
                if (
                    abs(v1.Point.x - x) < Config.tolerance
                    and abs(v2.Point.x - x) < Config.tolerance
                ):
                    edge_has_target_coord = True
                    break

            for y in y_coords:
                if (
                    abs(v1.Point.y - y) < Config.tolerance
                    and abs(v2.Point.y - y) < Config.tolerance
                ):
                    edge_has_target_coord = True
                    break

            if not edge_has_target_coord:
                edges_index_at_z.append(i + 1)
                # print(f"Found edge at z={v1.Point.z}: Edge{i + 1}")
                # print(f"  Coordinates: ({v1.Point.x}, {v1.Point.y}) to ({v2.Point.x}, {v2.Point.y})")
                edges_at_z.append(edge)

    print(f"Found {len(edges_at_z)} edges at z={target_z}")

    hollow_box = hollow_box.makeFillet(1, edges_at_z)

    # Experiment with cutting out the edges after filleting
    # Add centered cylinder cutout for front/back walls
    side_cylinder_radius = (
        Config.card_height / 2
    )  # Half of card height for radius (larger diameter)
    box_height = Config.card_width + Config.bottom_thickness + Config.player_thickness * 4

    # Create two shorter cylinders for front and back walls
    front_cylinder = Part.makeCylinder(
        side_cylinder_radius,
        wall_thickness * 12,  # Just enough to cut through front wall
        App.Vector(0, -wall_thickness * 4, 0),  # Start before front wall
        App.Vector(0, 1, 0),  # Along Y axis
    )

    back_cylinder = Part.makeCylinder(
        side_cylinder_radius,
        wall_thickness * 12,  # Just enough to cut through back wall
        App.Vector(0, Config.box_width - wall_thickness * 8, 0),  # Start before back wall
        App.Vector(0, 1, 0),  # Along Y axis
    )

    # Position cylinders centered on X and cutting 25mm down from top
    for i, cylinder in enumerate([front_cylinder, back_cylinder]):
        cylinder.translate(
            App.Vector(
                Config.box_width / 2,  # Center X
                0,
                box_height + (side_cylinder_radius - 25),  # Position so it cuts 25mm down
            )
        )
        # Add cylinders to document instead of cutting
        cylinder_shape = doc.addObject("Part::Feature", f"CutoutCylinder_{i+1}")
        cylinder_shape.ViewObject.hide()
        cylinder_shape.Shape = cylinder

        # Comment out the cut operation
        hollow_box = hollow_box.cut(cylinder)

    # Add to document
    box_shape = doc.addObject("Part::Feature", "Box")
    box_shape.Shape = hollow_box

    # Recompute the document
    doc.recompute()

    # Switch to isometric view and fit to window
    Gui.activeDocument().activeView().viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
