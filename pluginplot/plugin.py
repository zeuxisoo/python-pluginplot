#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import imp

__all__ = ['Plugin']

class PluginException(Exception): pass
class FilterError(PluginException): pass
class ActionError(PluginException): pass

class Plugin(object):

    def __init__(self, folder = None):
        self.actions = {}
        self.filters = {}
        self.folder  = folder

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

    def register_plot(self, plot):
        plot.register(self)

    def register_plots(self, module_name="pluginplot.plugins"):
        if not self.folder:
            raise PluginException("Plugin.folder can not be None")
        else:
            # Register base module
            self.register_module(module_name)

            for folder_path, folder_names, filenames in os.walk(self.folder):
                # Register plot module under base module
                # - when folder set to path/to/plots
                # - like path/to/plots/bar > module_name.bar
                for folder_name in folder_names:
                    self.register_module("{0}.{1}".format(module_name, folder_name))

                # Load each plot file
                # - like path/to/plots/bar/foo.py > module_name.bar.foo
                for filename in filenames:
                    if filename.endswith('.py'):
                        # path/to/plots/bar/foo.py > bar/foo.py > bar.foo > module_name.bar.foo
                        full_plot_path   = os.path.join(folder_path, filename)
                        base_plot_path   = os.path.relpath(full_plot_path, self.folder)
                        base_plot_name   = os.path.splitext(base_plot_path)[0].replace(os.path.sep, '.')
                        module_source_name = "{0}.{1}".format(module_name, base_plot_name)

                        loaded_module = imp.load_module(
                            module_source_name,
                            *imp.find_module(os.path.splitext(filename)[0], [folder_path])
                        )

                        self.register_plot(loaded_module.plot)

    def register_module(self, name):
        sys.modules[name] = imp.new_module(name)
