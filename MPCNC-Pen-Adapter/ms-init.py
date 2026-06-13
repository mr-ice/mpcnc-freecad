import os
import sys

os.chdir("/Users/michael/3dp/freeCAD")
sys.path.insert(0, ".")
from endstops import Config, MicroSwitch

doc = App.newDocument("Unnamed")
config = Config()
ms = MicroSwitch(doc)
negatives = ms.get_pin_holes
# ms1 = ms.get_assembly()
# msh = MicroSwitchHousing(doc, ms)
# msh1 = msh.get_assembly()
wall = 2.5
housing = doc.addObject("Part::Box", "Housing")
housing.Height = config.body_depth
housing.Width = config.body_width + wall * 2
housing.Length = config.body_height + wall * 2
housing.Placement.Base.x = -wall
housing.Placement.Base.y = -wall
housing.Placement.Base.z = config.body_offset_z

negatives += ms.get_negative()
cutter = housing

for tool in negatives:
    newcut = doc.addObject("Part::Cut", "Cut")
    newcut.Base = cutter
    newcut.Tool = tool
    # cutter.Visibility = False
    # tool.Visibility = False
    # newcut.ViewObject.ShapeColor=getattr(cutter.getLinkedObject(True).ViewObject,'ShapeColor', cutter.ViewObject.ShapeColor)
    # newcut.ViewObject.DisplayMode=getattr(cutter.getLinkedObject(True).ViewObject,'DisplayMode', cutter.ViewObject.DisplayMode)
    cutter = newcut

doc.recompute()
Gui.runCommand("Std_OrthographicCamera", 1)
Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
# from PenHolderConfig import *  # configuration elements

# from tube import tube
# for pasting into freecad that's not sufficient, and I've had to copy/paste the entire tube function in
