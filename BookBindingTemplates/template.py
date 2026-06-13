import config
import Draft
import FreeCAD as App
import FreeCADGui as Gui
import Part

import sizes


def make_plate(doc, x_mm, y_mm, height_mm, pos_x, pos_y, name):
    print(f"Making plate {name} at {pos_x}, {pos_y} " f"with size {x_mm}x{y_mm}x{height_mm}")
    plate = Part.makeBox(x_mm, y_mm, height_mm)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = plate
    obj.Placement = App.Placement(App.Vector(pos_x, pos_y, 0), App.Rotation())
    return obj


def create_keyhole_shape(center_x, center_y, pin_radius, slot_width, slot_length, thickness):
    """Create a keyhole-shaped pin/hole.

    Creates a shape with a circular top and rectangular slot below.
    Args:
        center_x, center_y: Center position of the circular part
        pin_radius: Radius of the circular part
        slot_width: Width of the rectangular slot (should be < 2*radius)
        slot_length: Length of the slot extending downward from circle
        thickness: Height of the shape
    """
    # Create the circular part at the top (cylinder)
    # Position cylinder so bottom edge is at center_y - pin_radius
    cylinder = Part.makeCylinder(
        pin_radius, thickness, App.Vector(center_x, center_y - pin_radius, 0), App.Vector(0, 0, 1)
    )

    # Create the rectangular slot below
    slot_bottom_y = center_y - pin_radius - slot_length
    slot_half_width = slot_width / 2
    slot_box = Part.makeBox(
        slot_width, slot_length, thickness, App.Vector(center_x - slot_half_width, slot_bottom_y, 0)
    )

    # Fuse cylinder and box to create keyhole shape
    keyhole_shape = cylinder.fuse(slot_box)

    return keyhole_shape


def create_corner_chamfer_cut(
    inner_corner_x, inner_corner_y, outer_corner_x, outer_corner_y, thickness
):
    """Create a chamfer cut for a corner.

    Creates a triangular prism that cuts from the outer corner,
    leaving config.triangle mm from the inner corner in both x and y.

    Args:
        inner_corner_x, inner_corner_y: Position of inner corner
        outer_corner_x, outer_corner_y: Position of outer corner
        thickness: Height of the cut
    """
    # Calculate the chamfer point
    # It should be config.triangle away from inner corner toward outer corner
    dir_x = outer_corner_x - inner_corner_x
    dir_y = outer_corner_y - inner_corner_y

    # Calculate chamfer point (config.triangle from inner corner)
    if dir_x < 0:  # Outer is to the left
        chamfer_x = inner_corner_x - config.triangle + config.margin
    else:  # Outer is to the right
        chamfer_x = inner_corner_x + config.triangle - config.margin

    if dir_y < 0:  # Outer is below
        chamfer_y = inner_corner_y - config.triangle + config.margin
    else:  # Outer is above
        chamfer_y = inner_corner_y + config.triangle - config.margin

    # Create triangle vertices:
    # p1: Outer corner
    # p2: Point on horizontal edge at chamfer distance
    # p3: Point on vertical edge at chamfer distance
    p1 = App.Vector(outer_corner_x, outer_corner_y, 0)
    p2 = App.Vector(chamfer_x, outer_corner_y, 0)
    p3 = App.Vector(outer_corner_x, chamfer_y, 0)

    # Create a face from the triangle
    triangle_wire = Part.makePolygon([p1, p2, p3, p1])
    triangle_face = Part.Face(triangle_wire)

    # Extrude to create a cutting volume
    chamfer_cut = triangle_face.extrude(App.Vector(0, 0, thickness))

    return chamfer_cut


