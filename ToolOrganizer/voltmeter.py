"""
Voltmeter FreeCAD Model Generator
Creates a voltmeter shape with main body and two extra bits on top edge
"""

import FreeCAD
import Part
import voltmeter_config as config


def create_voltmeter_shape(tolerance=0.0):
    """
    Creates the voltmeter model shape
    
    Args:
        tolerance: Additional size to add for hole cutting (default: 0.0)
        Tolerance is added uniformly to all dimensions
    
    Returns:
        Part.Shape: The voltmeter shape
    """
    # Calculate dimensions with tolerance (tolerance added to each side)
    length = config.VOLTMETER_LENGTH + (2 * tolerance)
    width = config.VOLTMETER_WIDTH + (2 * tolerance)
    height = config.VOLTMETER_HEIGHT + (2 * tolerance)
    
    # Create main body box (starts at origin)
    main_body = Part.makeBox(length, width, height)
    
    # Create first extra bit (24 x 20 with fillet)
    # Positioned at X=0 end (one end of the main body)
    # Extra bits use base width (no tolerance doubling)
    # Only add tolerance to own dimensions
    extra_1_w = config.EXTRA_BIT_1_WIDTH + (2 * tolerance)
    extra_1_h = config.EXTRA_BIT_1_HEIGHT + (2 * tolerance)
    # Use base width with tolerance (same as main body width)
    extra_1_depth = config.VOLTMETER_WIDTH + (2 * tolerance)

    # Create rectangular extra bit first
    extra_bit_1 = Part.makeBox(
        extra_1_w,
        extra_1_depth,  # Use calculated depth (same as main body width)
        extra_1_h
    )
    # Position at X=0 end, on top of main body (Z = height)
    extra_bit_1.translate(FreeCAD.Vector(
        0,  # At X=0 (left end)
        0,
        height - tolerance
    ))
    
    # Apply fillets to the corners of extra bit 1 on the top edge
    # First fillet: outer top-front corner
    # (X=extra_1_w, Y=0, Z=height+extra_1_h)
    # Second fillet: outer top-back corner
    # (X=extra_1_w, Y=extra_1_depth, Z=height+extra_1_h)
    try:
        fillet_radius = config.EXTRA_BIT_1_FILLET + tolerance
        tol = 0.1
        target_x = extra_1_w
        target_z = height + extra_1_h - tolerance
        

        # Fillet the top edges
        edges_to_fillet = []
        for edge in extra_bit_1.Edges:
            if len(edge.Vertexes) == 2:
                v1, v2 = edge.Vertexes[0], edge.Vertexes[1]
                v1_at_top_edge = abs(v1.Z - target_z) < tol
                v2_at_top_edge = abs(v2.Z - target_z) < tol
                if v1_at_top_edge and v2_at_top_edge:
                    edges_to_fillet.append(edge)

        print(f"Edges to fillet: {edges_to_fillet}")
        
        if len(edges_to_fillet) >= 2:
            extra_bit_1 = extra_bit_1.makeFillet(
                fillet_radius, edges_to_fillet[:2])
    
    except Exception as e:
        print(f"Warning: Could not apply fillets to extra bit 1: {e}")
    
    # Create second extra bit (20 x 8)
    # Positioned immediately after first extra bit
    extra_2_w = config.EXTRA_BIT_2_WIDTH
    extra_2_h = config.EXTRA_BIT_2_HEIGHT + tolerance
    # Use base width with tolerance (same as main body width)
    extra_2_depth = config.VOLTMETER_WIDTH + (2 * tolerance)
    
    extra_bit_2 = Part.makeBox(
        extra_2_w,
        extra_2_depth,  # Use calculated depth (same as main body width)
        extra_2_h
    )
    # Position after first extra bit (starting where first extra bit ends)
    extra_bit_2.translate(FreeCAD.Vector(
        extra_1_w,  # Right after first extra bit
        0,
        height - tolerance  # On top of main body
    ))
    
    # Combine all parts
    voltmeter = main_body.fuse(extra_bit_1)
    voltmeter = voltmeter.fuse(extra_bit_2)
    
    return voltmeter


def create_voltmeter_hole(tolerance=None):
    """
    Creates a voltmeter shape with tolerance for cutting a hole
    Tolerance is added to all dimensions uniformly (tolerance per side)
    
    Args:
        tolerance: Tolerance to add per side (default: uses DEFAULT_TOLERANCE)
    
    Returns:
        Part.Shape: The voltmeter shape with tolerance added to dimensions
    """
    if tolerance is None:
        tolerance = config.DEFAULT_TOLERANCE
    
    # Create shape with tolerance added to all dimensions
    return create_voltmeter_shape(tolerance=tolerance)

