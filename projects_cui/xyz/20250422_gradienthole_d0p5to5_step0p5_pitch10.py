import math
import string
import phidl.geometry as pg
from phidl import Device

rows = 10
pitch = 10
steps = 10
diam_ini = 0.5
diam_step = 0.5

angle_resolution = 60

GradHole = Device()
HoleLabel = Device()
HoleLabel_size = 7.5
for idx in range(steps):
    Hole_0 = Device()
    diameter = diam_ini + diam_step * idx
    Hole_0.add_ref(pg.circle(diameter / 2, angle_resolution))
    GradHole.add_ref(Hole_0).move([pitch * idx, 0])

    Label_0 = idx + 1
    HoleLabel.add_ref(
        pg.text(
            str(Label_0),
            HoleLabel_size
        )
    ).move([pitch * idx - pitch / 4, pitch])

HoleMatrix = Device()
HoleMatrix.add_array(
    GradHole,
    1,
    rows,
    [pitch, pitch]
)
HoleMatrix.add_ref(HoleLabel).move([0, pitch * rows])
HoleMatrix_letter = string.ascii_uppercase[:rows]
HoleMatrix_letter_rev = HoleMatrix_letter[::-1]

for row, letter in enumerate(HoleMatrix_letter_rev):
    HoleMatrix.add_ref(
        pg.text(
            letter,
            HoleLabel_size,
        )
    ).move(
        [
            -pitch * 2.5,
            pitch * row - pitch / 2
        ]
    )

columns_matrix = rows_matrix = 15
spacing = 250

quatre_chip = Device()
quatre_chip.add_array(HoleMatrix, columns_matrix, rows_matrix, [spacing, spacing])

label_size = 15
matrix_letter = string.ascii_uppercase[:columns_matrix]

for col, letter in enumerate(matrix_letter):
    for row, number in enumerate(range(1, rows_matrix + 1)):
        quatre_chip.add_ref(
            pg.text(
                letter + str(number),
                label_size
            )
        ).move(
            [
                spacing * col - 45,
                spacing * (rows_matrix - row) - 135
            ]
        )

deux_chip_spacing = spacing * columns_matrix
barcode_size = 335

deux_chip = Device()
deux_chip.add_ref(quatre_chip)
deux_chip.add_ref(quatre_chip).move([-deux_chip_spacing, deux_chip_spacing])

columns_wafer = rows_wafer = 8
spacing_wafer = 10000

Wafer = Device('Wafer')

jump = 10000
wafer_range = 45000
xs,ys = deux_chip.get_bounding_box().T
matrix_letter_wafer = string.ascii_uppercase[:8]
for i in range(-6, 6):
    for j in range(-6, 6):
        chip_diagonal = (xs[1] - xs[0]) ** 2 + (ys[1] - ys[0]) ** 2
        truth = 0
        for x in xs:
            for y in ys:
                if (x + i * jump) ** 2 + (y + j * jump) ** 2 < wafer_range ** 2:
                    truth += 1
        if truth == 4:
            temp = Wafer.add_ref(deux_chip)
            temp.x += i * jump
            temp.y += j * jump
            temp_1 = Wafer.add_ref(
                pg.text(
                    'Gradient Hole XYZ Cui Lab',
                    barcode_size
                )
            ).move([-2500, -600])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('250422_GradientHole.gds')
