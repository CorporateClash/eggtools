from eggtools.attributes.EggAttribute import EggAttribute


class EggBinAttribute(EggAttribute):
    def __init__(self, bin_name):
        # if bin_name is None, that means we clear the bin
        super().__init__(entry_type="Scalar", name="bin", contents=bin_name)

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        pass

    def _modify_group(self, egg_group):
        if self.target_nodes.check(egg_group.getName()):
            if not self.contents:
                egg_group.clearBin()
                return
            bin_name = egg_group.getBin()
            if not bin_name:
                egg_group.setBin(self.contents)


class EggBin(EggBinAttribute):
    def __init__(self, bin_name):
        super().__init__(bin_name)
