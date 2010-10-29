import numpy

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