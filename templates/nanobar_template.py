"""
Template: nanobar array on a 4-inch wafer.
Edit only the parameter block for routine designs.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gds_templates.common import WaferSpec, add_matrix_labels, duplicate_diagonal_pair, place_on_wafer, write_gds
from gds_templates.nanostructures import make_bar, make_regular_array
from phidl import Device


# Parameters
DIAMETER = 0.60
LENGTH = 1.90
PITCH = (7.20, 5.00)
FIELD_COLUMNS = 37
FIELD_ROWS = 50
ANGLE_RESOLUTION = 60

MATRIX_COLUMNS = 10
MATRIX_ROWS = 10
MATRIX_SPACING = 400
LABEL_SIZE = 10
LABEL_OFFSET = (-45, -145)

BARCODE_TEXT = "Nanobar Cui Lab"
BARCODE_SIZE = 335
BARCODE_OFFSET = (-4000, -600)
OUTPUT_GDS = "nanobar_template.gds"


def build_chip() -> Device:
    bar = make_bar(DIAMETER, LENGTH, ANGLE_RESOLUTION)
    field = make_regular_array(bar, FIELD_COLUMNS, FIELD_ROWS, PITCH, name="nanobar_field")

    matrix = Device("nanobar_matrix")
    matrix.add_array(field, MATRIX_COLUMNS, MATRIX_ROWS, [MATRIX_SPACING, MATRIX_SPACING])
    add_matrix_labels(matrix, MATRIX_COLUMNS, MATRIX_ROWS, MATRIX_SPACING, LABEL_SIZE, LABEL_OFFSET)

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
    write_gds(build_wafer(), OUTPUT_GDS)
