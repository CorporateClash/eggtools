"""
Define custom attributes here
"""

from dataclasses import dataclass, field

from eggtools.attributes.EggAlphaAttribute import EggAlphaAttribute, EggAlpha
from eggtools.attributes.EggBackstageAttribute import EggBackstage, EggBackstageAttribute
from eggtools.attributes.EggBillboardAttribute import EggBillboard
from eggtools.attributes.EggBinAttribute import EggBin
from eggtools.attributes.EggCollideAttribute import EggCollide
from eggtools.attributes.EggCollideMaskAttribute import EggCollideMask
from eggtools.attributes.EggDCSAttribute import EggDCS
from eggtools.attributes.EggDartAttribute import EggDart
from eggtools.attributes.EggDecalAttribute import EggDecalAttribute, EggDecal
from eggtools.attributes.EggModelAttribute import EggModel
from eggtools.attributes.EggSequenceAttribute import EggSequence
from eggtools.attributes.EggTagAttribute import EggTag
from eggtools.attributes.EggExtFileAttribute import EggExtFile


@dataclass
class _DefinedAttributes:
    DefinedAttributes: dict = field(default_factory=lambda: "")

    def register_attribute(self, attrname, attrvalue):
        self.DefinedAttributes[attrname] = attrvalue

    def get(self, attrname):
        return self.DefinedAttributes.get(attrname)

    def __getitem__(self, attrname):
        return self.DefinedAttributes[attrname]


DefinedAttributes = _DefinedAttributes(
    {
        "DualAttrib": EggAlphaAttribute("dual", False),
        "DualAttribOW": EggAlphaAttribute("dual", True),
        "DecalAttrib": EggDecalAttribute(),
        "BackstageAttrib": EggBackstageAttribute(),
    }
)

ObjectTypeDefs = {
    # Custom Surfaces
    "surface-grass": [
        EggTag("surface-grass", 1)
    ],
    "surface-snow": [
        EggTag("surface-snow", 1)
    ],
    "surface-metal": [
        EggTag("surface-metal", 1)
    ],
    "surface-water": [
        EggTag("surface-water", 1)
    ],
    "surface-dirt": [
        EggTag("surface-dirt", 1)
    ],
    "surface-gravel": [
        EggTag("surface-gravel", 1)
    ],
    "surface-asphalt": [
        EggTag("surface-asphalt", 1)
    ],
    "surface-wood": [
        EggTag("surface-wood", 1)
    ],
    "surface-ice": [
        EggTag("surface-ice", 1)
    ],
    "surface-sticky": [
        EggTag("surface-sticky", 1)
    ],

    # Bins
    "shground": [
        EggTag("cam", "shground")
    ],
    "shadow-ground": [
        EggTag("cam", "shground")
    ],
    "ground": [
        EggBin("ground")
    ],
    "shadow": [
        EggBin("shadow"),
        EggAlpha("blend-no-occlude")
    ],
    "bin-opaque": [
        EggBin("opaque")
    ],
    "opaque": [
        EggBin("opaque")
    ],
    "bin-transparent": [
        EggBin("transparent")
    ],
    "transparent": [
        EggBin("transparent")
    ],
    "bin-background": [
        EggBin("background")
    ],
    "bin-unsorted": [
        EggBin("unsorted")
    ],
    "bin-gui-popup": [
        EggBin("gui-popup")
    ],
    "bin-fixed": [
        EggBin("fixed")
    ],

    "decal": [
        EggDecal(True)
    ],

    # Billboard
    "billboard": [
        EggBillboard("axis")
    ],
    "billboard-axis": [
        EggBillboard("axis")
    ],
    "billboard-point": [
        EggBillboard("point")
    ],

    # TT Specific collide masks
    "pie": [
        EggCollideMask(0x100),
    ],
    "catch-grab": [
        EggCollideMask(0x10),
    ],
    # Temp furniture mover bitmask
    "safety-net": [
        EggCollideMask(0x32),
        # EggCollideMask(0x200),
    ],
    "safety-gate": [
        EggCollideMask(0x400),
    ],
    "pet": [
        EggCollideMask(0x08),
    ],

    # Collisions
    "trigger": [
        EggCollideMask(0x01),
        EggCollide('polyset', ['descend', 'intangible']),
    ],
    "trigger-sphere": [
        EggCollideMask(0x01),
        EggCollide('sphere', ['descend', 'intangible']),
    ],
    "trigger_sphere": [
        EggCollideMask(0x01),
        EggCollide('sphere', ['descend', 'intangible']),
    ],
    "floor": [
        EggCollideMask(0x02),
        EggCollide('polyset', ['descend', 'level']),
    ],
    "dupefloor": [
        EggCollideMask(0x02),
        EggCollide('polyset', ['keep', 'descend', 'level']),
    ],
    "floor-collide": [
        EggCollideMask(0x06),
    ],
    "smooth-floors": [
        EggCollide('polyset', ['keep', 'descend']),
        EggCollideMask(0x000fffff, 'from'),
        EggCollideMask(0x00000002, 'into'),
    ],
    "invsphere": [
        EggCollide('invsphere', ['descend']),
    ],
    "barrier": [
        EggCollideMask(0x01),
        EggCollide('polyset', ['descend']),
    ],
    "barrier-no-mask": [
        EggCollide('polyset', ['descend']),
    ],
    "cambarrier": [
        EggCollideMask(0x05),
        EggCollide('polyset', ['descend']),
    ],
    "camtransbarrier": [
        EggCollideMask(0x09),
        EggCollide('polyset', ['descend']),
    ],
    "camera-barrier-sphere": [
        EggCollideMask(0x05),
        EggCollide('Sphere', ['descend']),
    ],
    "cambarrier-sphere": [
        EggCollideMask(0x05),
        EggCollide('Sphere', ['descend']),
    ],
    "camera-collide": [
        EggCollideMask(0x04),
        EggCollide('polyset', ['descend']),
    ],
    "camcollide": [
        EggCollideMask(0x04),
        EggCollide('polyset', ['descend']),
    ],
    "sphere": [
        EggCollideMask(0x01),
        EggCollide('Sphere', ['descend']),
    ],
    "tube": [
        EggCollideMask(0x01),
        EggCollide('Tube', ['descend']),
    ],

    # DCS
    "localdcs": [
        EggDCS('local'),
    ],
    "dcs": [
        EggDCS(1),
    ],
    "notouch": [
        EggDCS('notouch'),
    ],
    "netdcs": [
        EggDCS('net'),
    ],

    # Dart
    "dart": [
        EggDart(1)
    ],
    "structured": [
        EggDart("structured")
    ],

    "model": [
        EggModel(),
    ],

    # Alpha
    "dual": [
        EggAlpha('dual')
    ],
    "blend": [
        EggAlpha('blend')
    ],
    "multisample": [
        EggAlpha('multisample')
    ],

    # Sequences
    # TODO: add support for <Switch>, <Scalar> fps { blah }
    # "seq2": [
    #     EggSequence(2.0)
    # ],

    # Misc
    "none": [],

}

# do NOT add backstage as an entry. EVER.
assert "backstage" not in ObjectTypeDefs.keys()
