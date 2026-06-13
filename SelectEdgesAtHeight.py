import FreeCAD as App
import FreeCADGui as Gui

# Get the active document
doc = App.activeDocument()

# Get the Box object
box = doc.getObject("Box")
hollow_box = box.Shape

target_z = 42.66666667
tolerance = 0.01


def fpequals(a, b):
    return abs(a - b) < tolerance


# Define specific coordinates to look for
x_coords = [13.0, 106.0, 112.0, 205.0]
y_coords = [13.0, 98.0, 307.0]


def get_edges_at_z(shape, target_z):
    # Get all edges at the specified Z height
    edges_at_z = []
    edges_index_at_z = []
    for i, edge in enumerate(shape.Edges):
        if len(edge.Vertexes) < 2:
            continue

        v1 = edge.Vertexes[0]
        v2 = edge.Vertexes[1]

        # Skip edges that are too short
        if edge.Length < tolerance:
            continue

        # Check if both vertices are at the target Z height
        if fpequals(v1.Point.z, target_z) and fpequals(v2.Point.z, target_z):
            # Check if edge contains any of our specific coordinates
            edge_has_target_coord = False
            for x in x_coords:
                if abs(v1.Point.x - x) < tolerance and abs(v2.Point.x - x) < tolerance:
                    edge_has_target_coord = True
                    break

            for y in y_coords:
                if abs(v1.Point.y - y) < tolerance and abs(v2.Point.y - y) < tolerance:
                    edge_has_target_coord = True
                    break

            if not edge_has_target_coord:
                edges_index_at_z.append(i + 1)
                print(f"Found edge at z={v1.Point.z}: Edge{i + 1}")
                print(
                    f"  Coordinates: ({v1.Point.x}, {v1.Point.y}) to ({v2.Point.x}, {v2.Point.y})"
                )
                edges_at_z.append(edge)

    return edges_at_z, edges_index_at_z


# Clear current selection
Gui.Selection.clearSelection()

edges_at_z, edges_index_at_z = get_edges_at_z(hollow_box, target_z)

# Select the edges
for edge_num in edges_index_at_z:
    Gui.Selection.addSelection(box, f"Edge{edge_num}")

# hollow_box = hollow_box.makeFillet(1, edges_at_z)
