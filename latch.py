import math
import FreeCAD as App
import Part
from FreeCAD import Base

# Basic parameters
width = 18.4
base_length = 50.0
gap = 7.5
latch_length = 15.0
wall_thickness = 2.0
clearance = 0.2
hinge_clearance = 0.1
base_height = 25

# How much of the post is used for the latch mount
post_height = 50.0

# Base of the latch offset on post by:
base_x_offset = (width - (width + 2 * wall_thickness)) / 2
base_y_offset = (base_length - (base_length + 2 * wall_thickness)) / 2
base_z_offset = (post_height - base_height - wall_thickness)

# Hinge Cone parameters
min_diameter = 3.0
max_diameter = 10.0
cone_height = 3.0

# Create hinge mounts
hinge_width = cone_height * 1.5
hinge_height = max_diameter * 2.25 + hinge_width# offset to center is 1.5, another .75 makes it match the length 
hinge_length = max_diameter * 1.5

# Create the main lever
#+ 2 * thickness + 2 * clearance + 2 * wall_thickness + 2 * hinge_clearance
total_length = base_length/2 + gap + latch_length + max_diameter / 2 + wall_thickness
lever_width = width + 2 * wall_thickness + 2 * hinge_width + 2 * clearance

latch_wedge_protrusion = 6.5
hinge_offset = base_length / 2.5


def horizontal_edges(obj, angle_threshold=16):
    horizontal_edges = []
    for edge in obj.Edges:
        if hasattr(edge, 'Curve') and isinstance(edge.Curve, Part.Line):
            direction = edge.Curve.Direction
            angle_with_vertical = abs(direction.z)
            if angle_with_vertical < math.cos(math.radians(angle_threshold)):
                horizontal_edges.append(edge)
    return horizontal_edges

def is_external_edge(edge, vertical_angle_threshold=16):
    """
    Check if an edge is external by examining its connected faces.
    
    Args:
        edge: A FreeCAD edge object
    
    Returns:
        bool: True if the edge is external, False if internal
    """
    # Get all faces that share this edge
    connected_faces = edge.Faces
    if len(connected_faces) != 2:  # External edges should connect exactly 2 faces
        return False
        
    # Get the normals of the two faces
    normals = [f.normalAt(0,0) for f in connected_faces]
    # If the faces are parallel (internal edge), their normals will be parallel or anti-parallel
    dot_product = abs(normals[0].dot(normals[1]))
    return dot_product < 0.99  # If not parallel, it's an external edge

def show_selected_edges(edges):
    if edges:
        vertical_compound = Part.Compound(edges)
        Part.show(vertical_compound, "VerticalEdgesToFillet")

