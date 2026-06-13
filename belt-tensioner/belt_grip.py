#!/usr/bin/env python3
import argparse
import openpyscad as ops
from MetricBolt import MetricBolt
from semicylinder import semicylinder
from Config import ReadConfig

config = ReadConfig('belt-tensioner.config')

AP = argparse.ArgumentParser(description="Create Belt Grip Parts")

AP.add_argument('--part', help='Which part to make', required=True)

AP.add_argument('--out', help='Output Filename')

args = AP.parse_args()

if not args.out:
    args.out = 'belt_tensioner_' + str(args.part) + '.scad'

with open (args.out, 'w') as fh:
    fh.write('$fn=180;\n')

    d = ops.Difference()
    u = ops.Union()
    u.append(semicylinder(config.griplength, config.gripradius, config.gripdepth))
    d.append(u)
    b = MetricBolt(3, 12, negative=True)
    c = b.cap
    s = b.shaft
    n = b.nut
    o = config.beltwidth/2 + b.shaft.r

    if args.part == 'top':
        d.append(b.bolt.rotate([0,-90,0]).translate([b.cap.h+config.boltgrip,o,config.griplength/2]))
        d.append(b.bolt.rotate([0,-90,0]).translate([b.cap.h+config.boltgrip,-o,config.griplength/2]))
    elif args.part == 'bottom':
        u.append(ops.Cube([config.gripdepth+config.boltgrip, config.beltwidth, config.griplength]).translate([0,-config.beltwidth/2,0]))
        both = b.bolt.rotate([0,0,30]).rotate([0,90,0])
        left = both.translate([-b.cap.h-b.shaft.h+config.boltgrip,o,config.griplength/2])
        right = both.translate([-b.cap.h-b.shaft.h+config.boltgrip,-o,config.griplength/2])
        d.append(left)
        d.append(right)

        for z in range(1, int(config.griplength), 2):
            d.append(ops.Cube([1,config.beltwidth,1]).translate([0,-config.beltwidth/2,z]))

        bolt = MetricBolt(3, config.griplength+2, negative=True)
        bolt.faces = 4
        d.append(bolt.bolt.rotate([0,0,45]).translate([config.gripdepth/2,0,-bolt.cap.h-3]))
    d.rotate([0,-90,0]).dump(fh)




