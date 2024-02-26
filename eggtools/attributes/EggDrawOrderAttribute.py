from eggtools.attributes.EggAttribute import EggAttribute


class EggDrawOrderAttribute(EggAttribute):
    def __init__(self, draw_order):
        self.draw_order = draw_order
        self.clear_draw_order = False
        if self.draw_order == "clear":
            self.clear_draw_order = True

        super().__init__(entry_type="Scalar", name="draw-order", contents=self.draw_order)

    def _modify_polygon(self, egg_polygon, tref=None):
        pass

    def _modify_node(self, egg_node):
        pass


class EggDrawOrder(EggDrawOrderAttribute):
    def __init__(self, draw_order):
        super().__init__(draw_order)
