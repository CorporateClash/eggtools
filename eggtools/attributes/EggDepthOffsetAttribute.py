from eggtools.attributes.EggAttribute import EggAttribute


class EggDepthOffsetAttribute(EggAttribute):
    def __init__(self, offset_value, overwrite=False):
        self.offset_value = offset_value
        self.overwrite = overwrite
        self.clear_offset = False
        if self.offset_value == "clear":
            self.clear_offset = True
        super().__init__(entry_type="Scalar", name="depth-offset", contents=self.offset_value)

    def _modify_polygon(self, egg_polygon, tref=None):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            if self.clear_offset:
                egg_node.clearDepthOffset()
                return
            depth_offset = egg_node.getDepthOffset()
            if not depth_offset:
                egg_node.setDepthOffset(self.offset_value)
            elif self.overwrite:
                if egg_node.getDepthOffset() != self.offset_value:
                    egg_node.setDepthOffset(self.offset_value)


class EggDepthOffset(EggDepthOffsetAttribute):
    def __init__(self, offset_value, overwrite=False):
        super().__init__(offset_value, overwrite)
