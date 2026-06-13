"""
Tool Organizer FreeCAD Model Generator
Creates a tool organizer box with configurable compartments
"""

import config
import FreeCAD
import Part
import voltmeter_config as vm_config


def get_floor_height_info(voltmeter_top_z=None):
    """
    Calculates floor height information for different sections

    Args:
        voltmeter_top_z: Top Z coordinate of voltmeter hole

    Returns
    -------
        dict: Floor height information with:
            - floor_sections: List of dicts with x_start, x_end, floor_z, floor_height
            - transitions: List of X positions where floor height changes
    """
    import voltmeter_config as vm_config

    if voltmeter_top_z is None:
        # No voltmeter, floor is at bottom (wall thickness)
        return {
            "floor_sections": [
                {
                    "x_start": 0,
                    "x_end": config.BASE_LENGTH,
                    "floor_z": config.OUTER_WALL_THICKNESS,
                    "floor_height": config.BASE_HEIGHT - config.OUTER_WALL_THICKNESS,
                }
            ],
            "transitions": [],
        }

    # Calculate X positions for different floor sections
    voltmeter_x_start = config.OUTER_WALL_THICKNESS
    extra_1_x_end = voltmeter_x_start + vm_config.EXTRA_BIT_1_WIDTH

    # After extra_3
    extra_3_x_start = (
        voltmeter_x_start
        + vm_config.EXTRA_BIT_1_WIDTH
        + vm_config.EXTRA_BIT_2_WIDTH
        + vm_config.EXTRA_BIT_2_TRANSLATE
    )
    extra_3_x_end = extra_3_x_start + vm_config.EXTRA_BIT_3_WIDTH
    main_body_after_x = extra_3_x_end

    # Voltmeter extends to
    voltmeter_x_end = voltmeter_x_start + vm_config.VOLTMETER_LENGTH

    # Floor sits on top of voltmeter, extends to BASE_HEIGHT
    floor_z = voltmeter_top_z
    floor_height = config.BASE_HEIGHT - floor_z

    floor_sections = [
        {
            "x_start": voltmeter_x_start,
            "x_end": extra_1_x_end,
            "floor_z": floor_z,
            "floor_height": floor_height,
        },
        {
            "x_start": main_body_after_x,
            "x_end": voltmeter_x_end,
            "floor_z": floor_z,
            "floor_height": floor_height,
        },
        {
            "x_start": voltmeter_x_end,
            "x_end": config.BASE_LENGTH,
            "floor_z": floor_z,
            "floor_height": floor_height,
        },
    ]

    transitions = [extra_1_x_end, main_body_after_x, voltmeter_x_end]

    return {"floor_sections": floor_sections, "transitions": transitions}


def create_compartment_holes(floor_info):
    """
    Creates individual compartment holes based on COMPARTMENTS config
    Handles multiple compartments in same X slot with even Y distribution

    Args:
        floor_info: Floor height information dict from get_floor_height_info

    Returns
    -------
        Part.Shape or None: Combined shape of all compartment holes
    """
    if not config.COMPARTMENTS:
        return None

    # Calculate available Y space
    available_y = config.BASE_WIDTH - (2 * config.OUTER_WALL_THICKNESS)
    internal_y_start = config.OUTER_WALL_THICKNESS

    holes = []
    current_x = config.OUTER_WALL_THICKNESS  # Start at internal X position

    for slot in config.COMPARTMENTS:
        # Parse slot: either [list_of_names, width] or [name, width]
        if isinstance(slot[0], list):
            # Multiple compartments in this slot
            names = slot[0]
            width = slot[1]
            num_compartments = len(names)

            # Calculate Y space per compartment
            # Total walls between compartments: (num_compartments - 1) * INNER_WALL_THICKNESS
            total_wall_space = (num_compartments - 1) * config.INNER_WALL_THICKNESS
            compartment_y_size = (available_y - total_wall_space) / num_compartments

            # Create holes for each compartment in this slot
            for i in range(num_compartments):
                # Calculate Y position for this compartment
                y_pos = internal_y_start + i * (compartment_y_size + config.INNER_WALL_THICKNESS)

                # Get floor height for this X position
                floor_z, floor_height = get_floor_height_at_x(current_x)

                # Create hole (extends from floor_z downward)
                hole = Part.makeBox(
                    width,  # X dimension
                    compartment_y_size,  # Y dimension
                    floor_height,  # Z dimension (depth of hole)
                )
                hole.translate(
                    FreeCAD.Vector(
                        current_x,
                        y_pos,
                        floor_z,  # Start at floor level
                    )
                )
                holes.append(hole)
        else:
            # Single compartment in this slot
            width = slot[1]

            # Single compartment uses full Y space
            # Get floor height for this X position
            floor_z, floor_height = get_floor_height_at_x(current_x)

            # Create hole
            hole = Part.makeBox(
                width,  # X dimension
                available_y,  # Y dimension (full available space)
                floor_height,  # Z dimension (depth of hole)
            )
            hole.translate(
                FreeCAD.Vector(
                    current_x,
                    internal_y_start,
                    floor_z,  # Start at floor level
                )
            )
            holes.append(hole)

        # Move to next slot position
        # Add wall thickness between slots
        current_x += width + config.INNER_WALL_THICKNESS

    # Combine all holes
    if holes:
        combined = holes[0]
        for hole in holes[1:]:
            combined = combined.fuse(hole)
        return combined

    return None


