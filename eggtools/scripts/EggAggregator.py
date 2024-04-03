"""
Usage:
egg-aggregate <base file> [eggs to aggregate into base] -o <output file>

"""
import argparse
import copy
import os
import sys

from panda3d.core import Filename

from eggtools.EggMan import EggMan

parser = argparse.ArgumentParser(
    prog='egg-aggregate',
    epilog='Aggregates egg files into one.',
    description='python -m eggtools.scripts.EggAggregator input.egg [eggs to aggregate into input] -o output.egg'
)
parser.add_argument(
    'input_egg',
)

parser.add_argument(
    'other_egg_filepaths', nargs="+", action="extend",
)

parser.add_argument(
    '-o',
    '--output',
    type=str,
    nargs='?',
    help='Output egg filename.',
)
parser.add_argument(
    '--inplace',
    # type=str,
    default=False,
    action='store_true',
    # nargs='?',
    help='If this option is given, the input egg files will be rewritten in place with the results.',
)

args = parser.parse_args()
input_loc = args.input_egg
if not input_loc:
    print("Error: You must specify an input egg file!")
    sys.exit()

if not args.other_egg_filepaths:
    print("Error: You must specify at least one other egg file to aggregate!")

input_egg = Filename.fromOsSpecific(input_loc)

output_loc = args.output
if not args.output and args.inplace:
    output_loc = os.path.join(os.getcwd(), args.input_egg)
if not output_loc:
    print("Error: You must either specify an output filepath with -o or use --inplace.")
    sys.exit()
output_file = Filename.fromOsSpecific(os.path.join(os.getcwd(), output_loc))

other_eggs = args.other_egg_filepaths
all_eggs = copy.deepcopy(other_eggs)
all_eggs.insert(0, input_egg)
eggman = EggMan(all_eggs)

other_egg_datas = []
for egg_name in other_eggs:
    other_egg_datas.append(eggman.get_egg_by_filename(egg_name))

_src_egg = eggman.get_egg_by_filename(input_egg)
eggman.merge_eggs(_src_egg, other_egg_datas)

eggman.write_egg(_src_egg, output_file)
print(f"Aggregated {len(other_egg_datas) + 1} egg files to {output_file.toOsSpecific()}")
