import scipy, numpy, Image, ImageDraw, ImageChops, ImageEnhance, ImageOps, ImageFilter
import config

def _upscan(f):
    for i, fi in enumerate(f):
        if fi == numpy.inf: continue
        for j in xrange(1,i+1):
            x = fi+j*j
            if f[i-j] < x: break
            f[i-j] = x

def distance_transform(bitmap):
    f = numpy.where(bitmap, 0.0, numpy.inf)
    for i in xrange(f.shape[0]):
        _upscan(f[i,:])
        _upscan(f[i,::-1])
    for i in xrange(f.shape[1]):
        _upscan(f[:,i])
        _upscan(f[::-1,i])
    numpy.sqrt(f,f)
    return f

def get_overlay_image (resolution, fill):
    img2 = Image.new('RGB', resolution)
    draw = ImageDraw.Draw(img2)
    draw.rectangle(((0,0), img2.size), fill=fill, outline=fill)
    return img2

def resize(img, **kwargs):
    size = kwargs.pop('size')
    resize_mode = kwargs.pop('mode')
    return img.resize(size, resize_mode)

def add_solid(image, **kwargs):
    colour = kwargs.pop('colour')
    img2 = get_overlay_image(image.size, colour)
    return ImageChops.add (image, img2)
    
def enhance_contrast(image, **kwargs):
    contrast = kwargs.pop('contrast')
    enh = ImageEnhance.Contrast(image)
    return enh.enhance(contrast)
