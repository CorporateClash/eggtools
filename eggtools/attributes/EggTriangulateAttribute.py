from eggtools.attributes.EggAttribute import EggAttribute
from panda3d.egg import EggGroupNode

name2id = {
    "polygon": EggGroupNode.T_polygon,
    "convex": EggGroupNode.T_convex,
    "composite": EggGroupNode.T_composite,
    "recurse": EggGroupNode.T_recurse,
    "flat": EggGroupNode.T_flat_shaded,
    "flat-shaded": EggGroupNode.T_flat_shaded,
    "flat_shaded": EggGroupNode.T_flat_shaded,
    "flatshaded": EggGroupNode.T_flat_shaded,
}


class EggTriangulateAttribute(EggAttribute):
    """
    Replace all higher-order polygons at this point in the scene graph and below with triangles.
    Returns the total number of new triangles produced, less degenerate polygons removed.

    If flags contains T_polygon and T_convex, both concave and convex polygons will be subdivided into triangles;
    with only T_polygon, only concave polygons will be subdivided, and convex polygons will be largely unchanged.
    """

    def __init__(self, flag):
        # Not a real attribute
        super().__init__("Modifier", "TriangulatePolygons", flag)
        self.flag = name2id[flag.lower()]

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()) and hasattr(egg_node, "triangulate_polygons"):
            egg_node.triangulate_polygons(self.flag)


class EggTriangulate(EggTriangulateAttribute):
    def __init__(self, flag):
        super().__init__(flag)
