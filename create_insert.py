"""Create the Dim Sum Organizer insert geometry."""

import config
import FreeCAD
import Part


def create_container_cylinder():
    """Create the main horizontal container cylinder."""
    # Create a cylinder with diameter 63mm and height 13mm
    # The cylinder is horizontal, so we rotate it 90 degrees around Y axis
    cylinder = Part.makeCylinder(
        config.CONTAINER_RADIUS,
        config.CONTAINER_HEIGHT,
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(0, 1, 0),  # Direction vector for horizontal orientation
    )
    return cylinder


def create_circle_token_positive():
    """Create a positive (cutout) for circle tokens."""
    # Circle tokens: 40.2mm diameter, 6.2mm tall
    # Position horizontally, tangent to container edge, top surfaces aligned
    # Container height is 13mm, token height is 6.2mm
    # So token bottom should be at: 13 - 6.2 = 6.8mm from container bottom

    # Calculate position: container radius is 31.5mm, token radius is 20.1mm
    # For tangent to edge: center offset = container_radius - token_radius
    # = 31.5 - 20.1 = 11.4mm from container center

    # Since container is horizontal (along Y axis), we need to position along X axis
    # The token cylinder should also be horizontal (along Y axis)
    token_cylinder = Part.makeCylinder(
        config.CIRCLE_TOKEN_RADIUS,
        config.CIRCLE_TOKEN_HEIGHT,
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(0, 1, 0),  # Horizontal along Y axis
    )

    # # Position: offset in X direction by (container_radius - token_radius)
    # # Z position: bottom at 6.8mm, so center at 6.8 + token_height/2 = 6.8 + 3.1 = 9.9mm
    # x_offset = config.CONTAINER_RADIUS - config.CIRCLE_TOKEN_RADIUS
    # z_center = config.CONTAINER_HEIGHT - config.CIRCLE_TOKEN_RADIUS

    # token_cylinder.translate(FreeCAD.Vector(x_offset, 0, z_center))

    return token_cylinder


def create_oval_token():
    """Create a positive (cutout) for oval tokens."""
    # Oval tokens: 38mm x 30mm, 12.2mm tall
    # Two stacks, tangent to circle tokens
    # Tokens are vertical (standing up)

    # Create an ellipse for the base in XY plane
    # Major axis: 38mm, Minor axis: 30mm
    ellipse = Part.Ellipse(
        FreeCAD.Vector(0, 0, 0),  # Center
        config.OVAL_TOKEN_MAJOR_RADIUS,  # Major radius (along X)
        config.OVAL_TOKEN_MINOR_RADIUS,  # Minor radius (along Y)
    )

    # Create an edge from the ellipse (this creates a closed edge)
    edge = Part.Edge(ellipse)

    # Create a wire from the edge
    wire = Part.Wire([edge])

    # Create a face from the closed wire using makeFace
    face = Part.makeFace(wire, "Part::FaceMakerSimple")

    # Extrude vertically (along Z axis) to create the oval token shape
    # Height is 12.2mm
    oval_shape = face.extrude(FreeCAD.Vector(0, 0, config.OVAL_TOKEN_HEIGHT))

    return oval_shape


def calculate_oval_positions():
    """Calculate positions for the two oval token stacks relative to circle tokens."""
    # Circle token center is at x_offset = 11.4mm from container center
    # Circle token radius = 20.1mm
    # Oval token major radius = 19mm, minor radius = 15mm

    # Circle token is horizontal (along Y axis), centered at:
    circle_center_x = config.CONTAINER_RADIUS - config.CIRCLE_TOKEN_RADIUS

    # For tangency with vertical oval tokens:
    # The oval tokens are vertical, so their base is a circle/ellipse in XY plane
    # Distance from circle center to oval center = circle_radius + oval_minor_radius
    # (using minor radius for side-by-side positioning)
    distance = config.CIRCLE_TOKEN_RADIUS + config.OVAL_TOKEN_MINOR_RADIUS - 7

    # Oval tokens: lowest point is 1mm above bottom
    # So oval bottom should be at z = 1mm
    # Oval center Z = 1.0 + 12.2/2 = 1.0 + 6.1 = 7.1mm
    oval_center_z = 1.0 + config.OVAL_TOKEN_HEIGHT / 2.0

    # Position two ovals on either side of the circle (in X direction)
    # One to the left (negative X), one to the right (positive X)
    # The oval's minor axis should be aligned with the line to the disc center for tangency
    y_offset = -1 * (config.OVAL_TOKEN_MINOR_RADIUS - config.CONTAINER_HEIGHT + 1.5)

    positions = [
        FreeCAD.Vector(-24.943, y_offset, 5.302),
        FreeCAD.Vector(4.952, y_offset, -24.805),
    ]

    return positions


