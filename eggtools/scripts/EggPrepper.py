"""
Prepares eggs for cooking.

Doesn't support wildcards... for now.
"""

import sys

# argparse setup
import argparse

from eggtools.utils.EggMaintenanceUtil import EggMaintenanceUtil

parser = argparse.ArgumentParser(
    prog='egg-prepper',
    epilog='Prepares eggs for cooking by removing defined UV names, '
           'converting <ObjectTypes> into their literal equivalents, and fixing TRef names.',
    description='python -m eggtools.scripts.EggPrepper input.egg -o output.egg'
)

parser.add_argument(
    'input_egg',
)

parser.add_argument(
    'other_egg_filepaths', nargs="*", action="extend", type=str,
)

args = parser.parse_args()

input_egg = args.input_egg
if not input_egg:
    print("Error: You must specify an input egg file!")
    sys.exit()

all_eggs = [input_egg]

if args.other_egg_filepaths:
    all_eggs += args.other_egg_filepaths

maintainer = EggMaintenanceUtil(file_list=all_eggs)
maintainer.eggman.remove_all_egg_materials()
maintainer.perform_general_maintenance()
