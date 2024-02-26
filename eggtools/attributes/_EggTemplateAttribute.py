from eggtools.attributes.EggAttribute import EggAttribute


class EggTemplateAttribute(EggAttribute):
    def __init__(self, entry_type="Entry", entry_name='foo', contents='bar'):
        """
        <Entry> foo { bar }
        """
        super().__init__(entry_type=entry_type, name=entry_name, contents=contents)

    def _modify_polygon(self, egg_polygon, tref):
        if self.target_nodes.check(tref.getName()):
            # Do something here for TRefs #
            pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            # Do something here for EggNodes #
            pass


class EggTemplate(EggTemplateAttribute):
    def __init__(self, entry_type="Entry", entry_name='foo', contents='bar'):
        super().__init__(entry_type, entry_name, contents)
