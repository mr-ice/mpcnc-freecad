import FreeCADGui as Gui
import FreeCAD as App
import Part
import math

class Config:
    box_width           = 320.0
    box_depth           = 130.0
    card_height         = 91.0
    card_width          = 59.0
    card_thickness      = 12.0   # per 20
    map_width           = 315
    map_thickness       = 30     # per 13
    player_length       = 305    # player boards
    player_width        = 150    # player boards
    player_thickness    = 4      # player boards
    mini_width          = 19.85  # mini base width
    mini_length         = 22.85  # base length
    mini_height         = 27.85  # mini height
    base_height         = 3.5    # base height
    mini_overall_width  = 28.25  # mini overall width
    mini_overall_height = 30     # mini overall height
    bitbox_length       = 129    # bitbox length
    bitbox_width        = 68     # bitbox width
    bitbox_height       = 22     # bitbox height
    clearance           = 2      # card clearance
    reboot_thickness    = 4.05   # reboot thickness
    reboot_width        = 21.5   # reboot width
    flag_side           = 25.56  # flag side
    flag_thickness      = 2.09   # flag thickness
    flag_height         = 20.05  # flag height
    flag_width          = 16.3   # flag width
    flag_pole           = 3.7    # flag pole
    bottom_thickness    = 2      # bottom thickness
    space_between_slots = bottom_thickness * 3

# Create a new document
doc = App.newDocument("BigBox")

# Create outer box
outer_box = Part.makeBox(Config.box_width, Config.box_width, Config.card_width + Config.bottom_thickness + Config.player_thickness * 4)

# Create inner box (smaller in all dimensions by wall_thickness * 2, and extra padding on bottom)
inner_box = Part.makeBox(
    Config.player_length + Config.clearance * 2,           # width
    Config.player_length + Config.clearance * 2,           # depth
    Config.box_depth - Config.bottom_thickness - Config.card_width  # height
)

wall_thickness = (Config.box_width - (Config.player_length + Config.clearance * 2)) / 2

# Position inner box (centered, raised by bottom padding)
inner_box.translate(App.Vector(
    wall_thickness,  # center on X
    wall_thickness,  # center on Y
    Config.bottom_thickness + Config.card_width  # same Z position
))

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.cut(inner_box)


# Calculate dimensions with clearance
slot_height = Config.card_height + Config.clearance
slot_width = Config.card_width + Config.clearance
slot_thickness = Config.card_thickness * 1.25
slot_spacing = Config.card_thickness

x_offset = wall_thickness * 2
y_offset = wall_thickness * 2
z_offset = Config.bottom_thickness

# make a hollow for the cards about 2/3 of the way up
hollow_top_card_slot = Part.makeBox(slot_height,
                                    Config.box_width - (x_offset * 2),
                                    slot_width/3)
hollow_top_card_slot.translate(App.Vector(x_offset, y_offset, z_offset + slot_width - slot_width/3))

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
    slot.translate(App.Vector(
        x_offset,
        y_offset + slot_spacing + (i * (slot_thickness + slot_spacing)),
        z_offset
    ))
    
    # Cut slot from hollow box
    hollow_box = hollow_box.cut(slot)

upgrade_slot = Part.makeBox(slot_height,
                            Config.card_thickness / 20 * 80 * 1.25,
                            slot_width)
upgrade_slot.translate(App.Vector(x_offset + slot_height + (Config.space_between_slots),
                                  y_offset + slot_spacing,
                                  z_offset))
                                  

hollow_box = hollow_box.cut(upgrade_slot)

# Create damage slot (7/8 size of upgrade slot)
damage_slot = Part.makeBox(slot_height,
                          Config.card_thickness / 20 * 80 * 1.25 * 0.875,  # 7/8 of upgrade slot
                          slot_width)
damage_slot.translate(App.Vector(
    x_offset,
    y_offset + slot_thickness + (slots_count * (slot_thickness + slot_spacing)),
    z_offset))

hollow_box = hollow_box.cut(damage_slot)

# Add hollow top for damage slot
hollow_top_damage_slot = Part.makeBox(slot_height,
                                      y_offset + upgrade_slot.BoundBox.YLength + slot_spacing,
                                      slot_width/3)
hollow_top_damage_slot.translate(App.Vector(
    x_offset + slot_height + (Config.space_between_slots),
    y_offset,
    z_offset + slot_width - slot_width/3))

hollow_box = hollow_box.cut(hollow_top_damage_slot)

cylinder_radius = Config.card_width / 2
cylinder_length = Config.box_width - (x_offset * 2)
# Add cylinder for damage slot
damage_cylinder = Part.makeCylinder(
    cylinder_radius,
    y_offset + upgrade_slot.BoundBox.YLength + slot_spacing,
    App.Vector(0,0,0),
    App.Vector(0,1,0)  # Align along Y axis
)

damage_cylinder.translate(App.Vector(
    x_offset + slot_height + (Config.space_between_slots) + Config.card_height/2,
    y_offset,
    Config.bottom_thickness + Config.card_width
))

