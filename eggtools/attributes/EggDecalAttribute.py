from eggtools.attributes.EggAttribute import EggAttribute

from eggtools.EggManConfig import DecalConfig


class EggDecalAttribute(EggAttribute):
    def __init__(self, apply=True):
        # <Scalar> decal { 1 }
        super().__init__(entry_type="Scalar", name="decal", contents=int(apply))

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if DecalConfig.check(egg_node.get_name()) or self.target_nodes.check(egg_node.get_name()):
            if egg_node.determineDecal():
                pass
                # logging.debug(f"{egg_node.get_name()} already has decal mode set")
            else:
                # logging.info(f"applying decal to {child.get_name()}")
                egg_node.setDecalFlag(True)


class EggDecal(EggDecalAttribute):
    def __init__(self, apply):
        super().__init__(apply)