def make_label(doc, text, pos_x, pos_y, name, height_mm=1.0, font_size="5.0 mm"):
    """Create a text label at the specified position."""
    label = Draft.make_text(text, App.Vector(pos_x, pos_y, height_mm + 0.1))
    # Store the internal name before changing the label
    internal_name = label.Name
    label.Label = name
    # Set font size on GUI document object using the internal name
    # Pattern: Gui.getDocument('Templates').getObject('Text').FontSize = '15 mm'
    try:
        gui_doc = Gui.getDocument(doc.Name)
        gui_obj = gui_doc.getObject(internal_name)
        if gui_obj and hasattr(gui_obj, "FontSize"):
            gui_obj.FontSize = font_size
            print(f"Set font size to {font_size} for {name} " f"(internal: {internal_name})")
        else:
            print(
                f"Warning: Could not find GUI object {internal_name} " f"or no FontSize attribute"
            )
    except Exception as e:
        print(f"Warning: Could not set font size for {name}: {e}")
    return label


def create_text_shape(text, font_name, font_size_mm, position):
    """Create a text shape directly as a Part object that can be extruded."""
    # Use Part.ShapeString to create text as a shape
    # This creates a Part object with a Shape attribute
    try:
        # Part.ShapeString creates text as a wire/face that can be extruded
        text_obj = Part.ShapeString(
            String=text,
            FontFile="",  # Empty uses default font
            Size=font_size_mm,
            Tracking=0,
        )
        # Apply placement
        text_obj.Placement = App.Placement(position, App.Rotation())
        return text_obj
    except Exception as e:
        print(f"Error creating Part.ShapeString: {e}")
        # Fallback: try alternative method
        try:
            # Some FreeCAD versions use makeShapeString
            if hasattr(Part, "makeShapeString"):
                text_shape = Part.makeShapeString(text, font_name, font_size_mm, 0)
                text_shape.Placement = App.Placement(position, App.Rotation())
                return text_shape
        except Exception as e2:
            print(f"Error with makeShapeString: {e2}")
        return None


def extrude_text(doc, label_obj, extrusion_height=1.0):
    """Extrude a text label to create a 3D shape."""
    # Get text properties from the Draft text object
    text_string = label_obj.Text
    font_name = getattr(label_obj, "FontName", "Arial")
    font_size_str = getattr(label_obj, "FontSize", "15 mm")
    try:
        font_size_val = float(font_size_str.split()[0])
    except (ValueError, AttributeError):
        font_size_val = 15.0

    # Get position from the label object
    position = label_obj.Placement.Base

    # Create text shape directly as Part object
    text_shape = create_text_shape(text_string, font_name, font_size_val, position)

    if text_shape is None:
        print(
            f"Warning: Could not create text shape for {label_obj.Name}. "
            "Skipping text extrusion."
        )
        return None

    # Extrude the shape
    direction = App.Vector(0, 0, extrusion_height)
    extruded = text_shape.extrude(direction)

    # Create a Part::Feature object with the extruded shape
    extrude_obj = doc.addObject("Part::Feature", f"{label_obj.Name}_extruded")
    extrude_obj.Shape = extruded
    return extrude_obj


