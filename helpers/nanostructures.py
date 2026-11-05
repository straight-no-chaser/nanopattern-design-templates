"""
Reusable nanostructure building blocks.
"""

from __future__ import annotations

import math
import string
from collections.abc import Sequence

import phidl.geometry as pg
from phidl import Device

from .common import Spacing, normalize_spacing


def make_pillar(diameter: float, angle_resolution: int = 60, layer: int = 0) -> Device:
    return pg.circle(radius=diameter / 2, angle_resolution=angle_resolution, layer=layer)


def make_bar(
    diameter: float,
    length: float,
    angle_resolution: int = 60,
    layer: int = 0,
) -> Device:
    bar = Device("bar")
    bar.add_ref(pg.circle(diameter / 2, angle_resolution, layer=layer))
    bar.add_ref(pg.circle(diameter / 2, angle_resolution, layer=layer)).move([length, 0])
    bar.add_ref(pg.rectangle([length, diameter], layer=layer)).move([0, -diameter / 2])
    return pg.union(bar, layer=layer)


def make_nanox(
    diameter: float,
    length: float | None = None,
    angle: float = 90.0,
    angle_resolution: int = 60,
    layer: int = 0,
) -> Device:
    arm_length = length if length is not None else diameter * 2.5
    arm = Device("nanox_arm")
    arm.add_ref(pg.circle(diameter / 2, angle_resolution, layer=layer)).move([arm_length, 0])
    arm.add_ref(pg.rectangle([arm_length, diameter], layer=layer)).move([0, -diameter / 2])
    arm = pg.union(arm, layer=layer)

    offset_x = diameter * math.sin(math.radians(angle / 2)) / 2
    offset_y = diameter * math.cos(math.radians(angle / 2)) / 2
    x_device = Device("nanox")
    x_device.add_ref(arm).rotate(angle / 2).move([offset_x, offset_y])
    x_device.add_ref(arm).rotate(-angle / 2).move([offset_x, -offset_y])
    x_device.add_ref(arm).rotate(180 - angle / 2).move([-offset_x, offset_y])
    x_device.add_ref(arm).rotate(180 + angle / 2).move([-offset_x, -offset_y])
    x_device.add_ref(pg.rectangle([max(offset_x * 4, 0.001), max(offset_y * 4, 0.001)], layer=layer)).move(
        [-offset_x * 2, -offset_y * 2]
    )
    return pg.union(x_device, layer=layer)


def make_regular_array(
    structure: Device,
    columns: int,
    rows: int,
    pitch: Spacing,
    name: str = "regular_array",
) -> Device:
    array = Device(name)
    array.add_array(structure, columns=columns, rows=rows, spacing=normalize_spacing(pitch))
    return array


def make_gradient_matrix(
    structure_type: str,
    rows: int,
    steps: int,
    pitch: Spacing,
    diam_ini: float,
    diam_step: float,
    length: float = 0.0,
    label_size: float = 7.5,
    angle_resolution: int = 60,
    layer: int = 0,
    name: str = "gradient_matrix",
) -> Device:
    # Create the labeled gradient block used by the chip design template.

    pitch_h, pitch_v = normalize_spacing(pitch)
    gradient_row = Device(f"{structure_type}_gradient_row")
    step_labels = Device("step_labels")

    for idx in range(steps):
        diameter = diam_ini + diam_step * idx
        if structure_type == "bar":
            structure = make_bar(diameter, length, angle_resolution, layer)
        elif structure_type in {"pillar", "hole"}:
            structure = make_pillar(diameter, angle_resolution, layer)
        else:
            raise ValueError("structure_type must be 'bar', 'pillar', or 'hole'")

        gradient_row.add_ref(structure).move([pitch_h * idx, 0])
        step_labels.add_ref(pg.text(str(idx + 1), label_size)).move([pitch_h * idx - pitch_h / 4, pitch_v])

    matrix = Device(name)
    matrix.add_array(gradient_row, columns=1, rows=rows, spacing=[pitch_h, pitch_v])
    matrix.add_ref(step_labels).move([0, pitch_v * rows])

    row_letters = string.ascii_uppercase[:rows][::-1]
    for row, letter in enumerate(row_letters):
        matrix.add_ref(pg.text(letter, label_size)).move([-pitch_h * 2.5, pitch_v * row - pitch_v / 2])

    return matrix


def make_nanox_sweep(
    diameters: Sequence[float],
    angles: Sequence[float],
    pitch: float,
    length_ratio: float = 2.5,
    label_size: float = 5.0,
    angle_resolution: int = 60,
    layer: int = 0,
    name: str = "nanox_sweep",
) -> Device:
    sweep = Device(name)

    for row, diameter in enumerate(diameters):
        sweep.add_ref(pg.text(str(round(diameter, 3)), size=label_size)).move(
            [-pitch * 2.5, -row * pitch - label_size / 2]
        )
        for col, angle in enumerate(angles):
            x_device = make_nanox(
                diameter=diameter,
                length=diameter * length_ratio,
                angle=angle,
                angle_resolution=angle_resolution,
                layer=layer,
            )
            sweep.add_ref(x_device).move([(col - 1) * pitch, -row * pitch])

            if row == 0:
                sweep.add_ref(pg.text(str(int(angle)), label_size)).move([(col - 1) * pitch - label_size, pitch])

    return sweep
