"""
TOOD: figure out what the hell this is suppose to DO lol
"""

from eggtools.attributes.EggAttribute import EggAttribute


class EggTexListAttribute(EggAttribute):
    """
    i have no clue what this is suppose to do it exists but there is literally zero documentation for it
    """

    def __init__(self, flag: bool = True):
        self.flag = bool(flag)
        super().__init__("TexList", "", self.flag)

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()) and hasattr(egg_node, "set_texlist_flag"):
            egg_node.set_texlist_flag(self.flag)


class EggTexList(EggTexListAttribute):
    def __init__(self, flag: bool = True):
        super().__init__(flag)
