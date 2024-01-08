import os

from panda3d.core import Filename
from panda3d.egg import EggData

from eggtools.EggMan import EggMan

if not os.path.isfile('tests/test_tiles.egg'):
    test_egg = Filename.fromOsSpecific('test_tiles.egg')
else:
    test_egg = Filename.fromOsSpecific(os.path.join(os.getcwd(), 'tests/test_tiles.egg'))

eggman = EggMan([])
eggdata = EggData()
eggdata.read(test_egg)
eggman.apply_attributes(eggdata)
