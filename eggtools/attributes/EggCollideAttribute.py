from panda3d.egg import EggGroup

from eggtools.attributes.EggAttribute import EggAttribute

cs2type = {
    'none': EggGroup.CST_none,
    'plane': EggGroup.CST_plane,
    'polygon': EggGroup.CST_polygon,
    'polyset': EggGroup.CST_polyset,
    'sphere': EggGroup.CST_sphere,
    'tube': EggGroup.CST_tube,
    'inv_sphere': EggGroup.CST_inv_sphere,
    'invsphere': EggGroup.CST_inv_sphere,
    'box': EggGroup.CST_box,
    'floor_mesh': EggGroup.CST_floor_mesh,

}

flags2type = {
    'none': EggGroup.CF_none,
    'descend': EggGroup.CF_descend,
    'event': EggGroup.CF_event,
    'keep': EggGroup.CF_keep,
    'solid': EggGroup.CF_solid,
    'center': EggGroup.CF_center,
    'turnstile': EggGroup.CF_turnstile,
    'level': EggGroup.CF_level,
    'intangible': EggGroup.CF_intangible,

}


class EggCollideAttribute(EggAttribute):
    def __init__(self, csname, flags, name=''):
        # <Collide> name { type [flags] }

        # Make sure flags is not empty & it's a proper list.
        if flags and flags is not type(list):
            flags = [flags]
        self.cstype = cs2type[csname.lower()]
        self.flags = list()

        #  Using <Collide> without 'descend' is deprecated, add it on:
        if 'descend' not in flags:
            flags.append('descend')

        for flag_entry in flags:
            self.flags.append(flags2type[flag_entry.lower()])

        super().__init__(entry_type="Collide", name=name, contents=csname + (' ' if flags else '') + ' '.join(flags))

    def _modify_polygon(self, egg_polygon, tref=None):
        pass

    def _modify_node(self, egg_node):
        pass

    def _modify_group(self, egg_group):
        if self.target_nodes.check(egg_group.getName()):
            for flag in self.flags:
                egg_group.setCollideFlags(flag)
            egg_group.setCollisionName(self.name)
            egg_group.setCsType(self.cstype)


class EggCollide(EggCollideAttribute):
    def __init__(self, csname, flags, name=''):
        if flags is not type(list):
            flags = []
        super().__init__(csname, flags, name)
