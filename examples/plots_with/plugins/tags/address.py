from pluginplot import Plot

plot = Plot()

@plot.filter()
def html_address(value):
    return "<address>{0}</address>".format(value)
