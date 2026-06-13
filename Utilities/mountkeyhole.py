import FreeCAD
import Part
import math

def create_keyhole(
    screw_head_diameter=10,
    screw_head_height=5,
    screw_shaft_diameter=4,
    backing_plate_height=3,
    corner_radius=4.99
):
    """
    Creates a keyhole mounting shape with rounded corners using FreeCAD
    
    Args:
        screw_head_diameter: Diameter of the bottom cylinder for screw head
        screw_head_height: Height of the cylinder for screw head
        screw_shaft_diameter: Diameter of the slot for screw shaft
        slot_length: Length of the slot extending from cylinder
        backing_plate_height: Height of the backing plate
        corner_radius: Radius for rounding corners
    """
    
    # Create the main cylinder for screw head
    screw_head = Part.makeCylinder(
        screw_head_diameter/2,  # radius
        screw_head_height,      # height
        FreeCAD.Vector(0, 0, 0),# placement
        FreeCAD.Vector(0, 0, 1) # direction
    )
    
    # Create the slot for screw shaft

    keyhole = Part.makeBox(screw_shaft_diameter, screw_head_diameter, screw_head_height)
    keyhole.translate(FreeCAD.Vector(-screw_shaft_diameter/2, 0, 0))

    keyhole = keyhole.fuse(screw_head)

    end = Part.makeCylinder(screw_shaft_diameter/2, screw_head_height, FreeCAD.Vector(0, screw_head_diameter, 0))
    keyhole = keyhole.fuse(end)

    tslot = Part.makeBox(screw_head_diameter, screw_head_diameter * 2, screw_head_height)
    tslot.translate(FreeCAD.Vector(-screw_head_diameter/2, -screw_head_diameter/2, backing_plate_height))
    
    fillet_edges = []
    for edge in tslot.Edges:
        if edge.Length > 0:
            if len(edge.Vertexes) > 1:
                v1 = edge.Vertexes[0]
                v2 = edge.Vertexes[1]
                if abs(v1.Point.z - v2.Point.z) > 0.01:
                    fillet_edges.append(edge)
    
    tslot = tslot.makeFillet(corner_radius, fillet_edges)
    
    keyhole = keyhole.fuse(tslot)


    return keyhole

if __name__ == "__main__":
    # Create document
    pass
doc = FreeCAD.activeDocument()

# Create keyhole
keyhole = create_keyhole()

# Create a FreeCAD part object
part = doc.addObject("Part::Feature", "Keyhole")
part.Shape = keyhole

# Refresh the document
doc.recompute()
