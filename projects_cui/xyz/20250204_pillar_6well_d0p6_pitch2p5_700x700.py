import phidl.geometry as pg
from phidl import Device

diameter_1 = 0.6
angle_resolution_1 = 60
pitch_1 = 2.5
columns_1 = rows_1 = 700

matrix_1 = Device()
matrix_1.add_array(pg.circle(diameter_1/2, angle_resolution_1), columns_1, rows_1, [pitch_1, pitch_1])

matrix_2 = Device()
matrix_2.add_array(matrix_1, 10, 10, [1750, 1750])

Wafer = Device('Wafer')
jump = 20000
xs, ys = matrix_2.get_bounding_box().T
for i in range(-3, 3):
    for j in range(-3, 3):
        chip_diagonal = (xs[1] - xs[0]) ** 2 + (ys[1] - ys[0]) ** 2
        truth = 0
        for x in xs:
            for y in ys:
                if (x + i * jump) ** 2 + (y + j * jump) ** 2 < (45000) ** 2:
                    truth += 1
        if truth == 4:
            temp = Wafer.add_ref(matrix_2)
            temp.x += i * jump
            temp.y += j * jump
            temp_1 = Wafer.add_ref(pg.text('Nov2023 Pillar Stripe .25 2.5Pitch', 350)).move([0, -600])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('250204_Pillars_6well.gds')
