import string
import phidl.geometry as pg
from phidl import Device

diameter_1 = 0.6
angle_resolution_1 = 60
pitch_1 = 2.5
columns_1 = 3200
rows_1 = 320

matrix_1 = Device()
matrix_1.add_array(pg.circle(diameter_1/2, angle_resolution_1), columns_1, rows_1, [pitch_1, pitch_1])

barcode_size_3 = 350

matrix_3 = Device()
matrix_3.add_array(matrix_1, 1, 5, [0, 1500])

columns_4 = rows_4 = 8
spacing_4 = 10000

Wafer = Device('Wafer')

jump = 10000
xs, ys = matrix_3.get_bounding_box().T
matrix_letter_4 = string.ascii_uppercase[:8]
for i in range(-6, 6):
    for j in range(-6, 6):
        chip_diagonal = (xs[1] - xs[0]) ** 2 + (ys[1] - ys[0]) ** 2
        truth = 0
        for x in xs:
            for y in ys:
                if (x + i * jump) ** 2 + (y + j * jump) ** 2 < (45000) ** 2:
                    truth += 1
        if truth == 4:

            temp = Wafer.add_ref(matrix_3)
            temp.x += i * jump
            temp.y += j * jump
            temp_1 = Wafer.add_ref(pg.text('Nov2023 Pillar Stripe .25 2.5Pitch', barcode_size_3)).move([0, -600])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('250204_Nanopillar.gds')