def main():
    """Create array of templates based on sizes."""
    doc = App.ActiveDocument

    # Spacing between rectangles (in mm)
    spacing = 50  # Generous spacing

    # Starting position
    x_offset = 0
    y_offset = 0

    for i, size in enumerate(sizes.sizes):
        x_inches, y_inches, spline_inches = size

        print(f"Size {i+1}: {x_inches}x{y_inches}x{spline_inches}")

        # Convert to mm
        x_mm = config.inch_to_mm(x_inches)
        y_mm = config.inch_to_mm(y_inches)
        spline_mm = config.inch_to_mm(spline_inches)

        # Create front box (x, y, thickness+1)
        make_plate(
            doc,
            x_mm,
            y_mm,
            config.thickness,
            x_offset,
            y_offset,
            f"Template_{i+1}_front",
        )
        make_plate(
            doc,
            spline_mm,
            y_mm,
            config.thickness,
            x_offset + x_mm + config.gap,
            y_offset,
            f"Template_{i+1}_spline",
        )
        make_plate(
            doc,
            x_mm,
            y_mm,
            config.thickness,
            x_offset + x_mm + config.gap + spline_mm + config.gap,
            y_offset,
            f"Template_{i+1}_back",
        )

        # Create wrapper plate around the three plates
        total_width = x_mm + config.gap + spline_mm + config.gap + x_mm
        wrapper_width = total_width + 2 * config.margin
        wrapper_height = y_mm + 2 * config.margin
        make_plate(
            doc,
            wrapper_width,
            wrapper_height,
            config.thickness,
            x_offset - config.margin,
            y_offset - config.margin,
            f"Template_{i+1}_wrapper",
        )

        # Create label on top of wrapper, inside the frame
        label_text = f"{x_inches} x {y_inches} x {spline_inches} inch"
        # Position text with some offset from the left to clear the chamfer
        label_x = x_offset + config.label_x_offset

        # Calculate vertical position to center text in the top margin area
        try:
            font_size_val = float(config.font_size.split()[0])
        except (ValueError, AttributeError):
            font_size_val = 15.0

        # Center of the margin area
        margin_center_y = y_offset + y_mm + (config.margin / 2)
        # Text baseline position: center - (font_height / 2)
        # (baseline is at bottom of text, so we subtract half the height)
        label_y = margin_center_y - (font_size_val / 2)

        label_obj = make_label(
            doc,
            label_text,
            label_x,
            label_y,
            f"Template_{i+1}_label",
            config.thickness,
            font_size=config.font_size,  # Font size in mm, max 17mm high
        )

        # Extrude the text label (may return None if it fails)
        text_extrusion = extrude_text(doc, label_obj, config.thickness)

        # Get references to the objects we need to subtract
        front_obj = doc.getObject(f"Template_{i+1}_front")
        spline_obj = doc.getObject(f"Template_{i+1}_spline")
        back_obj = doc.getObject(f"Template_{i+1}_back")
        wrapper_obj = doc.getObject(f"Template_{i+1}_wrapper")

        # Hide the front, spline, and back objects
        try:
            gui_doc = Gui.getDocument(doc.Name)
            for obj in [front_obj, spline_obj, back_obj]:
                if obj:
                    gui_obj = gui_doc.getObject(obj.Name)
                    if gui_obj:
                        gui_obj.Visibility = False
        except Exception as e:
            print(f"Warning: Could not hide objects: {e}")

        # Subtract front, spline, back, and text extrusion from wrapper
        # Create a list of objects to subtract (text_extrusion may be None)
        objects_to_cut = [front_obj, spline_obj, back_obj]
        if text_extrusion is not None:
            objects_to_cut.append(text_extrusion)

        # Perform boolean cut operation
        # We'll do this step by step: wrapper - front - spline - back - text
        current_shape = wrapper_obj.Shape
        for obj_to_cut in objects_to_cut:
            try:
                current_shape = current_shape.cut(obj_to_cut.Shape)
            except Exception as e:
                print(f"Warning: Could not cut {obj_to_cut.Name} " f"from wrapper: {e}")

        # Create corner chamfers
        # Calculate corner positions
        wrapper_x_min = x_offset - config.margin
        wrapper_x_max = x_offset - config.margin + wrapper_width
        wrapper_y_min = y_offset - config.margin
        wrapper_y_max = y_offset - config.margin + wrapper_height

        # Inner corners (where margin meets inner plates)
        inner_x_min = x_offset
        inner_x_max = x_offset + total_width
        inner_y_min = y_offset
        inner_y_max = y_offset + y_mm

        # Create chamfer cuts for all 4 corners
        # Bottom-left corner
        chamfer_bl = create_corner_chamfer_cut(
            inner_x_min, inner_y_min, wrapper_x_min, wrapper_y_min, config.thickness
        )
        # Bottom-right corner
        chamfer_br = create_corner_chamfer_cut(
            inner_x_max, inner_y_min, wrapper_x_max, wrapper_y_min, config.thickness
        )
        # Top-left corner
        chamfer_tl = create_corner_chamfer_cut(
            inner_x_min, inner_y_max, wrapper_x_min, wrapper_y_max, config.thickness
        )
        # Top-right corner
        chamfer_tr = create_corner_chamfer_cut(
            inner_x_max, inner_y_max, wrapper_x_max, wrapper_y_max, config.thickness
        )

        # Apply chamfer cuts to the wrapper shape
        for chamfer in [chamfer_bl, chamfer_br, chamfer_tl, chamfer_tr]:
            if chamfer is not None:
                try:
                    current_shape = current_shape.cut(chamfer)
                except Exception as e:
                    print(f"Warning: Could not apply chamfer cut: {e}")

        # Cut out right half for templates exceeding max printer dimension
        max_dimension = max(wrapper_width, wrapper_height)

        if max_dimension > config.max_printer_dimension:
            # Split is at the middle of the total width
            split_x = x_offset + (total_width / 2)

            # Create a mask for the left half only
            left_mask = Part.makeBox(
                total_width / 2 + config.margin + 1,
                wrapper_height + 2,
                config.thickness * 2,
                App.Vector(wrapper_x_min - 1, wrapper_y_min - 1, -config.thickness),
            )

            # Keep only the left half
            current_shape = current_shape.common(left_mask)

            # Add pin shape aligned with center of frame bar
            # Pin is config.margin/2 away from max_y, left edge aligned to right edge of frame
            pin_y = wrapper_y_max - (config.margin / 2)
            # The pin's left edge should be at split_x (right edge of left half)
            # For a keyhole pointing right, the circle is on the left, slot extends right
            # After rotation, the leftmost point will be at the circle center minus radius
            # So circle center should be at split_x + pin_radius
            pin_center_x = split_x + config.pin_radius

            # Create pin shape (facing right, +x direction)
            pin_shape = create_keyhole_shape(
                pin_center_x,
                pin_y,
                config.pin_radius,
                config.slot_width,
                config.slot_length,
                config.thickness,
            )
            # Rotate 90 degrees so slot points right (+x)
            # pin_shape.rotate(
            #     App.Vector(pin_center_x, pin_y, 0), App.Vector(0, 0, 1), 270
            # )
            pin_shape.rotate(App.Vector(pin_center_x, pin_y, 0), App.Vector(0, 0, 1), 270)
            pin_shape.translate(App.Vector(config.slot_length, 0, 0))

            # Fuse pin to the left half
            current_shape = current_shape.fuse(pin_shape)

            # Position hole in lower arm of frame
            # Right edge should align with split_x (right edge of frame)
            # Vertically centered in lower margin area
            hole_radius = config.pin_radius + config.pin_hole_tolerance
            hole_slot_length = config.slot_length
            # After rotation 90 degrees, the rightmost point is at center_x + radius + slot_length
            # So to have right edge at split_x: center_x = split_x - (radius + slot_length)
            hole_center_x = split_x - (hole_radius + hole_slot_length)
            # Vertically in lower margin (bottom margin area)
            hole_center_y = wrapper_y_min + (config.margin / 2)

            hole_shape = create_keyhole_shape(
                0,
                0,
                hole_radius,
                config.slot_width + config.pin_hole_tolerance * 2,
                hole_slot_length,
                config.thickness,
            )
            hole_shape.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 90)
            # Translate so right edge aligns with split_x
            hole_shape.translate(App.Vector(hole_center_x, hole_center_y, 0))

            # Add hole_shape as a document object for troubleshooting
            hole_obj = doc.addObject("Part::Feature", f"Template_{i+1}_hole_shape")
            hole_obj.Shape = hole_shape

            current_shape = current_shape.cut(hole_shape)

        # Update the wrapper object with the cut shape
        wrapper_obj.Shape = current_shape

        # Update offset for next set of rectangles
        # Place them in a row, moving x_offset
        x_offset += x_mm + config.gap + spline_mm + config.gap + x_mm + spacing

    # Recompute the document
    doc.recompute()
