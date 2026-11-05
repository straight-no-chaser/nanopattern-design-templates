"""
Template: NanoX angle/diameter sweep on a 4-inch wafer.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from helpers.common import WaferSpec, add_matrix_labels, duplicate_diagonal_pair, place_on_wafer, write_gds
from helpers.nanostructures import make_nanox_sweep
from phidl import Device


# Parameters
DIAMETER_START = 1.00
DIAMETER_STEP = 0.10
DIAMETER_STEPS = 11
ANGLES = [15, 30, 45, 60, 75, 90]
PITCH = 15
LENGTH_RATIO = 2.5
ANGLE_RESOLUTION = 60

MATRIX_COLUMNS = 15
MATRIX_ROWS = 13
MATRIX_SPACING = (250, 300)
LABEL_SIZE = 10
LABEL_OFFSET = (-45, 15)

BARCODE_TEXT = "NanoX Cui Lab"
BARCODE_SIZE = 75
BARCODE_OFFSET = (-1000, -300)
OUTPUT_GDS = "nanox_template.gds"


def build_chip() -> Device:
    diameters = [DIAMETER_START + DIAMETER_STEP * i for i in range(DIAMETER_STEPS)]
    sweep = make_nanox_sweep(
        diameters=diameters,
        angles=ANGLES,
        pitch=PITCH,
        length_ratio=LENGTH_RATIO,
        angle_resolution=ANGLE_RESOLUTION,
    )

    matrix = Device("nanox_matrix")
    matrix.add_array(sweep, MATRIX_COLUMNS, MATRIX_ROWS, MATRIX_SPACING)
    add_matrix_labels(matrix, MATRIX_COLUMNS, MATRIX_ROWS, MATRIX_SPACING, LABEL_SIZE, LABEL_OFFSET)

    diagonal_spacing = MATRIX_SPACING[0] * MATRIX_COLUMNS
    return duplicate_diagonal_pair(matrix, (diagonal_spacing, diagonal_spacing + 300))


def build_wafer() -> Device:
    return place_on_wafer(
        build_chip(),
        barcode_text=BARCODE_TEXT,
        barcode_size=BARCODE_SIZE,
        barcode_offset=BARCODE_OFFSET,
        spec=WaferSpec(),
    )


if __name__ == "__main__":
    write_gds(build_wafer(), OUTPUT_GDS)
