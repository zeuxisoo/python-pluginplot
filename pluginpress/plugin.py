#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Plugin']

class PluginException(Exception): pass
class FilterError(PluginException): pass
class ActionError(PluginException): pass

class Plugin(object):

    def __init__(self):
        self.actions = {}
        self.filters = {}

    def add_filter(self, name, method):
        self.filters[name] = method

    def add_action(self, name, method):
        self.actions[name] = method

    def apply_filter(self, name, *args, **kwargs):
        filter_ = self.filters.get(name)

        if not filter_:
            raise FilterError("Not found filter named: {0}".format(name))
        else:
            return filter_(*args, **kwargs)

    def do_action(self, name, *args, **kwargs):
        action = self.actions.get(name)

        if not action:
            raise ActionError("Not found action named: {0}".format(name))
        else:
            action(*args, **kwargs)
