from __future__ import division, print_function, absolute_import
import numpy as np
import math
import string

import matplotlib.pyplot as plot

from phidl import Device, Layer, LayerSet, make_device
from phidl import quickplot2 as qp
import phidl.geometry as pg
import phidl.routing as pr
import phidl.utilities as pu

pad_size=800
init_x,init_y=-555,-320
el_size = 30
stop1_width_bot = 15
stop2_width_bot = 30
stop3_width_bot = 75
pitch = 150
elec_col = 8

full_device=pg.Device()

Electrode_positions = []

for row in range(elec_col):
    for col in range(1, 1+elec_col):
        if (row == 0 and col == 1) or (row == elec_col-1 and col == 1) or (row == 0 and col == elec_col) or (row == elec_col-1 and col == elec_col):
            continue
        pos_pad_x = ((col - 1) * pitch) - (elec_col-1)*pitch/2
        pos_pad_y = ((8 - row) * pitch) - (elec_col+1)*pitch/2
        full_device << pg.rectangle((el_size, el_size)).movex(pos_pad_x).movey(pos_pad_y)
        Electrode_positions.append((pos_pad_x,pos_pad_y))
print(Electrode_positions)

def qD(el_size):
    d=pg.Device()

    for i in range(15):
        pos_pad_x,pos_pad_y=-10250, -10250+1450+1200*i
        d << pg.rectangle((pad_size,pad_size)).movex(pos_pad_x).movey(pos_pad_y)
    d << pg.rectangle((1000,1000)).movex(-10250).movey(-10250)
    d << pg.arc(radius=3000, width=500, theta =25).rotate(213)
    port_banana_x,port_banana_y=-2100,-2100
    port_grd_x,port_grd_y=-9480,-9480
    p1=pg.Port(midpoint=(port_banana_x,port_banana_y),width=el_size,orientation=45)
    p2=pg.Port(midpoint=(port_grd_x,port_grd_y),width=5*el_size,orientation=45)
    d<<pr.route_quad(p1,p2)
    return d

def wD(el_size):
    d=pg.Device()

    path_points={
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)],
        [(100,100)]
    }

    electrode_points_left_lane=[
        (-525.0, 375.0),
        (-525.0, 225.0),
        (-375.0, 225.0),
        (-525.0, 75.0),
        (-375.0, 75.0),
        (-225.0, 75.0),
        (-525.0, -75.0),
        (-375.0, -75.0),
        (-225.0, -75.0),
        (-75.0, -75.0),
        (-525.0, -225.0),
        (-375.0, -225.0),
        (-225.0, -225.0),
        (-525.0, -375.0),
        (-375.0, -375.0),
    ]

    for i in range(15):
        points = np.array(path_points(i))
        points.append(electrode_points_left_lane[i])
        orientation=13-i*2
        port_electrode = pg.Port(midpoint=electrode_points_left_lane[i],width=el_size,orientation=orientation)

        pos_pad_x,pos_pad_y=-10250, -10250+1450+1200*i
        port_margin = pg.Port(midpoint=(pos_pad_x,pos_pad_y),width=5*el_size,orientation=orientation)

        Path_0 = pp.smooth(
        points = points,
        radius = 10,
        corner_fun = pp.euler,
        use_eff = False,
        )

        d << phidl.routing.route_smooth(port_margin, port_electrode, radius=10, width=None, path_type='manual', manual_path=Path_0)

for i in range(4):
    full_device<<pg.deepcopy(qD(el_size)).rotate(90*i)
    full_device<<pg.deepcopy(wD(el_size)).rotate(90*i)

full_device<<pg.text('I', size = 250, justify = 'center').movex(2500).movey(3000)
full_device<<pg.text('II', size = 250, justify = 'center').movex(-2500).movey(3000)
full_device<<pg.text('III', size = 250, justify = 'center').movex(-2500).movey(-3250)
full_device<<pg.text('IV', size = 250, justify = 'center').movex(2500).movey(-3250)

full_device << pg.rectangle((45,500)).movex(pos_pad_x).movey(pos_pad_y).rotate(45).movex(-3200).movey(-1070)
full_device << pg.rectangle((45,500)).rotate(225).movex(1100).movey(1460)

Wafer=pg.Device()
bbox=full_device.get_bounding_box()
dx,dy=np.diff(bbox,axis=0)[0]
ctr=1

for j in range(1,-3,-1):
    for i in range(-1,3):
        if not (((i==-1)&(j==-2))or((i==2)&(j==-2))or((i==2)&(j==1))or((i==-1)&(j==1))):
            Wafer<<pg.deepcopy(full_device).movex(+bbox[0][0]+i*dx).movey(+bbox[1][0]+j*dy)
            Wafer<<pg.text('D'+str(ctr),size=25).movex(+bbox[0][0]+i*dx).movey(+bbox[1][0]+j*dy)
            ctr+=1

Wafer.write_gds('NEAv11_L2_test.gds')
