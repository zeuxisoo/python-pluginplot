#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from os.path import abspath, dirname

try:
    from pluginpress import Plugin
except ImportError:
    import sys
    sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

    from pluginpress import Plugin

def filter_case(plugin):
    plugin.add_filter('div', lambda value: "<div>{0}</div>".format(value))
    plugin.add_filter('p', lambda value: "<p>{0}</p>".format(value))

    print("Apply Filter")
    print("==" * 25)
    print(">   div  : {0}".format(plugin.apply_filter('div', 'This is div tag message')))
    print(">    p   : {0}".format(plugin.apply_filter('p', 'This is p tag message')))
    print("> div + p : {0}".format(plugin.apply_filter('div', plugin.apply_filter('p', 'This is p tag message'))))

def action_case(plugin):
    plugin.add_action('puts', lambda value: print(value))
    plugin.add_action('sum_start_end_num', lambda start, end: print(sum(range(start, end))))

    print("Do Action")
    print("==" * 25)
    print("> puts :")
    plugin.do_action("puts", "This is a message from plugin.add_action.puts")
    print("> sum_start_end_num :")
    plugin.do_action("sum_start_end_num", 1, 100)

def main():
    plugin = Plugin()

    filter_case(plugin)
    print()
    print()
    action_case(plugin)

if __name__ == '__main__':
    main()
