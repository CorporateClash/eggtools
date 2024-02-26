from eggtools.attributes.EggAttribute import EggAttribute


class EggOccluderAttribute(EggAttribute):
    """
    This makes the first (or only) polygon within this group node into an occluder.
    The polygon must have exactly four vertices.  An occluder polygon is invisible.

    When the occluder is activated with model.set_occluder(occluder),
    objects that are behind the occluder will not be drawn.

    This can be a useful rendering optimization for complex scenes,
    but should not be overused or performance can suffer.
    """

    def __init__(self, flag: bool = True):
        self.flag = bool(flag)
        super().__init__("Scalar", "occluder", self.flag)

    def _modify_group(self, egg_group):
        pass

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()) and hasattr(egg_node, "set_occluder_flag"):
            egg_node.set_occluder_flag(self.flag)


class EggOccluder(EggOccluderAttribute):
    def __init__(self, flag: bool = True):
        super().__init__(flag)
