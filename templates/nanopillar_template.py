"""
Template: nanopillar array on a 4-inch wafer.
Edit only the parameter block for routine designs.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gds_templates.common import WaferSpec, place_on_wafer, write_gds
from gds_templates.nanostructures import make_pillar, make_regular_array
from phidl import Device


# Parameters
DIAMETER = 0.60
PITCH = 2.50
FIELD_COLUMNS = 3200
FIELD_ROWS = 320
ANGLE_RESOLUTION = 60

REPEAT_COLUMNS = 1
REPEAT_ROWS = 5
REPEAT_SPACING = (0, 1500)

BARCODE_TEXT = "Nanopillar Cui Lab"
BARCODE_SIZE = 350
BARCODE_OFFSET = (0, -600)
OUTPUT_GDS = "nanopillar_template.gds"


def build_chip() -> Device:
    pillar = make_pillar(DIAMETER, ANGLE_RESOLUTION)
    field = make_regular_array(pillar, FIELD_COLUMNS, FIELD_ROWS, PITCH, name="nanopillar_field")

    chip = Device("nanopillar_chip")
    chip.add_array(field, REPEAT_COLUMNS, REPEAT_ROWS, REPEAT_SPACING)
    return chip


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
