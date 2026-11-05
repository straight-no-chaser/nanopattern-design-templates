import math
import string
import phidl.geometry as pg
from phidl import Device

Bar_array = Device()
rows_1 = 50
columns_1 = 50
pitch_1 = 5
diameter = 0.75
length = 2.60
angle_resolution = 60
diameter_label_size = 5
angle_label_size = 5

Bar_0 = Device()
Bar_0.add_ref(pg.circle(diameter / 2, angle_resolution))
Bar_0.add_ref(pg.circle(diameter / 2, angle_resolution)).move([length, 0])
Bar_0.add_ref(pg.rectangle([length, diameter])).move([0, -diameter / 2])
Bar = pg.union(Bar_0)

matrix_1 = Device()
matrix_1.add_array(Bar, columns_1, rows_1, [pitch_1, pitch_1])

columns_2 = rows_2 = 10
spacing_2 = 400

matrix_2 = Device()
matrix_2.add_array(matrix_1, columns_2, rows_2, [spacing_2, spacing_2])

label_size_2 = 10
matrix_letter_2 = string.ascii_uppercase[:columns_2]

for col, letter in enumerate(matrix_letter_2):
    for row, number in enumerate(range(1, rows_2+1)):
        matrix_2.add_ref(pg.text(letter + str(number), label_size_2)).move([spacing_2*col, spacing_2*(rows_2-row)-145])

spacing_3 = spacing_2 * columns_2
barcode_size_3 = 335

matrix_3 = Device()
matrix_3.add_ref(matrix_2)
matrix_3.add_ref(matrix_2).move([-spacing_3, spacing_3])

columns_4 = rows_4 = 8
spacing_4 = 10000

Wafer = Device('Wafer')

jump=10000
xs,ys=matrix_3.get_bounding_box().T
matrix_letter_4 = string.ascii_uppercase[:8]
for i in range(-6,6):
    for j in range(-6,6):
        chip_diagonal=(xs[1]-xs[0])**2+(ys[1]-ys[0])**2
        truth=0
        for x in xs:
            for y in ys:
                if (x+i*jump)**2+(y+j*jump)**2<(45000)**2:
                    truth+=1
        if truth==4:
            temp=Wafer.add_ref(matrix_3)
            temp.x+=i*jump
            temp.y+=j*jump
            temp_1 = Wafer.add_ref(pg.text('Nov2023 Nanobar 2.00x0.13 5Pitch', barcode_size_3)).move([-4000, -600])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('241130_Nanobar.gds')
