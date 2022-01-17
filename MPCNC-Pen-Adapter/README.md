MPCNC Pen Holder

This is an adapter for holding a Fisher Space Plotter Pen (from [1])
in place of the cutting tool on the MPCNC Lowrider 2.

My router plate has a single 36mm round hole for the router bit.  I didn't
use the recommended dewalt, so I didn't need the dust collection.   The
router I did buy has its own dust collection cover.  The friction ring is very
tight currently.  You might need to adjust it.

This fits into the hole I made for the router using friction, and sits on top of the router plate
on the CNC machine.  It allows the pen to move up and down but not side to side with three
vertical 150mm steel rods and linear bearings

- 150mm rods - [2]
- linear bearings - [3]

These are the parts in this model

- Base - holds the rods vertical, sits on top of the Lowrider's router plate
- Insert - cylinder to push through the base and the router plate's hole to hold everything together
- Slider - This holds three sets of linear bearings to allow the pen to move up and down.  It also 
           provides space for up to 40 US nickel (5c) coins at 5g each to provide 250g of downward force
           as recommended on the pens (200g of coins + the slider and bearings is way too much, reduce
           your coins until you get between 200 and 250g)
- Caddy - The clip that grabs the pen top (remove the tape label)

Currently at v1.0 the caddy is meant to glue to the bottom of the slider.   A future version may
provide a way to slide this down through the weight tube and glue it there (still needs to be
glued so that the entire slider moves when pressed on the pen tip.

Python:

These models are presented as python that runs within FreeCAD's CLI.   Open FreeCAD, paste the
init.py first, then tube.py.   For various reasons I couldn't get import <file> to work properly.

Then paste each additional file into a new document.  This will give you the models in FreeCad
to tweak or export to stl for your slicer.

[1] https://www.amazon.com/gp/product/B07645YD1M/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1

[2] https://www.amazon.com/gp/product/B01NCOMFLT/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1

[3] https://www.amazon.com/gp/product/B07KR6H3XK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1
