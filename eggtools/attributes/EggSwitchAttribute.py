from eggtools.attributes.EggAttribute import EggAttribute

"""
Not to be confused with <SwitchCondition>, which is used for LODs.

Usually is accompanied by EggFPS
"""


class EggSwitchAttribute(EggAttribute):
    def __init__(self, switchVal=1):
        """
        <Switch> { boolean-value }
        """
        assert switchVal == 1 or switchVal == 0
        super().__init__(entry_type="", name="Switch", contents=switchVal)

    def _modify_polygon(self, egg_polygon, tref):
        if self.target_nodes.check(tref.getName()):
            # Do something here for TRefs #
            pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            egg_node.setSwitchFlag(self.contents)


class EggSwitch(EggSwitchAttribute):
    def __init__(self, switchVal=1):
        super().__init__(switchVal)