def create_latch_mechanism(width, base_length, height, gap, latch_length, clearance=0.5, thickness=5.0, debug_edges=None):

    # Create the main lever parts
    lever_cylinder = Part.makeCylinder(total_length/2, thickness)
    lever_cylinder.translate(Base.Vector((total_length/2 + thickness)/2, total_length/2 + thickness, 0))
    
    # Create cutting box to trim cylinder
    trim_box = Part.makeBox(total_length, total_length, thickness)
    trim_box.translate(Base.Vector(0, total_length, 0))
    
    # Trim cylinder
    lever_cylinder = lever_cylinder.cut(trim_box)
    
    # Create and fuse lever box
    lever_box = Part.makeBox(lever_width, total_length, thickness)
    lever = lever_cylinder.fuse(lever_box)

    left_hinge_supported_length= hinge_length + 20
    
    # Left hinge
    left_hinge = Part.makeBox(hinge_width, left_hinge_supported_length, hinge_height)

    clip_protruding = hinge_height - thickness + clearance

    left_hinge_clip = Part.makeBox(hinge_width, hinge_height + 50, hinge_height + 50)
    left_hinge_clip.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), 45)
    left_hinge_clip.translate(Base.Vector(0, math.sqrt((hinge_height + 50) ** 2 / 2) +
                                          left_hinge_supported_length - clip_protruding, - math.sqrt((hinge_height + 50) ** 2 / 2)))
    left_hinge = left_hinge.cut(left_hinge_clip)
    left_hinge.translate(Base.Vector(0, 0, -hinge_height + hinge_width))
    
    # Create cone hole with matching z-offset to base
    left_cone_hole = Part.makeCone(max_diameter/2 + hinge_clearance, 
                                  min_diameter/2 + hinge_clearance, 
                                  cone_height)
    left_cone_hole.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    left_cone_hole.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
    left_cone_hole.translate(Base.Vector(hinge_width, hinge_length/2, -max_diameter * 1.5))

    left_hinge = left_hinge.cut(left_cone_hole)
    
    # Right hinge
    right_hinge = Part.makeBox(hinge_width, total_length + hinge_length/2, hinge_height)
    right_hinge.translate(Base.Vector(lever_width - hinge_width, 0, -hinge_height + hinge_width))  
    # right_hinge.translate(Base.Vector(lever_width, base_length/2 - hinge_length/2, -hinge_height))
    # Part.show(right_hinge, "RightHinge")
    
    right_cone_hole = Part.makeCone(max_diameter/2 + hinge_clearance, 
                                   min_diameter/2 + hinge_clearance, 
                                   cone_height)
    right_cone_hole.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    right_cone_hole.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 90)
    right_cone_hole.translate(Base.Vector(lever_width - hinge_width, hinge_length/2, -max_diameter * 1.5))
    
    right_hinge = right_hinge.cut(right_cone_hole)
    
    # Create handle
    handle_length = 40
    handle_angle = 90 - 15
    handle = Part.makeBox(lever_width, thickness, handle_length)
    
    # Add indent in handle
    indent_diameter = 14.0
    indent_depth = 1.75
    indent = Part.makeCylinder(indent_diameter/2, indent_depth,
                              Base.Vector(0, 0, 0),
                              Base.Vector(0, 1, 0))

    
    # Position and rotate indent to match handle angle before cutting
    indent.translate(Base.Vector(lever_width/2, 0, 18.772))
    handle = handle.cut(indent)
    
    # Rotate handle after adding indent
    handle.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), handle_angle)

    
    # Create and position left wedge
    left_wedge = Part.makeBox(hinge_width * 5, hinge_length, thickness+latch_wedge_protrusion)
    left_wedge_cut = Part.makeBox(hinge_width*2, hinge_length, hinge_height)
    left_wedge_cut.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), handle_angle)
    left_wedge = left_wedge.cut(left_wedge_cut)
    left_wedge.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), 180)
    left_wedge.translate(Base.Vector(hinge_width, total_length + hinge_length/2, -latch_wedge_protrusion))

    # Part.show(left_wedge, "LeftWedge")

    # Create transition piece between wedge and cylinder
    transition_radius = hinge_width * 7.5 # Adjust radius for desired curve
    transition_angle = 90  # Quarter circle
    transition = Part.makeCylinder(transition_radius, thickness,
                                 Base.Vector(0,0,0),
                                 Base.Vector(0,0,1),
                                 transition_angle)
    
    # Position and rotate the transition piece.  The center should keep the left edge
    # tangent and coincident with the left edge of the left_wedge.
    transition.rotate(Base.Vector(0, 0, 0),
                    Base.Vector(0,0,1), 180)
    transition.translate(Base.Vector(transition_radius - hinge_width * 4, total_length - hinge_length/2, 0))


    # Combine all parts
    latch = lever.fuse(handle)
    latch.translate(Base.Vector(0, hinge_length/2, 0))
    latch = latch.fuse(left_hinge)
    latch = latch.fuse(right_hinge)
    latch = latch.fuse(left_wedge)
    latch = latch.fuse(transition)
    
    # After all parts are combined, add fillets
    vertical_radius = 3.0
    horizontal_radius = 2.0
    vertical_angle_threshold = math.cos(math.radians(16))
    
    edges_to_fillet = []
    horizontal_edges = []
    
    for edge in latch.Edges:
        if hasattr(edge, 'Curve') and isinstance(edge.Curve, Part.Line) and is_external_edge(edge):
            # Get edge direction vector
            direction = edge.Curve.Direction
            # Calculate angle with vertical (0,0,1)
            angle_with_vertical = abs(direction.z)
            
            if abs(angle_with_vertical) > vertical_angle_threshold:
                edges_to_fillet.append(edge)
            elif abs(direction.z) < 0.1:  # Nearly horizontal edges
                horizontal_edges.append(edge)
    
    if debug_edges == 'vertical':
        if edges_to_fillet:
            vertical_compound = Part.Compound(edges_to_fillet)
            Part.show(vertical_compound, "VerticalEdgesToFillet")
    elif debug_edges == 'horizontal':
        if horizontal_edges:
            horizontal_compound = Part.Compound(horizontal_edges)
            Part.show(horizontal_compound, "HorizontalEdgesToFillet")
    elif debug_edges is None:
        # Apply fillets only if edges were found
        if edges_to_fillet:
            latch = latch.makeFillet(vertical_radius, edges_to_fillet)
        if horizontal_edges:
            latch = latch.makeFillet(horizontal_radius, horizontal_edges)
    
    return latch

