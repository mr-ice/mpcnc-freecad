import FreeCAD as App
import FreeCADGui as Gui
# from Draft import make_polar_array
# make_polar_array(cut, 3, use_link=True)

doc = App.ActiveDocument

def tube(h, od, id):
    """A tube is a cylinder with a (presumably smaller) cylinder removed"""
    oc = doc.addObject("Part::Cylinder","OutCylinder")
    ic = doc.addObject("Part::Cylinder","InCylinder")

    oc.Height = h
    ic.Height = h+2

    oc.Radius = od/2
    ic.Radius = id/2

    ic.Placement.Base.z=-1

    cut = doc.addObject("Part::Cut", "Cut")
    cut.Base = oc
    cut.Tool = ic
    App.Gui.activeDocument().hide("OutCylinder")
    App.Gui.activeDocument().hide("InCylinder")
    doc.recompute()
    return cut

