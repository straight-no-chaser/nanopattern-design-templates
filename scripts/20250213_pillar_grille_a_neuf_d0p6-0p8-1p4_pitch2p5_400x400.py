import string
import phidl.geometry as pg
from phidl import Device

diameter_200 = 0.6
diameter_400 = 0.8
diameter_1000 = 1.4

columns = rows = 400
pitch = 2.5

angle_resolution = 60

matrix_label_size = 25

matrix_200 = Device()
matrix_200.add_array(
    pg.circle(
        diameter_200/2,
        angle_resolution
    ),
    columns,
    rows,
    [pitch, pitch]
)

matrix_200.add_ref(pg.text('Reseau de 200 nanometres', matrix_label_size)).move([0, -50])

matrix_400 = Device()
matrix_400.add_array(
    pg.circle(
        diameter_400/2,
        angle_resolution
    ),
    columns,
    rows,
    [pitch, pitch]
)

matrix_400.add_ref(pg.text('Reseau de 400 nanometres', matrix_label_size)).move([0, -50])

matrix_1000 = Device()
matrix_1000.add_array(
    pg.circle(
        diameter_1000/2,
        angle_resolution
    ),
    columns,
    rows,
    [pitch, pitch]
)

matrix_1000.add_ref(pg.text('Reseau de 1000 nanometres', matrix_label_size)).move([0, -50])

barcode_size = 350

matrix_3x3 = Device()
matrix_3x3.add_ref(matrix_200).move([0, 0])
matrix_3x3.add_ref(matrix_200).move([1500, -1500])
matrix_3x3.add_ref(matrix_200).move([3000, -3000])

matrix_3x3.add_ref(matrix_400).move([1500, 0])
matrix_3x3.add_ref(matrix_400).move([3000, -1500])
matrix_3x3.add_ref(matrix_400).move([0, -3000])

matrix_3x3.add_ref(matrix_1000).move([3000, 0])
matrix_3x3.add_ref(matrix_1000).move([0, -1500])
matrix_3x3.add_ref(matrix_1000).move([1500, -3000])

deux_chip_spacing = 4500
barcode_size = 300

deux_chip = Device()
deux_chip.add_ref(matrix_3x3)
deux_chip.add_ref(matrix_3x3).move([-deux_chip_spacing, deux_chip_spacing])

Wafer = Device('Wafer')

jump = 10000
xs, ys = deux_chip.get_bounding_box().T
for i in range(-6, 6):
    for j in range(-6, 6):
        chip_diagonal = (xs[1] - xs[0]) ** 2 + (ys[1] - ys[0]) ** 2
        truth = 0
        for x in xs:
            for y in ys:
                if (x + i * jump) ** 2 + (y + j * jump) ** 2 < (45000) ** 2:
                    truth += 1
        if truth == 4:
            temp = Wafer.add_ref(deux_chip)
            temp.x += i * jump
            temp.y += j * jump
            temp_1 = Wafer.add_ref(pg.text('Grille a neuf par XYZ Cui Lab', barcode_size)).move([-3000, -3750])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('250213_Grille_a_neuf.gds')
