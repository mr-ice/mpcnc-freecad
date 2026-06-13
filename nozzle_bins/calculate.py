#!/usr/local/bin/python3
"""Calculate what we need for the nozzle labels.

Labels are 8mm on a side, 1mm thick, with a chamfer to 1/2 their
thickness.
"""
import math

thickness = 1  # mm
a = thickness / 2
width = 8  # mm

# isosceles right triangle
# hb = sqrt( a**2 - (0.5 * b) **2

# The height is the value of the chamfer where the sides are 0.5mm and the base
b = math.sqrt(a**2 + a**2)  # (hypotenuse)

print(math.sqrt(a**2 - (0.5 * b) ** 2))
