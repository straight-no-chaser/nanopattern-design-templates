"""
Template: gradient-size pillar/bar/hole array on a 4-inch wafer.
"""

from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gds_templates.common import WaferSpec, add_matrix_labels, duplicate_diagonal_pair, place_on_wafer, write_gds
from gds_templates.nanostructures import make_gradient_matrix
from phidl import Device


# Parameters
STRUCTURE_TYPE = "bar"  # "bar", "pillar", or "hole"
ROWS = 10
STEPS = 10
PITCH = (10, 10)
DIAMETER_START = 0.60
DIAMETER_STEP = 0.10
LENGTH = 1.90
ANGLE_RESOLUTION = 60
STEP_LABEL_SIZE = 7.5

MATRIX_COLUMNS = 15
MATRIX_ROWS = 15
MATRIX_SPACING = 250
MATRIX_LABEL_SIZE = 15
MATRIX_LABEL_OFFSET = (-45, -135)

BARCODE_TEXT = "Gradient Nanostructure Cui Lab"
BARCODE_SIZE = 335
BARCODE_OFFSET = (-2500, -600)


def build_chip() -> Device:
    gradient = make_gradient_matrix(
        structure_type=STRUCTURE_TYPE,
        rows=ROWS,
        steps=STEPS,
        pitch=PITCH,
        diam_ini=DIAMETER_START,
        diam_step=DIAMETER_STEP,
        length=LENGTH,
        label_size=STEP_LABEL_SIZE,
        angle_resolution=ANGLE_RESOLUTION,
    )

    matrix = Device("gradient_chip_matrix")
    matrix.add_array(gradient, MATRIX_COLUMNS, MATRIX_ROWS, [MATRIX_SPACING, MATRIX_SPACING])
    add_matrix_labels(matrix, MATRIX_COLUMNS, MATRIX_ROWS, MATRIX_SPACING, MATRIX_LABEL_SIZE, MATRIX_LABEL_OFFSET)
    return duplicate_diagonal_pair(matrix, MATRIX_SPACING * MATRIX_COLUMNS)


def build_wafer() -> Device:
    return place_on_wafer(
        build_chip(),
        barcode_text=BARCODE_TEXT,
        barcode_size=BARCODE_SIZE,
        barcode_offset=BARCODE_OFFSET,
        spec=WaferSpec(),
    )


if __name__ == "__main__":
    date = datetime.today().strftime("%Y-%m-%d")
    write_gds(build_wafer(), f"{date}-{STRUCTURE_TYPE}-gradient-template.gds")
