from pluginplot import Plot

plot = Plot()

@plot.action('out_html')
def out_html(encoded, decoded):
    print("HTML action:")
    print("Encoded: <strong>{0}</strong>".format(encoded))
    print("Decoded: <strong>{0}</strong>".format(decoded))
