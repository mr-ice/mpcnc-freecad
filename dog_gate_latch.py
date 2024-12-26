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

latch_wedge_protrusion = 4  

def create_base_mount(width, base_length, height, clearance=0.5, thickness=5.0):    
    # Create the main mounting box
    mount = Part.makeBox(width + 2 * thickness,
                         base_length + 2 * thickness,
                         height + 2 * thickness)
    
    hollow = Part.makeBox(width + 2 * clearance,
                          base_length + 2 * clearance,
                          height + 2 * thickness)
    hollow.translate(Base.Vector(thickness - clearance, thickness - clearance, -thickness))
    mount = mount.cut(hollow)
    
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

def create_latch_mechanism(width, base_length, height, gap, latch_length, clearance=0.5, thickness=5.0):

    lever = Part.makeBox(lever_width, total_length, thickness)
    # lever.translate(Base.Vector(-lever_width / 2 + width / 2, base_length/2 - max_diameter/2 - wall_thickness, 0))
    

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
    # Rotate to make bit stick up to activate latch
    handle.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), handle_angle)

    
    # on the left side over the gate post create a wedge to allow the gate to nudge open the latch

    left_wedge = Part.makeBox(hinge_width, hinge_length, hinge_width+latch_wedge_protrusion)
    left_wedge_cut = Part.makeBox(hinge_width*2, hinge_length, hinge_height)
    left_wedge_cut.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), handle_angle)
    left_wedge_cut.translate(Base.Vector(0, 0, 0))
    left_wedge = left_wedge.cut(left_wedge_cut)
    left_wedge.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), 180)

    left_wedge.translate(Base.Vector(hinge_width, total_length + hinge_length/2, -latch_wedge_protrusion))

    # Combine all parts
    latch = lever.fuse(handle)
    latch.translate(Base.Vector(0, hinge_length/2, 0))
    latch = latch.fuse(left_hinge)
    latch = latch.fuse(right_hinge)
    latch = latch.fuse(left_wedge)
    
    return latch

def main():
    # Create document
    doc = App.newDocument("GateLatch")
    
    # Create gate components (posts)
    fixed_post = Part.makeBox(width, base_length, post_height)  # Post with latch mount
    gate_post = Part.makeBox(width, base_length, post_height)   # Moving gate post
    
    # Position gate post with the gap
    gate_post.translate(Base.Vector(0, base_length + gap, 0))
    
    # Create latch components
    base = create_base_mount(width, base_length, base_height, clearance=clearance, thickness=wall_thickness)
    latch = create_latch_mechanism(width, base_length, base_height, gap, latch_length)
    
    # Position components
    # Center the base on the fixed post and place it wall_thickness above

    base.translate(Base.Vector(base_x_offset, base_y_offset, post_height - base_height - wall_thickness))
    
    # latch.translate(Base.Vector(- wall_thickness - clearance, 0, post_height + wall_thickness + clearance))
    latch.translate(Base.Vector(base.BoundBox.XLength/2 - lever_width/2 - clearance * 2 - hinge_width, 0, post_height + wall_thickness + clearance))
    
    # Add to document
    Part.show(fixed_post, "FixedPost")
    Part.show(gate_post, "GatePost")
    Part.show(base, "Base")
    Part.show(latch, "Latch")
    # Save and recompute
    doc.recompute()

if __name__ == "__main__":
    main()