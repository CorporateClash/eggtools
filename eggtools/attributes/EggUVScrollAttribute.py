from eggtools.attributes.EggAttribute import EggAttribute


class EggUVScrollAttribute(EggAttribute):

    def __init__(self, u_speed, v_speed, w_speed, r_speed):
        self.u_speed = u_speed
        self.v_speed = v_speed
        self.w_speed = w_speed
        self.r_speed = r_speed
        super().__init__(entry_type="Scalar", name="uv-scroll", contents="")

    def _modify_polygon(self, egg_polygon, tref=None):
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()) and hasattr(egg_node, "set_scroll_u"):
            egg_node.set_scroll_u(self.u_speed)
            egg_node.set_scroll_v(self.v_speed)
            egg_node.set_scroll_w(self.w_speed)
            egg_node.set_scroll_r(self.r_speed)


class EggUVScroll(EggUVScrollAttribute):
    def __init__(self, u_speed, v_speed, w_speed, r_speed):
        super().__init__(u_speed, v_speed, w_speed, r_speed)
