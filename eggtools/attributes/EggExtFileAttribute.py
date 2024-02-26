from panda3d.core import Filename
from panda3d.egg import EggFilenameNode, EggExternalReference

from eggtools.attributes.EggAttribute import EggAttribute

from eggtools.config.EggVariableConfig import CCMODELS_MODELS_PATH
import os

# Example file usage:
"""
  <Instance> trolley_car {
    <DCS> { 1 }
    <Transform> {
      <Matrix4> {
        0 0 -1 0
        0 1 0 0
        1 0 0 0
        15.7509878401373 -0.984615280789567 -14.1587830297147 1
      }
    }
    <File> {
      "trolley.egg"
    }
  }
"""
"""
<CoordinateSystem> { Z-Up }

<Comment> {
  "flt2egg -tbnall -nv 60 -o trolley.egg trolley.flt"
}
<Group> trolley_top {
  <Model> { 1 }
  <Group> trolley {
    <Model> { 1 }
    <Group> l1 {
      <SwitchCondition> {
        <Distance> { 70 0 <Vertex> { 0 0 0 } }
      }
      <File> {
        cc_m_prp_toon_trolley-1000.egg
      }
    }
    <Group> l2 {
      <SwitchCondition> {
        <Distance> { 125 70 <Vertex> { 0 0 0 } }
      }
      <File> {
        cc_m_prp_toon_trolley-500.egg
      }
    }
    <Group> l3 {
      <SwitchCondition> {
        <Distance> { 10000000 125 <Vertex> { 0 0 0 } }
      }
      <File> {
        cc_m_prp_toon_trolley-250.egg
      }
    }
  }
}

"""


class EggExtFileAttribute(EggAttribute):
    """
    Instances behave like <Group> nodes, but do not usually contain any polygon data.
    Instead, polygon data is resourced from an input <File> -- when called, it will substitute the <File>
    group with the contents of the egg file, if it can be found.
    """

    def __init__(self, filename: str, node_name: str = ""):
        """
        <File> {
            my_file.egg
        }
        """
        self.node_name = node_name
        if not os.path.isfile(filename):
            filename = os.path.join(CCMODELS_MODELS_PATH, filename)

        if not os.path.isfile(filename):
            print(f"Warning: Still couldn't find a file {filename}")

        self.file = Filename.fromOsSpecific(filename)
        self.file.makeRelativeTo(Filename.fromOsSpecific(CCMODELS_MODELS_PATH))

        super().__init__(entry_type="File", name=self.node_name, contents=self.file)

    def _modify_polygon(self, egg_polygon, tref):
        if self.target_nodes.check(tref.getName()):
            # Do something here for TRefs #
            pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            fileNode = EggExternalReference(self.node_name, self.file.getFullpath())
            # Check to see if the node already has the external reference defined.
            for child in egg_node.getChildren():
                if isinstance(child, EggExternalReference) and child.getName() == fileNode.getName():
                    return
            print(f"Adding {fileNode} to {egg_node.getName()}")
            egg_node.addChild(fileNode)


class EggExtFile(EggExtFileAttribute):
    def __init__(self, filename: str, node_name: str = ""):
        super().__init__(filename, node_name)
