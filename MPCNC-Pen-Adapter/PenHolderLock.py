# PenHolderLock holds the PenCaddy to the slider

import FreeCAD as App
import FreeCADGui as Gui
from Draft import make_polar_array
from PenHolderConfig import *


doc = App.ActiveDocument

# Tube butt up against the slider base
# nickel tube is nickel_diameter+4
# to get a bit of a lip around that, add another 4
# pen holder tube is pen_diameter + 3, add 0.2 for tolerance to fit over it
c1 = tube(base_thickness, nickel_diameter + 8, pen_diameter + 3 + tolerance)

w1 = doc.addObject("Part::Box", "Wing1")
w1.Height = base_thickness * 4
w1.Length = pen_diameter
w1.Width = base_thickness

# offset these by half the thickness of the slider wings
w1.Placement.Base.y = upright_hole/2/2 + tolerance
w1.Placement.Base.x = (nickel_diameter + 4)/2 - 1

w2 = doc.addObject("Part::Box", "Wing1")
w2.Height = base_thickness * 4
w2.Length = pen_diameter
w2.Width = base_thickness

# offset these by half the thickness of the slider wings
w2.Placement.Base.y = -upright_hole/2/2 - tolerance - base_thickness
w2.Placement.Base.x = (nickel_diameter + 4)/2 - 1

wingb = doc.addObject("Part::Fuse", "WingBase")
wingb.Base = w1
wingb.Tool = w2

cutter = doc.addObject("Part::Cylinder", "WingCutter")
cutter.Radius = (nickel_diameter + 4)/2 + tolerance
cutter.Height = w2.Height + 2
cutter.Placement.Base.z = -1 

wings = doc.addObject("Part::Cut", "Wings")
wings.Base = wingb
wings.Tool = cutter

wall = doc.addObject("Part::Cylinder", "WallBase")
wall.Height = w2.Height
wall.Radius = c1.Base.Radius
wall.Angle = 100
wall.Placement.Rotation = App.Rotation(-110, 0, 0)

justwall = doc.addObject("Part::Cut", "CutWall")
justwall.Base = wall
justwall.Tool = cutter

wingwall = doc.AddObject("Part::Fuse", "WingWall")
wingwall.Base = justwall
wingwall.Tool = wings

wingarray = make_polar_array(wingwall, 3, use_link=True)


doc.recompute()

Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
