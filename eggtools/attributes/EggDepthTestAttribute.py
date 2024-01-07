from eggtools.attributes.EggAttribute import EggAttribute
from panda3d.egg import EggRenderMode

name2id = {
    "unspecified": EggRenderMode.DTM_unspecified,  # 0
    "off": EggRenderMode.DTM_off,  # 1
    "on": EggRenderMode.DTM_on,  # 2
}


class EggDepthTestAttribute(EggAttribute):
    def __init__(self, depth_type, overwrite=False):
        self.overwrite = overwrite
        if not isinstance(depth_type, str):
            if depth_type:
                depth_type = "on"
            else:
                depth_type = "off"
        super().__init__(entry_type="Scalar", name="depth-test", contents=depth_type)
        self.depth_type = name2id[depth_type.lower()]

    def _modify_polygon(self, egg_polygon, tref=None):
        target_nodes = self.target_nodes

        if target_nodes.check(egg_polygon.getName()):
            depth_test_mode = egg_polygon.getDepthTestMode()
            if not depth_test_mode:
                egg_polygon.setDepthTestMode(self.depth_type)
            elif self.overwrite:
                if depth_test_mode.getDepthTestMode() != self.depth_type:
                    egg_polygon.setDepthTestMode(self.depth_type)

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()):
            # First, check if we HAVE a render mode in the first place:
            render_mode = egg_node.getDepthTestMode()  # type: EggRenderMode

            # If we do not have a render node, then we do not have a depth-test value.
            if not render_mode:
                # Generate our initial <Scalar> depth-test {} value:
                # This will also generate our missing render mode.
                egg_node.setDepthTestMode(self.depth_type)

            # If we already have a render mode, that means there may be a depth-test value already set!
            # If we already have a depth-test attribute, forcibly change it if overwrite is enabled.
            elif self.overwrite:
                if render_mode.getDepthTestMode() != self.depth_type:
                    render_mode.setDepthTestMode(self.depth_type)

    def _modify_group(self, egg_group):
        pass


class EggDepthTest(EggDepthTestAttribute):
    def __init__(self, depth_type, overwrite=False):
        super().__init__(depth_type, overwrite)
