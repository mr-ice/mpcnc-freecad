# import FreeCAD
# from FreeCAD import App, FreeCADGui, Gui
from math import sqrt

# i
box_chamfer_target_height = App.ActiveDocument.Spreadsheet.B7
# t
thickness = App.ActiveDocument.Spreadsheet.B6

# l
box_chamfer_target_length = sqrt(box_chamfer_target_height**2 + \
                            box_chamfer_target_height**2)



# The chamfer for the hole starts offset by -thickness, -thickness 


# Box and Box001 are offset by thickness.  But we want the chamfer to also
# be only separated by thickness.  To do this we need to find l the length
# of the outer chamfer, and m the length of the inner chamfer.
#
#              \ \ both t
#                    / /
#                           _
# -                /\       
# h               /  \         _
# -            l / /\ \     i 
#               / /  \ \     
#     _        /_/____\_\   _  j
#      t      m /      \     
#     _        /________\      _
#

# j
hole_chamfer_target_height = box_chamfer_target_height.Value - sqrt(thickness.Value **2 + thickness.Value **2) + thickness.Value

print(f"""\
      {hole_chamfer_target_height=}
      {box_chamfer_target_height=}
      """)

hole_chamfer_target_length = sqrt(
    hole_chamfer_target_height**2 +\
    hole_chamfer_target_height**2
)
print(f"{box_chamfer_target_length=}, {hole_chamfer_target_length=}")



print(f"""\
An isosceles triangle with sides {box_chamfer_target_length} differs in
height from an isosceles triangle with sides {hole_chamfer_target_length}
by 
{sqrt(hole_chamfer_target_length**2 /2) - sqrt(box_chamfer_target_height**2 /2)} which should be very close to {sqrt(8)}
""")

doc = FreeCAD.ActiveDocument

doc.addObject("Part::Chamfer","Chamfer")
doc.Chamfer.Base = doc.Box
__fillets__ = []
__fillets__.append((7,box_chamfer_target_length,box_chamfer_target_length))
doc.Chamfer.Edges = __fillets__
del __fillets__
FreeCADGui.ActiveDocument.Box.Visibility = False

doc.Chamfer.ViewObject.LineColor=getattr(doc.Box.getLinkedObject(True).ViewObject,'LineColor',doc.Chamfer.ViewObject.LineColor)
doc.Chamfer.ViewObject.PointColor=getattr(doc.Box.getLinkedObject(True).ViewObject,'PointColor',doc.Chamfer.ViewObject.PointColor)
Gui.activeDocument().resetEdit()

doc.addObject("Part::Chamfer","Chamfer001")
doc.Chamfer001.Base = doc.Box001
__fillets__ = []
__fillets__.append((7,hole_chamfer_target_length,hole_chamfer_target_length))
doc.Chamfer001.Edges = __fillets__
del __fillets__
FreeCADGui.ActiveDocument.Box001.Visibility = False

doc.Chamfer001.ViewObject.LineColor=getattr(doc.Chamfer001.Box001.getLinkedObject(True).ViewObject,'LineColor',doc.Chamferr001.ViewObject.LineColor)
doc.Chamfer001.ViewObject.PointColor=getattr(doc.Chamfer001.Box001.getLinkedObject(True).ViewObject,'PointColor',doc.Chamfer001.ViewObject.PointColor)
Gui.activeDocument().resetEdit()

# Cut the hole out of the box

doc.addObject("Part::Cut","Cut")
doc.Cut.Base = doc.Chamfer
doc.Cut.Tool = doc.Chamfer001
FreeCADGui.ActiveDocument.Chamfer.Visibility=False
FreeCADGui.ActiveDocument.Chamfer001.Visibility=False
doc.Cut.ViewObject.ShapeColor=getattr(doc.Chamfer.getLinkedObject(True).ViewObject,'ShapeColor',doc.Cut.ViewObject.ShapeColor)
doc.Cut.ViewObject.DisplayMode=getattr(doc.Chamfer.getLinkedObject(True).ViewObject,'DisplayMode',doc.Cut.ViewObject.DisplayMode)
doc.recompute()
