from Draft import make_polar_array
outer_diameter = 37.75  # of the hole, not the fitting
base_thickness = 3
upright_height = 17
upright_diameter = 15
end_diameter = upright_diameter + 2
upright_hole = 8

fitting_diameter = outer_diameter + 6

end_radius = end_diameter/2

doc = App.activeDocument()

c1 = tube(upright_height, upright_diameter, upright_hole)
c1.Placement.Base.x = outer_diameter
c2 = doc.addObject("Part::Cylinder", "Pole Holder")
c2.Placement.Base.x = outer_diameter
c2.Height = base_thickness
c2.Radius = end_radius

f1 = doc.addObject("Part::Fuse", "Pole_Holder_Base")
f1.Tool = c1
f1.Base = c2

a1 = make_polar_array(f1, 3, use_link=True)

p1 = doc.addObject("Part::Prism","Triangle")
p1.Polygon=3
p1.Circumradius=outer_diameter+end_diameter
p1.Height=2.00
p1.FirstAngle=0.00
p1.SecondAngle=0.00
p1.Placement=App.Placement(App.Vector(0.00,0.00,0.00),App.Rotation(App.Vector(0.00,0.00,1.00),0.00))
p1.Label='Prism'

fillet = doc.addObject("Part::Fillet","Fillet")
fillet.Base = p1
__fillets__ = []
__fillets__.append((1,8.50,8.50))
__fillets__.append((2,8.50,8.50))
__fillets__.append((5,8.50,8.50))
fillet.Edges = __fillets__
del __fillets__
p1.Visibility = False

cutout = doc.addObject("Part::Cylinder", "CutOut")
cutout.Height = base_thickness+2
cutout.Radius = outer_diameter/2 + 0.2
cutout.Placement.Base.z = -1

base = doc.addObject("Part::Cut", "Full_Base")
base.Base = fillet
base.Tool = cutout
fillet.Visibility = False
cutout.Visibility = False

whole = doc.addObject("Part::Fuse", "Whole_Base")
whole.Base = base
whole.Tool = a1
base.Visibility = False
a1.Visibility = False

doc.recompute()

Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