def create_voltmeter_hole_with_finger_cutout(tolerance=None):
    """
    Creates a voltmeter shape with a finger cutout
    Includes an additional extra bit (20 x 12) adjacent to extra_bit_2
    """
    if tolerance is None:
        tolerance = config.DEFAULT_TOLERANCE
    
    # Start with the base voltmeter shape
    voltmeter_shape = create_voltmeter_shape(tolerance=tolerance)
    
    # Calculate dimensions for the third extra bit (20 x 12)
    height = config.VOLTMETER_HEIGHT + (2 * tolerance)
    extra_3_w = config.EXTRA_BIT_3_WIDTH + (2 * tolerance)  # Width (X dimension)
    extra_3_h = config.EXTRA_BIT_3_HEIGHT + (2 * tolerance)  # Height (Z dimension)
    extra_3_depth = config.VOLTMETER_WIDTH + (2 * tolerance)  # Depth (Y)
    
    # Calculate position: adjacent to extra_bit_2
    # extra_bit_1 width: EXTRA_BIT_1_WIDTH + 2*tolerance = 24 + 2*tolerance
    # extra_bit_2 width: EXTRA_BIT_2_WIDTH = 20 (from create_voltmeter_shape)
    # So extra_bit_3 starts at: extra_1_w + extra_2_w
    extra_1_w = config.EXTRA_BIT_1_WIDTH + (2 * tolerance)
    extra_2_w = config.EXTRA_BIT_2_WIDTH  # Note: extra_2 doesn't add tolerance to width
    
    # Create the third extra bit
    extra_bit_3 = Part.makeBox(
        extra_3_w,
        extra_3_depth,
        extra_3_h
    )
    # Position adjacent to extra_bit_2 (after extra_bit_1 + extra_bit_2)
    extra_bit_3.translate(FreeCAD.Vector(
        extra_1_w + extra_2_w + config.EXTRA_BIT_2_TRANSLATE,  # After extra_bit_1 and extra_bit_2
        0,
        height - tolerance  # On top of main body
    ))
    
    # Apply fillets to the corners of extra bit 3 on the top edge
    # Same fillets as extra_bit_1 (9mm radius)
    try:
        fillet_radius = config.EXTRA_BIT_1_FILLET + tolerance
        tol = 0.1
        target_z = height + extra_3_h - tolerance
        
        # Fillet the top edges (same approach as extra_bit_1)
        edges_to_fillet = []
        for edge in extra_bit_3.Edges:
            if len(edge.Vertexes) == 2:
                v1, v2 = edge.Vertexes[0], edge.Vertexes[1]
                v1_at_top_edge = abs(v1.Z - target_z) < tol
                v2_at_top_edge = abs(v2.Z - target_z) < tol
                if v1_at_top_edge and v2_at_top_edge:
                    edges_to_fillet.append(edge)
        
        if len(edges_to_fillet) >= 2:
            extra_bit_3 = extra_bit_3.makeFillet(
                fillet_radius, edges_to_fillet[:2])
    except Exception as e:
        print(f"Warning: Could not apply fillets to extra bit 3: {e}")
    
    # Fuse the third extra bit with the voltmeter shape
    voltmeter_shape = voltmeter_shape.fuse(extra_bit_3)
    
    return voltmeter_shape


def build_hole_model(doc, offset_x=0.0, offset_y=0.0, offset_z=0.0):
    """
    Creates and adds the voltmeter hole model to the provided FreeCAD document
    """
    # Remove existing voltmeter hole object if it exists
    if hasattr(doc, "VoltmeterHole"):
        doc.removeObject("VoltmeterHole")
    
    # Create the hole shape (with tolerance)
    hole_shape = create_voltmeter_hole_with_finger_cutout(tolerance=0.0)
    
    # Apply offsets
    if offset_x != 0.0 or offset_y != 0.0 or offset_z != 0.0:
        hole_shape.translate(FreeCAD.Vector(offset_x, offset_y, offset_z))
    
    # Create FreeCAD object for hole shape
    obj_hole = doc.addObject("Part::Feature", "VoltmeterHole")
    obj_hole.Shape = hole_shape
    
    return obj_hole

def build_model(doc, offset_x=0.0, offset_y=0.0, offset_z=0.0):
    """
    Creates and adds the voltmeter model to the provided FreeCAD document
    Creates both the normal shape and the hole shape
    
    Args:
        doc: FreeCAD document to add objects to
        offset_x: X offset to apply to voltmeter position (default: 0.0)
        offset_y: Y offset to apply to voltmeter position (default: 0.0)
        offset_z: Z offset to apply to voltmeter position (default: 0.0)
    
    Returns:
        tuple: (voltmeter_obj, voltmeter_hole_obj)
    """
    # Remove existing voltmeter objects if they exist
    if hasattr(doc, "Voltmeter"):
        doc.removeObject("Voltmeter")
    if hasattr(doc, "VoltmeterHole"):
        doc.removeObject("VoltmeterHole")
    
    # Create the hole shape (with tolerance) first - appears behind
    hole_shape = create_voltmeter_hole()
    
    # Apply offsets
    if offset_x != 0.0 or offset_y != 0.0 or offset_z != 0.0:
        hole_shape.translate(FreeCAD.Vector(offset_x, offset_y, offset_z))
    
    # Create FreeCAD object for hole shape (create first so it appears behind)
    obj_hole = doc.addObject("Part::Feature", "VoltmeterHole")
    obj_hole.Shape = hole_shape
    
    # Create the normal voltmeter shape second - appears in front
    voltmeter_shape = create_voltmeter_shape(tolerance=0.0)
    
    # Apply offsets
    if offset_x != 0.0 or offset_y != 0.0 or offset_z != 0.0:
        voltmeter_shape.translate(FreeCAD.Vector(offset_x, offset_y, offset_z))
    
    # Create FreeCAD object for normal shape
    # (create second so it appears in front)
    obj = doc.addObject("Part::Feature", "Voltmeter")
    obj.Shape = voltmeter_shape
    
    return obj, obj_hole


if __name__ == "__main__":
    doc = FreeCAD.ActiveDocument
    if doc is None:
        doc = FreeCAD.newDocument("Voltmeter")
    build_model(doc)

