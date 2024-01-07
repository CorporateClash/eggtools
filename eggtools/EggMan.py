"""
EggMan: The docile robust egg manager for installing & maintaining models.

Allows you to do bulk/individual modifications to a set of egg files, including support for:
- Repathing textures, with support for auto-resolving broken texture paths
- Renaming TRefs to be something more appropriate and not like lambert69SG
- Removing defined UV names, which have a history of causing issues
- Removing Material/MRef data, since we don't have any use for them
- Renaming Group nodes
"""

import logging
from enum import Enum
from typing import Set

from panda3d.core import Filename
from panda3d.egg import *
from dataclasses import dataclass, field
import os, sys
from pathlib import Path

from eggtools.EggManConfig import DecalConfig, DualConfig, NodeNameConfig
from eggtools.AttributeDefs import DefinedAttributes, ObjectTypeDefs
from eggtools.attributes.EggAlphaAttribute import EggAlphaAttribute
from eggtools.attributes.EggAttribute import EggAttribute
from eggtools.attributes.EggUVNameAttribute import EggUVNameAttribute
from eggtools.config.EggVariableConfig import CCMODELS_MAPS_PATH, CCMODELS_DIR

BASE_PATH = CCMODELS_MAPS_PATH


class EggGroupRenameType(str, Enum):
    RenamePrefixes = "rename_prefix"
    RenameSuffixes = "rename_suffix"
    ReplaceAll = "replace_all"


logging.basicConfig(level=logging.CRITICAL)


@dataclass
class EggContext:
    """
    Holds iterable attributes for an EggData object
    """

    # Holds the filename of the egg
    filename: Filename

    # If egg has been altered in memory, it is considered dirty and subject to overwrite what's on the disk.
    dirty: bool = field(default_factory=lambda: False)

    egg_textures: Set = field(default_factory=lambda: set())
    egg_texture_collection: EggTextureCollection = field(default_factory=lambda: EggTextureCollection())
    egg_materials: Set = field(default_factory=lambda: set())
    egg_attributes: Set = field(default_factory=lambda: set())
    egg_timestamp_old: int = field(default_factory=lambda: False)
    egg_ext_file_refs: Set = field(default_factory=lambda: set())

    def __hash__(self):
        return hash(str(self))


