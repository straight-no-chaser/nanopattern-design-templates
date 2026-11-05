import string
import phidl.geometry as pg
from phidl import Device

diameter_1 = 1.0
angle_resolution_1 = 60
pitch_1 = 2.5
columns_1 = rows_1 = 100

matrix_1 = Device()
matrix_1.add_array(pg.circle(diameter_1/2, angle_resolution_1), columns_1, rows_1, [pitch_1, pitch_1])

columns_2 = 20
rows_2 = 3
spacing_2 = 375

matrix_2 = Device()
matrix_2.add_array(matrix_1, columns_2, rows_2, [spacing_2, spacing_2])

label_size_2 = 10
matrix_letter_2 = string.ascii_uppercase[:columns_2]

for col, letter in enumerate(matrix_letter_2):
    for row, number in enumerate(range(1, rows_2+1)):
        matrix_2.add_ref(pg.text(letter + str(number), label_size_2)).move([spacing_2*col, spacing_2*(rows_2-row)-120])

barcode_size_3 = 75

matrix_3 = Device()
matrix_3.add_array(matrix_2, 1, 4, [0, 2000])

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
            temp_1 = Wafer.add_ref(pg.text('OCT2023 Pillar Stripe Pitch 2.5 ' + matrix_letter_4[-j-5] + str(i+5), barcode_size_3)).move([-1000, -400])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('Pillars_Stripe.gds')