def create_insert(doc):
    """Create the complete insert geometry and token objects."""
    # Start with the container cylinder
    container = create_container_cylinder()

    # Validate container
    if container.isNull():
        raise ValueError("Container shape is null")

    # Create circle token positive (cutout)
    FreeCAD.Console.PrintMessage("Creating circle token...\n")
    circle_token = create_circle_token_positive()

    # Validate circle token
    if circle_token.isNull():
        raise ValueError("Circle token shape is null")
    FreeCAD.Console.PrintMessage(
        f"Circle token created successfully. IsNull: {circle_token.isNull()}\n"
    )

    circle_offset = config.CONTAINER_RADIUS - config.CIRCLE_TOKEN_RADIUS
    circle_token.translate(FreeCAD.Vector(circle_offset, 0, circle_offset))

    # Calculate positions for oval tokens
    FreeCAD.Console.PrintMessage("Calculating oval token positions...\n")
    oval_positions = calculate_oval_positions()
    FreeCAD.Console.PrintMessage(
        f"Found {len(oval_positions)} oval positions: {[str(p) for p in oval_positions]}\n"
    )

    # Create two oval token cutouts at their positions
    oval_tokens = []
    for i, pos in enumerate(oval_positions):
        FreeCAD.Console.PrintMessage(f"Processing oval token {i+1} at position {pos}\n")

        # Create a new oval token at the specified position
        oval_shape = create_oval_token()

        # Validate the shape
        if oval_shape.isNull():
            FreeCAD.Console.PrintError(f"Oval token {i+1} shape is null!\n")
            raise ValueError(f"Oval token shape is null at position {pos}")

        FreeCAD.Console.PrintMessage(f"Oval token {i+1} created. IsNull: {oval_shape.isNull()}\n")

        # Position the token at the specified location
        # The pos is the center position, but ellipse should be at base z
        # Create ellipse at base (x, y from pos, z = pos.z - height/2)
        base_pos = FreeCAD.Vector(pos.x, pos.y, pos.z - config.OVAL_TOKEN_HEIGHT / 2.0)

        # Translate to position
        oval_shape.translate(pos)
        FreeCAD.Console.PrintMessage(f"Oval token {i+1} translated to {pos}\n")

        # Rotate first oval token (index 0) by 90 degrees around Y axis
        if i == 0:
            FreeCAD.Console.PrintMessage(
                f"Rotating oval token {i+1} by 102 degrees around Y axis\n"
            )
            # Rotate around the center position (pos)
            oval_shape.rotate(
                pos,  # Rotation center
                FreeCAD.Vector(0, 1, 0),  # Y axis
                102.0,  # Angle in degrees
            )
        else:
            FreeCAD.Console.PrintMessage(
                f"Rotating oval token {i+1} by 348 degrees around Y axis\n"
            )
            oval_shape.rotate(
                pos,  # Rotation center
                FreeCAD.Vector(0, 1, 0),  # Y axis
                348.0,  # Angle in degrees
            )

        # Add to document for visualization
        FreeCAD.Console.PrintMessage(f"Adding oval token {i+1} to document as 'OvalToken_{i+1}'\n")
        try:
            feature = doc.addObject("Part::Feature", f"OvalToken_{i+1}")
            if feature is None:
                FreeCAD.Console.PrintError(f"doc.addObject returned None for OvalToken_{i+1}!\n")
            else:
                feature.Shape = oval_shape
                FreeCAD.Console.PrintMessage(
                    f"Feature 'OvalToken_{i+1}' created. Shape assigned. "
                    f"IsNull: {feature.Shape.isNull()}, "
                    f"Volume: {feature.Shape.Volume}, "
                    f"Type: {type(feature)}\n"
                )
                # Check if shape is valid
                if feature.Shape.isNull():
                    FreeCAD.Console.PrintError(
                        f"WARNING: Feature 'OvalToken_{i+1}' has null shape!\n"
                    )
                else:
                    FreeCAD.Console.PrintMessage(
                        f"Feature 'OvalToken_{i+1}' shape is valid. "
                        f"Bounding box: {feature.Shape.BoundBox}\n"
                    )
        except Exception as e:
            FreeCAD.Console.PrintError(
                f"Exception creating feature OvalToken_{i+1}: {type(e).__name__}: {e}\n"
            )
            import traceback

            FreeCAD.Console.PrintError(traceback.format_exc())

        oval_tokens.append(oval_shape)
        FreeCAD.Console.PrintMessage(
            f"Oval token {i+1} added to cutouts list. Total: {len(oval_tokens)}\n"
        )

    # Add circle token to document
    FreeCAD.Console.PrintMessage("Adding circle token to document...\n")
    feature = doc.addObject("Part::Feature", "CircleToken")
    feature.Shape = circle_token
    FreeCAD.Console.PrintMessage("CircleToken feature created successfully\n")

    # Combine all cutouts
    FreeCAD.Console.PrintMessage(
        f"Combining {len(oval_tokens)} oval tokens with circle token for cutting\n"
    )
    all_cutouts = [circle_token] + oval_tokens

    # Cut the container with all the token cutouts
    FreeCAD.Console.PrintMessage("Starting cut operations...\n")
    for i, cutout in enumerate(all_cutouts):
        FreeCAD.Console.PrintMessage(
            f"Cut operation {i+1}/{len(all_cutouts)}: {'CircleToken' if i == 0 else f'OvalToken_{i}'}\n"
        )
        try:
            container = container.cut(cutout)
            if container.isNull():
                FreeCAD.Console.PrintError(f"Cut operation {i} resulted in null shape!\n")
                raise ValueError(f"Cut operation {i} resulted in null shape")
            FreeCAD.Console.PrintMessage(f"Cut operation {i+1} completed successfully\n")
        except Exception as e:
            FreeCAD.Console.PrintError(f"Cut operation {i} failed: {e}\n")
            raise ValueError(f"Cut operation {i} failed: {e}")

    # Add insert to document
    FreeCAD.Console.PrintMessage("Adding insert to document...\n")
    feature = doc.addObject("Part::Feature", "Insert")
    feature.Shape = container
    FreeCAD.Console.PrintMessage("Insert feature created successfully\n")
    return feature


