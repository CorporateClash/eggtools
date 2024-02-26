from eggtools.attributes.EggAttribute import EggAttribute
from panda3d.egg import EggGroup

name2id = {
    "unspecified": EggGroup.DC_unspecified,  # 0
    "none": EggGroup.DC_none,  # 16
    "local": EggGroup.DC_local,  # 32
    "net": EggGroup.DC_net,  # 48
    "no_touch": EggGroup.DC_no_touch,  # 64
    "no-touch": EggGroup.DC_no_touch,  # 64
    "notouch": EggGroup.DC_no_touch,  # 64
    "default": EggGroup.DC_default,  # 80

}


class EggDCSAttribute(EggAttribute):
    def __init__(self, dcs_type):
        # <DCS> { boolean-value }
        # or
        # <DCS> { dcs-type }
        # https://loonaticx.github.io/panda3d-egg-bible/home/syntax/general.html#dcs-attributes
        if type(dcs_type) is bool or type(dcs_type) is int:
            if dcs_type:
                # True/1
                dcs_type = "default"
            else:
                # False/0
                dcs_type = "none"
        self.dcs_type = dcs_type
        super().__init__(entry_type="DCS", name="", contents=self.dcs_type)
        self.dcs_mode = name2id[dcs_type.lower()]

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if not hasattr(egg_node, "hasDcsType"):
            return
        # 'panda3d.egg.EggVertexPool' object has no attribute 'hasDcsType'
        if self.target_nodes.check(egg_node.getName()):
            if not egg_node.hasDcsType():
                egg_node.setDcsType(self.dcs_mode)
        pass


class EggDCS(EggDCSAttribute):
    def __init__(self, dcs_type):
        super().__init__(dcs_type)
