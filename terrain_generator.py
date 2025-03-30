import FreeCAD as App
import Part
import random
from FreeCAD import Base
import math

def create_water_tile(width_squares=2, length_squares=2, square_size_inch=1.25, thickness_mm=2.25, wave_amplitude=0.5):
    """
    Create a water terrain tile with specified dimensions
    
    Parameters:
    width_squares: number of squares wide
    length_squares: number of squares long
    square_size_inch: size of each square in inches
    thickness_mm: thickness of the base in mm
    wave_amplitude: height of the water ripples in mm
    """
    
    # Convert inches to mm
    square_size_mm = square_size_inch * 25.4
    total_width = width_squares * square_size_mm
    total_length = length_squares * square_size_mm
    
    # Create base document
    doc = App.newDocument()
    
    # Create base plate
    base = Part.makeBox(total_width, total_length, thickness_mm)
    
    # Create water surface with ripples
    steps = 15 * width_squares  # Reduced steps for simpler surface
    dx = total_width / steps
    dy = total_length / steps
    
    # Create poles for the NURBS surface
    poles = []
    for i in range(steps + 1):
        row = []
        for j in range(steps + 1):
            x = i * dx
            y = j * dy
            
            # Create more irregular water pattern
            random.seed(i * 73 + j * 31)  # Prime numbers for less regular patterns
            z = thickness_mm + wave_amplitude * (
                math.sin(x * 0.3 + y * 0.2) * 0.3 +  # Base wave
                math.sin(x * 0.7 - y * 0.4) * 0.2 +  # Cross wave
                math.cos(x * 0.5 + y * 0.6) * 0.2 +  # Diagonal wave
                random.random() * 0.3  # Random component
            )
            
            row.append(Base.Vector(x, y, z))
        poles.append(row)
    
    # Create multiplicities and matching knots
    # For (steps+1) poles and degree 3, we need (steps-1) knot values
    mults_u = [4] + [1] * (steps - 3) + [4]  # First and last have multiplicity 4
    mults_v = mults_u[:]

    # Generate knots with even spacing
    num_knots = len(mults_u)  # Same as steps-1
    knots_u = []
    for i in range(num_knots):
        if i == 0:
            knots_u.append(0.0)  # First knot
        elif i == num_knots - 1:
            knots_u.append(1.0)  # Last knot
        else:
            # Evenly space the middle knots
            knots_u.append(i / (num_knots - 1))
    knots_v = knots_u[:]

    print(f"poles: {len(poles)}x{len(poles[0])}")
    print(f"knots_u: {len(knots_u)=} {knots_u=}")
    print(f"knots_v: {len(knots_v)=} {knots_v=}")
    print(f"mults_u: {sum(mults_u)=} {mults_u=}")
    print(f"mults_v: {sum(mults_v)=} {mults_v=}")
    
    # Create NURBS surface
    degree = 3
    water_surface = Part.BSplineSurface()
    try:
        water_surface.buildFromPolesMultsKnots(poles, 
                                             mults_u, mults_v,
                                             knots_u, knots_v,
                                             False, False, 
                                             degree, degree)
        
        face = water_surface.toShape()
        
        # Instead of extruding, create a solid by connecting to base
        # Create wire frame at base level
        base_wire = Part.makePolygon([
            Base.Vector(0, 0, 0),
            Base.Vector(total_width, 0, 0),
            Base.Vector(total_width, total_length, 0),
            Base.Vector(0, total_length, 0),
            Base.Vector(0, 0, 0)
        ])
        
        # Create a loft between water surface and base
        side_faces = []
        water_wire = Part.Wire(face.Edges)
        side_faces = Part.makeLoft([base_wire, water_wire], True)
        
        # Combine all faces into a solid
        shell = Part.Shell([face, Part.Face(base_wire), *side_faces.Faces])
        water_solid = Part.Solid(shell)
        
        # Create cutting lines for squares with rounded edges
        cuts = []
        for i in range(1, width_squares):
            # Create box for the main cut
            center_x = i * square_size_mm
            box = Part.makeBox(1.2, total_length, thickness_mm * 2,
                             Base.Vector(center_x - 0.6, 0, 0.4))
            
            # Create cylinders for the rounded edges
            radius = 0.6
            cyl1 = Part.makeCylinder(radius, total_length, 
                                   Base.Vector(center_x - 0.6, 0, 0.4 + radius), 
                                   Base.Vector(0, 1, 0))
            cyl2 = Part.makeCylinder(radius, total_length, 
                                   Base.Vector(center_x + 0.6, 0, 0.4 + radius), 
                                   Base.Vector(0, 1, 0))
            
            # Combine shapes
            cut_shape = box.fuse([cyl1, cyl2])
            cuts.append(cut_shape)
        
        for i in range(1, length_squares):
            # Create box for the main cut
            center_y = i * square_size_mm
            box = Part.makeBox(total_width, 1.2, thickness_mm * 2,
                             Base.Vector(0, center_y - 0.6, 0.4))
            
            # Create cylinders for the rounded edges
            radius = 0.6
            cyl1 = Part.makeCylinder(radius, total_width, 
                                   Base.Vector(0, center_y - 0.6, 0.4 + radius), 
                                   Base.Vector(1, 0, 0))
            cyl2 = Part.makeCylinder(radius, total_width, 
                                   Base.Vector(0, center_y + 0.6, 0.4 + radius), 
                                   Base.Vector(1, 0, 0))
            
            # Combine shapes
            cut_shape = box.fuse([cyl1, cyl2])
            cuts.append(cut_shape)
        
        # Create rounded edges for the outer perimeter
        edge_radius = 1.0
        perimeter_cuts = []
        
        # Top edge cylinder
        top_cyl = Part.makeCylinder(edge_radius, total_width,
                                  Base.Vector(0, total_length + edge_radius, edge_radius),
                                  Base.Vector(1, 0, 0))
        perimeter_cuts.append(top_cyl)
        
        # Bottom edge cylinder
        bottom_cyl = Part.makeCylinder(edge_radius, total_width,
                                    Base.Vector(0, -edge_radius, edge_radius),
                                    Base.Vector(1, 0, 0))
        perimeter_cuts.append(bottom_cyl)
        
        # Left edge cylinder
        left_cyl = Part.makeCylinder(edge_radius, total_length,
                                   Base.Vector(-edge_radius, 0, edge_radius),
                                   Base.Vector(0, 1, 0))
        perimeter_cuts.append(left_cyl)
        
        # Right edge cylinder
        right_cyl = Part.makeCylinder(edge_radius, total_length,
                                    Base.Vector(total_width + edge_radius, 0, edge_radius),
                                    Base.Vector(0, 1, 0))
        perimeter_cuts.append(right_cyl)
        
        # Create final shape by cutting the solid
        final_shape = water_solid.cut(cuts)
        final_shape = final_shape.cut(perimeter_cuts)
        
        # Create FreeCAD object
        terrain = doc.addObject("Part::Feature", "WaterTerrain")
        terrain.Shape = final_shape
        
        doc.recompute()
        return doc
        
    except Exception as e:
        print(f"Error creating surface: {e}")
        raise

# Create a 2x2 water tile (2.5" square)
# doc = create_water_tile(2, 2) 