def create_oval_token_object_at_position(pos, rotate_90=False):
    """Create an actual oval token object at the specified position (for visualization)."""
    # The pos is the center position, but ellipse should be at base z
    # Create ellipse at base (x, y from pos, z = pos.z - height/2)
    base_pos = FreeCAD.Vector(pos.x, pos.y, pos.z - config.OVAL_TOKEN_HEIGHT / 2.0)

    ellipse = Part.Ellipse(
        base_pos,  # Center at base position (will be in XY plane at base z)
        config.OVAL_TOKEN_MAJOR_RADIUS,  # Major radius (along X)
        config.OVAL_TOKEN_MINOR_RADIUS,  # Minor radius (along Y)
    )

    # Create edge, wire, and face
    edge = Part.Edge(ellipse)
    wire = Part.Wire([edge])
    face = Part.makeFace(wire, "Part::FaceMakerSimple")

    # Extrude vertically upward
    oval_shape = face.extrude(FreeCAD.Vector(0, 0, config.OVAL_TOKEN_HEIGHT))

    # Rotate by 90 degrees around Y axis if requested
    if rotate_90:
        oval_shape.rotate(
            FreeCAD.Vector(pos.x, pos.y, pos.z),  # Rotation center
            FreeCAD.Vector(0, 1, 0),  # Y axis
            90.0,  # Angle in degrees
        )

    return oval_shape
