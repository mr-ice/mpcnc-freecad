"""Create the Dim Sum Organizer insert that fits between baskets."""

import math

import config
import FreeCAD
import Part


def create_base_cylinder():
    """Create the base cylinder that is 3mm larger than BASKET_SEPARATION."""
    # Base diameter = BASKET_SEPARATION + 3mm
    base_diameter = config.BASKET_SEPARATION + 3.0
    base_radius = base_diameter / 2.0
    # Reduce height by lid thickness
    base_height = config.BASKET_HEIGHT - config.LID_THICKNESS

    # Create vertical cylinder
    cylinder = Part.makeCylinder(
        base_radius,
        base_height,
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(0, 0, 1),  # Vertical (Z axis)
    )

    return cylinder


def create_lid():
    """Create the lid."""
    # Lid diameter = BASKET_SEPARATION + 3mm (same as base)
    lid_diameter = config.BASKET_SEPARATION + 3.0
    lid_radius = lid_diameter / 2.0
    lid_height = config.LID_THICKNESS

    # Create vertical cylinder for lid
    lid = Part.makeCylinder(
        lid_radius,
        lid_height,
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(0, 0, 1),  # Vertical (Z axis)
    )

    return lid


def calculate_basket_positions():
    """Calculate positions of 6 baskets arranged in a circle."""
    # 6 baskets at 60-degree intervals
    # Center-to-center distance between opposite baskets = BASKET_SEPARATION + BASKET_DIAMETER
    # So radius = (BASKET_SEPARATION + BASKET_DIAMETER) / 2
    center_separation = config.BASKET_SEPARATION + config.BASKET_DIAMETER
    basket_radius = center_separation / 2.0
    positions = []

    FreeCAD.Console.PrintMessage(
        f"Basket center separation: {center_separation}mm, " f"Circle radius: {basket_radius}mm\n"
    )

    for i in range(6):
        angle = math.radians(i * 60)  # 60 degrees per basket
        x = basket_radius * math.cos(angle)
        y = basket_radius * math.sin(angle)
        positions.append(FreeCAD.Vector(x, y, 0))
        FreeCAD.Console.PrintMessage(f"Basket {i+1} position: ({x:.2f}, {y:.2f}, 0)\n")

    return positions


def create_basket_cylinders():
    """Create 6 cylinders representing the baskets."""
    basket_positions = calculate_basket_positions()
    basket_radius = config.BASKET_DIAMETER / 2.0
    basket_height = config.BASKET_HEIGHT

    cylinders = []
    for i, pos in enumerate(basket_positions):
        cylinder = Part.makeCylinder(
            basket_radius,
            basket_height,
            pos,
            FreeCAD.Vector(0, 0, 1),  # Vertical (Z axis)
        )
        cylinders.append(cylinder)

    return cylinders


def create_circle_token_positive(position):
    """Create a positive (protruding) circle token on the lid, shrunk by 0.5mm diameter."""
    # Shrink diameter by 0.5mm, so radius reduced by 0.25mm
    shrunk_radius = config.CIRCLE_TOKEN_RADIUS - 0.25
    # Protrude above lid surface
    protrusion_height = config.TOKEN_PROTRUSION_HEIGHT

    # Position at the same location as the cutout, but at top of lid
    # The position passed in is the cutout position, we need to adjust Z
    # Token should start at top of lid (LID_THICKNESS) and protrude above
    lid_z = config.LID_THICKNESS  # Start at top of lid surface

    token_position = FreeCAD.Vector(position.x, position.y, lid_z)

    # Create vertical cylinder (along Z axis) for the positive token
    token_cylinder = Part.makeCylinder(
        shrunk_radius,
        protrusion_height,
        token_position,
        FreeCAD.Vector(0, 0, 1),  # Vertical (Z axis)
    )

    FreeCAD.Console.PrintMessage(
        f"Circle token positive created at position {token_position}, "
        f"radius: {shrunk_radius}mm, height: {protrusion_height}mm\n"
    )

    return token_cylinder


