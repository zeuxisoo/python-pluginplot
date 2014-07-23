#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pluginplot import Plugin, Plot

plugin = Plugin(folder='plugins', package='hi.plugins')
plugin.register_plots()

with plugin:
    from hi.plugins.crypt import encrypt, decrypt
    from hi.plugins.tags.address import html_address
    from hi.plugins.tags.strong import html_strong

    data    = 'This is a test data'
    data_en = encrypt.xor_encrypt(data)
    data_de = decrypt.xor_decrypt(data_en)

    print("The Data   : {0}".format(data))
    print("Encrypt    : {0}".format(data_en))
    print("Decrypt    : {0}".format(data_de))
    print("TagAddress : {0}".format(html_address(data)))
    print("TagStrong  : {0}".format(html_strong(data)))
