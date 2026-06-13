import FreeCAD as App
import Part
import Draft

def create_token():
    # Create base cylinder
    radius = 25  # 50mm diameter
    height = 3   # 3mm thick
    cylinder = Part.makeCylinder(radius, height)
    
    # Create fillets on top and bottom edges
    edges = []
    for edge in cylinder.Edges:
        if edge.curvatureAt(0) > 0:  # Select circular edges
            edges.append(edge)
        
    # import code
    # code.interact(local=dict(globals(), **locals()))
    
    filleted_cylinder = cylinder.makeFillet(1.49, edges)
    
    # Create Part object
    token = App.ActiveDocument.addObject("Part::Feature", "InitiativeToken")
    token.Shape = filleted_cylinder
    
def create_text():
    # Create "GO" text
    text = Draft.make_text("GO", placement=App.Placement())
    text.ViewObject.FontSize = 20  # Adjust size as needed
    
    # Convert text to shape
    shape_view = Draft.make_shape2dview(text)
    App.ActiveDocument.recompute()
    
    # Get the shape from the view object and extrude it
    shape = shape_view.Shape
    extrusion = shape.extrude(App.Vector(0, 0, 2))  # 2mm height for text
    
    # Create Part object
    text_part = App.ActiveDocument.addObject("Part::Feature", "GOText")
    text_part.Shape = extrusion

def main():
    # Create new document if none exists
    if App.ActiveDocument is None:
        App.newDocument()
    
    create_token()
    create_text()
    
    App.ActiveDocument.recompute()

if __name__ == '__main__':
    main()
