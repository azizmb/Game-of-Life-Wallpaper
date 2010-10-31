import scipy, Image, ImageDraw, ImageChops, ImageEnhance, ImageOps, ImageFilter
import config
from distance import distance_transform
    

def get_overlay_image (resolution):
    img2 = Image.new('RGB', resolution)
    draw = ImageDraw.Draw(img2)
    draw.rectangle(((0,0), img2.size), fill=config.fill, outline=config.fill)
    return img2


def generate_image (array, resolution):
    if config.binary_image:
        scale_mode = Image.NEAREST
    else:
        array = distance_transform(array)
        scale_mode = Image.ANTIALIAS
        
    img = scipy.misc.toimage(array)
    img = img.convert("RGB")
    
    img2 = get_overlay_image(resolution)
    
    img = ImageOps.autocontrast(img)
    img = ImageChops.add (img, img2)
    img = img.resize(resolution, scale_mode)
    return img