def create_oval_token_positive(position, rotation_angle=0.0):
    """Create a positive (protruding) oval token on the lid, shrunk by 0.5mm diameter."""
    # Shrink by 0.5mm diameter means reduce both radii by 0.25mm
    shrunk_major_radius = config.OVAL_TOKEN_MAJOR_RADIUS - 0.25
    shrunk_minor_radius = config.OVAL_TOKEN_MINOR_RADIUS - 0.25
    # Protrude above lid surface
    protrusion_height = config.TOKEN_PROTRUSION_HEIGHT

    # Position at the same location as the cutout, but at top of lid
    # Token should start at top of lid (LID_THICKNESS) and protrude above
    lid_z = config.LID_THICKNESS  # Start at top of lid surface

    token_position = FreeCAD.Vector(position.x, position.y, lid_z)

    # Create ellipse in XY plane
    ellipse = Part.Ellipse(
        token_position,  # Center at position
        shrunk_major_radius,  # Major radius (along X)
        shrunk_minor_radius,  # Minor radius (along Y)
    )

    # Create edge, wire, and face
    edge = Part.Edge(ellipse)
    wire = Part.Wire([edge])
    face = Part.makeFace(wire, "Part::FaceMakerSimple")

    # Extrude vertically (along Z) upward
    oval_shape = face.extrude(FreeCAD.Vector(0, 0, protrusion_height))

    # Rotate around Z axis if specified
    if rotation_angle != 0.0:
        oval_shape.rotate(
            token_position,  # Rotation center at position
            FreeCAD.Vector(0, 0, 1),  # Z axis
            rotation_angle,  # Rotation angle in degrees
        )

    FreeCAD.Console.PrintMessage(
        f"Oval token positive created at position {token_position}, "
        f"major radius: {shrunk_major_radius}mm, minor radius: {shrunk_minor_radius}mm, "
        f"height: {protrusion_height}mm, rotation: {rotation_angle}°\n"
    )

    return oval_shape


def create_circle_token_cutout():
    """Create a circle token cylinder cutout positioned between two basket holes."""
    # Position the circle token between two adjacent baskets
    # Baskets are at 60-degree intervals, so position at 30 degrees (between 0° and 60°)
    # Position at 30 degrees (halfway between baskets at 0° and 60°)
    angle = math.radians(30)
    # Position at about 2/3 of the way to the basket radius
    # Move 1mm toward center from original position
    token_radius = config.CIRCLE_TOKEN_RADIUS - 1.0
    x_offset = token_radius * math.cos(angle)
    y_offset = token_radius * math.sin(angle)
    # Position at the top of the base (reduced by lid thickness)
    # Token bottom at new top - token height
    base_height = config.BASKET_HEIGHT - config.LID_THICKNESS
    z_position = base_height - config.CIRCLE_TOKEN_HEIGHT

    token_position = FreeCAD.Vector(x_offset, y_offset, z_position)

    FreeCAD.Console.PrintMessage(
        f"Circle token positioned between baskets at angle 30°, "
        f"radius: {token_radius:.2f}mm, position: ({x_offset:.2f}, {y_offset:.2f}, {z_position:.2f})\n"
    )

    # Create horizontal cylinder (along Y axis) for the circle token
    token_cylinder = Part.makeCylinder(
        config.CIRCLE_TOKEN_RADIUS,
        config.CIRCLE_TOKEN_HEIGHT,
        token_position,
        FreeCAD.Vector(0, 0, 1),  # Horizontal along Y axis
    )

    FreeCAD.Console.PrintMessage(
        f"Circle token cutout created at position {token_position}, "
        f"radius: {config.CIRCLE_TOKEN_RADIUS}mm, height: {config.CIRCLE_TOKEN_HEIGHT}mm\n"
    )

    return token_cylinder


def create_oval_token_cutout(position, rotation_angle=0.0):
    """Create an oval token cutout at the specified position (horizontal, oval face up).

    Args:
        position: Center position of the oval
        rotation_angle: Rotation angle in degrees around Z axis (vertical)
    """
    # Create ellipse in XY plane (horizontal, oval face up)
    ellipse = Part.Ellipse(
        position,  # Center at position
        config.OVAL_TOKEN_MAJOR_RADIUS,  # Major radius (along X)
        config.OVAL_TOKEN_MINOR_RADIUS,  # Minor radius (along Y)
    )

    # Create edge, wire, and face
    edge = Part.Edge(ellipse)
    wire = Part.Wire([edge])
    face = Part.makeFace(wire, "Part::FaceMakerSimple")

    # Extrude vertically (along Z) to create the oval token shape
    oval_shape = face.extrude(FreeCAD.Vector(0, 0, config.OVAL_TOKEN_HEIGHT))

    # Rotate around Z axis if specified
    if rotation_angle != 0.0:
        oval_shape.rotate(
            position,  # Rotation center at position
            FreeCAD.Vector(0, 0, 1),  # Z axis
            rotation_angle,  # Rotation angle in degrees
        )

    return oval_shape


