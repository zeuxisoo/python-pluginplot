from pluginplot import Plot

plot = Plot()

@plot.filter()
def html_strong(value):
    return "<strong>{0}</strong>".format(value)
