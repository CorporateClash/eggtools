import shutil

from panda3d.core import Filename

from eggtools.EggMan import EggMan

rename_list = {}


class EggMaintenanceUtil:

    # might be wise to use **kwargs here for configs
    def __init__(self, file_list: list, custom_rename_list: dict = None, base_path=None):
        """
        :param dict custom_rename_list: A dictionary consisting of old_name keys & new_name values.
        """
        self.base_path = base_path
        if not self.base_path:
            self.base_path = GAMEASSETS_MAPS_PATH
        self.eggman = EggMan(file_list)
        if not custom_rename_list:
            self.rename_list = rename_list
        else:
            self.rename_list = custom_rename_list

    def perform_general_maintenance(self):
        self.eggman.fix_broken_texpaths()
        self.eggman.rename_all_trefs()
        self.eggman.apply_all_attributes()
        self.eggman.write_all_eggs_manually()

    def perform_rename_operations(
            self,
            rename_texture_file=False,
            put_into_tex_folder=False,
            copy_only=False,
            partial_replace=False,
    ):
        subfolder = ""
        allTextures = self.rename_list
        for egg_obj in self.eggman.egg_datas.keys():
            eggctx = self.eggman.egg_datas[egg_obj]
            for texbase in self.eggman.get_texture_basenames(egg_obj, include_extension=False):
                for textureEntry in allTextures.keys():
                    newTexture = ""
                    if partial_replace and textureEntry in texbase:
                        newTexture = texbase.replace(textureEntry, allTextures[textureEntry])
                    elif texbase == textureEntry:
                        newTexture = allTextures[texbase]
                    if not newTexture:
                        continue

                    egg_texture = self.eggman.get_texture_by_name(egg_obj, texbase)
                    _old_eggtex = egg_texture.getFullpath()

                    self.base_path = eggctx.filename.getDirname()
                    if put_into_tex_folder:
                        os.makedirs(
                            os.path.join(Filename.toOsSpecific(Filename.fromOsSpecific(self.base_path)), "tex"),
                            exist_ok=True
                        )
                        subfolder = "tex"
                    else:
                        subfolder = egg_texture.getFullpath().getDirname()

                    rebase_texture = f"{subfolder}/{newTexture}.png"

                    old_texture_source = Filename.toOsSpecific(Filename.fromOsSpecific(
                        os.path.join(eggctx.filename.getDirname(), _old_eggtex)
                    ))
                    rebase_texture_source = Filename.toOsSpecific(Filename.fromOsSpecific(
                        os.path.join(eggctx.filename.getDirname(), rebase_texture)
                    ))

                    if rename_texture_file and \
                            os.path.isfile(old_texture_source) and not \
                            os.path.isfile(rebase_texture_source):
                        if copy_only:
                            print(f"copying image {_old_eggtex} -> {rebase_texture}")
                            shutil.copy(
                                old_texture_source,
                                rebase_texture_source
                            )
                        else:
                            print(f"moving image {_old_eggtex} -> {rebase_texture}")
                            shutil.move(
                                old_texture_source,
                                rebase_texture_source
                            )
                    print(f"repathing {eggctx.filename} ({texbase} --> {newTexture})")
                    self.eggman.repath_egg_texture(egg_obj, egg_texture, Filename.fromOsSpecific(rebase_texture))
            self.eggman.write_egg_manually(egg_obj)

    def perform_texpath_fixes(self, put_into_tex_folder=True, copy_only=False):
        """
        For each texture in an egg file, it will try to locate the texture by the defined texpath
        If it can find the texture, it will relocate it to be next to the model (or in a tex/ folder)

        This is ideal for cloud/drive asset management but not for asset repositories.
        """

        # Like a ninja... silent.
        subfolder = ""
        for egg_obj in self.eggman.egg_datas.keys():
            eggctx = self.eggman.egg_datas[egg_obj]
            for texbase in self.eggman.get_texture_basenames(egg_obj, include_extension=False):
                self.base_path = eggctx.filename.getDirname()
                if put_into_tex_folder:
                    print(f"moving {eggctx.filename}")
                    os.makedirs(
                        os.path.join(Filename.toOsSpecific(Filename.fromOsSpecific(self.base_path)), "tex"),
                        exist_ok=True
                    )
                    subfolder = "tex/"
                rebase_texture = f"{subfolder}{texbase}.png"
                egg_texture = self.eggman.get_texture_by_name(egg_obj, texbase)
                _old_eggtex = egg_texture.getFullpath().getBasename()

                old_texture_source = Filename.toOsSpecific(Filename.fromOsSpecific(
                    os.path.join(eggctx.filename.getDirname(), _old_eggtex)
                ))
                rebase_texture_source = Filename.toOsSpecific(Filename.fromOsSpecific(
                    os.path.join(eggctx.filename.getDirname(), rebase_texture)
                ))

                if os.path.isfile(old_texture_source) and not os.path.isfile(rebase_texture_source):
                    if copy_only:
                        print(f"copying image {_old_eggtex} -> {rebase_texture}")
                        shutil.copy(
                            old_texture_source,
                            rebase_texture_source
                        )
                    else:
                        print(f"moving image {_old_eggtex} -> {rebase_texture}")
                        shutil.move(
                            old_texture_source,
                            rebase_texture_source
                        )
                print(f"repathing {eggctx.filename} ({texbase} --> {rebase_texture})")
                self.eggman.repath_egg_texture(egg_obj, egg_texture, Filename.fromOsSpecific(rebase_texture))
            self.eggman.write_egg(egg_obj)


"""
Test module
"""

if __name__ == "__main__":
    from eggtools.config.EggVariableConfig import GAMEASSETS_MODELS_PATH, GAMEASSETS_MAPS_PATH
    import os

    file_list = []

    target_path = os.getcwd()
    for dirpath, _, filenames in os.walk(os.path.join(target_path)):
        for file in filenames:
            if file.endswith(".egg"):
                print(f"adding file {file}")
                file_list.append(os.path.abspath(os.path.join(dirpath, file)))

    eggmaint = EggMaintenanceUtil(file_list, base_path=target_path)

"""
Sample Implementation
"""

if 0:
    from eggtools.config.EggVariableConfig import GAMEASSETS_MODELS_PATH, GAMEASSETS_MAPS_PATH
    import os

    file_list = []

    # target_path = "C:\\Path\\To\\Assets"
    target_path = GAMEASSETS_MODELS_PATH
    for dirpath, _, filenames in os.walk(os.path.join(target_path)):
        for file in filenames:
            if file.endswith(".egg"):
                print(f"adding file {file}")
                file_list.append(os.path.abspath(os.path.join(dirpath, file)))

    eggmaint = EggMaintenanceUtil(file_list, base_path=target_path)
    # Use put_into_tex_folder if we are operating on storing assets individually
    eggmaint.perform_rename_operations(rename_texture_file=True, put_into_tex_folder=True, copy_only=False)
    eggmaint.perform_texpath_fixes()
    eggmaint.perform_general_maintenance()
