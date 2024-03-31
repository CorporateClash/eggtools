"""
given: dir (recursive?)
old prefix
new prefix
iterate thru all eggh files for any textures with that old prefix and then change it to new prefix
if it finds img file then it will also rename image file

cc_t_gdg_prp_XYZ
-->
cc_t_ara_est_prp_furn_gdg


unrelated todo:
if there is a duplicate <UV> with same name, only keep one (but hard to determine which one automatically)
might be fine to pick the first instance since thats what will be used in egg2bam

Todo: See why depth write just dies with unrelated textures

"""
from eggtools.utils.EggMaintenanceUtil import EggMaintenanceUtil

if __name__ == "__main__":
    from eggtools.config.EggVariableConfig import GAMEASSETS_PATH
    import os
    # BE VERY VERY CAREFUL ABOUT BROAD NAMES

    prefixRepaths = {
        "***REMOVED***": "***REMOVED***"
    }

    # When we get a texture file that matches a key in prefixRepaths, we will replace the old prefix with the new
    # textureFileName : newTextureFileName
    # this will be passed into EggMaintenanceUtil
    _textureRenames = {}

    file_list = []

    target_path = GAMEASSETS_PATH
    target_path = os.path.join(target_path, "***REMOVED***")
    print(f"target ={target_path}")

    # target_path = "G:\\Shared drives\\Creative Team\\Game Assets\\Props\\Environmental Props\\Gardening Items\\planter"
    # ***REMOVED***
    for dirpath, _, filenames in os.walk(os.path.join(target_path)):
        for fileName in filenames:
            # if fileName.endswith(".png"):
            #     for prefixName in prefixRepaths.keys():
            #         if prefixName in fileName:
            #             newName = fileName.replace(prefixName, prefixRepaths[prefixName])
            #             _textureRenames[fileName] = newName
            if fileName.endswith(".egg"):
                print(f"adding file {fileName}")
                file_list.append(os.path.abspath(os.path.join(dirpath, fileName)))

    eggmaint = EggMaintenanceUtil(file_list, base_path=target_path, custom_rename_list=prefixRepaths)
    # Use put_into_tex_folder if we are operating on drive assets

    putinTexFolder = target_path != GAMEASSETS_PATH
    eggmaint.perform_rename_operations(rename_texture_file=True, put_into_tex_folder=False, copy_only=False, partial_replace=True)
    # eggmaint.perform_texpath_fixes(put_into_tex_folder=putinTexFolder)
    eggmaint.perform_general_maintenance() # # XXXX performing general maaintenance kills depth write
    # eggmaint.eggman.write_all_eggs_manually()