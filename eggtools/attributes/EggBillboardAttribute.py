from eggtools.attributes.EggAttribute import EggAttribute
from panda3d.egg import EggGroup

name2id = {
    "none": EggGroup.BT_none,
    "axis": EggGroup.BT_axis,
    "point": EggGroup.BT_point_camera_relative,
    "point_camera_relative": EggGroup.BT_point_camera_relative,
    "point_world_relative": EggGroup.BT_point_world_relative,
}


class EggBillboardAttribute(EggAttribute):
    def __init__(self, billboard_type):
        self.billboard_type = billboard_type
        self.billboard_mode = name2id[billboard_type.lower()]
        super().__init__(entry_type="Billboard", name="", contents=billboard_type)

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            if not egg_node.getBillboardType():
                egg_node.setBillboardType(self.billboard_mode)


class EggBillboard(EggBillboardAttribute):
    def __init__(self, billboard_type):
        super().__init__(billboard_type)
