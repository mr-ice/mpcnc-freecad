import FreeCAD as App
import FreeCADGui as Gui

# Get the active document
doc = App.activeDocument()

# Get the Box object
box = doc.getObject("Box")

target_z = 42.66666667
tolerance = 0.01

# Define specific coordinates to look for
x_coords = [11.0, 110.0, 203.0, 104.0]
y_coords = [309.0, 11.0, 94.0]

# Get all edges at the specified Z height
edges_at_z = []
edges_index_at_z = []
for i, edge in enumerate(box.Shape.Edges):
    if len(edge.Vertexes) < 2:
        continue
        
    v1 = edge.Vertexes[0]
    v2 = edge.Vertexes[1]
    
    # Skip edges that are too short
    if edge.Length < tolerance:
        continue
    
    # Check if both vertices are at the target Z height
    if (abs(v1.Point.z - target_z) < tolerance and 
        abs(v2.Point.z - target_z) < tolerance):
        
        # Check if edge contains any of our specific coordinates
        edge_has_target_coord = False
        for x in x_coords:
            if (abs(v1.Point.x - x) < tolerance and 
                abs(v2.Point.x - x) < tolerance):
                edge_has_target_coord = True
                break
                
        for y in y_coords:
            if (abs(v1.Point.y - y) < tolerance and 
                abs(v2.Point.y - y) < tolerance):
                edge_has_target_coord = True
                break
        
        if not edge_has_target_coord:
            edges_index_at_z.append(i + 1)
            print(f"Found edge at z={v1.Point.z}: Edge{i + 1}")
            print(f"  Coordinates: ({v1.Point.x}, {v1.Point.y}) to ({v2.Point.x}, {v2.Point.y})")
            edges_at_z.append(edge)

# Clear current selection
Gui.Selection.clearSelection()

# Select the edges
for edge_num in edges_index_at_z:
    Gui.Selection.addSelection(box, f"Edge{edge_num}")