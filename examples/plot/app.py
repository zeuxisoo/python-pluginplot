#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pluginplot import Plugin
from plugin import secret

def main():
    plugin = Plugin()
    plugin.register_plot(secret.plot)

    content = "This is test message"
    encoded = plugin.apply_filter('encode_content', content)
    decoded = plugin.apply_filter('decode_content', encoded)

    plugin.do_action('render_result', {
        'encoded': encoded,
        'decoded': decoded
    })

if __name__ == '__main__':
    main()