hollow_box = hollow_box.cut(damage_cylinder)

# Create cylinder for top cutout
card_cylinder = Part.makeCylinder(
    cylinder_radius,
    cylinder_length,
    App.Vector(0,0,0),
    App.Vector(0,1,0)  # Align along Y axis
)

# Position cylinder:
# x: same as card slots
# y: offset by 4 * wall_thickness and half the card height
# z: wall_thickness + card_width + (card_width/2)
# because the cylinder is aligned along Y, we need to offset the x by half the card height
card_cylinder.translate(App.Vector(
    x_offset + Config.card_height / 2,
    x_offset,
    Config.bottom_thickness + Config.card_width
))

# Cut cylinder from hollow box
hollow_box = hollow_box.cut(card_cylinder)

# Create reboot token slots
reboot_slot_width = Config.reboot_width + Config.clearance
reboot_slot_thickness = Config.reboot_thickness + Config.clearance
sphere_radius = reboot_slot_width * 0.4  # 80% of width for sphere cutouts

# Position offset from damage slot
reboot_x_offset = x_offset + Config.card_height * 2 + Config.bottom_thickness * 8

reboot_slot = Part.makeBox(reboot_slot_width,
                            reboot_slot_thickness * 8,
                            reboot_slot_width)
    
    # Position slot
reboot_slot.translate(App.Vector(
    reboot_x_offset,
    y_offset + sphere_radius,
    z_offset + Config.card_width - reboot_slot_width
))
    
# Create spherical cutouts at ends
front_sphere = Part.makeSphere(sphere_radius)
back_sphere = Part.makeSphere(sphere_radius)

# Position spheres at ends of slot
front_sphere.translate(App.Vector(
    reboot_x_offset + (reboot_slot_width/2),
    y_offset + sphere_radius,
    z_offset + Config.card_width - (Config.bottom_thickness/2)
))

back_sphere.translate(App.Vector(
    reboot_x_offset + (reboot_slot_width/2),
    y_offset + reboot_slot.BoundBox.YLength + sphere_radius,
    z_offset + Config.card_width + (Config.bottom_thickness/2)
))

# Cut slots and spheres from box
hollow_box = hollow_box.cut(reboot_slot)
hollow_box = hollow_box.cut(front_sphere)
hollow_box = hollow_box.cut(back_sphere)


# Create staggered cube cutouts for flag side
flag_cutout_width = Config.flag_side + Config.clearance
flag_cutout_depth = Config.flag_side + Config.clearance
flag_cutout_height = Config.flag_height + Config.clearance

flag_cutout_spacing = (Config.flag_thickness + Config.clearance) * 6
flag_x_offset = reboot_x_offset + reboot_slot_width + Config.space_between_slots
flag_y_offset = y_offset

# Create and position 6 overlapping cubes
for i in range(6):
    # Create cube
    flag_cube = Part.makeBox(flag_cutout_width,
                            flag_cutout_height,
                            flag_cutout_depth)
    
    # Calculate diagonal distance from corner to center (using Pythagorean theorem)
    corner_to_center = (flag_cutout_width * math.sqrt(2)) / 2
    
    # Rotate 45 degrees counter-clockwise around Z axis
    flag_cube.rotate(App.Vector(0,0,0), App.Vector(0,0,1), 45)
    
    # Position cube with offset
    flag_cube.translate(App.Vector(
        flag_x_offset + corner_to_center,  # offset by corner_to_center distance
        flag_y_offset,
        z_offset + Config.card_width - flag_cutout_depth
    ))
    
    # Cut cube from box
    hollow_box = hollow_box.cut(flag_cube)

    # flag_x_offset -= Config.clearance + Config.flag_thickness
    flag_y_offset += Config.clearance + Config.flag_thickness

flag_sphere = Part.makeSphere(Config.flag_side * 0.66)
flag_sphere.translate(App.Vector(
    flag_x_offset + corner_to_center,
    flag_y_offset + corner_to_center * 1.5,
    z_offset + Config.card_width
))

hollow_box = hollow_box.cut(flag_sphere)

misc_box_height = inner_box.BoundBox.XLength - (x_offset + slot_height + (Config.space_between_slots))
misc_box_width = inner_box.BoundBox.YLength - (y_offset + upgrade_slot.BoundBox.YLength + slot_spacing * 2 + Config.space_between_slots)

misc_box = Part.makeBox(
    misc_box_height,
    misc_box_width,
    slot_width + Config.clearance * 2
)

misc_box.translate(App.Vector(
    x_offset + slot_height + (Config.space_between_slots),
    y_offset + upgrade_slot.BoundBox.YLength + slot_spacing * 2 + Config.space_between_slots,
    Config.bottom_thickness
))

hollow_box = hollow_box.cut(misc_box)


# Add to document
box_shape = doc.addObject("Part::Feature", "Box")
box_shape.Shape = hollow_box

# Recompute the document
doc.recompute()

# Switch to isometric view and fit to window
Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")


