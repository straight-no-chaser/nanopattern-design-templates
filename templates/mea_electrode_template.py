"""
Template: MEA electrode device with nanoelectrode variants.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gds_templates.common import write_gds
from gds_templates.mea import MEASpec, make_mea_device, tile_mea_devices


# Parameters
ELECTRODE_SIZE = 15
ELECTRODE_PITCH = 150
NANO_DIAMETER = 2.5
NANO_LAYER = 1
ANGLE_RESOLUTION = 15
OUTPUT_GDS = "mea_electrode_template.gds"


def build_wafer():
    spec = MEASpec(
        electrode_size=ELECTRODE_SIZE,
        pitch=ELECTRODE_PITCH,
        nano_diameter=NANO_DIAMETER,
        nano_layer=NANO_LAYER,
        angle_resolution=ANGLE_RESOLUTION,
    )
    device = make_mea_device(spec)
    return tile_mea_devices(device)


if __name__ == "__main__":
    write_gds(build_wafer(), OUTPUT_GDS)
