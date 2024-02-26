from panda3d.egg import EggTexture, EggVertexPool

from eggtools.attributes.EggAttribute import EggAttribute


class EggUVNameAttribute(EggAttribute):
    def __init__(self, uv_name='UVMap', new_uv_name=''):
        """
        <Scalar> uv-name { uv_name }

        If new_uv_name is empty (default), then UV names will be killed.
        """
        self.uv_name = uv_name
        self.new_uv_name = new_uv_name
        super().__init__(entry_type="Scalar", name="uv-name", contents=uv_name)

    def _modify_polygon(self, egg_polygon, tref):
        pass

    def _modify_node(self, egg_node):
        if isinstance(egg_node, EggTexture):
            egg_texture = egg_node
            uvName = egg_texture.getUvName()
            if uvName:
                # Clear foo from <Scalar> uv-name { foo }
                egg_texture.uv_name = self.new_uv_name
                if not bool(self.new_uv_name):
                    egg_texture.clearUvName()

        if isinstance(egg_node, EggVertexPool):
            for vpoolchild in egg_node:  # should only contain EggVertexes
                uv = vpoolchild.modifyUvObj(self.uv_name)
                if uv:
                    # Clear foo from <UV> foo { ... }
                    uv.setName(self.new_uv_name)


class EggUVName(EggUVNameAttribute):
    def __init__(self, uv_name='UVMap', new_uv_name=''):
        super().__init__(uv_name, new_uv_name)
