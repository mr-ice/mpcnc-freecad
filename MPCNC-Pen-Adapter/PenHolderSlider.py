# import FreeCAD as App
# import FreeCADGui as Gui
from Draft import make_polar_array
from PenHolderConfig import *
# from tube import tube

doc = App.ActiveDocument

c1 = tube(bearing_height*2, bearing_diameter+4, bearing_diameter)
# c1.Placement.Base.x = outer_diameter

tubeslot = doc.addObject("Part::Cylinder", "TubeSlot")
tubeslot.Height = c1.Base.Height
tubeslot.Radius = c1.Base.Radius
tubeslot.Angle = 5

slottedtube = doc.addObject("Part::Cut", "SlottedTube")
slottedtube.Base = c1
slottedtube.Tool = tubeslot

slottedtube.Placement.Base.x = outer_diameter

array = make_polar_array(slottedtube, 3, use_link=True)

# nickel stack for weight.  While 42 is a good number for 40 nickels, it turns out the
# rest of the slider weighs something so we don't need 40 nickels, closer to 28
c2 = tube(nickel_height * 30, nickel_diameter+4, nickel_diameter+loose*2)
c2_bottom = tube(base_thickness, nickel_diameter+4, pen_diameter + 3 + loose)

stacktube = doc.addObject("Part::Fuse", "StackTube")
stacktube.Base = c2
stacktube.Tool = c2_bottom

wing = doc.addObject("Part::Box", "Box")
wing.Height = bearing_height * 2
wing.Width = upright_hole/2
wing.Length = outer_diameter - nickel_diameter + 1
wing.Placement.Base.y = -upright_hole/4
wing.Placement.Base.x = nickel_diameter/2 + 1


array2 = make_polar_array(wing, 3, use_link=True)

f1 = doc.addObject("Part::Fuse", "threes")
f1.Base = array
f1.Tool = array2

f2 = doc.addObject("Part::Fuse", "SliderAssembly")
f2.Base = f1
f2.Tool = stacktube

doc.recompute()

Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
