import os

import builtins

from panda3d.core import loadPrcFile

"""
define builtin path locations
"""

# WARNING: os.getcwd() is subjective, strongly prefer you DON'T hit the default case and
# instead have your environment variables defined!

CCMODELS_DEVTOOLS_PATH = os.getcwd()

CCMODELS_PATH = os.path.abspath(os.environ.get('CC_GAMEASSETS_SRC', os.path.join(os.getcwd(), '../src')))
builtins.CCMODELS_PATH = CCMODELS_PATH

CCMODELS_MAPS_PATH = os.path.abspath(os.environ.get('CC_GAMEASSETS_MAPS', os.path.join(os.getcwd(), '../src/maps')))
builtins.CCMODELS_MAPS_PATH = CCMODELS_MAPS_PATH

CCMODELS_MODELS_PATH = os.path.abspath(os.environ.get('CC_GAMEASSETS_MODELS', os.path.join(os.getcwd(), '../src/models')))
builtins.CCMODELS_MODELS_PATH = CCMODELS_MODELS_PATH

# %CCMODELS%/maps/clothing
CCMODELS_MAPS_CLOTHING_PATH = os.path.abspath(
    os.environ.get('CC_GAMEASSETS_MAPS_CLOTHING', os.path.join(CCMODELS_MAPS_PATH, "clothing"))
)
builtins.CCMODELS_MAPS_CLOTHING_PATH = CCMODELS_MAPS_CLOTHING_PATH

CCMODELS_MAPS_GUI_PATH = os.path.abspath(
    os.environ.get('CC_GAMEASSETS_MAPS_GUI', os.path.join(CCMODELS_MAPS_PATH, "gui"))
)

CCMODELS_INSTALL_PATH = os.path.abspath(os.environ.get('CC_GAMEASSETS_INSTALL', "../built"))
builtins.CCMODELS_INSTALL_PATH = CCMODELS_INSTALL_PATH

# Required for egg-palettize to behave correctly
CCMODELS_DIR = os.environ.get('CC_GAMEASSETS_SRC', '../src')
builtins.CCMODELS_DIR = CCMODELS_DIR

CCMODELS_INSTALL_DIR = os.environ.get('CC_GAMEASSETS_INSTALL', "../built")
builtins.CCMODELS_INSTALL_DIR = CCMODELS_INSTALL_DIR

CCMODELS_BIN_DIR = os.environ.get('CC_GAMEASSETS_BIN', "../built")

CCMODELS_INDEX_DIR = os.environ.get('CC_GAMEASSETS_INDEX', '../index')
builtins.CCMODELS_INDEX_DIR = CCMODELS_DIR

# CCMODELS_TXAOUT_DIR = os.environ.get('CC_GAMEASSETS_TXAOUT', '../index')
# builtins.CCMODELS_TXAOUT_DIR = CCMODELS_DIR

"""
config stuff

"""

# NB: This doesn't actually work. You must edit the prc file associated with the egg2bam binary.
# from panda3d.core import loadPrcFile
# print(loadPrcFile("config/objecttypes.prc"))
# loadPrcFile("config/eggconf.prc")

if __name__ == "__main__":
    print(f"CC_GAMEASSETS_SRC = {CCMODELS_PATH}")