# Holds some general rules
import fnmatch
from dataclasses import field, dataclass

_DECAL_STARTS_WITH = [
    "door_flat_",
]
_DECAL_ENDS_WITH = [
    "_DECAL",
]
_DECAL_INCLUDES = [
    "***REMOVED***"
]


class DecalConfig:

    @staticmethod
    def check(name):
        return any(
            [name.startswith(term) for term in _DECAL_STARTS_WITH] +
            [name.endswith(term) for term in _DECAL_ENDS_WITH] +
            [term in name for term in _DECAL_INCLUDES]
        )


_DUAL_STARTS_WITH = [
    "cc_t_fx_shadow_circle_"

]

_DUAL_ENDS_WITH = [
    "anc",
    "bruh",
    "coll_*",
    "mama_*_1",

]

_DUAL_INCLUDES = [
    "cc_t_bat_prp_cup_red",

]


@dataclass
class NodeNameConfig:
    NODE_INCLUDES: list
    NODE_STARTSWITH: list = field(default_factory=lambda: "")
    NODE_ENDSWITH: list = field(default_factory=lambda: "")

    def _populate(self, node_name):
        # Wildcard support
        wildcard_endswith = lambda: [fnmatch.filter([node_name], "*" + node) for node in self.NODE_ENDSWITH]
        wildcard_startswith = lambda: [fnmatch.filter([node_name], node + "*") for node in self.NODE_STARTSWITH]
        wildcard_includes = lambda: [fnmatch.filter([node_name], "*" + node + "*") for node in self.NODE_STARTSWITH]
        print(wildcard_endswith())

        self.NODE_INCLUDES = list(set(sum(list(filter(None, wildcard_includes())), [])))
        self.NODE_STARTSWITH = list(set(sum(list(filter(None, wildcard_startswith())), [])))
        self.NODE_ENDSWITH = list(set(sum(list(filter(None, wildcard_endswith())), [])))

    def check(self, name):
        self._populate(name)
        return any(
            [term in name for term in self.NODE_INCLUDES] +
            [name.startswith(term) for term in self.NODE_STARTSWITH] +
            [name.endswith(term) for term in self.NODE_ENDSWITH]
        )


DualConfig = NodeNameConfig(_DUAL_INCLUDES, _DUAL_STARTS_WITH, _DUAL_ENDS_WITH)

if __name__ == "__main__":
    test_name = "mama_coll_1"
    test_name_2 = "lol_1"
    test = DualConfig.check(test_name)
    print(test)
