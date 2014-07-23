from itertools import izip, cycle
from base64 import decodestring
from pluginplot import Plot

plot = Plot()

@plot.filter()
def xor_decrypt(data, key='my my my key'):
    data  = decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    return xored
