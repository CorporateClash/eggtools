"""
Use this to check for models with non-empty UVMap names (known to cause issues)
"""

from panda3d.core import Filename
import os
import sys
from eggtools.EggMan import EggMan

# argparse setup
import argparse

from eggtools.attributes.EggUVNameAttribute import EggUVNameAttribute

parser = argparse.ArgumentParser(
    prog='egg-uv-remover',
    epilog='Removes UV names off a given egg file.',
    description='python -m eggtools.scripts.UVNameRemover input.egg -o output.egg'
)

parser.add_argument(
    'input_egg',
)

parser.add_argument(
    '-o',
    '--output',
    # '-->',
    type=str,
    nargs='?',
    help='Output egg filename.',
)
parser.add_argument(
    '--inplace',
    type=bool,
    default=False,
    help='If this option is given, the input egg files will be rewritten in place with the results.',
)
args = parser.parse_args()
input_loc = args.input_egg
if not input_loc:
    print("Error: You must specify an input egg file!")
    sys.exit()

input_egg = Filename.fromOsSpecific(input_loc)

output_loc = args.output
if not args.output and args.inplace:
    output_loc = os.path.join(os.getcwd(), args.input_egg)
if not output_loc:
    print("Error: You must either specify an output filepath with -o or use --inplace.")
    sys.exit()
output_file = Filename.fromOsSpecific(os.path.join(os.getcwd(), output_loc))

eggman = EggMan([input_egg])
eggdata = eggman.get_egg_by_filename(input_egg)
ctx = eggman.egg_datas[eggdata]
for eggattr in ctx.egg_attributes:
    if isinstance(eggattr, EggUVNameAttribute):
        print(f"Removing {eggattr} from {ctx.filename}")
        eggattr.apply(eggdata, ctx)
        ctx.dirty = True
if not ctx.dirty:
    print(f"Couldn't find a UVNameAttribute from {ctx.filename}, not doing anything.")

eggman.write_egg(eggdata, output_file)