class EggMan(object):
    # This is used to quickly grab EggData via a texture name
    _egg_name_2_egg_data = dict()
    _search_paths = list()

    def __str__(self):
        out = f"Eggman ({id(self)})\n"
        for egg in self.egg_datas.keys():
            out += str(self.egg_datas[egg]) + "\n"
        return out

    @property
    def search_paths(self) -> list:
        return self._search_paths

    @search_paths.setter
    def search_paths(self, path: list):
        if type(path) is not list:
            path = [path]
        for sp in path:
            self._search_paths.append(sp)

    def __init__(self, egg_filepaths: list, search_paths: list[str] = None) -> None:
        if not search_paths:
            search_paths = [BASE_PATH]
        self.search_paths = search_paths
        # use egg_datas to work with registered eggs
        # filename is stored in EggContext.filename
        self.egg_datas = dict()  # { EggData : EggContext }
        self.defined_attributes = DefinedAttributes

        self.register_eggs(egg_filepaths)

    def register_eggs(self, egg_filepaths: list[Filename | str]) -> None:
        if not egg_filepaths:
            return
        for fp in egg_filepaths:
            if not isinstance(fp, Filename):
                fp = Filename.fromOsSpecific(fp)
            if fp.getExtension() != "egg":
                print(f"{fp.getBasenameWoExtension()} does not have egg extension, not registering {fp.getFullpath()}")
                continue
            egg_data = EggData()
            egg_data.read(fp)
            self.egg_datas[egg_data] = EggContext(fp)
            ctx = self.egg_datas[egg_data]
            ctx.egg_texture_collection.findUsedTextures(egg_data)
            self._traverse_egg(egg_data, ctx)
            self._egg_name_2_egg_data[fp.getBasename()] = egg_data

    def _register_egg_texture(self, ctx: EggContext, target_node: EggTexture) -> None:
        """
        Register an egg texture with the given EggContext. This is used when traversing down the egg.
        """
        ctx.egg_textures.add(target_node)
        uvName = target_node.getUvName()
        if uvName:
            uvAttr = EggUVNameAttribute(uvName)
            ctx.egg_attributes.add(uvAttr)

    def _traverse_egg(self, egg: EggData | EggGroup, ctx: EggContext) -> None:
        """
        Traverses down an egg tree and records data mapped to the ctx key.

        :param EggData | EggGroup egg: Egg to traverse
        :param EggContext ctx: The original EggContext, required to keep things in order during recursion.
        """
        # we ask for ctx just to keep things in order
        for child in egg.getChildren():
            if isinstance(child, EggGroup):
                self._replace_object_types(ctx, child)
                # print(f"ObjectTypes for {child.getName()} - {child.getObjectTypes()}")
                self._traverse_egg(child, ctx)
            # <Material> { ... }
            if isinstance(child, EggMaterial):
                ctx.egg_materials.add(child)
            # <Texture> { blah.png }
            if isinstance(child, EggTexture):
                self._register_egg_texture(ctx, child)
            # <File> { filename.egg }
            if isinstance(child, EggExternalReference):
                ctx.egg_ext_file_refs.add(child)

    def merge_eggs(self, destination_egg: EggData, target_eggs: list[EggData] | EggData) -> None:
        """
        Source egg(s) will be removed from egg datas and cannot be searched for anymore.

        Result will be the object passed through the destination_egg argument.
        """
        if not isinstance(target_eggs, list):
            target_eggs = [target_eggs]

        for sacrifice in target_eggs:
            ctx = self.egg_datas[sacrifice]
            # Remove old egg from dict
            del self._egg_name_2_egg_data[ctx.filename.getBasename()]
            destination_egg.merge(sacrifice)
            del self.egg_datas[sacrifice]

        self.mark_dirty(destination_egg)

    """
    Egg Group Management
    """

    def strip_all_group_prefix(self, prefixes, recurse):
        for egg_data in self.egg_datas.keys():
            self.strip_group_prefix(egg_data, prefixes=prefixes, recurse=recurse)

    def strip_group_prefix(self, egg: EggNode, prefixes, recurse):
        """
        wrapper for rename_group_nodes
        """
        self.rename_group_nodes(egg, rename_type=EggGroupRenameType.RenamePrefixes, substrings=prefixes,
                                recurse=recurse)

    def strip_all_group_suffix(self, suffixes, recurse):
        for egg_data in self.egg_datas.keys():
            self.strip_group_suffix(egg_data, suffixes=suffixes, recurse=recurse)

    def strip_group_suffix(self, egg: EggNode, suffixes, recurse):
        """
        wrapper for rename_group_nodes
        """
        self.rename_group_nodes(egg, rename_type=EggGroupRenameType.RenameSuffixes, substrings=suffixes,
                                recurse=recurse)

    def rename_all_group_nodes(self, rename_type: EggGroupRenameType, substrings: list, recurse=True):
        for egg_data in self.egg_datas.keys():
            self.mark_dirty(egg_data)
            self.rename_group_nodes(egg_data, rename_type, substrings, recurse)

    def rename_group_nodes(self, egg: EggNode, rename_type: EggGroupRenameType, substrings: list, recurse: bool = True):
        """
        :param bool recurse: If true, will rename every nested group in the egg.
            False will only rename the highest layer.
        """

        def strip_group_prefix(egg: EggGroup, prefixes: list):
            # note: removeprefix exists in python 3.9
            name = egg.get_name()
            for prefix in prefixes:
                if name.startswith(prefix):
                    return name[len(prefix):]
            return name

        def strip_group_suffix(egg: EggGroup, suffixes: list):
            name = egg.get_name()
            for suffix in suffixes:
                if name.endswith(suffix):
                    return name.rstrip(suffix)
            return name

        def traverse_egg(egg: EggNode, ctx: EggContext):
            """
            Traverses down an egg tree and records data mapped to the ctx key.

            :param egg: Egg to traverse
            :type egg: EggData | EggGroup
            :param ctx: The original EggContext, required to keep things in order during recursion.
            :type ctx: EggContext
            """
            # we ask for ctx just to keep things in order
            for child in egg.getChildren():
                if isinstance(child, EggGroup):
                    if rename_type == EggGroupRenameType.RenamePrefixes:
                        child.set_name(strip_group_prefix(child, substrings))
                    elif rename_type == EggGroupRenameType.RenameSuffixes:
                        child.set_name(strip_group_suffix(child, substrings))
                    else:
                        # replace all
                        new_name = child.get_name().replace(substrings[0], substrings[1])
                        child.set_name(new_name)
                    if recurse:
                        traverse_egg(child, ctx)

        traverse_egg(egg, self.egg_datas[egg])

    """
    Egg Attribute Management
    """

    def apply_all_attributes(self, egg_attributes: dict[EggAttribute] = None) -> None:
        """
        By default, will clear up all the defined UV names if applicable
        """
        for egg_data in self.egg_datas.keys():
            self.apply_attributes(egg_data, egg_attributes)

    def apply_attributes(self, egg_base: EggData, egg_attributes: dict[EggAttribute] = None) -> None:
        if not egg_base:
            return
        if not egg_attributes:
            egg_attributes = dict()
        ctx = self.egg_datas[egg_base]
        for attribute in egg_attributes.keys():
            node_entries = egg_attributes[attribute]
            attribute.apply(egg_base, ctx, node_entries)
        for attribute in ctx.egg_attributes:
            attribute.apply(egg_base, ctx)
        self.mark_dirty(egg_base)

    def _replace_object_types(self, ctx: EggContext, target_node: EggGroup) -> None:
        if not hasattr(target_node, "getObjectTypes"):
            return
        # Hack- Find egg data from ctx (reverse operation)
        egg_base = list(filter(lambda x: self.egg_datas[x] == ctx, self.egg_datas))[0]
        for object_type_name in target_node.getObjectTypes():
            object_type_def = ObjectTypeDefs.get(object_type_name, list())
            if not object_type_def:
                continue
            for attribute in object_type_def:
                # Apply EggAttribute equivalents defined for this object type
                attribute.apply(egg_base, ctx, node_entries=[target_node.getName()])
            target_node.removeObjectType(object_type_name)
            ctx.dirty = True

    """
    Texture Reference Methods
    """

    def rebase_egg_texture(self, tref: str, new_tex_path: str, old_egg_texture: EggTexture) -> EggTexture:
        """
        Generates a new EggTexture with a given tref + texpath while copying the attributes of the old EggTexture.

        :param str tref: TextureReference name
        :param str new_tex_path: New texture path for the EggTexture
        :param EggTexture old_egg_texture: EggTexture to inherit attributes from
        :return: EggTexture with modified tref/tex path
        :rtype: EggTexture
        """
        # lord, forgive me for my sins
        et = EggTexture(tref, new_tex_path)

        et.alpha_file_channel = old_egg_texture.alpha_file_channel
        et.alpha_filename = old_egg_texture.alpha_filename
        et.alpha_fullpath = old_egg_texture.alpha_fullpath
        et.alpha_scale = old_egg_texture.alpha_scale
        et.anisotropic_degree = old_egg_texture.anisotropic_degree
        et.border_color = old_egg_texture.border_color
        et.color = old_egg_texture.color
        et.compression_mode = old_egg_texture.compression_mode
        et.env_type = old_egg_texture.env_type
        et.format = old_egg_texture.format
        et.lod_bias = old_egg_texture.lod_bias
        et.magfilter = old_egg_texture.magfilter
        et.max_lod = old_egg_texture.max_lod
        et.min_lod = old_egg_texture.min_lod
        et.minfilter = old_egg_texture.minfilter
        # et.multitexture_sort = old_egg_texture.multitexture_sort
        et.multiview = old_egg_texture.multiview
        et.num_views = old_egg_texture.num_views
        et.priority = old_egg_texture.priority
        et.quality_level = old_egg_texture.quality_level
        et.read_mipmaps = old_egg_texture.read_mipmaps
        et.rgb_scale = old_egg_texture.rgb_scale
        et.saved_result = old_egg_texture.saved_result
        et.stage_name = old_egg_texture.stage_name
        et.tex_gen = old_egg_texture.tex_gen
        et.texture_type = old_egg_texture.texture_type
        et.uv_name = old_egg_texture.uv_name  # meh we dont like these but let's play fair now
        et.wrap_mode = old_egg_texture.wrap_mode
        et.wrap_u = old_egg_texture.wrap_u
        et.wrap_v = old_egg_texture.wrap_v
        return et

    def _replace_poly_tref(self,
                           egg_polygon: EggPolygon, new_tex: EggTexture, tex_to_replace: EggTexture,
                           replace_by_name: bool = True) -> None:
        """
        Low level method for replacing EggTextures associated with an EggPolygon.

        :param bool replace_by_name: Renames TRefs to the name of the texture (excluding extension)
        """
        poly_textures = egg_polygon.getTextures()
        new_textures = list()
        for texture_ref in range(len(poly_textures)):
            if replace_by_name:
                replace_by_name = poly_textures[texture_ref].getFilename() == tex_to_replace.getFilename()
            if poly_textures[texture_ref] == tex_to_replace or replace_by_name:
                new_textures.append(new_tex)
            else:
                new_textures.append(poly_textures[texture_ref])
        egg_polygon.clearTexture()
        for tex in new_textures:
            egg_polygon.add_texture(tex)

    def do_tex_replace(self, egg: EggData, new_tex: EggTexture, old_tex: EggTexture) -> None:
        """
        Base method used for replacing texture instances in an egg file.

        Recursively replaces an EggTexture with another in a EggData instance.
        """

        def traverse_egg(egg, ctx):
            """
            Traverses down an egg tree and records data mapped to the ctx key.

            :param egg: Egg to traverse
            :type egg: EggData | EggGroup
            :param ctx: The original EggContext, required to keep things in order during recursion.
            :type ctx: EggContext
            """
            # we ask for ctx just to keep things in order
            for child in egg.getChildren():
                if isinstance(child, EggGroupNode):
                    traverse_egg(child, ctx)
                if isinstance(child, EggPolygon):
                    self._replace_poly_tref(child, new_tex, old_tex)

        traverse_egg(egg, self.egg_datas[egg])

    def repath_egg_texture(self, egg: EggData, egg_texture: EggTexture, filename: Filename) -> None:
        """
        Repaths an EggTexture while *also* renaming the corresponding TRefs

        Todo: Since filename can be a filepath, we should have a relative mode.

        :param EggData egg: base egg file
        :param EggTexture egg_texture: texture to repath
        :param Filename filename: new filename for egg texture
        """
        self.mark_dirty(egg)

        test_tref = "test_tref"
        ctx = self.egg_datas[egg]
        # gotta iterate through the texture set to find our particular EggTexture
        for egg_tex in ctx.egg_textures:
            if egg_tex != egg_texture:
                continue
            temp_tex = EggTexture(egg_texture)
            temp_tex.assign(self.rebase_egg_texture(test_tref, filename, egg_tex))
            self.do_tex_replace(egg, new_tex=temp_tex, old_tex=egg_tex)
            egg_tex.setFilename(filename)
        self.rename_trefs(egg)

    def get_tref(self, egg: EggData, egg_texture: EggTexture) -> str:
        """
        Gets the name of the tref for the given EggTexture

        Example:
            <Texture> texture1 { ... }
            <TRef> { texture1 }
        will return 'texture1'
        """
        ctx = self.egg_datas[egg]
        # Ya I know, looks ugly, but don't blame me! There's no way to get the TRef from the Egg API!
        return repr(
            ctx.egg_texture_collection.findFilename(egg_texture.getFilename())
        ).replace("EggTexture ", "", 1)

    def _replace_tref(self, egg: EggData, old_tex: EggTexture, new_tex: EggTexture) -> None:
        ctx = self.egg_datas[egg]
        self.do_tex_replace(egg, new_tex, old_tex)
        old_tex.assign(new_tex)
        self.mark_dirty(ctx)

    def rename_trefs(self, egg: EggData) -> None:
        """
        Rename texture references (trefs)

        Example: texture1 is a tref
        <Texture> texture1 { ... }
        <TRef> texture1
        """
        ctx = self.egg_datas[egg]
        for egg_tex in ctx.egg_textures:
            self.mark_dirty(ctx)
            egg_fn = egg_tex.getFilename().getBasenameWoExtension()
            new_tex = self.rebase_egg_texture(egg_fn, egg_tex.getFullpath(), egg_tex)
            self.do_tex_replace(egg, new_tex, egg_tex)
            egg_tex.assign(new_tex)
        # Guarantees that each texture in the collection has a unique TRef name
        # Hmm, maybe we shouldn't put it here just yet. This leads ot .ref1.png files getting exported.
        # ctx.egg_texture_collection.uniquifyTrefs()

    def rename_all_trefs(self) -> None:
        """
        Renames all texture references (trefs) registered with EggMan.

        Example: texture1 is a tref
        <Texture> texture1 { ... }
        <TRef> texture1
        """
        for egg_data in self.egg_datas.keys():
            self.rename_trefs(egg_data)

    def get_current_textures(self, egg: EggData) -> list[EggTexture]:
        # workaround attempt
        ctx = self.egg_datas[egg]
        egg_textures = []
        for texture in ctx.egg_textures:
            egg_textures.append(texture)
        return egg_textures

    def get_texture_filepaths(self, egg: EggData) -> list[Filename]:
        ctx = self.egg_datas[egg]
        # test = list(lambda texname: texname.getFilename() for texname in ctx.egg_textures)
        return [texname.getFilename() for texname in ctx.egg_textures]

    def get_texture_basenames(self, egg: EggData, include_extension: bool = True) -> list[str]:
        ctx = self.egg_datas[egg]
        # test = list(lambda texname: texname.getFilename() for texname in ctx.egg_textures)
        if include_extension:
            return [texname.getFilename().getBasename() for texname in ctx.egg_textures]
        return [texname.getFilename().getBasenameWoExtension() for texname in ctx.egg_textures]

    def get_texture_by_name(self, egg: EggData, texture_name: str) -> EggTexture:
        """
        Ensure that texture_name is the Basename (.getBasename()))
        """
        ctx = self.egg_datas[egg]
        for egg_texture in ctx.egg_textures:
            if texture_name in egg_texture.getFilename().getBasename():
                return egg_texture

    def get_tex_info(self, egg_texture: EggTexture) -> str:
        """
        Returns the anisotropic filtering degree that has been specified for this texture,
        or 0 if nothing has been specified.

        1 = Off
        """
        return f"Anisotropic Degree: {egg_texture.anisotropic_degree}\n" \
               f"Alpha File Channel: {egg_texture.alpha_file_channel}"

    def get_all_egg_filenames(self, prepend_dir=".", as_filename_object: bool = False) -> list[Filename] | list[str]:
        filenames = list()
        for egg_data in self.egg_datas.keys():
            if as_filename_object:
                filenames.append(Filename.fromOsSpecific(os.path.join(prepend_dir, self.get_egg_filename(egg_data))))
            else:
                filenames.append(os.path.join(prepend_dir, self.get_egg_filename(egg_data)))
        return filenames

    def get_egg_filename(self, egg: EggData) -> Filename:
        """
        Get the Filename attribute from the given EggData object.
        """
        ctx = self.egg_datas[egg]
        return ctx.filename

    def get_egg_by_filename(self, filename: str) -> EggData:
        """
        Search for a specific egg data entry given a filename

        :param str filename: Must include extension at the end.
        """
        if hasattr(filename, 'getBasename'):
            filename = filename.getBasename()
        return self._egg_name_2_egg_data.get(filename)

    """
    Egg External File Methods
    """

    """
    EggMan Helper Methods
    """

    def mark_dirty(self, egg: EggData | EggContext) -> None:
        if isinstance(egg, EggContext):
            egg.dirty = True
        else:
            self.egg_datas[egg].dirty = True

    def try_different_names(self, filename: str, prefix_type: str = "t") -> str:
        new_filename = filename.replace("ttcc_", f"cc_{prefix_type}_")
        if not new_filename.startswith(f"cc_{prefix_type}_"):
            new_filename = f"cc_{prefix_type}_{filename}"
        if os.path.isfile(os.path.join(BASE_PATH, new_filename)):
            logging.info(f"found similar texture name to {filename}: {new_filename}")
            return new_filename
        # can't find any hits, just return em back
        return filename

    def resolve_egg_textures(self, egg: EggData, want_auto_resolve: bool = True, try_names: bool = True) -> None:
        def auto_resolve(tex_path: str):
            """
            :return: new filename for setFilename
            """
            tex_file = Path(tex_path).name
            if try_names:
                tex_file = self.try_different_names(tex_file)
            for search_path in self.search_paths:
                new_tex_file = os.path.join(search_path, tex_file)
                if not os.path.isfile(new_tex_file):
                    continue
                logging.info(f"Rebasing texture path for {tex_file} to CCMODELS_MAPS")
                tex_path = os.path.relpath(
                    new_tex_file, os.path.dirname(os.path.abspath(ctx.filename))
                ).replace(os.sep, '/')
                logging.debug(f"new tex path--> {tex_path} ({search_path}")
                self.mark_dirty(ctx)
            return tex_path

        ctx = self.egg_datas[egg]

        for egg_texture in ctx.egg_textures:
            fixed_path = os.path.abspath(os.path.join(os.path.dirname(ctx.filename), egg_texture.getFullpath()))
            # TODO: ensure_relative function
            try:
                rel_tex_path = os.path.relpath(
                    fixed_path, os.path.dirname(os.path.abspath(ctx.filename))
                ).replace(os.sep, '/')
            except ValueError:
                # An exception can be thrown if the relative texture is on a different drive (ie: google drive)
                rel_tex_path = ""

            ensure_test = rel_tex_path in str(egg_texture.getFilename())
            # if not os.path.isfile(os.path.abspath(egg_texture.getFullpath())):
            # EDGE CASE: what if file is using absolute filepath and checks the os.path.isfile check?
            # we still don't want to use absolute filepaths.

            if not (os.path.isfile(fixed_path) and not os.path.isfile(os.path.abspath(egg_texture.getFullpath()))):
                logging.warning(f"Warning, couldn't find texture {egg_texture.getFilename()}")
                # if relative (good), this should give is an invalid path.
                logging.debug(f"(path){os.path.abspath(egg_texture.getFullpath())}")
                if want_auto_resolve:
                    tref = repr(
                        ctx.egg_texture_collection.findFilename(egg_texture.getFilename())
                    ).replace("EggTexture ", "", 1)
                    egg_texture.assign(
                        self.rebase_egg_texture(tref, auto_resolve(egg_texture.getFullpath()), egg_texture)
                    )
            elif os.path.isfile(fixed_path) and not ensure_test:
                print(f"ensure_test returned false")

                tref = repr(
                    ctx.egg_texture_collection.findFilename(egg_texture.getFilename())
                ).replace("EggTexture ", "", 1)
                egg_texture.assign(
                    self.rebase_egg_texture(tref, auto_resolve(egg_texture.getFullpath()), egg_texture)
                )
            else:
                logging.info(f"Found texture {egg_texture.getFilename()}")
                logging.debug(f"(filepath){os.path.abspath(egg_texture.getFullpath())}")
                logging.debug(f"(fixedpath){fixed_path}")

    def resolve_external_refs(self, egg:EggData):
        ctx = self.egg_datas[egg]
        for external_ref in ctx.egg_ext_file_refs:
            # TODO, can copy what was done w/ ensuring texture
            pass

    """
    General Maintenance Methods
    """

    def remove_texture_duplicates(self, egg:EggData=None):
        if not egg:
            for egg_data in self.egg_datas.keys():
                egg_data.collapseEquivalentTextures()
        else:
            egg.collapseEquivalentTextures()

    def remove_timestamps(self, egg: EggData = None) -> None:
        if not egg:
            for egg_data in self.egg_datas.keys():
                self.remove_timestamp(egg_data)
        else:
            self.remove_timestamp(egg)

    def remove_timestamp(self, egg: EggData = None) -> None:
        ctx = self.egg_datas[egg]
        ctx.egg_timestamp_old = egg.getEggTimestamp()
        egg.setEggTimestamp(1)

    def fix_broken_texpaths(self, egg: EggData = None) -> None:
        if not egg:
            # ok we'll just fix all of the ones we've registered then
            for egg_data in self.egg_datas.keys():
                self.resolve_egg_textures(egg_data)
        else:
            self.resolve_egg_textures(egg)

    def remove_egg_materials(self, egg: EggData) -> None:
        ctx = self.egg_datas[egg]
        for material in ctx.egg_materials:
            material.clearAmb()
            material.clearBase()
            material.clearDiff()
            material.clearEmit()
            material.clearIor()
            material.clearLocal()
            material.clearMetallic()
            material.clearRoughness()
            material.clearShininess()
            material.clearSpec()

        egg.collapseEquivalentMaterials()
        ctx.egg_materials = set()
        self.mark_dirty(ctx)

    def purge_all_comments(self, egg:EggData=None) -> None:
        if not egg:
            for egg_data in self.egg_datas.keys():
                self.purge_comments(egg_data)
        else:
            self.purge_comments(egg)

    def purge_comments(self, egg: EggData) -> None:
        # We can probably actually put EggComments anywhere in the egg file, but people mostly
        # put them in the beginning of the egg file not in a nested group.
        for child in egg.getChildren():
            if isinstance(child, EggComment):
                # idk how to completely get rid of Comments rn
                child.setComment("")
                self.mark_dirty(egg)
                # < Comment> { dfsjkofjhksdf }

    """
    Write/Output Methods
    """

    def write_all_eggs(self, custom_suffix="", dryrun=False):
        for egg_data in self.egg_datas.keys():
            self.write_egg(egg_data, custom_suffix=custom_suffix, dryrun=False)

    def write_egg(self, egg, filename: Filename = None, custom_suffix="", dryrun=False):
        if not filename:
            filename = egg.egg_filename
        filename = Filename(filename.getFullpath() + custom_suffix)
        ctx = self.egg_datas[egg]
        if ctx.dirty:
            if not dryrun:
                # If we put uniquifyTRefs here, it will not generate .tref.png files.
                ctx.egg_texture_collection.uniquifyTrefs()
                # We get a PermissionDenied error once in a while with models that are not scoped to the target env.
                if not egg.writeEgg(filename + custom_suffix):
                    logging.error(f"something went wrong when trying to write {egg.egg_filename}")
            else:
                print(egg)
        else:
            logging.debug(f"{egg.egg_filename} was not dirty, not writing anything")

    def write_all_eggs_manually(self, custom_suffix=""):
        """
        NB: This will cause eggs to have truncated floating point values for data.
        Ensure that this isn't causing weird visual dislocation issues
        """
        for egg_data in self.egg_datas.keys():
            self.write_egg_manually(egg_data, custom_suffix=custom_suffix)

    def write_egg_manually(self, egg, filename="", custom_suffix="", ):
        # because for some reason write_egg doesn't ... work???
        if not filename:
            filename = egg.egg_filename
        filename = Filename(filename.getFullpath() + custom_suffix)
        ctx = self.egg_datas[egg]
        if ctx.dirty:
            # If we put uniquifyTRefs here, it will not generate .tref.png files.
            ctx.egg_texture_collection.uniquifyTrefs()
            # We get a PermissionDenied error once in a while with models that are not scoped to the target env.
            try:
                with open(filename, "w") as egg_file:
                    logging.info(f"trying to write {filename}")
                    egg_file.write(str(egg))
            except Exception as e:
                print(f"Failed to save file ({e})")
        else:
            pass
            # logging.debug(f"not rewriting {filename}")


