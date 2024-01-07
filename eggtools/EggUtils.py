"""
Subprocess-based functions for utilizing common egg operations.

Warning: Modifications made using EggUtils do not sync with EggManagers; you would need to generate a new EggManager
if you decide to operate on a set of egg files.
"""

import subprocess


def make_texpaths_relative(egg):
    # -ps rel will make the texture path relative instead of absolute
    egg_trans_config = [
        "egg-trans",
        '-ps',
        'rel',
        "-o",
        egg,
        egg
    ]
    subprocess.run(egg_trans_config)


def collapse_trefs(egg):
    """
    uses egg-trans to apply texture matrices from TRefs onto UVs, then collapses identical TRefs

    when to use this:
    post-palettize;
    post-egg-texcard

    when not to use this:
    - pre-palettize; some dupe textures may exist just as a way to separate parts that have complimentary UV layouts
    """
    egg_trans_config = [
        "egg-trans",
        "-t",
        "-T",
        "-o",
        egg,
        egg
    ]
    subprocess.run(egg_trans_config)
