import string
import phidl.geometry as pg
from phidl import Device

diameter_1500 = 2.5
diameter_2000 = 2.5
diameter_2500 = 2.5

columns = 100
rows = 400
pitch = 15

angleResolution = 60

matrixLabelSize = 100

mushroom_1500 = Device()
mushroom_1500.add_array(
    pg.circle(
        diameter_1500/2,
        angleResolution
    ),
    columns,
    rows,
    [pitch, pitch]
)

mushroom_2000 = Device()
mushroom_2000.add_array(
    pg.circle(
        diameter_2000/2,
        angleResolution
    ),
    columns,
    rows,
    [pitch, pitch]
)

mushroom_2500 = Device()
mushroom_2500.add_array(
    pg.circle(
        diameter_2500/2,
        angleResolution
    ),
    columns,
    rows,
    [pitch, pitch]
)

barcodeSize = 250

matrix_3x = Device()
matrix_3x.add_ref(mushroom_1500).move([0, 0])
matrix_3x.add_ref(mushroom_2000).move([2000, 0])
matrix_3x.add_ref(mushroom_2500).move([4000, 0])

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
            temp_1 = Wafer.add_ref(pg.text('Mushrooms 2.5um XYZ Cui Lab', barcodeSize)).move([0, -400])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('251005_Mushroom.gds')