# test_tex_collection = EggTextureCollection()

# if any methods depend on the name of the TRef for anything, be wary of:
# (EggTexture cc_tnurseShark_palette_4allc_1, EggTexture cc_tnurseShark_palette_4allc_1.tref1)

if __name__ == "__main__":
    mdls = [
        # Filename.fromOsSpecific(os.path.join(CCMODELS_DIR, "***REMOVED***.egg")),
        Filename.fromOsSpecific(os.path.join(CCMODELS_DIR, "***REMOVED***")),

        # Filename.fromOsSpecific(os.path.join(CCMODELS_DIR, "***REMOVED***.egg"))
    ]
    # eg1 = EggContext("***REMOVED***.egg")
    # eg2 = EggContext("***REMOVED***.egg")
    #
    # models = ["cogpodium.egg"]
    f1 = "test1"
    f2 = "test2"
    eggman = EggMan(mdls)
    eggs = eggman.egg_datas.keys()
    ets = []
    # repath_egg_texture1
    for egg in eggs:
        eggman.rename_group_nodes(egg, ["cup_"])
        # print(egg)
        # ctx = eggman.egg_datas[egg]
        # for egg_texture in ctx.egg_textures:
        #     new_filename = str(egg_texture.getFilename().getBasenameWoExtension())[::-1]
        #     new_fullpath =  str(egg_texture.getFullpath().getBasenameWoExtension())[::-1]
        #
        #     eggman.repath_egg_texture(egg, egg_texture, new_fullpath, new_filename)
        # print(egg)

        # ets.append(eggman.egg_datas[egg])
        # print(eggman.egg_datas[egg].filename)

    # print(ets[0].egg_textures == ets[1].egg_textures)
    # # repath_egg_texture
    # for egg in eggs:
    #     # print(egg)
    #     # eggman.rename_trefs(egg)
    #     # print(egg)
    #     ctx = eggman.egg_datas[egg]
    #     for egg_tex in ctx.egg_textures:
    #         print(eggman.get_tex_info(egg_tex))
    #     # # print(ctx.egg_texture_collection.getTextures())
    #     # for egg_tex in ctx.egg_textures:
    #     #     egg_fn = egg_tex.getFilename().getBasenameWoExtension()
    #     #     new_tex = eggman.rebase_egg_texture(egg_fn, egg_tex.getFilename(), egg_tex)
    #     #     do_tex_replace(egg, ctx, new_tex, egg_tex)
    #     # print(egg)
    #
    #         # print(new_tex)
