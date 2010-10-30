import os

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

# colour to add the generated image with
fill = "#97799b" # this is a purple close to the ubuntu purple

# Type of image to be displayed
binary_image = False

# if true, will save all the image files generated, ie, will not overwrite
save_all = False

# sleep interval
sleep_interval = 2

#transition interval
transition_interval = 1