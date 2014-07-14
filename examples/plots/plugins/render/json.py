from __future__ import absolute_import
from json import dumps
from pluginplot import Plot

plot = Plot()

@plot.action('out_json')
def out_json(results):
    print("JSON action:")
    print(dumps(results))
