import logging
import os

from panda3d.core import Filename
from panda3d.egg import EggData

from eggtools.EggMan import EggMan

"""
Input egg has a broken texture path: folder is incorrect and there is missing prefix.
"""
if not os.path.isfile('tests/name_card.egg'):
    test_egg = Filename.fromOsSpecific('name_card.egg')
else:
    test_egg = Filename.fromOsSpecific(os.path.join(os.getcwd(), 'tests/name_card.egg'))

eggman = EggMan(
    [test_egg],
    search_paths=[Filename.fromOsSpecific(os.path.join(os.getcwd(), 'tests/maps/')).getDirname()],
    loglevel=logging.DEBUG
)
eggman.NameResolver.OLD_PREFIX = "toontown"
eggman.NameResolver.NEW_PREFIX = "tt"
egg = eggman.get_egg_by_filename("name_card.egg")
ctx = eggman.egg_datas[egg]

eggman.fix_broken_texpaths()
# Other method that can be used (will do the same thing):
# eggman.resolve_egg_textures(egg)

# Output should have correct texture path.
print(egg)
