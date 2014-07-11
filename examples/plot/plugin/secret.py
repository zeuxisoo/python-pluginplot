#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64encode, b64decode
from pluginplot import Plot

plot = Plot()

@plot.filter('encode_content')
def encode_content(content):
    return b64encode(content)

@plot.filter('decode_content')
def decode_content(content):
    return b64decode(content)

@plot.action('render_result')
def render_result(results):
    print results
    print("\n".join([
        "Encode:\n> {0}".format(results.get('encoded')),
        "Decode:\n> {0}".format(results.get('decoded'))
    ]))
