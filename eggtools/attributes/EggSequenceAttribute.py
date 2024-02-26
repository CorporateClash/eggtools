from eggtools.attributes.EggAttribute import EggAttribute
from eggtools.attributes.EggFPSAttribute import EggFPSAttribute
from eggtools.attributes.EggSwitchAttribute import EggSwitchAttribute


class EggSequenceAttribute(EggSwitchAttribute, EggFPSAttribute):
    def __init__(self, fps_rate=24.0, enable=1):
        """
        Combination of both:
        <Switch> { enable }
        <Scalar> fps { fps_rate }
        """
        self.seq = [
            EggSwitchAttribute().__init__(enable),
            EggFPSAttribute().__init__(fps_rate)
        ]

    def _modify_polygon(self, egg_polygon, tref):
        for seqAttr in self.seq:
            seqAttr._modify_polygon(egg_polygon, tref)

    def _modify_node(self, egg_node):
        for seqAttr in self.seq:
            seqAttr._modify_node(egg_node)


class EggSequence(EggSequenceAttribute):
    def __init__(self, fps_rate=24.0, enable=1):
        super().__init__(fps_rate, enable)
