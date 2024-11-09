import FreeCADGui as Gui
import FreeCAD as App
import Part

class Config:
    box_width        = 320.0
    box_depth        = 130.0
    card_height      = 91.0
    card_width       = 59.0
    card_thickness   = 12.0   # per 20
    map_width        = 315
    map_thickness    = 30     # per 13
    player_length    = 305    # player boards
    player_width     = 150    # player boards
    player_thickness = 4      # player boards
    mini_width       = 19.85  # mini base width
    mini_length      = 22.85  # base length
    mini_height      = 27.85  # mini height
    base_height      = 3.5    # base height
    mini_overall_width  = 28.25  # mini overall width
    mini_overall_height = 30     # mini overall height
    bitbox_length    = 129    # bitbox length
    bitbox_width     = 68     # bitbox width
    bitbox_height    = 22     # bitbox height
    card_clearance   = 2      # card clearance
    reboot_thickness = 4.05   # reboot thickness
    reboot_width     = 21.5   # reboot width
    flag_side        = 25.56  # flag side
    flag_thickness   = 2.09   # flag thickness
    flag_height      = 20.05  # flag height
    flag_width       = 16.3   # flag width
    flag_pole        = 3.7    # flag pole
    wall_thickness   = 2      # wall thickness

# Create a new document
doc = App.newDocument("BigBox")

# Create outer box
outer_box = Part.makeBox(Config.box_width, Config.box_width, Config.box_depth)

# Create inner box (smaller in all dimensions by wall_thickness * 2, and extra padding on bottom)
inner_box = Part.makeBox(
    Config.box_width - (Config.wall_thickness * 2),           # width
    Config.box_width - (Config.wall_thickness * 2),           # depth
    Config.box_depth - Config.wall_thickness - Config.card_width  # height
)

# Position inner box (centered, raised by bottom padding)
inner_box.translate(App.Vector(
    Config.wall_thickness,
    Config.wall_thickness,
    Config.wall_thickness + Config.card_width
))

# Create hollow box by subtracting inner from outer
hollow_box = outer_box.cut(inner_box)


# Calculate dimensions with clearance
slot_height = Config.card_height + Config.card_clearance
slot_width = Config.card_width + Config.card_clearance
slot_thickness = Config.card_thickness * 1.25
slot_spacing = Config.card_thickness

x_offset = Config.wall_thickness * 4
y_offset = Config.wall_thickness * 4
z_offset = Config.wall_thickness

# make a hollow for the cards about 2/3 of the way up
hollow_top_card_slot = Part.makeBox(slot_height,
                                    Config.box_width - (Config.wall_thickness * 8),
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
        Config.wall_thickness * 4,
        Config.wall_thickness * 4 + slot_thickness + (i * (slot_thickness + slot_spacing)),
        Config.wall_thickness
    ))
    
    # Cut slot from hollow box
    hollow_box = hollow_box.cut(slot)

upgrade_slot = Part.makeBox(slot_height,
                            Config.card_thickness / 20 * 80 * 1.25,
                            slot_width)
upgrade_slot.translate(App.Vector(x_offset,
                                  y_offset + slot_thickness + (slots_count * (slot_thickness + slot_spacing)),
                                  z_offset))

hollow_box = hollow_box.cut(upgrade_slot)

# Create damage slot (7/8 size of upgrade slot)
damage_slot = Part.makeBox(slot_height,
                          Config.card_thickness / 20 * 80 * 1.25 * 0.875,  # 7/8 of upgrade slot
                          slot_width)
damage_slot.translate(App.Vector(
    x_offset + slot_height + (Config.wall_thickness * 3),  # offset from upgrade slot
    y_offset + slot_thickness + (slots_count * (slot_thickness + slot_spacing)),
    z_offset))

hollow_box = hollow_box.cut(damage_slot)

# Add hollow top for damage slot
hollow_top_damage_slot = Part.makeBox(slot_height,
                                     Config.box_width - (Config.wall_thickness * 8),
                                     slot_width/3)
hollow_top_damage_slot.translate(App.Vector(
    x_offset + slot_height + (Config.wall_thickness * 3),
    y_offset,
    z_offset + slot_width - slot_width/3))

hollow_box = hollow_box.cut(hollow_top_damage_slot)

# Add cylinder for damage slot
damage_cylinder = Part.makeCylinder(
    cylinder_radius,
    cylinder_length,
    App.Vector(0,0,0),
    App.Vector(0,1,0)  # Align along Y axis
)

damage_cylinder.translate(App.Vector(
    x_offset + slot_height + (Config.wall_thickness * 3) + Config.card_height/2,
    Config.wall_thickness * 4,
    Config.wall_thickness + Config.card_width
))

hollow_box = hollow_box.cut(damage_cylinder)

# Create cylinder for top cutout
cylinder_radius = Config.card_width / 2
cylinder_length = Config.box_width - (Config.wall_thickness * 8)
cylinder = Part.makeCylinder(
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
cylinder.translate(App.Vector(
    Config.wall_thickness * 4 + Config.card_height / 2,
    Config.wall_thickness * 4,
    Config.wall_thickness + Config.card_width
))

# Cut cylinder from hollow box
hollow_box = hollow_box.cut(cylinder)

# Create reboot token slots
reboot_slot_width = Config.reboot_width + Config.card_clearance
reboot_slot_thickness = Config.reboot_thickness + Config.card_clearance
sphere_radius = reboot_slot_width * 0.4  # 80% of width for sphere cutouts

# Position offset from damage slot
reboot_x_offset = x_offset + Config.card_height * 2 + Config.wall_thickness * 8

reboot_slot = Part.makeBox(reboot_slot_width,
                            reboot_slot_thickness * 8,
                            reboot_slot_width)
    
    # Position slot
reboot_slot.translate(App.Vector(
    reboot_x_offset,
    y_offset + slot_thickness + (slots_count * (slot_thickness + slot_spacing)),
    z_offset + Config.card_width - reboot_slot_width
))
    
# Create spherical cutouts at ends
front_sphere = Part.makeSphere(sphere_radius)
back_sphere = Part.makeSphere(sphere_radius)

# Position spheres at ends of slot
front_sphere.translate(App.Vector(
    reboot_x_offset + (reboot_slot_width/2),
    y_offset + slot_thickness + (slots_count * (slot_thickness + slot_spacing)),
    z_offset + Config.card_width - (Config.wall_thickness/2)
))

back_sphere.translate(App.Vector(
    reboot_x_offset + (reboot_slot_width/2),
    y_offset + slot_thickness + (slots_count * (slot_thickness + slot_spacing)) + reboot_slot_thickness * 8,
    z_offset + Config.card_width + (Config.wall_thickness/2)
))

# Cut slots and spheres from box
hollow_box = hollow_box.cut(reboot_slot)
hollow_box = hollow_box.cut(front_sphere)
hollow_box = hollow_box.cut(back_sphere)

# Add to document
box_shape = doc.addObject("Part::Feature", "Box")
box_shape.Shape = hollow_box

# Recompute the document
doc.recompute()

# Switch to isometric view and fit to window
Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")


