from abc import ABC, abstractmethod

from panda3d.egg import EggGroupNode, EggPolygon, EggNode

from eggtools.EggManConfig import NodeNameConfig


class EggAttribute(ABC):
    def __hash__(self):
        return hash(f"{self.entry_type}_{self.name}{'_' if self.name else ''}{self.contents}")

    def __str__(self):
        return f"EggAttribute: <{self.entry_type}> {self.name}{' ' if self.name else ''}{{ {self.contents} }}"

    def __init__(self, entry_type, name, contents, base_node_config: NodeNameConfig = None):
        """
        <entry-type> name { contents }

        Note: Constructor parameters are ONLY used as a friendly name identifier for EggAttribute objects.
        """
        self.entry_type = entry_type
        self.name = name
        self.contents = contents
        self.ident_name = f"{self.entry_type}_{self.name}_{self.contents}"
        self.target_nodes = NodeNameConfig(list())
        self.base_node_config = base_node_config
        self._applied = False

    def set_target_nodes(self, node_entries):
        if type(node_entries) is str:
            node_entries = [node_entries]
        if self.base_node_config:
            node_entries += self.base_node_config.NODE_INCLUDES
        self.target_nodes = NodeNameConfig(node_entries)

    def apply(self, egg_base, egg_ctx, node_entries=None):
        # For now we will skip checking to see if we have already applied an EggAttribute with a given node
        # if egg_ctx in self.appliedToCtx:
        #     return
        if not egg_base:
            return
        if not node_entries:
            node_entries = list()
        self.set_target_nodes(node_entries)

        def traverse_egg(egg, ctx):
            """
            Traverses down an egg tree and records data mapped to the ctx key.

            :param egg: Egg to traverse
            :type egg: EggData | EggGroup
            :param ctx: The original EggContext, required to keep things in order during recursion.
            :type ctx: EggContext
            """
            # we ask for ctx just to keep things in order
            for child in egg.getChildren():
                if isinstance(child, EggNode):
                    self._modify_node(child)
                if isinstance(child, EggGroupNode):
                    self._modify_group(child)
                    traverse_egg(child, ctx)
                if isinstance(child, EggPolygon):
                    poly_textures = child.getTextures()
                    for texture_ref in poly_textures:
                        self._modify_polygon(child, texture_ref)

        traverse_egg(egg_base, egg_ctx)

    @abstractmethod
    def _modify_polygon(self, egg_polygon, tref):
        # This method is to be overridden by a subclass.
        pass

    @abstractmethod
    def _modify_node(self, egg_node):
        pass

    @abstractmethod
    def _modify_group(self, egg_group):
        # NOTE: We may need to remove this method as it is redundant.
        pass
