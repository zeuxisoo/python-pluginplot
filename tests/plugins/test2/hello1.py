# -*- coding: utf-8 -*-

from pluginplot import Plot

plot = Plot()

@plot.filter('plugin_test2_hello1')
def plugin_test2_hello1(value):
    return "{0} | plugin_test2_hello1".format(value)