def create_finger_access_cylinder(oval_positions):
    """Create a finger access cylinder positioned between the two ovals."""
    # Calculate position between the two ovals
    # Ovals are at angles 150° and 270°
    # Position at the midpoint, slightly off center

    # Get the two oval positions
    pos1 = oval_positions[0]
    pos2 = oval_positions[1]

    # Calculate midpoint between the two ovals
    mid_x = (pos1.x + pos2.x) / 2.0
    mid_y = (pos1.y + pos2.y) / 2.0

    # Move away from center to avoid intersecting circle token
    # Increase the distance from center
    offset_factor = 1.3  # Move 30% away from center
    mid_x = mid_x * offset_factor
    mid_y = mid_y * offset_factor

    # Check distance from circle token and adjust if too close
    circle_token_radius = config.CIRCLE_TOKEN_RADIUS
    circle_angle = math.radians(30)
    circle_x = circle_token_radius * math.cos(circle_angle)
    circle_y = circle_token_radius * math.sin(circle_angle)

    dist_from_circle = math.sqrt((mid_x - circle_x) ** 2 + (mid_y - circle_y) ** 2)
    min_separation = config.CIRCLE_TOKEN_RADIUS + 10.0 + 2.0  # finger_radius + clearance

    if dist_from_circle < min_separation:
        # Move further away from center
        current_dist = math.sqrt(mid_x**2 + mid_y**2)
        target_dist = current_dist * 1.5  # Move 50% further out
        if current_dist > 0:
            mid_x = mid_x * (target_dist / current_dist)
            mid_y = mid_y * (target_dist / current_dist)

    # Z position: start at bottom of base to extend all the way through
    z_position = 0.0

    finger_position = FreeCAD.Vector(mid_x, mid_y, z_position)

    # Create a cylinder for finger access
    # Make it large enough for a finger to reach in
    # Extend all the way through the base
    finger_radius = 10.0  # mm - comfortable finger size
    finger_height = config.BASKET_HEIGHT * 1.5  # Tall enough to extend through entire base

    finger_cylinder = Part.makeCylinder(
        finger_radius,
        finger_height,
        finger_position,
        FreeCAD.Vector(0, 0, 1),  # Vertical (Z axis)
    )

    FreeCAD.Console.PrintMessage(
        f"Finger access cylinder created at position {finger_position}, "
        f"radius: {finger_radius}mm, height: {finger_height}mm\n"
    )

    return finger_cylinder


