#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import unittest
from contextlib import contextmanager
from StringIO import StringIO
from pluginplot import Plugin, Plot

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin()

    def test_add_filter(self):
        def strong(value):
            return "<strong>{0}</strong>".format(value)

        self.plugin.add_filter(name='strong', method=strong)

        self.assertEquals(self.plugin.filters['strong'], strong)

    def test_apply_filter(self):
        strong  = lambda value: "<strong>{0}</strong>".format(value)
        address = lambda value: "<address>{0}</address>".format(value)

        self.plugin.add_filter(name='strong', method=strong)
        self.plugin.add_filter(name='address', method=address)

        self.assertEquals(self.plugin.apply_filter('strong', 'strong method'), strong('strong method'))
        self.assertEquals(self.plugin.apply_filter('strong', 'strong method'), '<strong>strong method</strong>')

        mixed_result = self.plugin.apply_filter('address', self.plugin.apply_filter('strong', 'strong + address method'))

        self.assertEquals(mixed_result, address(strong('strong + address method')))
        self.assertEquals(mixed_result, '<address><strong>strong + address method</strong></address>')

    def test_add_action(self):
        def puts(value):
            print(value)

        self.plugin.add_action(name='puts', method=puts)

        self.assertEquals(self.plugin.actions['puts'], puts)

    def test_do_action(self):
        def puts(value):
            print(value)

        self.plugin.add_action(name='puts', method=puts)

        with captured_output() as (out, err):
            self.plugin.do_action('puts', 'put method')
            self.assertEquals(out.getvalue().strip(), 'put method')

    def test_register_plot(self):
        plot = Plot()

        @plot.filter('strong')
        def strong(value):
            return "<strong>{0}</strong>".format(value)

        @plot.action('puts')
        def puts(value):
            print(value)

        self.plugin.register_plot(plot)

        with captured_output() as (out, err):
            self.assertNotEquals(self.plugin.filters, {})
            self.assertNotEquals(self.plugin.actions, {})

            self.assertEquals(self.plugin.apply_filter('strong', 'strong method'), '<strong>strong method</strong>')

            self.plugin.do_action('puts', 'puts method')
            self.assertEquals(out.getvalue().strip(), 'puts method')
