# -*- coding: utf-8 -*-

from pluginplot import Plot

plot = Plot()

@plot.filter('plugin_test2_hello2')
def plugin_test2_hello2(value):
    return "{0} | plugin_test2_hello2".format(value)
