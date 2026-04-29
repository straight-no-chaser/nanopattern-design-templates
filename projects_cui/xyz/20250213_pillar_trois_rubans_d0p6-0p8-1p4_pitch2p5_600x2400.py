import string
import phidl.geometry as pg
from phidl import Device

diameter_200 = 0.6
diameter_400 = 0.8
diameter_1000 = 1.4

columns = 600
rows = 2400
pitch = 2.5

angle_resolution = 60

matrix_label_size = 25

ruban_200 = Device()
ruban_200.add_array(
    pg.circle(
        diameter_200/2,
        angle_resolution
    ),
    columns,
    rows,
    [pitch, pitch]
)

ruban_200.add_ref(pg.text('Ruban de 200 nanometres', matrix_label_size)).move([0, -50])

ruban_400 = Device()
ruban_400.add_array(
    pg.circle(
        diameter_400/2,
        angle_resolution
    ),
    columns,
    rows,
    [pitch, pitch]
)

ruban_400.add_ref(pg.text('Ruban de 400 nanometres', matrix_label_size)).move([0, -50])

ruban_1000 = Device()
ruban_1000.add_array(
    pg.circle(
        diameter_1000/2,
        angle_resolution
    ),
    columns,
    rows,
    [pitch, pitch]
)

ruban_1000.add_ref(pg.text('Ruban de 1000 nanometres', matrix_label_size)).move([0, -50])

barcode_size = 250

matrix_3x = Device()
matrix_3x.add_ref(ruban_200).move([0, 0])
matrix_3x.add_ref(ruban_400).move([2000, 0])
matrix_3x.add_ref(ruban_1000).move([4000, 0])

Wafer = Device('Wafer')

jump = 10000
xs, ys = matrix_3x.get_bounding_box().T
for i in range(-6, 6):
    for j in range(-6, 6):
        chip_diagonal = (xs[1] - xs[0]) ** 2 + (ys[1] - ys[0]) ** 2
        truth = 0
        for x in xs:
            for y in ys:
                if (x + i * jump) ** 2 + (y + j * jump) ** 2 < (45000) ** 2:
                    truth += 1
        if truth == 4:
            temp = Wafer.add_ref(matrix_3x)
            temp.x += i * jump
            temp.y += j * jump
            temp_1 = Wafer.add_ref(pg.text('Trois rubans par XYZ Cui Lab', barcode_size)).move([0, -400])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('250213_Trois_rubans.gds')
