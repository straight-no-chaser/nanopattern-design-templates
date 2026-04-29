import string
import phidl.geometry as pg
from phidl import Device

size_1 = 500
pitch_1 = 550
columns_1 = rows_1 = 10

matrix_0 = Device()
matrix_00 = Device()
matrix_0.add_array(pg.rectangle(size = (size_1, size_1)), columns_1, rows_1, [pitch_1, pitch_1])
matrix_00.add_ref(pg.circle(radius = 2250, angle_resolution = 5)).move([2250,2250])

matrix_1 = pg.boolean(A = matrix_0, B = matrix_00, operation = 'and', precision = 1e-6, num_divisions = [1,1], layer = 0)

Wafer = Device()
jump=10000
barcode_size = 75
xs,ys=matrix_1.get_bounding_box().T
matrix_letter = string.ascii_uppercase[:9]
for i in range(-6,6):
    for j in range(-6,6):
        chip_diagonal=(xs[1]-xs[0])**2+(ys[1]-ys[0])**2
        truth=0
        for x in xs:
            for y in ys:
                if (x+i*jump)**2+(y+j*jump)**2<(45000)**2:
                    truth+=1
        if truth==4:
            temp=Wafer.add_ref(matrix_1)
            temp.x+=i*jump
            temp.y+=j*jump
            temp_1 = Wafer.add_ref(pg.text('OCT2023 Square 500 ' + matrix_letter[-j-5] + str(i+5), barcode_size)).move([2000, -300])
            temp_1.x += i * jump
            temp_1.y += j * jump

Wafer.write_gds('Squares.gds')
