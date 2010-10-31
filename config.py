import os
import ip
import Image

# specify directory name so that remaning paths can be relative
basedir = os.path.abspath(os.path.dirname(__file__))
expandpath = lambda path: os.path.join(basedir, path)

# file to read initial cell configuration
life = expandpath("patterns/achimsp144_106.lif")

# screen resolution
resolution = (1260, 800)

# board size
rows = 25
cols = 40

# directory to store the wallpaper image
directory = expandpath("demos")

# number of cycles after which image is saved
sample_rate = 1

# number of iterations to perform 
steps = 144

# sleep interval
sleep_interval = 2

# transition interval
transition_interval = 1


### ADVANCED ###
# Bellow are the hooks to further customise the image generation.
# Format for specifying functions: ((func1, argumentDict1), (func2, argumentDict2))

# Functions that will manipulate the array before generating the image.
# Currently available are: 
# ip.distance_transform : this performs a eucledean distance transform over the matrix
array_manipulators = (
    # Commenting this will give you binary images
    (ip.distance_transform, {}),
)

# Functions that will manipulate the image generated from the array.
# Currently available functions are:
# ip.add_solid : Performs addition of the generated image with the solid colour specified
#                as an argument.
# ip.enhance_contrast : Implementation ImageEnhance modules contrast function
# ImageOps.autocontrast : Implementation of colour from ImageEnhance module
image_manipulators = (
    # its a good idea not to omit the convert and resize functions unless you are writing
    # your own 
    (Image.Image.convert, {'mode':'RGB'}),
    (ip.enhance_contrast, {'contrast': 5}),	
    (ip.resize, {'size':resolution, 'mode':Image.ANTIALIAS}),
    (ip.add_solid, {'colour': "#97799b"}),
)