def get_floor_height_at_x(x_pos) -> tuple[float, float]:
    """
    Gets the floor Z position and available height at a given X position

    Args:
        x_pos: X position to check
        floor_info: Floor height information dict

    Returns
    -------
        tuple: (floor_z, floor_height)
    """
    available_depth = [
        # this part is over the voltmeter protrusions and finger hole
        config.BASE_HEIGHT
        - (2 * config.OUTER_WALL_THICKNESS)
        - vm_config.VOLTMETER_HEIGHT
        - max(
            vm_config.EXTRA_BIT_1_HEIGHT, vm_config.EXTRA_BIT_2_HEIGHT, vm_config.EXTRA_BIT_3_HEIGHT
        ),
        # to the right of the finger cutout
        config.BASE_HEIGHT - (2 * config.OUTER_WALL_THICKNESS) - vm_config.VOLTMETER_HEIGHT,
        # to the right of the voltmeter
        config.BASE_HEIGHT - config.OUTER_WALL_THICKNESS,
    ]

    if x_pos > vm_config.VOLTMETER_LENGTH + (2 * config.OUTER_WALL_THICKNESS):
        return config.OUTER_WALL_THICKNESS, available_depth[2]

    if (
        x_pos
        > 2 * config.OUTER_WALL_THICKNESS
        + vm_config.EXTRA_BIT_1_WIDTH
        + vm_config.EXTRA_BIT_2_WIDTH
        + vm_config.EXTRA_BIT_3_WIDTH
    ):
        return config.BASE_HEIGHT - available_depth[1], available_depth[1]

    return config.BASE_HEIGHT - available_depth[0], available_depth[0]


def create_tool_organizer():
    """
    Creates a solid tool organizer box
    """
    # Create solid box
    organizer = Part.makeBox(config.BASE_LENGTH, config.BASE_WIDTH, config.BASE_HEIGHT)

    # Fillet outer corners
    organizer = fillet_outer_corners(organizer)

    return organizer


def fillet_outer_corners(shape):
    """
    Applies fillets to the outer corners of the organizer
    Finds vertical edges at the four corners and fillets them
    """
    try:
        edges_to_fillet = []
        tolerance = 0.1

        # Corner positions (x, y) at various Z heights
        # We want vertical edges at the four corners
        corners = [
            (0, 0),  # front-left (X=0, Y=0)
            (config.BASE_LENGTH, 0),  # front-right (X=LENGTH, Y=0)
            (0, config.BASE_WIDTH),  # back-left (X=0, Y=WIDTH)
            (config.BASE_LENGTH, config.BASE_WIDTH),  # back-right (X=LENGTH, Y=WIDTH)
        ]

        for edge in shape.Edges:
            # Check if this is a vertical edge at a corner
            if len(edge.Vertexes) == 2:
                v1, v2 = edge.Vertexes[0], edge.Vertexes[1]
                # Check if edge is vertical (same x, y, different z)
                if abs(v1.X - v2.X) < tolerance and abs(v1.Y - v2.Y) < tolerance:
                    x, y = v1.X, v1.Y
                    # Check if this matches a corner position
                    for corner_x, corner_y in corners:
                        if abs(x - corner_x) < tolerance and abs(y - corner_y) < tolerance:
                            edges_to_fillet.append(edge)
                            break

        # Apply fillet if we found edges
        if edges_to_fillet:
            filleted = shape.makeFillet(config.CORNER_FILLET_RADIUS, edges_to_fillet)
            return filleted

    except Exception as e:
        print(f"Warning: Could not apply fillets: {e}")
        return shape

    return shape


def build_model(doc, voltmeter_hole_obj=None):
    """
    Creates and adds the tool organizer model to the provided FreeCAD document
    Subtracts voltmeter hole and creates individual compartment holes

    Args:
        doc: FreeCAD document to add object to
        voltmeter_hole_obj: Optional voltmeter hole object to subtract

    Returns
    -------
        Part::Feature: The created tool organizer object
    """
    # Remove existing tool organizer if it exists
    if hasattr(doc, "ToolOrganizer"):
        doc.removeObject("ToolOrganizer")

    # Calculate voltmeter top Z for floor height calculations
    voltmeter_top_z = None
    if voltmeter_hole_obj is not None:
        hole_bbox = voltmeter_hole_obj.Shape.BoundBox
        voltmeter_top_z = hole_bbox.ZMax

    # Get floor height information (tracked for future hole creation)
    floor_info = get_floor_height_info(voltmeter_top_z)

    # Create solid organizer
    organizer_shape = create_tool_organizer()

    # Subtract voltmeter hole if provided
    if voltmeter_hole_obj is not None:
        organizer_shape = organizer_shape.cut(voltmeter_hole_obj.Shape)

    # Create individual compartment holes
    compartment_holes = create_compartment_holes(floor_info)
    if compartment_holes:
        organizer_shape = organizer_shape.cut(compartment_holes)

    # Create FreeCAD object
    obj = doc.addObject("Part::Feature", "ToolOrganizer")
    obj.Shape = organizer_shape

    return obj


if __name__ == "__main__":
    doc = FreeCAD.ActiveDocument
    if doc is None:
        doc = FreeCAD.newDocument("ToolOrganizer")
    build_model(doc)
