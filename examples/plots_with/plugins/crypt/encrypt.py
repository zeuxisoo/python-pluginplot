from itertools import izip, cycle
from base64 import encodestring
from pluginplot import Plot

plot = Plot()

@plot.filter()
def xor_encrypt(data, key='my my my key'):
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    return encodestring(xored).strip()
