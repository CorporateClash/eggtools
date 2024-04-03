import os

import builtins

"""
define builtin path locations
"""

# WARNING: os.getcwd() is subjective, strongly prefer you DON'T hit the default case and
# instead have your environment variables defined!

GAMEASSETS_PATH = os.path.abspath(
    os.environ.get('GAMEASSETS_SRC', os.path.join(os.getcwd(), '../src'))
)
builtins.GAMEASSETS_PATH = GAMEASSETS_PATH
# Required for egg-palettize to behave correctly
GAMEASSETS_DIR = os.environ.get('GAMEASSETS_SRC', '../src')
builtins.GAMEASSETS_DIR = GAMEASSETS_DIR

GAMEASSETS_MAPS_PATH = os.path.abspath(
    os.environ.get('GAMEASSETS_MAPS', os.path.join(os.getcwd(), '../src/maps'))
)
builtins.GAMEASSETS_MAPS_PATH = GAMEASSETS_MAPS_PATH

GAMEASSETS_MODELS_PATH = os.path.abspath(
    os.environ.get('GAMEASSETS_MODELS', os.path.join(os.getcwd(), '../src/models'))
)
builtins.GAMEASSETS_MODELS_PATH = GAMEASSETS_MODELS_PATH

if __name__ == "__main__":
    print(f"Gameassets SRC = {GAMEASSETS_PATH}")
