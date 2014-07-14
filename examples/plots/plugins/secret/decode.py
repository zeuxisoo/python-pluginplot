from base64 import b64decode
from pluginplot import Plot

plot = Plot()

@plot.filter('decode')
def decode(value):
    return b64decode(value)
