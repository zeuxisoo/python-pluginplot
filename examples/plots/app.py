#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import abspath
from pluginplot import Plugin

def main():
    plugin = Plugin(folder=abspath('plugins'))
    plugin.register_plots()

    content = "This is test message"
    encoded = plugin.apply_filter('encode', content)
    decoded = plugin.apply_filter('decode', encoded)

    plugin.do_action('out_html', encoded, decoded)
    plugin.do_action('out_json', {
        'encoded': encoded,
        'decoded': decoded
    })

if __name__ == '__main__':
    main()
