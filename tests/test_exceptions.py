import os

from panda3d.core import Filename
from panda3d.egg import EggData

from eggtools.EggMan import EggMan

if not os.path.isfile('tests/test_tiles.egg'):
    test_egg = Filename.fromOsSpecific('test_tiles.egg')
else:
    test_egg = Filename.fromOsSpecific(os.path.join(os.getcwd(), 'tests/test_tiles.egg'))

# Initialize an empty EggMan instance
eggman = EggMan([])

# Generate an arbitrary EggData instance outside the EggMan
eggdata = EggData()
eggdata.read(test_egg)

# Try to read an EggData that isn't initialized with our EggMan. This should cause an exception.
eggman.apply_attributes(eggdata)