def calculate_oval_token_positions(circle_token_pos):
    """Calculate positions for two oval tokens that don't intersect circle token or base edges."""
    base_radius = (config.BASKET_SEPARATION) / 2.0
    circle_token_radius = config.CIRCLE_TOKEN_RADIUS

    # Circle token is at 30 degrees
    circle_angle = math.radians(30)

    # Position ovals at angles away from the circle token
    # Try 150° and 210° (or -30° and 90°)
    # Make sure they fit within base and don't intersect circle token

    # Check distance from circle token
    # Circle token is at (circle_token_radius * cos(30°), circle_token_radius * sin(30°))
    circle_x = circle_token_radius * math.cos(circle_angle)
    circle_y = circle_token_radius * math.sin(circle_angle)

    positions = []
    rotations = []
    # Position ovals 120 degrees from circle token (at 30°)
    # So ovals should be at: 30° + 120° = 150° and 30° + 240° = 270°
    test_angles = [150, 270]  # 120° away from circle token

    # Oval 1: rotate 300° around its center, then position so outer edge is 0.8mm inside base
    # Oval 2: move toward center until outer edge is 0.8mm inside base

    for i, angle_deg in enumerate(test_angles):
        angle = math.radians(angle_deg)

        # Set rotations
        if i == 0:
            rotation = 240.0  # Oval 1: rotate 240° around its center
        else:
            rotation = 0.0  # Oval 2: no rotation

        # Position oval center at base_radius - minor_radius - 0.8 from center
        # This ensures the outer edge (center + minor_radius) is at base_radius - 0.8
        # Move 3mm toward center
        test_radius = base_radius - config.OVAL_TOKEN_MINOR_RADIUS + 1
        x = test_radius * math.cos(angle)
        y = test_radius * math.sin(angle)

        # Check distance from circle token center
        dist_from_circle = math.sqrt((x - circle_x) ** 2 + (y - circle_y) ** 2)
        # min_separation = (
        #     config.CIRCLE_TOKEN_RADIUS + config.OVAL_TOKEN_MAJOR_RADIUS + 3.0
        # )  # 3mm clearance

        # if dist_from_circle < min_separation:
        #     # Adjust radius to maintain separation from circle token
        #     # Move closer to center if needed
        #     test_radius = min_separation * 0.7
        #     x = test_radius * math.cos(angle)
        #     y = test_radius * math.sin(angle)

        # Z position: align top of oval with top of base (reduced by lid thickness)
        base_height = config.BASKET_HEIGHT - config.LID_THICKNESS
        z_position = base_height - config.OVAL_TOKEN_HEIGHT

        positions.append(FreeCAD.Vector(x, y, z_position))
        rotations.append(rotation)

        FreeCAD.Console.PrintMessage(
            f"Oval token {i+1} at angle {angle_deg}°, radius: {test_radius:.2f}mm, "
            f"position: ({x:.2f}, {y:.2f}, {z_position:.2f}), "
            f"rotation: {rotation}°, "
            f"distance from circle token: {dist_from_circle:.2f}mm\n"
        )

    return positions, rotations


