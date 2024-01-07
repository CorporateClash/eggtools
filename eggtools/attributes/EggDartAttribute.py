from eggtools.attributes.EggAttribute import EggAttribute
from panda3d.egg import EggGroup

name2id = {
    "none": EggGroup.DT_none,
    "structured": EggGroup.DT_structured,
    "sync": EggGroup.DT_sync,
    "no_sync": EggGroup.DT_nosync,
    "no-sync": EggGroup.DT_nosync,
    "nosync": EggGroup.DT_nosync,
    "default": EggGroup.DT_default,
}


class EggDartAttribute(EggAttribute):
    def __init__(self, dart_type, override_dart_type):
        self.override_dart_type = override_dart_type
        if type(dart_type) is bool or type(dart_type) is int:
            if dart_type:
                # True/1
                dart_type = "default"
            else:
                # False/0
                dart_type = "none"
        self.dart_type = dart_type
        super().__init__(entry_type="Dart", name="", contents=self.dart_type)
        self.dart_mode = name2id[dart_type.lower()]

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            # can hit EggTable objects
            if hasattr(egg_node, 'getDartType') and (self.override_dart_type or not egg_node.getDartType()):
                egg_node.setDartType(self.dart_mode)

    def _modify_group(self, egg_group):
        pass


class EggDart(EggDartAttribute):
    def __init__(self, dart_type, override_dart_type=False):
        super().__init__(dart_type, override_dart_type)
