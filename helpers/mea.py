"""
Reusable multielectrode array building blocks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

import phidl.geometry as pg
import phidl.routing as pr
import phidl.routing as rt
from phidl import Device

from .nanostructures import make_bar, make_nanox


DEFAULT_CONDITION_TO_CHANNEL = {
    "Single": [85, 84, 74, 64, 83, 73, 82],
    "Three": [63, 62, 61, 54, 53, 51, 71],
    "Five": [52, 42, 41, 43, 44, 31, 32, 21],
    "Nine": [33, 22, 12, 23, 13, 34, 24],
    "Big": [14, 15, 25, 35, 16, 26, 17],
    "Eclipse": [36, 28, 37, 38, 45, 46, 48],
    "Cross": [47, 57, 58, 56, 55, 68, 67, 78],
    "Flat": [66, 77, 87, 76, 86, 65, 75],
    "Stimulation": [27, 72],
}


WIRE_PATHS = [
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
    [[-9850, -8400], [-3200, -2400], [-2700, -1450], [-1500, -1300], [-375.0, -375.0]],
]


@dataclass(frozen=True)
class MEASpec:
    pad_size: float = 800.0
    electrode_size: float = 15.0
    pitch: float = 150.0
    electrode_grid: int = 8
    nano_diameter: float = 2.5
    nano_layer: int = 1
    angle_resolution: int = 15
    condition_to_channel: Mapping[str, list[int]] = field(default_factory=lambda: DEFAULT_CONDITION_TO_CHANNEL)


def is_corner(row: int, col: int, spec: MEASpec) -> bool:
    last = spec.electrode_grid - 1
    return (row == 0 and col == 1) or (row == last and col == 1) or (row == 0 and col == spec.electrode_grid) or (
        row == last and col == spec.electrode_grid
    )


def electrode_position(channel: int, spec: MEASpec) -> tuple[float, float] | None:
    col = int(str(channel)[0])
    row = int(str(channel)[1]) - 1
    if is_corner(row, col, spec):
        return None
    x = ((col - 1) * spec.pitch) - (spec.electrode_grid - 1) * spec.pitch / 2
    y = ((spec.electrode_grid - row) * spec.pitch) - (spec.electrode_grid + 1) * spec.pitch / 2
    return x, y


def make_quadrant_pads(spec: MEASpec) -> Device:
    device = Device("mea_quadrant_pads")
    for i in range(15):
        x, y = -10250, -10250 + 1450 + 1200 * i
        device << pg.rectangle((spec.pad_size, spec.pad_size)).movex(x).movey(y)
    device << pg.rectangle((1000, 1000)).movex(-10250).movey(-10250)
    device << pg.arc(radius=3000, width=500, theta=25).rotate(213)

    p1 = pg.Port(midpoint=(-2100, -2100), width=spec.electrode_size, orientation=45)
    p2 = pg.Port(midpoint=(-9480, -9480), width=5 * spec.electrode_size, orientation=45)
    device << pr.route_quad(p1, p2)
    return device


def make_quadrant_wires(spec: MEASpec) -> Device:
    device = Device("mea_quadrant_wires")
    for k, waypoints in enumerate(WIRE_PATHS):
        orientation = 14 - k * 2
        port_electrode = pg.Port(midpoint=waypoints[-1], width=spec.electrode_size, orientation=orientation)
        pad_y = -10250 + 1450 + 1200 * k
        port_margin = pg.Port(midpoint=(-10250, pad_y), width=10 * spec.electrode_size, orientation=orientation)
        device << rt.route_smooth(
            port_margin,
            port_electrode,
            radius=10,
            path_type="manual",
            manual_path=waypoints,
        )
    return device


def add_base_electrodes(device: Device, spec: MEASpec) -> None:
    for row in range(spec.electrode_grid):
        for col in range(1, spec.electrode_grid + 1):
            if is_corner(row, col, spec):
                continue
            x = ((col - 1) * spec.pitch) - (spec.electrode_grid - 1) * spec.pitch / 2
            y = ((spec.electrode_grid - row) * spec.pitch) - (spec.electrode_grid + 1) * spec.pitch / 2
            device << pg.circle(radius=spec.electrode_size / 2).movex(x).movey(y)


def add_nanoelectrodes(device: Device, spec: MEASpec) -> None:
    diameter = spec.nano_diameter
    layer = spec.nano_layer

    for condition, channels in spec.condition_to_channel.items():
        if condition == "Stimulation":
            continue

        for channel in channels:
            pos = electrode_position(channel, spec)
            if pos is None:
                continue
            x, y = pos

            if condition == "Single":
                device << pg.circle(radius=diameter / 2, layer=layer).movex(x).movey(y)
            elif condition == "Three":
                distance = 5
                device << pg.circle(radius=diameter / 2, layer=layer).movex(x - distance / 2).movey(y - distance * 0.2887)
                device << pg.circle(radius=diameter / 2, layer=layer).movex(x + distance / 2).movey(y - distance * 0.2887)
                device << pg.circle(radius=diameter / 2, layer=layer).movex(x).movey(y + distance * 0.5774)
            elif condition == "Five":
                distance = 8
                pillar = Device("five_pillar")
                pillar << pg.circle(radius=diameter / 2, layer=layer)
                device.add_array(pillar, columns=2, rows=2, spacing=[distance, distance]).movex(x - distance / 2).movey(y - distance / 2)
                device << pg.circle(radius=diameter / 2, layer=layer).movex(x).movey(y)
            elif condition == "Nine":
                distance = 4
                pillar = Device("nine_pillar")
                pillar << pg.circle(radius=diameter / 2, layer=layer)
                device.add_array(pillar, columns=3, rows=3, spacing=[distance, distance]).movex(x - distance).movey(y - distance)
            elif condition == "Big":
                device << pg.circle(radius=diameter, layer=layer).movex(x).movey(y)
            elif condition == "Eclipse":
                device.add_ref(make_bar(diameter=diameter, length=8, angle_resolution=spec.angle_resolution, layer=layer)).movex(x - 4).movey(y)
            elif condition == "Cross":
                device.add_ref(make_nanox(diameter=diameter, length=5, angle=90, angle_resolution=spec.angle_resolution, layer=layer)).movex(x).movey(y)
            elif condition == "Flat":
                device.add_ref(pg.rectangle([10, 10], layer=layer)).movex(x - 5).movey(y - 5)


def make_mea_device(spec: MEASpec = MEASpec()) -> Device:
    device = Device("mea_device")
    add_base_electrodes(device, spec)

    for i in range(4):
        device << pg.deepcopy(make_quadrant_pads(spec)).rotate(90 * i)
        device << pg.deepcopy(make_quadrant_wires(spec)).rotate(90 * i)

    device << pg.text("I", size=250, justify="center").movex(2300).movey(2700)
    device << pg.text("II", size=250, justify="center").movex(-2300).movey(2700)
    device << pg.text("III", size=250, justify="center").movex(-2300).movey(-2900)
    device << pg.text("IV", size=250, justify="center").movex(2300).movey(-2900)
    device << pg.rectangle((45, 500)).rotate(140).movex(700).movey(725)
    device << pg.rectangle((45, 500)).rotate(320).movex(-700).movey(-725)

    add_nanoelectrodes(device, spec)
    return device


def tile_mea_devices(device: Device, columns: int = 4, rows: int = 4, label_size: float = 25) -> Device:
    wafer = Device("mea_wafer")
    bbox = device.get_bounding_box()
    if bbox is None:
        raise ValueError("MEA device has no geometry")

    dx = bbox[1][0] - bbox[0][0]
    dy = bbox[1][1] - bbox[0][1]
    counter = 1

    for row in range(rows):
        for col in range(columns):
            if (row, col) in {(0, 0), (0, columns - 1), (rows - 1, 0), (rows - 1, columns - 1)}:
                continue
            x = (col - (columns - 1) / 2) * dx
            y = ((rows - 1) / 2 - row) * dy
            wafer << pg.deepcopy(device).movex(x).movey(y)
            wafer << pg.text(f"D{counter}", size=label_size).movex(x + bbox[0][0]).movey(y + bbox[0][1])
            counter += 1

    return wafer