def create_basket_insert(doc):
    """Create the basket insert with base and basket cutouts."""
    FreeCAD.Console.PrintMessage("Creating basket insert...\n")

    # Create base cylinder
    FreeCAD.Console.PrintMessage("Creating base cylinder...\n")
    base = create_base_cylinder()
    FreeCAD.Console.PrintMessage(
        f"Base cylinder created. Radius: {config.BASKET_SEPARATION / 2.0 + 1.5}mm, "
        f"Height: {config.BASKET_HEIGHT}mm\n"
    )

    # Create basket cylinders
    FreeCAD.Console.PrintMessage("Creating basket cylinders...\n")
    basket_cylinders = create_basket_cylinders()
    FreeCAD.Console.PrintMessage(f"Created {len(basket_cylinders)} basket cylinders\n")

    # Add basket cylinders to document for visualization
    for i, basket_cyl in enumerate(basket_cylinders):
        feature = doc.addObject("Part::Feature", f"Basket_{i+1}")
        feature.Shape = basket_cyl
        if FreeCAD.GuiUp:
            feature.ViewObject.ShapeColor = (1.0, 0.5, 0.5)  # Light red

    # Cut base with basket cylinders to remove basket areas
    FreeCAD.Console.PrintMessage("Cutting base with basket cylinders...\n")
    for i, basket_cyl in enumerate(basket_cylinders):
        FreeCAD.Console.PrintMessage(f"Cutting base with basket {i+1}...\n")
        try:
            base = base.cut(basket_cyl)
            if base.isNull():
                FreeCAD.Console.PrintError(f"Cut with basket {i+1} resulted in null shape!\n")
                raise ValueError(f"Cut with basket {i+1} resulted in null shape")
            FreeCAD.Console.PrintMessage(
                f"Successfully cut with basket {i+1}. Remaining volume: {base.Volume}\n"
            )
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error cutting with basket {i+1}: {e}\n")
            raise

    # Create and cut circle token
    FreeCAD.Console.PrintMessage("Creating circle token cutout...\n")
    circle_token_cutout = create_circle_token_cutout()

    # Add circle token to document for visualization
    circle_feature = doc.addObject("Part::Feature", "CircleToken")
    circle_feature.Shape = circle_token_cutout
    if FreeCAD.GuiUp:
        circle_feature.ViewObject.ShapeColor = (0.5, 0.8, 1.0)  # Light blue

    # Cut base with circle token
    FreeCAD.Console.PrintMessage("Cutting base with circle token...\n")
    try:
        base = base.cut(circle_token_cutout)
        if base.isNull():
            FreeCAD.Console.PrintError("Cut with circle token resulted in null shape!\n")
            raise ValueError("Cut with circle token resulted in null shape")
        FreeCAD.Console.PrintMessage(
            f"Successfully cut with circle token. Remaining volume: {base.Volume}\n"
        )
    except Exception as e:
        FreeCAD.Console.PrintError(f"Error cutting with circle token: {e}\n")
        raise

    # Create and cut oval tokens
    FreeCAD.Console.PrintMessage("Creating oval token cutouts...\n")
    base_height = config.BASKET_HEIGHT - config.LID_THICKNESS
    circle_token_pos = FreeCAD.Vector(
        (config.CIRCLE_TOKEN_RADIUS - 1.0) * math.cos(math.radians(30)),
        (config.CIRCLE_TOKEN_RADIUS - 1.0) * math.sin(math.radians(30)),
        base_height - config.CIRCLE_TOKEN_HEIGHT,
    )
    oval_positions, oval_rotations = calculate_oval_token_positions(circle_token_pos)

    oval_cutouts = []
    for i, (pos, rotation) in enumerate(zip(oval_positions, oval_rotations)):
        FreeCAD.Console.PrintMessage(
            f"Creating oval token cutout {i+1} with rotation {rotation}°...\n"
        )
        oval_cutout = create_oval_token_cutout(pos, rotation_angle=rotation)
        oval_cutouts.append(oval_cutout)

        # Add to document for visualization
        oval_feature = doc.addObject("Part::Feature", f"OvalToken_{i+1}")
        oval_feature.Shape = oval_cutout
        if FreeCAD.GuiUp:
            oval_feature.ViewObject.ShapeColor = (0.5, 1.0, 0.8)  # Light green

    # Cut base with oval tokens
    FreeCAD.Console.PrintMessage("Cutting base with oval tokens...\n")
    for i, oval_cutout in enumerate(oval_cutouts):
        FreeCAD.Console.PrintMessage(f"Cutting base with oval token {i+1}...\n")
        try:
            base = base.cut(oval_cutout)
            if base.isNull():
                FreeCAD.Console.PrintError(f"Cut with oval token {i+1} resulted in null shape!\n")
                raise ValueError(f"Cut with oval token {i+1} resulted in null shape")
            FreeCAD.Console.PrintMessage(
                f"Successfully cut with oval token {i+1}. Remaining volume: {base.Volume}\n"
            )
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error cutting with oval token {i+1}: {e}\n")
            raise

    # Create and cut finger access cylinder
    FreeCAD.Console.PrintMessage("Creating finger access cylinder...\n")
    finger_cylinder = create_finger_access_cylinder(oval_positions)

    # Add to document for visualization
    finger_feature = doc.addObject("Part::Feature", "FingerAccess")
    finger_feature.Shape = finger_cylinder
    if FreeCAD.GuiUp:
        finger_feature.ViewObject.ShapeColor = (1.0, 1.0, 0.5)  # Light yellow

    # Cut base with finger access cylinder
    FreeCAD.Console.PrintMessage("Cutting base with finger access cylinder...\n")
    try:
        base = base.cut(finger_cylinder)
        if base.isNull():
            FreeCAD.Console.PrintError("Cut with finger access cylinder resulted in null shape!\n")
            raise ValueError("Cut with finger access cylinder resulted in null shape")
        FreeCAD.Console.PrintMessage(
            f"Successfully cut with finger access cylinder. Remaining volume: {base.Volume}\n"
        )
    except Exception as e:
        FreeCAD.Console.PrintError(f"Error cutting with finger access cylinder: {e}\n")
        raise

    # Add final insert to document
    FreeCAD.Console.PrintMessage("Adding insert to document...\n")
    feature = doc.addObject("Part::Feature", "Insert")
    feature.Shape = base
    FreeCAD.Console.PrintMessage("Insert feature created successfully\n")

    # Create lid with positive tokens
    FreeCAD.Console.PrintMessage("Creating lid...\n")
    lid = create_lid()

    # Cut basket holes from lid (same positions as base)
    FreeCAD.Console.PrintMessage("Cutting basket holes from lid...\n")
    basket_cylinders = create_basket_cylinders()
    for i, basket_cyl in enumerate(basket_cylinders):
        try:
            lid = lid.cut(basket_cyl)
            if lid.isNull():
                FreeCAD.Console.PrintError(
                    f"Cut with basket {i+1} resulted in null shape on lid!\n"
                )
                raise ValueError(f"Cut with basket {i+1} resulted in null shape on lid")
            FreeCAD.Console.PrintMessage(
                f"Successfully cut basket {i+1} from lid. Remaining volume: {lid.Volume}\n"
            )
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error cutting basket {i+1} from lid: {e}\n")
            raise

    # Get positions for positive tokens (same XY as cutouts, but for lid)
    base_height = config.BASKET_HEIGHT - config.LID_THICKNESS
    circle_token_cutout_pos = FreeCAD.Vector(
        (config.CIRCLE_TOKEN_RADIUS - 1.0) * math.cos(math.radians(30)),
        (config.CIRCLE_TOKEN_RADIUS - 1.0) * math.sin(math.radians(30)),
        base_height - config.CIRCLE_TOKEN_HEIGHT,  # Same Z as cutout
    )

    # Create positive circle token on lid
    FreeCAD.Console.PrintMessage("Creating positive circle token on lid...\n")
    circle_positive = create_circle_token_positive(circle_token_cutout_pos)
    lid = lid.fuse(circle_positive)

    # Create positive oval tokens on lid
    FreeCAD.Console.PrintMessage("Creating positive oval tokens on lid...\n")
    for i, (pos, rotation) in enumerate(zip(oval_positions, oval_rotations)):
        FreeCAD.Console.PrintMessage(f"Creating positive oval token {i+1} on lid...\n")
        oval_positive = create_oval_token_positive(pos, rotation_angle=rotation)
        lid = lid.fuse(oval_positive)

    # Add finger hole through lid
    FreeCAD.Console.PrintMessage("Adding finger hole to lid...\n")
    # Calculate finger position (same XY as base, but at lid z=0)
    pos1 = oval_positions[0]
    pos2 = oval_positions[1]
    mid_x = (pos1.x + pos2.x) / 2.0
    mid_y = (pos1.y + pos2.y) / 2.0
    offset_factor = 1.3  # Same as base
    mid_x = mid_x * offset_factor
    mid_y = mid_y * offset_factor

    # Check distance from circle token and adjust if needed (same logic as base)
    circle_token_radius = config.CIRCLE_TOKEN_RADIUS
    circle_angle = math.radians(30)
    circle_x = circle_token_radius * math.cos(circle_angle)
    circle_y = circle_token_radius * math.sin(circle_angle)
    dist_from_circle = math.sqrt((mid_x - circle_x) ** 2 + (mid_y - circle_y) ** 2)
    min_separation = config.CIRCLE_TOKEN_RADIUS + 10.0 + 2.0

    if dist_from_circle < min_separation:
        current_dist = math.sqrt(mid_x**2 + mid_y**2)
        target_dist = current_dist * 1.5
        if current_dist > 0:
            mid_x = mid_x * (target_dist / current_dist)
            mid_y = mid_y * (target_dist / current_dist)

    finger_pos_lid = FreeCAD.Vector(mid_x, mid_y, 0.0)  # Start at bottom of lid
    finger_radius = 10.0
    finger_height = config.LID_THICKNESS * 1.5  # Tall enough to go through lid

    finger_cylinder_lid = Part.makeCylinder(
        finger_radius,
        finger_height,
        finger_pos_lid,
        FreeCAD.Vector(0, 0, 1),  # Vertical (Z axis)
    )
    lid = lid.cut(finger_cylinder_lid)

    # Add lid to document
    FreeCAD.Console.PrintMessage("Adding lid to document...\n")
    lid_feature = doc.addObject("Part::Feature", "Lid")
    lid_feature.Shape = lid
    if FreeCAD.GuiUp:
        lid_feature.ViewObject.ShapeColor = (0.8, 0.8, 0.8)  # Light gray
    FreeCAD.Console.PrintMessage("Lid feature created successfully\n")

    return feature
