"""
Sample code for applying custom attributes to EGG files.
"""
import os
from panda3d.core import *
from panda3d.egg import *
from eggtools.EggMan import EggMan, EggContext

# We will use our lovely Spot model as a demo
modelName = "test_spot"

# Spot is compressed with pzip since he's a tad bulky.
ext = "egg.pz"

# Import egg file
if not os.path.isfile(f'tests/models/{modelName}.{ext}'):
    testEgg = Filename.fromOsSpecific(f'{modelName}.{ext}')
else:
    testEgg = Filename.fromOsSpecific(os.path.join(os.getcwd(), f'tests/models/{modelName}.{ext}'))

# If you fail here, just adjust the paths accordingly.
assert testEgg

# Generate the egg manager for this model.
eggman = EggMan(egg_filepaths=[testEgg])

# Get our Spot model from the manager.
egg = eggman.get_egg_by_filename(f"{modelName}.{ext}")  # type: EggData
ctx = eggman.egg_datas[egg]  # type: EggContext

# Our model only has a single node, "spot_geom". Let's mess around and see what we can do with it.

# Let's define some custom EGG attribute configs:
from eggtools.attributes.EggUVScrollAttribute import EggUVScrollAttribute
from eggtools.attributes import EggBillboard

customAttributes = {
    # Instantiate the Attribute object here...
    EggUVScrollAttribute(u_speed=1, v_speed=0, w_speed=0, r_speed=0): [
        # And define node names to be affected by the attribute here.
        "spot_geom"
    ],
    EggBillboard("axis"): [
        # Same geom name, but if your model has other node names, they can be placed here.
        "spot_geom"
    ]
}

# And apply our attributes. Feel free to uncomment this and re-run the program to see how the model changes.
eggman.apply_attributes(egg, customAttributes)

from direct.showbase.ShowBase import ShowBase


class MyEggScene(ShowBase):
    """
    Test Scene

    Rather than re-exporting our modified EGG file, we can just preview our changes made to it here.
    """

    def __init__(self):
        # Setup ShowBase
        super().__init__(self)
        eggModel = loadEggData(egg)  # type: PandaNode
        eggNode = NodePath(eggModel)
        # Make our beautiful model visible for all to see!
        eggNode.reparentTo(render)

        # Hack: Texture path is in a weird state, so we will try to find it a different way.
        spotTex = loader.loadTexture("tests/maps/spot_texture.png", okMissing=True)
        if spotTex:
            eggNode.setTexture(spotTex, 1)

        # See our attributes applied in the scene graph!
        render.ls()
        # Freecam
        base.oobe()
        # Ignore obstructive camera model
        base.camera.hide()

        # Start the show!
        base.run()


# Run the Scene program so that we can see our visual changes applied to the model.
MyEggScene()

# If instead we want to save our changes out to disk, we can do the following:
# eggman.write_all_eggs_manually()
# Note: May override any pre-existing egg files with the same name.
