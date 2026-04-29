import math
import string
import phidl.geometry as pg
from phidl import Device
from datetime import datetime

# Params

# diam_step == 0: uniform pillar/bar
# diam_step > 0: gradient pillar/bar
# length == 0: pillar
# length > 0: bar
# angle_resolution > 30 to prevent memory overflow on MLA

rows = steps = 10
pitch_h = 10
pitch_v = 10

diam_ini = 0.6
diam_step = 0.1
length = 3.5
angle_resolution = 60

label_size = 7.5
barcode_size = 335

columns_matrix = rows_matrix = 15
spacing = 250

# Determine chip types

if diam_step == 0:
    gradient_type = "uniform"
else:
    gradient_type = "gradient"

if length == 0:
    structure_type = "pillar"
else:
    structure_type = "bar"

chip_types = f"{gradient_type}{structure_type}-Cui Lab"

# Create substrate profile

GradBar = Device()
BarLabel = Device()

for idx in range(steps):
    Bar_0 = Device()
    diameter = diam_ini + diam_step * idx
    
    Bar_0.add_ref(pg.circle(diameter / 2, angle_resolution))
    Bar_0.add_ref(pg.circle(diameter / 2, angle_resolution)).move([length, 0])
    Bar_0.add_ref(pg.rectangle([length, diameter])).move([0, -diameter / 2])
    
    Bar_0 = pg.union(Bar_0)
    GradBar.add_ref(Bar_0).move([pitch_h * idx, 0])
    
    Label_0 = idx + 1
    BarLabel.add_ref(
        pg.text(
            str(Label_0),
            label_size
        )
    ).move([pitch_h * idx - pitch_h / 4, pitch_v])

# Create chip matrix and label

BarMatrix = Device()
BarMatrix.add_array(
    GradBar,
    1,
    rows,
    [pitch_h, pitch_v]
)
BarMatrix.add_ref(BarLabel).move([0, pitch_v * rows])
BarMatrix_letter = string.ascii_uppercase[:rows]
BarMatrix_letter_rev = BarMatrix_letter[::-1]

for row, letter in enumerate(BarMatrix_letter_rev):
    BarMatrix.add_ref(
        pg.text(
            letter,
            label_size,
        )
    ).move(
        [
            -pitch_h * 2.5,
            pitch_v * row - pitch_v / 2
        ]
    )

quatre_chip = Device()
quatre_chip.add_array(
    BarMatrix,
    columns_matrix,
    rows_matrix,
    [spacing, spacing]
)

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

deux_chip = Device()
deux_chip.add_ref(quatre_chip)
deux_chip.add_ref(quatre_chip).move([-deux_chip_spacing, deux_chip_spacing])

Wafer = Device('Wafer')

# Embedding to standard 4-inch wafer

# b = Wafer.add_array(Chip, columns = 8, rows = 8, spacing = (10000, 10000))
# b.move(destination = (-40000, -40000))
# Wafer << pg.ring(radius = 50000, width = 10)
# qp(Wafer)

jump = 10000
wafer_range = 45000
columns_wafer = rows_wafer = 8
spacing_wafer = 10000

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
                    chip_types,
                    barcode_size
                )
            ).move([-2500, -600])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds(datetime.today().strftime('%Y-%m-%d')+'-'+str(chip_types)+'.gds')
