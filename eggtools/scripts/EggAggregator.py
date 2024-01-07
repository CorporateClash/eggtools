"""
Usage:
egg-aggregate <base file> [eggs to aggregate into base] -o <output file>

"""
import argparse
import os

from panda3d.core import Filename

from eggtools.EggMan import EggMan

parser = argparse.ArgumentParser(
    prog='egg-aggregate',
    epilog='Aggregates egg files into one.',
    description='egg-aggregate input.egg [eggs to aggregate into input] -o output.egg'
)
parser.add_argument(
    'input_egg',
)

parser.add_argument(
    'other_egg_filepaths', nargs="+", action="extend", type=str,
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
    type=str,
    nargs='?',
    help='If this option is given, the input egg files will be rewritten in place with the results.',
)


args = parser.parse_args()
print(args)
print(args.output)

print(f"{args.input_egg} | {args.other_egg_filepaths}")

input_egg = Filename.fromOsSpecific(os.path.join(os.getcwd(), args.input_egg))
other_eggs = args.other_egg_filepaths
all_eggs = other_eggs.insert(0, input_egg)

eggman = EggMan(all_eggs)
_src_egg = eggman.get_egg_by_filename(input_egg)
print(_src_egg.getName())
