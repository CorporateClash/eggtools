"""
TOOD: figure out what the hell this is suppose to DO lol
"""

from eggtools.attributes.EggAttribute import EggAttribute


class EggFogAttribute(EggAttribute):
    """
    i have no clue what this is suppose to do it exists but there is literally zero documentation for it
    """

    def __init__(self, disable: bool = False):
        self.flag = bool(disable)
        super().__init__("Scalar", "nofog", self.flag)

    def _modify_group(self, egg_group):
        pass

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()) and hasattr(egg_node, "set_nofog_flag"):
            egg_node.set_nofog_flag(self.flag)


class EggFog(EggFogAttribute):
    def __init__(self, disable: bool = False):
        super().__init__(disable)
