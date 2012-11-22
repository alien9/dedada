#!/usr/bin/python
## The equivalent of:
##  "Working with Depth, Color and Audio Maps"
## in the OpenNI user guide.

"""
This creates a depth generator, checks if it can generate VGA maps in 30 FPS,
configures it to that mode, and then reads frames from it, printing out the
middle pixel value.
"""


from openni import *
import math, sys
ctx = Context()
ctx.init()

CX=0
FX=1000

# Create a depth generator
depth = DepthGenerator()
depth.create(ctx)

# Set it to VGA maps at 30 FPS
depth.set_resolution_preset(RES_VGA)
depth.fps = 30

# Start generating
ctx.start_generating_all()

while True:
    # Update to next frame
    nRetVal = ctx.wait_one_update_all(depth)

    depthMap = depth.map

    # Get the coordinates of the middle pixel
    x = depthMap.width / 2
    w = depthMap.width
    y = depthMap.height / 2
    
    f=False
    ds=0
    xs=[]
    n=0
    for i in range(depthMap.width):
        d=depthMap[i, y]
        if d < 1000 and d > 0:
            n+=1
            ds+=d
            xs.append(i)            
            f=True
        elif f:
            z_world=ds/n
            x_screen=xs[int(math.ceil(n/2))]
            x_world = (x_screen - CX) * z_world / FX
            sys.stdout.write(str({"x":x_world,"y":z_world}))
            sys.stdout.flush()
            break
            
