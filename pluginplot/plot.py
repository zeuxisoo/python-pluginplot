#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Plot']

class Plot(object):

    CATEGORY_FILTER = 'filter'
    CATEGORY_ACTION = 'action'

    def __init__(self):
        self.deferred_filters = []
        self.deferred_actions = []

    def filter(self, name=None):
        def wrapper(method):
            self.add_deferred_method(self.CATEGORY_FILTER, name, method)
            return method
        return wrapper

    def action(self, name=None):
        def wrapper(method):
            self.add_deferred_method(self.CATEGORY_ACTION, name, method)
            return method
        return wrapper

    def add_deferred_method(self, category, name, method):
        if name is None:
            name = method.__name__

        if category == self.CATEGORY_FILTER:
            self.deferred_filters.append(lambda target: target.add_filter(name, method))
        elif category == self.CATEGORY_ACTION:
            self.deferred_actions.append(lambda target: target.add_action(name, method))
        else:
            raise ValueError("Can not match category when add deferred method")

    def register(self, plugin):
        for deferred_filter in self.deferred_filters:
            deferred_filter(plugin)

        for deferred_action in self.deferred_actions:
            deferred_action(plugin)
