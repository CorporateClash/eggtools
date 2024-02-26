import os

from panda3d.core import Filename
from panda3d.egg import EggData

from eggtools.EggMan import EggMan
from eggtools.attributes.EggFlattenTransformAttribute import EggFlattenTransform

"""
PandaNode models
  ModelRoot xform.egg
    GeomNode cube_1_unfrozen (1 geoms: S:(ColorAttrib)) T:m(pos 0 -4.2943 3.45109 hpr 32.6694 35.6993 -15.2209 scale 3.56143)
    GeomNode cube_1_frozen (1 geoms: S:(ColorAttrib)) T:m(pos 0 -4.2943 3.45109)
    ModelNode dcs_net_unfrozen T:m(pos 0.969136 2.91796 4.521 hpr -100.736 34.308 -158.412 scale 2.39883)
    ModelNode dcs_net_frozen T:m(pos 0.969136 2.91796 4.521)
    
>>>>>>>>>>>>
    
PandaNode models
  ModelRoot xform_out.egg
    GeomNode cube_1_unfrozen (1 geoms: S:(ColorAttrib))
    GeomNode cube_1_frozen (1 geoms: S:(ColorAttrib))
    ModelNode dcs_net_unfrozen
    ModelNode dcs_net_frozen
"""

if not os.path.isfile('tests/xform.egg'):
    test_egg = Filename.fromOsSpecific('xform.egg')
else:
    test_egg = Filename.fromOsSpecific(os.path.join(os.getcwd(), 'tests/xform.egg'))

eggman = EggMan([test_egg])
egg = eggman.get_egg_by_filename("xform.egg")
ctx = eggman.egg_datas[egg]
egg_attributes = {
    EggFlattenTransform(): [
        "cube_1_unfrozen",
        "cube_1_frozen",
        "dcs_net_unfrozen",
        "dcs_net_frozen",
    ],
}

eggman.apply_attributes(egg, egg_attributes)
eggman.write_egg(egg, filename=Filename.fromOsSpecific("xform_out.egg"))
