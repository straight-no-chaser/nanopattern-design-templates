import math
import string
import phidl.geometry as pg
from phidl import Device

X_array = Device()
rows_1 = 10
pitch = 15
angle_resolution = 60
diameter_label_size = 5
angle_label_size = 5
angles_cross = [15, 30, 45, 60, 75, 90]

for row in range(0, rows_1 + 1):
    diameter = 1 + row / 10

    X_array.add_ref(pg.text(str(round(diameter - 0.8, 2)), size=diameter_label_size)).move(
        [-pitch * 2.5, -row * pitch - 2.5])

    for col, angle in enumerate(angles_cross):
        length = diameter * 2.5

        Bar_0 = Device()
        Bar_0.add_ref(pg.circle(diameter / 2, angle_resolution)).move([length, 0])
        Bar_0.add_ref(pg.rectangle([length, diameter])).move([0, -diameter / 2])
        Bar_1 = pg.union(Bar_0)
        Bar_1.add_ref()

        offset_x = diameter * math.sin(math.radians(angle / 2)) / 2
        offset_y = diameter * math.cos(math.radians(angle / 2)) / 2
        X_1 = Device()
        X_1.add_ref(Bar_1).rotate(angle / 2).move([offset_x, offset_y])
        X_1.add_ref(Bar_1).rotate(-angle / 2).move([offset_x, -offset_y])
        X_1.add_ref(Bar_1).rotate(180 - angle / 2).move([-offset_x, offset_y])
        X_1.add_ref(Bar_1).rotate(180 + angle / 2).move([-offset_x, -offset_y])
        X_1.add_ref(pg.rectangle([offset_x * 4, offset_y * 4])).move([-offset_x * 2, -offset_y * 2])
        X = pg.union(X_1)

        X_array.add_ref(X).move([(col - 1) * pitch, -row * pitch])

        if row == 0:
            for col, numbers in enumerate(angles_cross):
                X_array.add_ref(pg.text(str(int(numbers)), angle_label_size)).move([(col - 1) * pitch - 4.0, pitch])

columns_2 = 15
rows_2 = 13
spacing_x_2 = 250
spacing_y_2 = 300
matrix_2 = Device()
matrix_2.add_array(X_array, columns_2, rows_2, [spacing_x_2, spacing_y_2])

label_size_2 = 10
matrix_letter_2 = string.ascii_uppercase[:columns_2]
for col, letter in enumerate(matrix_letter_2):
    for row, number in enumerate(range(1, rows_2 + 1)):
        matrix_2.add_ref(pg.text(letter + str(number), label_size_2)).move(
            [spacing_x_2 * col - 45, spacing_y_2 * (rows_2 - row - 1) + 15])

spacing_3 = spacing_x_2 * columns_2
barcode_size_3 = 75
matrix_3 = Device()
matrix_3.add_ref(matrix_2)
matrix_3.add_ref(matrix_2).move([-spacing_3, spacing_3 + 300])

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
            temp_1 = Wafer.add_ref(pg.text('OCT2023 X Pitch 15 Gradient ' + matrix_letter_4[-j-5] + str(i+5), barcode_size_3)).move([-1000, -300])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('NanoX.gds')
