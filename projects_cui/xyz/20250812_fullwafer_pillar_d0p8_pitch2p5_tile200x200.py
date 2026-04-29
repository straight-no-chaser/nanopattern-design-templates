import phidl
D = Device()
tile = Device()
pillar = pg.circle(radius=0.4, angle_resolution=90)
tile.add_array(pillar,columns=200,rows=200,spacing=(2.5,2.5))
D.add_array(tile,columns=200, rows=200, spacing=(500,500))
D.move(origin=D.center,destination=(0,0))
D.write_gds('250812_fullWafer.gds')
