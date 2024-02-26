"""
"Backstage" is a special kind of attribute.

This has no equivalent; it is treated as a special case.
It means that the geometry at this node and below should not be translated.
This will normally be used on scale references and other modeling tools.

"""

from eggtools.attributes.EggAttribute import EggAttribute
from eggtools.EggManConfig import BackstageConfig, NodeNameConfig


class EggBackstageAttribute(EggAttribute):
    def __init__(self, backstage_flag=True):
        # <ObjectType> { backstage }
        self.backstage_flag = backstage_flag
        super().__init__(entry_type="ObjectType", name="", contents="backstage", base_node_config=BackstageConfig)

    def _modify_polygon(self, egg_polygon, tref=None):
        pass

    def _modify_node(self, egg_node):
        if not hasattr(egg_node, "hasObjectType"):
            return
        if self.target_nodes.check(egg_node.getName()):
            if not egg_node.hasObjectType('backstage'):
                egg_node.addObjectType('backstage')


class EggBackstage(EggBackstageAttribute):
    def __init__(self, backstage_flag=True):
        super().__init__(backstage_flag)
