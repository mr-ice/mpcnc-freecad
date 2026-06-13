import FreeCAD as App
import Part
from FreeCAD import Base
import parameters as params

precision = 0.01

def cut_slot(shape):
    """Create a slot by sweeping a cylinder along a path"""
    # Create the path for the sweep
    path_points = [
        Base.Vector(0, params.BASE_OD/2, 0),                    # Start at bottom
        Base.Vector(0, params.BASE_OD/2, params.SLOT_DEPTH),    # Vertical up
        Base.Vector(0, params.BASE_OD/2 + params.SLOT_LENGTH, params.SLOT_DEPTH)  # Horizontal out
    ]
    
    # Create a series of cylinders along the path
    cylinders = []
    
    # Create cylinders along vertical path
    steps = 10  # Number of intermediate cylinders
    for i in range(steps + 1):
        t = i / steps
        pos_z = t * params.SLOT_DEPTH
        cyl = Part.makeCylinder(params.SLOT_WIDTH/2, params.BASE_OD)
        cyl.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
        cyl.translate(Base.Vector(0, 0, pos_z))
        cylinders.append(cyl)
    
    # Create cylinders along horizontal path
    for i in range(steps + 1):
        t = i / steps
        pos_y = params.BASE_OD/2 + t * params.SLOT_LENGTH
        cyl = Part.makeCylinder(params.SLOT_WIDTH/2, params.BASE_OD)
        cyl.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
        cyl.translate(Base.Vector(0, 0, params.SLOT_DEPTH))
        cyl.translate(Base.Vector(0, t * params.SLOT_LENGTH, 0))
        cylinders.append(cyl)
    
    # Combine all cylinders
    sweep = cylinders[0]
    for cyl in cylinders[1:]:
        sweep = sweep.fuse(cyl)
    
    Part.show(sweep, "Sweep")
    
    # Create and position second sweep (180 degrees rotation)
    sweep2 = sweep.copy()
    sweep2.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 180)
    
    # Cut both sweeps from the shape
    result = shape.cut(sweep)
    result = result.cut(sweep2)
    
    return result



def create_tapered_section(bottom_od, bottom_id, top_od, top_id, height):
    if bottom_od == top_od:
        outer = Part.makeCylinder(bottom_od / 2, height)
    else:
        outer = Part.makeCone(bottom_od / 2, top_od / 2, height)

    if bottom_id == top_id:
        inner = Part.makeCylinder(bottom_id / 2, height)
    else:
        inner = Part.makeCone(bottom_id / 2, top_id / 2, height)

    return outer.cut(inner)


def create_fillet(shape, at, radius):
    fillet_edges = []
    for edge in shape.Edges:
        if len(edge.Vertexes) == 1:
            if (edge.Vertexes[0].Point.x - at) < precision:
                fillet_edges.append(edge)  
    return shape.makeFillet(radius, fillet_edges)


def create_path_points_object():
    """Create a compound object from the path points used in slot creation"""
    # Calculate x position for the third point using Pythagorean theorem
    # The point should lie on the cylinder surface at BASE_OD/2
    y_pos = params.BASE_OD/2
    x_pos = 0
    
    path_points = [
        Base.Vector(0, params.BASE_OD/2, 0),                    # Start at bottom
        Base.Vector(0, params.BASE_OD/2, params.SLOT_DEPTH),    # Vertical up
        Base.Vector(x_pos, y_pos, params.SLOT_DEPTH)         # Horizontal out, on surface
    ]
    
    # Create small spheres at each point
    spheres = []
    for point in path_points:
        sphere = Part.makeSphere(1, point)  # 1mm radius spheres for visibility
        spheres.append(sphere)
        Part.show(sphere, "Sphere")
    
    # Create a compound from all spheres
    path_compound = Part.makeCompound(spheres)
    
    # Add to document
    doc = App.activeDocument()
    path_obj = doc.addObject("Part::Feature", "SlotPath")
    path_obj.Shape = path_compound
    
    # Create mirrored path points (180 degrees rotation)
    spheres_mirror = []
    for point in path_points:
        # For mirroring, we need to handle the x position correctly
        if point.y > params.BASE_OD/2:  # Only the third point
            mirrored_point = Base.Vector(x_pos, -point.y, point.z)
        else:
            mirrored_point = Base.Vector(0, -point.y, point.z)
        sphere = Part.makeSphere(1, mirrored_point)
        spheres_mirror.append(sphere)
    
    path_compound_mirror = Part.makeCompound(spheres_mirror)
    path_obj_mirror = doc.addObject("Part::Feature", "SlotPathMirrored")
    path_obj_mirror.Shape = path_compound_mirror


def create_adapter():
    doc = App.activeDocument()
    
    # Create and show path points
    create_path_points_object()
    
    # Create base cylinder
    base = create_tapered_section(
        params.BASE_OD,
        params.BASE_ID,
        params.BASE_OD,
        params.BASE_ID,
        params.BASE_HEIGHT,
    )
    first_ridge = create_tapered_section(
        params.FIRST_RIDGE_OD,
        params.FIRST_RIDGE_ID,
        params.FIRST_RIDGE_OD,
        params.FIRST_RIDGE_ID,
        params.RIDGE_HEIGHT,
    )
    first_ridge = create_fillet(first_ridge, 
                                params.FIRST_RIDGE_OD,
                                params.RIDGE_HEIGHT/2 - precision)
    first_ridge.translate(Base.Vector(0, 0, params.BASE_HEIGHT))

    # Create middle section
    mid_section = create_tapered_section(
        params.MID_OD,
        params.MID_ID,
        params.TOP_OD,
        params.TOP_ID,
        params.MID_HEIGHT + params.RIDGE_HEIGHT,
    )
    mid_section.translate(
        Base.Vector(0, 0, params.BASE_HEIGHT + params.RIDGE_HEIGHT)
    )
    second_ridge = create_tapered_section(
        params.SECOND_RIDGE_OD,
        params.SECOND_RIDGE_ID,
        params.SECOND_RIDGE_OD,
        params.SECOND_RIDGE_ID,
        params.RIDGE_HEIGHT,
    )
    second_ridge = create_fillet(second_ridge, 
                                params.SECOND_RIDGE_OD,
                                params.RIDGE_HEIGHT/2 - precision)
    second_ridge.translate(
        Base.Vector(
            0, 0, params.BASE_HEIGHT + params.RIDGE_HEIGHT + params.MID_HEIGHT
        )
    )
    top_section = create_tapered_section(
        params.TOP_OD,
        params.TOP_ID,
        params.TOP_UPPER_OD,
        params.TOP_UPPER_ID,
        params.TOP_HEIGHT
    )
    top_section.translate(
        Base.Vector(
            0,
            0,
            params.BASE_HEIGHT
            + params.RIDGE_HEIGHT
            + params.MID_HEIGHT
            + params.RIDGE_HEIGHT,
        )
    )
    final_shape = (
        cut_slot(base).fuse(first_ridge).fuse(mid_section).fuse(second_ridge).fuse(top_section)
    )

    # Create FreeCAD object
    adapter = doc.addObject("Part::Feature", "Adapter1")
    adapter.Shape = final_shape

    doc.recompute()
    return adapter


if __name__ == "__main__":
    # Create a new document if none exists
    if App.activeDocument() is None:
        doc = App.newDocument("Adapter1")

    create_adapter()
