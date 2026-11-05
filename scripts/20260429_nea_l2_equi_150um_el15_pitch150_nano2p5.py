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
import phidl.path as pp
import phidl.routing as rt

pad_size = 800
init_x, init_y = -555, -320
el_size = 15
stop1_width_bot = 15
stop2_width_bot = 30
stop3_width_bot = 75
pitch = 150
elec_col = 8
angle_resolution = 15

def qD(el_size):
    d = pg.Device()

    for i in range(15):
        pos_pad_x, pos_pad_y = -10250, -10250+1450+1200*i
        d << pg.rectangle((pad_size, pad_size)).movex(
            pos_pad_x).movey(pos_pad_y)
    d << pg.rectangle((1000, 1000)).movex(-10250).movey(-10250)
    d << pg.arc(radius=3000, width=500, theta=25).rotate(213)
    port_banana_x, port_banana_y = -2100, -2100
    port_grd_x, port_grd_y = -9480, -9480
    p1 = pg.Port(midpoint=(port_banana_x, port_banana_y),
                 width=el_size, orientation=45)
    p2 = pg.Port(midpoint=(port_grd_x, port_grd_y),
                 width=5*el_size, orientation=45)
    d << pr.route_quad(p1, p2)
    return d

def wD(el_size):
    w = pg.Device()

    path_points = [
        [[-9850, 8400], [-3200, 2500], [-2800, 1400], [-1500, 1300], [-525.0, 375.0]],
        [[-9850, 7200], [-3400, 2400], [-2900, 1200], [-1600, 1100], [-600, 350], [-520, 300], [-428, 300], [-375.0, 225.0]],
        [[-9850, 6000], [-3600, 2150], [-3050, 1000], [-1700, 1000], [-525.0, 225.0]],
        [[-9850, 4800], [-3800, 1900], [-3100, 810], [-1800, 900], [-700, 192], [-300, 170], [-225.0, 75.0]],
        [[-9850, 3600], [-4000, 1650], [-3200, 600], [-1800, 750], [-900, 135], [-547, 135], [-375.0, 75.0]],
        [[-9850, 2400], [-4400, 1300], [-3300, 400], [-1800, 500], [-900, 75], [-525.0, 75.0]],
        [[-9850, 1200], [-4600, 900], [-3361, 200], [-1800, 300], [-900, 10], [-550, 10], [-375.0, -75.0]],
        [[-9850, 0], [-525.0, -75.0]],
        [[-9850, -1200], [-530, -125], [-300, -130], [-225.0, -75.0]],
        [[-9850, -2400], [-530, -175], [-170, -180], [-75.0, -75.0]],
        [[-9850, -3600], [-3800, -1800], [-3000, -1000], [-1670, -800], [-750, -300], [-525.0, -225.0]],
        [[-9850, -4800], [-3700, -2100], [-2950, -1150], [-1650, -940], [-525, -270], [-420, -270], [-375.0, -225.0]],
        [[-9850, -6000], [-3550, -2250], [-2875, -1250], [-1600, -1050], [-525, -320], [-280, -320], [-225.0, -225.0]],
        [[-9850, -7200], [-3400, -2400], [-2800, -1350], [-1600, -1200], [-525.0, -375.0]],
        [[-9850, -8400], [-3200, -2400], [-2700, -1450], [-1500, -1300], [-375.0, -375.0]]
    ]

    for k in range(15):
        waypoints = path_points[k]
        orientation = 14-k*2
        port_electrode = pg.Port(
            midpoint=((path_points[k][-1])), width=el_size, orientation=orientation)

        pos_pad_x, pos_pad_y = -10250, -10250+1450+1200*k
        port_margin = pg.Port(midpoint=(pos_pad_x, pos_pad_y),
                              width=10*el_size, orientation=orientation)

        w << rt.route_smooth(
            port_margin, port_electrode, radius=10, path_type='manual', manual_path=waypoints)
    return w

full_device = pg.Device()
layer1 = 1

for row in range(elec_col):
    for col in range(1, 1+elec_col):
        if (row == 0 and col == 1) or (row == elec_col-1 and col == 1) or (row == 0 and col == elec_col) or (row == elec_col-1 and col == elec_col):
            continue
        pos_pad_x = ((col-1)*pitch)-(elec_col-1)*pitch/2
        pos_pad_y = ((8-row)*pitch)-(elec_col+1)*pitch/2
        full_device << pg.circle(radius=el_size/2).movex(
            pos_pad_x).movey(pos_pad_y)

for i in range(4):
    full_device << pg.deepcopy(qD(el_size)).rotate(90*i)
    full_device << pg.deepcopy(wD(el_size)).rotate(90*i)

full_device << pg.text('I', size=250, justify='center').movex(2300).movey(2700)
full_device << pg.text(
    'II', size=250, justify='center').movex(-2300).movey(2700)
full_device << pg.text(
    'III', size=250, justify='center').movex(-2300).movey(-2900)
full_device << pg.text(
    'IV', size=250, justify='center').movex(2300).movey(-2900)

full_device << pg.rectangle((45, 500)).rotate(140).movex(700).movey(725)
full_device << pg.rectangle((45, 500)).rotate(320).movex(-700).movey(-725)

