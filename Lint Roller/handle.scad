// pin diameter = 8mm
// roll diameter = 53.75mm
// roll length = 102mm

pin_radius = 4;  // pin diameter = 8mm

roll_radius = 26.875; // roll diameter = 53.75

roll_length = 102;  // roll length (height)


rotate(0,90,0)
cylinder(roll_length, roll_radius, roll_radius, $fn=180);

// 2