from eggtools.attributes.EggAttribute import EggAttribute
from panda3d.egg import EggRenderMode

name2id = {
    "unspecified": EggRenderMode.VM_unspecified,
    "off": EggRenderMode.VM_hidden,
    "hidden": EggRenderMode.VM_hidden,
    "on": EggRenderMode.VM_normal,
    "normal": EggRenderMode.VM_normal,

}


class EggVisibilityAttribute(EggAttribute):
    def __init__(self, visibility_type, overwrite=False):
        if not isinstance(visibility_type, str):
            if visibility_type:
                visibility_type = "on"
            else:
                visibility_type = "off"

        self.visibility_type = visibility_type
        self.overwrite = overwrite
        super().__init__(entry_type="Scalar", name="visibility", contents=self.visibility_type)
        self.visibility_type = name2id[visibility_type.lower()]

    def _modify_polygon(self, egg_polygon, tref=None):
        target_nodes = self.target_nodes

        if target_nodes.check(egg_polygon.getName()):
            visbility_mode = egg_polygon.getVisibilityMode()
            if not visbility_mode:
                egg_polygon.setVisibilityMode(self.visibility_type)
            elif self.overwrite:
                if visbility_mode.getVisibilityMode() != self.visibility_type:
                    egg_polygon.setVisibilityMode(self.visibility_type)

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            visbility_mode = egg_node.getVisibilityMode()
            if not visbility_mode:
                egg_node.setVisibilityMode(self.visibility_type)
            elif self.overwrite:
                if egg_node.getVisibilityMode() != self.visibility_type:
                    egg_node.setVisibilityMode(self.visibility_type)

    def _modify_group(self, egg_group):
        pass


class EggVisibility(EggVisibilityAttribute):
    def __init__(self, visibility_type, overwrite=False):
        super().__init__(visibility_type, overwrite)
