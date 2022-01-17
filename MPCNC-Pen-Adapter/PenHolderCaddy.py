# PenHolderCaddy holds the pen to the slider

import FreeCAD as App
import FreeCADGui as Gui
from PenHolderConfig import *

doc = App.ActiveDocument

# Tube butt up against the slider base
c1 = tube(base_thickness, nickel_diameter + 4, pen_diameter)
c1.Height = 1
c1.Radius = nickel_diameter/2 + 2

# Tube to hold the top of the pen (0.2 tolerance here, we want a snug fit)
c2 = tube(pen_shank_overall, pen_diameter + 3, pen_diameter + 0.2)
# c2.Placement.Base.z=-pen_shank_overall

# currently glue together, but future may be to lock this onto the 
# slider flanges with matching wings and some kind of fastening.  Problem
# becomes printing it with the wings, as there will be some kind of bridging
# # make a wing flange to hold this to the slider wings
# w1 = doc.addObject("Part::Box", "WingFlange")
# w1.Height = pen_shank_overall
# w1.Width = upright_hole/2
# w1.Length = outer_diameter - nickel_diameter + 1
# w1.Placement.Base.y = upright_hole/4
# w1.Placement.Base.x = nickel_diameter/2

# # fillet the outside corners of the flange

# cutter = doc.addObject("Part::Cylinder", "WingCutter")
# cutter.Height = pen_shank_overall + 2
# cutter.Radius = (nickel_diameter + 4)/2

# w2 = doc.addObject("Part::Cut", "Wing")
# w2.Base = w1
# w2.Tool = cutter

doc.recompute()

Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
