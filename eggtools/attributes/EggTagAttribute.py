from eggtools.attributes.EggAttribute import EggAttribute


# <Tag> ouch { 5 }
# <Tag> surface-snow { 1 }
class EggTagAttribute(EggAttribute):

    def __init__(self, name, contents, target_nodes=None):
        super().__init__("Tag", name, str(contents))
        # self.ident_name = f"Tag_{name}_{contents}"
        if target_nodes:
            self.set_target_nodes(target_nodes)

    def _modify_group(self, egg_group):
        if self.target_nodes.check(egg_group.getName()):
            egg_group.setTag(self.name, self.contents)

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        # x: ensure this doesnt somehow pick up egg group nodes :x
        if self.target_nodes.check(egg_node.getName()) and hasattr(egg_node, "setTag"):
            egg_node.setTag(self.name, self.contents)
            # egg_node.getParent().setTag(self.name, self.contents)


class EggTag(EggTagAttribute):
    def __init__(self, name, contents, target_nodes=None):
        super().__init__(name, contents, target_nodes)
