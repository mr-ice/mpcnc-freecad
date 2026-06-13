import FreeCAD as App
import Part


def make_chevron_rib(length=15):
    # Dimensions
    width = 3  # Width of the rib
    height = 1.5  # Height of the chevron
    thickness = 0.8  # Thickness of the walls

    # Create outer chevron profile
    outer_points = [
        App.Vector(thickness, 0, 0),
        App.Vector(width / 2, height - thickness, 0),
        App.Vector(width - thickness, 0, 0),
        App.Vector(width, 0, 0),
        App.Vector(width / 2, height, 0),
        App.Vector(0, 0, 0),
    ]

    # Create wire and face
    wire = Part.makePolygon(outer_points + [outer_points[0]])
    face = Part.Face(wire)

    # Extrude along Y axis
    return face.extrude(App.Vector(0, 0, length))
    return face


# Test the chevron
doc = App.newDocument()
chevron = doc.addObject("Part::Feature", "chevron")
chevron.Shape = make_chevron_rib()
doc.recompute()
