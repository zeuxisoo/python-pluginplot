from base64 import b64encode
from pluginplot import Plot

plot = Plot()

@plot.filter('encode')
def encode(value):
    return b64encode(value)
