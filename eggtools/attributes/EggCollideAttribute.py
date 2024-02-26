from panda3d.egg import EggGroup, EggVertexPool, EggPolygon

from eggtools.attributes.EggAttribute import EggAttribute

# Collision Solids
cs2type = {
    'none': EggGroup.CST_none,

    # The geometry represents an infinite plane.
    # The first polygon found in the group will define the plane.
    'plane': EggGroup.CST_plane,

    # The geometry represents a single polygon.
    # The first polygon is used.
    'polygon': EggGroup.CST_polygon,

    # The geometry represents a complex shape made up of several polygons.
    # This collision type should not be overused, as it provides the least optimization benefit.
    'polyset': EggGroup.CST_polyset,

    # The geometry represents a sphere.
    # The vertices in the group are averaged together to determine the sphere’s center and radius.
    'sphere': EggGroup.CST_sphere,

    # The geometry represents a tube.
    # This is a cylinder-like shape with hemispherical endcaps;
    # it is sometimes called a capsule or a lozenge in other packages.
    # The smallest tube shape that will fit around the vertices is used.
    'tube': EggGroup.CST_tube,

    # The geometry represents an inverse sphere.
    # This is the same as Sphere, with the normal inverted, so that the solid part of an inverse sphere is the
    # entire world outside of it.
    # Note that an inverse sphere is in infinitely large solid with a finite hole cut into it.
    'inv_sphere': EggGroup.CST_inv_sphere,
    'invsphere': EggGroup.CST_inv_sphere,

    # The geometry represents a box.
    # The smallest axis-alligned box that will fit around the vertices is used.
    'box': EggGroup.CST_box,

    'floor_mesh': EggGroup.CST_floor_mesh,
}

# Collision Flags

flags2type = {
    'none': EggGroup.CF_none,

    # Each group descended from this node that contains geometry will define a new collision object of the given type.
    # The event name, if any, will also be inherited from the top node and shared among all the collision objects.
    # This option will soon be the default; it is suggested that it is always specified for most compatibility.
    'descend': EggGroup.CF_descend,

    # Throws the name of the <Collide> entry, or the name of the surface if the <Collide> entry has no name,
    # as an event whenever an avatar strikes the solid.
    # This is the default if the <Collide> entry has a name.
    'event': EggGroup.CF_event,

    # Don’t discard the visible geometry after using it to define a collision surface;
    # create both an invisible collision surface and the visible geometry.
    'keep': EggGroup.CF_keep,

    'solid': EggGroup.CF_solid,

    'center': EggGroup.CF_center,

    'turnstile': EggGroup.CF_turnstile,

    # Stores a special effective normal with the collision solid that points up,
    # regardless of the actual shape or orientation of the solid.
    # This can be used to allow an avatar to stand on a sloping surface without having a tendency to slide downward.
    'level': EggGroup.CF_level,

    # Rather than being a solid collision surface, the defined surface represents a boundary.
    # The name of the surface will be thrown as an event when an avatar crosses into the interior,
    # and name-out will be thrown when an avatar exits.
    'intangible': EggGroup.CF_intangible,

}


class EggCollideAttribute(EggAttribute):
    def __init__(self, csname, flags, name='', preserve_uv_data=True):
        # <Collide> name { type [flags] }
        self.cstype = cs2type[csname.lower()]
        self.flags = list()

        # Make sure flags is not empty & it's a proper list.
        if flags and not isinstance(flags, list):
            flags = [flags]

        #  Using <Collide> without 'descend' is deprecated, add it on:
        if 'descend' not in flags:
            flags.append('descend')

        for flag_entry in flags:
            self.flags.append(flags2type[flag_entry.lower()])

        self.preserve_uv_data = preserve_uv_data

        super().__init__(entry_type="Collide", name=name, contents=csname + (' ' if flags else '') + ' '.join(flags))

    def _modify_polygon(self, egg_polygon, tref=None):
        # print(egg_polygon.hasColor())
        pass

    def _modify_node(self, egg_node):
        if self.target_nodes.check(egg_node.getName()) and hasattr(egg_node, "setCollideFlags"):
            # We must aggregate all of the collision bits
            collisionFlag = 0
            for flag in self.flags:
                collisionFlag |= flag
            egg_node.setCollideFlags(collisionFlag)
            egg_node.setCollisionName(self.name)
            egg_node.setCsType(self.cstype)
            if not self.preserve_uv_data:
                self.remove_uv_data(egg_node)

    def _modify_group(self, egg_group):
        pass

    def remove_uv_data(self, egg_node):
        # if hasattr(egg_node, "has_vertex_color"):
        #     print(type(egg_node))
        # if egg_node.hasColor():
        #     print(egg_node.getColor())

        if isinstance(egg_node, EggGroup):
            for child in egg_node.getChildren():
                self.remove_uv_data(child)

        # print(type(egg_node))
        if isinstance(egg_node, EggVertexPool):
            for vpoolchild in egg_node:  # should only contain EggVertexes
                vpoolchild.clear_uv()

        if isinstance(egg_node, EggPolygon):
            # print(egg_node.has_vertex_color())
            # print(egg_node.connected_shading)
            if "keep" not in self.flags:
                egg_node.clear_texture()
                egg_node.clear_material()


class EggCollide(EggCollideAttribute):
    def __init__(self, csname, flags, name='', preserve_uv_data=True):
        super().__init__(csname, flags, name, preserve_uv_data=preserve_uv_data)
