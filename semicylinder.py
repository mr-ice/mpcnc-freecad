length = 19
height = 9
diameter = 25
radius = diameter/2

def semicylinder( l = length, r = radius, h = height):
    d = radius * 2 + 2

    doc = App.activeDocument()
    sc = doc.addObject("Part::Cylinder","Cylinder")
    sc.Height = l
    sc.Radius = r

    cube = doc.addObject("Part::Box", "Box")
    cube.Height = d
    cube.Width = d
    cube.Length = d
    cube.Placement.move(Base.Vector(-r-h,-r-1,-1))

    cut = doc.addObject("Part::Cut","Cut")
    cut.Base = App.activeDocument().Cylinder
    cut.Tool = App.activeDocument().Box
    cut.Label = "SemiCylinder"
    sc.Visibility=False
    cube.Visibility=False
    cut.ViewObject.ShapeColor=getattr(App.getDocument('Unnamed').getObject('Cylinder').getLinkedObject(True).ViewObject,'ShapeColor',App.getDocument('Unnamed').getObject('Cut').ViewObject.ShapeColor)
    cut.ViewObject.DisplayMode=getattr(App.getDocument('Unnamed').getObject('Cylinder').getLinkedObject(True).ViewObject,'DisplayMode',App.getDocument('Unnamed').getObject('Cut').ViewObject.DisplayMode)

if __name__ == "__main__":
    semicylinder()
    doc.recompute()
    Gui.activeDocument().activeView().viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")