diameter_std = 2.5
condition_to_channel = {'Single': [85, 84, 74, 64, 83, 73, 82],
                        'Three': [63, 62, 61, 54, 53, 51, 71],
                        'Five': [52, 42, 41, 43, 44, 31, 32, 21],
                        'Nine': [33, 22, 12, 23, 13, 34, 24],
                        'Big': [14, 15, 25, 35, 16, 26, 17],
                        'Eclipse': [36, 28, 37, 38, 45, 46, 48],
                        'Cross': [47, 57, 58, 56, 55, 68, 67, 78],
                        'Flat': [66, 77, 87, 76, 86, 65, 75],
                        'Stimulation' : [27, 72]
                        }

for condition in condition_to_channel.keys():

    for ch in condition_to_channel[condition]:
        col = int(str(ch)[0])
        row = int(str(ch)[1])-1
        if (row == 0 and col == 1) or (row == elec_col-1 and col == 1) or (row == 0 and col == elec_col) or (row == elec_col-1 and col == elec_col):
            continue
        pos_pad_x = ((col-1)*pitch)-(elec_col-1)*pitch/2
        pos_pad_y = ((8-row)*pitch)-(elec_col+1)*pitch/2
        if condition == 'Single':
            full_device << pg.circle(radius=diameter_std/2, layer = layer1).movex(
                pos_pad_x).movey(pos_pad_y)
        elif condition == 'Three':
            pillar_distance = 5
            full_device << pg.circle(radius=diameter_std/2, layer = layer1).movex(
                pos_pad_x-pillar_distance/2).movey(pos_pad_y-pillar_distance*0.2887)
            full_device << pg.circle(radius=diameter_std/2, layer = layer1).movex(
                pos_pad_x+pillar_distance/2).movey(pos_pad_y-pillar_distance*0.2887)
            full_device << pg.circle(radius=diameter_std/2, layer = layer1).movex(
                pos_pad_x).movey(pos_pad_y+pillar_distance*0.5774)
        elif condition == 'Five':
            pillar_distance = 8
            P = Device()
            P << pg.circle(radius=diameter_std/2, layer = layer1)
            full_device.add_array(P, columns = 2, rows = 2, spacing = [pillar_distance, pillar_distance]).movex(
                pos_pad_x-pillar_distance/2).movey(pos_pad_y-pillar_distance/2)
            full_device << pg.circle(radius=diameter_std/2, layer = layer1).movex(
                pos_pad_x).movey(pos_pad_y)
        elif condition == 'Nine':
            pillar_distance = 4
            P = Device()
            P << pg.circle(radius=diameter_std/2, layer = layer1)
            full_device.add_array(P, columns = 3, rows = 3, spacing = [pillar_distance, pillar_distance]).movex(
                pos_pad_x-pillar_distance).movey(pos_pad_y-pillar_distance)
        elif condition == 'Big':
            full_device << pg.circle(radius=diameter_std, layer = layer1).movex(
                pos_pad_x).movey(pos_pad_y)
        elif condition == 'Eclipse':
            P = Device()
            length = 8
            P << pg.circle(diameter_std / 2, angle_resolution, layer = layer1)
            P << pg.circle(diameter_std / 2, angle_resolution, layer = layer1).move([length, 0])
            P << pg.rectangle([length, diameter_std], layer = layer1).move([0, -diameter_std / 2])
            full_device.add_ref(P).movex(
                pos_pad_x-length/2).movey(pos_pad_y)
        elif condition == 'Cross':

            angle = 90
            length = 5
            Bar_0 = Device()
            Bar_0.add_ref(pg.circle(diameter_std / 2, angle_resolution, layer = layer1)).move([length, 0])
            Bar_0.add_ref(pg.rectangle([length, diameter_std], layer = layer1)).move([0, -diameter_std / 2])
            Bar_0 = pg.union(Bar_0, layer = layer1)

            offset_x = diameter_std * math.sin(math.radians(angle / 2)) / 2
            offset_y = diameter_std * math.cos(math.radians(angle / 2)) / 2
            X_1 = Device()
            X_1.add_ref(Bar_0).rotate(angle / 2).move([offset_x, offset_y])
            X_1.add_ref(Bar_0).rotate(-angle / 2).move([offset_x, -offset_y])
            X_1.add_ref(Bar_0).rotate(180 - angle / 2).move([-offset_x, offset_y])
            X_1.add_ref(Bar_0).rotate(180 + angle / 2).move([-offset_x, -offset_y])
            X_1.add_ref(pg.rectangle([offset_x * 4, offset_y * 4], layer = layer1)).move([-offset_x * 2, -offset_y * 2])

            full_device.add_ref(X_1).movex(
                pos_pad_x).movey(pos_pad_y)
        elif condition == 'Flat':
            full_device.add_ref(pg.rectangle([10,10], layer = layer1)).movex(
                pos_pad_x-5).movey(pos_pad_y-5)

Wafer = pg.Device()
bbox = full_device.get_bounding_box()
dx, dy = np.diff(bbox, axis=0)[0]
ctr = 1

for j in range(1, -3, -1):
    for i in range(-1, 3):
        if not (((i == -1) & (j == -2)) or ((i == 2) & (j == -2)) or ((i == 2) & (j == 1)) or ((i == -1) & (j == 1))):
            Wafer << pg.deepcopy(
                full_device).movex(+bbox[0][0]+i*dx).movey(+bbox[1][0]+j*dy)
            Wafer << pg.text(
                'D'+str(ctr), size=25).movex(+bbox[0][0]+i*dx-18).movey(+bbox[1][0]+j*dy-12)
            ctr += 1

Wafer.write_gds('NEAv11_L2_test.gds')
