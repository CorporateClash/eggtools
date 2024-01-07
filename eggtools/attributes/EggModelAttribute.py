from eggtools.attributes.EggAttribute import EggAttribute


class EggModelAttribute(EggAttribute):
    def __init__(self, model_flag=True):
        # <Model> { boolean-value }
        super().__init__(entry_type="Model", name="", contents=int(model_flag))
        self.model_flag = model_flag

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        pass

    def _modify_group(self, egg_group):
        if self.target_nodes.check(egg_group.get_name()):
            if egg_group.getModelFlag():
                pass
            else:
                egg_group.setModelFlag(self.model_flag)


class EggModel(EggModelAttribute):
    def __init__(self, model_flag=True):
        super().__init__(model_flag)
