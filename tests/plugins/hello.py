# -*- coding: utf-8 -*-

from pluginplot import Plot

plot = Plot()

@plot.filter('plugin_hello')
def plugin_hello(value):
    return "{0} | plugin_hello".format(value)
