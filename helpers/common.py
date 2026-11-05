"""
Shared layout helpers for PHIDL GDS scripts.
"""

from __future__ import annotations

import string
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import phidl.geometry as pg
from phidl import Device


Point = tuple[float, float]
Spacing = float | Sequence[float]


@dataclass(frozen=True)
class WaferSpec:
    # Placement settings for a standard circular wafer.

    radius: float = 45_000.0
    step: float = 10_000.0
    scan_min: int = -6
    scan_max: int = 6
    include_edge_ring: bool = False
    edge_ring_width: float = 10.0


def normalize_spacing(spacing: Spacing) -> Point:
    if isinstance(spacing, (int, float)):
        return float(spacing), float(spacing)
    if len(spacing) != 2:
        raise ValueError("spacing must be a number or a pair")
    return float(spacing[0]), float(spacing[1])


def require_bbox(device: Device):
    bbox = device.get_bounding_box()
    if bbox is None:
        raise ValueError(f"Device {device.name!r} has no geometry")
    return bbox


def corners_inside_radius(device: Device, offset: Point, radius: float) -> bool:
    bbox = require_bbox(device)
    xs, ys = bbox.T
    dx, dy = offset
    return all((x + dx) ** 2 + (y + dy) ** 2 < radius**2 for x in xs for y in ys)


def add_matrix_labels(
    device: Device,
    columns: int,
    rows: int,
    spacing: Spacing,
    label_size: float = 10.0,
    offset: Point = (-45.0, -145.0),
) -> None:
    # Add A1-style labels to a matrix.

    sx, sy = normalize_spacing(spacing)
    letters = string.ascii_uppercase[:columns]
    for col, letter in enumerate(letters):
        for row, number in enumerate(range(1, rows + 1)):
            label = pg.text(f"{letter}{number}", label_size)
            device.add_ref(label).move([sx * col + offset[0], sy * (rows - row) + offset[1]])


def duplicate_diagonal_pair(device: Device, spacing: Spacing, name: str = "two_chip") -> Device:
    # Place two copies in the diagonal pattern used by the original scripts.

    sx, sy = normalize_spacing(spacing)
    pair = Device(name)
    pair.add_ref(device)
    pair.add_ref(device).move([-sx, sy])
    return pair


def place_on_wafer(
    unit: Device,
    barcode_text: str,
    barcode_size: float,
    barcode_offset: Point = (-2_500.0, -600.0),
    spec: WaferSpec = WaferSpec(),
    name: str = "Wafer",
) -> Device:
    # Tile a chip/unit anywhere its four bounding-box corners fit on the wafer.

    wafer = Device(name)
    if spec.include_edge_ring:
        wafer.add_ref(pg.ring(radius=spec.radius, width=spec.edge_ring_width))

    for i in range(spec.scan_min, spec.scan_max):
        for j in range(spec.scan_min, spec.scan_max):
            offset = (i * spec.step, j * spec.step)
            if not corners_inside_radius(unit, offset, spec.radius):
                continue

            wafer.add_ref(unit).move(offset)
            label = wafer.add_ref(pg.text(barcode_text, barcode_size))
            label.move([barcode_offset[0] + offset[0], barcode_offset[1] + offset[1]])

    return wafer


def write_gds(device: Device, filename: str, output_dir: str | Path = "output") -> Path:
    # Write GDS into a predictable output directory.

    path = Path(output_dir) / filename if output_dir else Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    device.write_gds(str(path))
    return path
