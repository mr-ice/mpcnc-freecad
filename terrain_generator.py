import FreeCAD as App
import Part
import random
import datetime
from FreeCAD import Base
import math
from config import config


def create_channel_cutter(length=2 * config.square_size, thickness_mm=2.75, width=1.2, radius=0.6):
    """
    Create a channel cutter profile.
    
    The channels are to outline the edges of the tile, and round off the top edge.
    """

    vert_height_offset = 0.05 + 0.4
    vert_height = thickness_mm - radius - vert_height_offset
    radii_height = thickness_mm - vert_height_offset

    # Create profile edges
    # Bottom edge
    bottom = Part.makeLine(
        Base.Vector(0, -width/2, 0),  # Bottom left
        Base.Vector(0, width/2, 0)    # Bottom right
    )

    
    # Right vertical side
    right_vert = Part.makeLine(
        Base.Vector(0, width/2, 0),              # Bottom right
        Base.Vector(0, width/2, vert_height)     # Top of vertical right
    )

    
    # Right arc (from vertical to horizontal)
    right_arc = Part.makeCircle(
        radius,                                          # Radius
        Base.Vector(0, width/2 + radius, radii_height),  # Center point moved out by radius
        Base.Vector(1, 0, 0),                            # Normal along X axis
        90, 180                                          # Arc angles
    )
    right_arc.translate(Base.Vector(0, 0, -radius))
    
    # Top Vertical Line
    top_vert_right = Part.makeLine(
        Base.Vector(0, width/2 + radius, thickness_mm + radius),  # Right end
        Base.Vector(0, width/2 + radius, vert_height + radius)     # Top of vertical right
    )
    # Top horizontal line
    top = Part.makeLine(
        Base.Vector(0, width/2 + radius, thickness_mm + radius),  # Right end
        Base.Vector(0, -width/2 - radius, thickness_mm + radius)  # Left end
    )

    # Top vertical line
    top_vert_left = Part.makeLine(
        Base.Vector(0, -width/2 - radius, thickness_mm + radius),  # Left end
        Base.Vector(0, -width/2 - radius, vert_height + radius)     # Top of vertical left
    )

    # Left arc (from horizontal to vertical)
    left_arc = Part.makeCircle(
        radius,                                          # Radius
        Base.Vector(0, -width/2 - radius, radii_height), # Center point moved out by radius
        Base.Vector(1, 0, 0),                            # Normal along X axis
        0, 90                                            # Arc angles
    )
    left_arc.translate(Base.Vector(0, 0, -radius))

    
    # Left vertical side
    left_vert = Part.makeLine(
        Base.Vector(0, -width/2, vert_height),  # Top of vertical left
        Base.Vector(0, -width/2, 0)             # Back to start
    )

    
    # Create the complete wire for reference
    edges = [bottom, right_vert, right_arc, top_vert_right, top, top_vert_left, left_arc, left_vert]
    wire = Part.Wire(edges)
    # wire_obj = App.ActiveDocument.addObject("Part::Feature", "wire")
    # wire_obj.Shape = wire
    
    # Create a face from the wire
    face = Part.Face(wire)
    
    # Create the solid by extruding the face
    solid = face.extrude(Base.Vector(length, 0, 0))  # Extrude along X axis
    
    return solid


def create_water_tile(width_squares=2, length_squares=2, thickness_mm=2.25, wave_amplitude=0.5):
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
    total_width = width_squares * config.square_size
    total_length = length_squares * config.square_size
    
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
            random.seed(i * 73 + j * 31 + datetime.datetime.now().microsecond)  # Prime numbers for less regular patterns
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
        for x in range(length_squares+1):
            cutter = create_channel_cutter(total_width + 0.4, thickness_mm, 1.2)
            cutter.translate(Base.Vector(-0.2, x * config.square_size, 0.6))
            cuts.append(cutter)
            cutterObj = doc.addObject("Part::Feature", "ChannelCutter")
            cutterObj.Shape = cutter

        for y in range(width_squares+1):
            cutter = create_channel_cutter(total_length + 0.4, thickness_mm, 1.2)
            cutter.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), 90)
            cutter.translate(Base.Vector(y * config.square_size, -0.2, 0.6))  # three layers at 0.2mm
            cuts.append(cutter)
            cutterObj = doc.addObject("Part::Feature", "ChannelCutter")
            cutterObj.Shape = cutter
        

        # Create final shape by cutting the solid
        final_shape = water_solid
        for cut in cuts:
            final_shape = final_shape.cut(cut)
        
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