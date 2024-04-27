import os

from panda3d.core import Filename
from panda3d.egg import EggData

from eggtools.EggMan import EggMan
from eggtools.attributes.EggCollideAttribute import EggCollide
from eggtools.attributes.EggDCSAttribute import EggDCSAttribute
from eggtools.attributes.EggOccluderAttribute import EggOccluder
from eggtools.attributes.EggPointLightAttribute import EggPointLightAttribute

from eggtools.attributes.EggTagAttribute import EggTag
from eggtools.attributes.EggTexListAttribute import EggTexList
from eggtools.attributes.EggUVNameAttribute import EggUVNameAttribute
from eggtools.attributes.EggUVScrollAttribute import EggUVScroll

# Import egg file
if not os.path.isfile('tests/coll_test.egg'):
    test_egg = Filename.fromOsSpecific('coll_test.egg')
else:
    test_egg = Filename.fromOsSpecific(os.path.join(os.getcwd(), 'tests/coll_test.egg'))

eggman = EggMan([test_egg])
egg = eggman.get_egg_by_filename("coll_test.egg")
ctx = eggman.egg_datas[egg]

"""
PandaNode models
  ModelRoot coll_test.egg
    CollisionNode pSphere1 (400 solids) (hidden)
    CollisionNode pTorus1 (400 solids) (hidden)
    GeomNode pCone1 (1 geoms: S:(ColorAttrib))
    GeomNode pCylinder1 (1 geoms: S:(ColorAttrib))
    GeomNode pCube1 (1 geoms: S:(ColorAttrib))
    PandaNode pDisc1
    GeomNode pPlane1 (1 geoms: S:(ColorAttrib))
"""

egg_attributes = {
    EggTag("TestKey", "TestValue"): [
        "pCube1",
    ],

    EggCollide("polygon", "descend", name='', preserve_uv_data=False): [
        "pCube1",
    ],

    # # Set UV Name from blank to Hehe
    EggUVNameAttribute("", "Hehe"): [
        "pPlane1",
    ],

    EggUVScroll(1.0, 2.0, 3.0, 4.0): [
        "pPlane1",
    ],
    EggDCSAttribute("notouch"): [
        "pPlane1",
    ],

    EggTexList(): [
        "pPlane1",
    ],
}
eggman.apply_attributes(egg, egg_attributes)

eggman.write_all_eggs_manually(dryrun=True)
