from eggtools.attributes.EggAttribute import EggAttribute


class EggFlattenTransformAttribute(EggAttribute):
    """
    Removes any transform and instance records from this node in the scene graph and below.

    If an instance node is encountered, removes the instance and applies the transform to its vertices,
    duplicating vertices if necessary.

    Since this function may result in duplicated vertices,
    it may be a good idea to call remove_unused_vertices() after calling this.
    """

    def __init__(self):
        # Not a real attribute
        super().__init__("Modifier", "flatten-transforms", "True")

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()) and hasattr(egg_node, "flatten_transforms"):
            egg_node.flatten_transforms()


class EggFlattenTransform(EggFlattenTransformAttribute):
    def __init__(self):
        super().__init__()