def create_base_mount(width, base_length, height, clearance=0.5, thickness=5.0, max_diameter=10.0):    
    # Create the main mounting box
    mount = Part.makeBox(width + 2 * thickness,
                         base_length + 2 * thickness,
                         height + 2 * thickness)
    
    hollow = Part.makeBox(width + 2 * clearance,
                          base_length + 2 * clearance,
                          height + 2 * thickness)
    hollow.translate(Base.Vector(thickness - clearance, thickness - clearance, -thickness))
    mount = mount.cut(hollow)
    # Part.show(mount, "InitialMount")
    # Add tab on back
    tab_depth = 7.0
    tab = Part.makeBox(width + 2 * thickness, tab_depth, 2 * thickness)
    tab.translate(Base.Vector(0, -tab_depth, height))
    # Part.show(tab, "BaseTab")
    mount = mount.fuse(tab)
    
    # Add indent in tab
    indent_diameter = 14.0
    indent_depth = 1.75
    indent = Part.makeCylinder(indent_diameter/2, indent_depth,
                              Base.Vector(0, 0, 0),
                              Base.Vector(0, 0, -1))
    # Part.show(indent, "Indent")
    # Position indent in center of tab
    indent.translate(Base.Vector((width + 2 * thickness)/2, 2, height + 2 * thickness))
    # Part.show(indent, "IndentAfterMove")
    mount = mount.cut(indent)
    
    # Left cone
    left_cone = Part.makeCone(max_diameter/2, min_diameter/2, cone_height)
    left_cone.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    left_cone.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
    left_cone.translate(Base.Vector(0, base_length / 2, height + 2 * thickness - max_diameter * 1.5))
    
    # Right cone
    right_cone = Part.makeCone(max_diameter/2, min_diameter/2, cone_height)
    right_cone.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    right_cone.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 90)
    right_cone.translate(Base.Vector(width + 2 * thickness, base_length / 2, height + 2 * thickness - max_diameter * 1.5))
    
    # Add cones to mount
    mount = mount.fuse(left_cone)
    mount = mount.fuse(right_cone)

    return mount

def main():
    # Create document
    doc = App.newDocument("GateLatch")
    
    # Create gate components (posts)
    # fixed_post = Part.makeBox(width, base_length, post_height)  # Post with latch mount
    # gate_post = Part.makeBox(width, base_length, post_height)   # Moving gate post
    
    # # Position gate post with the gap
    # gate_post.translate(Base.Vector(0, base_length + gap, 0))
    
    # Create latch components
    base = create_base_mount(width, base_length, base_height, clearance=clearance, thickness=wall_thickness, max_diameter=max_diameter)
    latch = create_latch_mechanism(width, base_length, base_height, gap, latch_length, 
                                 debug_edges='vertical')  # 'vertical', 'horizontal', or None
    
    # Position components
    # Center the base on the fixed post and place it wall_thickness above

    base.translate(Base.Vector(base_x_offset, base_y_offset, post_height - base_height - wall_thickness))
    
    # latch.translate(Base.Vector(- wall_thickness - clearance, 0, post_height + wall_thickness + clearance))
    latch.translate(Base.Vector(base.BoundBox.XLength/2 - lever_width/2 - clearance * 2 - hinge_width, 0, post_height + wall_thickness + clearance))
    
    # Add to document
    # Part.show(fixed_post, "FixedPost")
    # Part.show(gate_post, "GatePost")
    Part.show(base, "Base")
    Part.show(latch, "Latch")
    # Save and recompute
    doc.recompute()

if __name__ == "__main__":
    main()