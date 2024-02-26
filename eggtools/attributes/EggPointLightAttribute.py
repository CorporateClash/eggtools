from eggtools.attributes.EggAttribute import EggAttribute
from panda3d.egg import EggGroup, EggPoint


class EggPointLightAttribute(EggAttribute):
    """
    ima be honest and tell you idk what this does theres not enough info in the documentation
    """

    def __init__(self, thickness: float = 1.0, perspective: bool = False):
        """
        <Scalar> thick { number }
        <Scalar> perspective { boolean-value }

        :param thickness: This specifies the size of the PointLight (or the width of a line),
            in pixels, when it is rendered.
            This may be a floating-point number, but the fractional part is meaningful only when
            antialiasing is in effect. The default is 1.0

        :param perspective: If this is specified, then the thickness, above, is to interpreted as a size in 3-d spatial
            units, rather than a size in pixels, and the point should be scaled according
            to its distance from the viewer normally.
        """
        self.perspective = perspective
        self.thickness = thickness

        super().__init__(entry_type="PointLight", name="", contents=f"{self.perspective}_{self.thickness}")

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        # Can either affect egg groups or egg points
        if self.target_nodes.check(egg_node.getName()):
            self.configure_pointlight(egg_node)

    def configure_pointlight(self, egg_node):
        if isinstance(egg_node, EggGroup):
            # print(EggPoint.__init__(name="Point"))
            print(egg_node.make_point_primitives())
            for child in egg_node.getChildren():
                self.configure_pointlight(child)


class EggPointLight(EggPointLightAttribute):
    def __init__(self, thickness: float = 1.0, perspective: bool = False):
        super().__init__(thickness, perspective)
