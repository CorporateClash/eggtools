from panda3d.egg import EggGroup

from eggtools.attributes.EggAttribute import EggAttribute


class EggBackfaceAttribute(EggAttribute):
    """
    Sets the backfacing flag of the polygon.
    If this is true, the polygon will be rendered so that both faces are visible;
    if it is false, only the front face of the polygon will be visible.
    """

    def __init__(self, want_backface=True):
        self.backface = want_backface
        super().__init__(entry_type="BFace", name='', contents=f"{self.backface}")

    def _modify_polygon(self, egg_polygon, tref=None):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            self.modify_backfaces(egg_node)

    def modify_backfaces(self, egg_node):
        if isinstance(egg_node, EggGroup):
            for child in egg_node.getChildren():
                self.modify_backfaces(child)

        if hasattr(egg_node, "bface_flag"):
            egg_node.bface_flag = self.backface


class EggBackface(EggBackfaceAttribute):
    def __init__(self, want_backface=True):
        super().__init__(want_backface)
