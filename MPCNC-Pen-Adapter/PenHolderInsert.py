from Draft import make_polar_array
outer_diameter = 37.75  # outer diameter (hole in plate)
inner_diameter = 11.7   # inner diameter (hole for pen)
pen_depth = 10 # holder depth

# from Draft import make_polar_array
# make_polar_array(cut, 3, use_link=True)
doc = App.activeDocument()

# vertical walls
c1 = tube(pen_depth, outer_diameter, outer_diameter-4)

# horizontal stop
c2 = tube(2, outer_diameter+4, outer_diameter)

# friction points
c3 = tube(pen_depth*.75, outer_diameter+0.6, outer_diameter-4)
c3.Base.Angle = 10.0
c3 = make_polar_array(c3, 3, use_link=True)

u1 = doc.addObject("Part::Fuse", "Fusion")
u1.Base = c1
u1.Tool = c2

u2 = doc.addObject("Part::Fuse", "Fusion")
u2.Base = u1
u2.Tool = c3

doc.recompute()

Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
