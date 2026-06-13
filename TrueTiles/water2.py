import FreeCAD as App
import Part

# Create a new document
doc = App.newDocument()

# Create a 30.75mm square base
base_length = 30.75
base = Part.makeBox(base_length, base_length, 1)

# Create an array of points to define the wave shape
wave_amplitude = 2.0
wave_wavelength = 12.0
wave_points = []
for i in range(101):
    x = i / 100.0 * base_length
    y = wave_amplitude * (1 - (x - wave_wavelength / 2.0) ** 2 / (wave_wavelength / 2.0) ** 2)
    wave_points.append((x, y, 1))

# Create a closed wire object from the wave points
wire = Part.Wire.makePolygon(wave_points, closed=True)

# Extrude the wire to create the wave shape
wave_height = 0.5
face = wire.extrude((0, 0, wave_height))

# Cut the wave shape from the base to create the final shape
final_shape = base.cut(face)

# Add the final shape to the document and save it
doc.addObject("Part::Feature", "Final_Shape").Shape = final_shape
doc.recompute()
App.ActiveDocument.save("30.75mm_square_with_wave_top_surface.FCStd")
