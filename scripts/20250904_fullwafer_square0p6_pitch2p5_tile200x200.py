import phidl
from phidl import Device, geometry as pg

D = Device()
tile = Device()
pillar = pg.rectangle(size = (0.6, 0.6), layer = 0)

pillar_ref = tile.add_ref(pillar)
pillar_ref.rotate(angle=45, center=(0, 0))

tile.add_array(pillar, columns=200, rows=200, spacing=(2.5, 2.5))
D.add_array(tile, columns=200, rows=200, spacing=(500, 500))
D.move(origin=D.center, destination=(0, 0))
D.write_gds('250812_fullWafer.gds')
