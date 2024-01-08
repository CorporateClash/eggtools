import fnmatch
from dataclasses import dataclass, field


@dataclass
class NodeNameConfig:
    """
    NodeNameConfig has two uses:
        - Replacing characters that start/end with a certain character (renaming)
        - Applying certain attributes to nodes that contain a certain string.
            - Don't use STARTS/ENDSWITH for configs related to attributes.
    """
    NODE_INCLUDES: list
    NODE_STARTSWITH: list = field(default_factory=list)
    NODE_ENDSWITH: list = field(default_factory=list)

    def _populate(self, node_name):
        self.NODE_INCLUDES = {
            node for term in self.NODE_INCLUDES for node in fnmatch.filter([node_name], "*" + term + "*")
        }
        # self.NODE_INCLUDES.add(node_name)
        self.NODE_STARTSWITH = {
            node for term in self.NODE_STARTSWITH for node in fnmatch.filter([node_name], term + "*")
        }
        self.NODE_ENDSWITH = {
            node for term in self.NODE_ENDSWITH for node in fnmatch.filter([node_name], "*" + term)
        }

    def check(self, name):
        # TODO: fix
        # self._populate(name)
        # print(self.NODE_INCLUDES)
        return (
                any(term in name for term in self.NODE_INCLUDES) or
                any(name.startswith(term) for term in self.NODE_STARTSWITH) or
                any(name.endswith(term) for term in self.NODE_ENDSWITH)
        )


DualConfig = NodeNameConfig(
    NODE_INCLUDES=["cc_t_bat_prp_cup_red"],
    NODE_STARTSWITH=["cc_t_fx_shadow_circle_"],
    NODE_ENDSWITH=["anc", "bruh", "coll_*", "*_1"]
)

DecalConfig = NodeNameConfig(
    NODE_INCLUDES=["cc_t_bat_prp_cup_red"],
    NODE_STARTSWITH=["cc_t_fx_shadow_circle_"],
    NODE_ENDSWITH=["anc", "bruh", "coll_*", "*_1"]
)

BackstageConfig = NodeNameConfig(
    NODE_INCLUDES=["bkstg"],
)

if __name__ == "__main__":
    test_name = "mama_coll_1"
    test = DualConfig.check(test_name)
    print(test)
