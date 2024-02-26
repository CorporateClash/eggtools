from eggtools.attributes.EggAttribute import EggAttribute


class EggBinAttribute(EggAttribute):
    def __init__(self, bin_name):
        # if bin_name is None, that means we clear the bin
        super().__init__(entry_type="Scalar", name="bin", contents=bin_name)

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            if not self.contents:
                egg_node.clearBin()
                return
            bin_name = egg_node.getBin()
            if not bin_name:
                egg_node.setBin(self.contents)


class EggBin(EggBinAttribute):
    def __init__(self, bin_name):
        super().__init__(bin_name)
