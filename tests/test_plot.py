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

class TestPlot(unittest.TestCase):

    def setUp(self):
        self.plot = Plot()

    def test_filter(self):
        @self.plot.filter('strong')
        def strong(value):
            return "<strong>{0}</strong>".format(value)

        @self.plot.filter()
        def address(value):
            return "<address>{0}</address>".format(value)

        self.assertNotEquals(self.plot.deferred_filters, [])
        self.assertEquals(len(self.plot.deferred_filters), 2)

    def test_action(self):
        @self.plot.action('puts')
        def puts(value):
            print(value)

        @self.plot.action()
        def pp(value):
            print("<p>{0}</p>".format(value))

        self.assertNotEquals(self.plot.deferred_actions, [])
        self.assertEquals(len(self.plot.deferred_actions), 2)

    def test_add_deferred_method(self):
        self.plot.add_deferred_method(self.plot.CATEGORY_FILTER, 'address', lambda value: "<address>{0}</address>".format(value))
        self.plot.add_deferred_method(self.plot.CATEGORY_FILTER, 'div', lambda value: "<div>{0}</div>".format(value))
        self.plot.add_deferred_method(self.plot.CATEGORY_ACTION, 'sumrange', lambda a, b: print(sum(range(a, b))))

        self.assertNotEquals(self.plot.deferred_filters, [])
        self.assertNotEquals(self.plot.deferred_actions, [])
        self.assertEquals(len(self.plot.deferred_filters), 2)
        self.assertEquals(len(self.plot.deferred_actions), 1)

    def test_register(self):
        @self.plot.filter('strong')
        def strong(value):
            return "<strong>{0}</strong>".format(value)

        @self.plot.action('puts')
        def puts(value):
            print(value)

        @self.plot.filter()
        def strong_without_name(value):
            return "<strong>{0}</strong>".format(value)

        @self.plot.action()
        def puts_without_name(value):
            print(value)

        plugin = Plugin()
        self.plot.register(plugin)

        self.assertNotEquals(plugin.filters.get('strong'), None)
        self.assertNotEquals(plugin.filters.get('strong_without_name'), None)
        self.assertNotEquals(plugin.actions.get('puts'), None)
        self.assertNotEquals(plugin.actions.get('puts_without_name'), None)

        with captured_output() as (out, err):
            self.assertEquals(plugin.apply_filter('strong', 'message'), '<strong>message</strong>')

            plugin.do_action('puts', 'hello world')

            self.assertEquals(out.getvalue().strip(), 'hello world')


