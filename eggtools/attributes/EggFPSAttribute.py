from eggtools.attributes.EggAttribute import EggAttribute


class EggFPSAttribute(EggAttribute):
    def __init__(self, fps_rate: float = 24):
        """
        :param int fps_rate: amount of frames per second
        """
        if fps_rate is not type(float):
            fps_rate = float(fps_rate)
        super().__init__(entry_type="Scalar", name='fps', contents=fps_rate)

    def _modify_polygon(self, egg_polygon, tref):
        if self.target_nodes.check(tref.getName()):
            # Do something here for TRefs #
            pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            # Do something here for EggNodes #
            pass

    def _modify_group(self, egg_group):
        if self.target_nodes.check(egg_group.getName()):
            egg_group.setSwitchFps(self.contents)


class EggFPS(EggFPSAttribute):
    def __init__(self, fps_rate: float = 24):
        super().__init__(fps_rate)
