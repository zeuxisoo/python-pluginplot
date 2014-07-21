#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import types
import threading
import hashlib
import uuid
import imp
import __builtin__ as builtin

__all__ = ['Plugin']

local_data = threading.local()

shared_space = types.ModuleType(__name__ + '.shared_space')
shared_space.__path__ = []
sys.modules[shared_space.__name__] = shared_space

class PluginException(Exception): pass
class FilterError(PluginException): pass
class ActionError(PluginException): pass

class Plugin(object):

    def __init__(self, folder=None, package=None):
        self.actions = {}
        self.filters = {}
        self.folder  = folder
        self.package = package

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

    def register_plots(self):
        if not self.folder:
            raise PluginException("Plugin.folder can not be None")
        else:
            self._init_plugin_files()
            self._init_with_statement()

    def register_module(self, module_name):
        module_names = module_name.split('.')
        parent_names = []

        for name in module_names:
            parent_module_name  = '.'.join(parent_names)
            current_module_name = "{0}.{1}".format(parent_module_name, name) if parent_module_name else name

            # Try to load exists module. If not exists, create it
            try:
                new_module = __import__(current_module_name, fromlist=['__name__'])
            except:
                new_module = types.ModuleType(current_module_name)
                sys.modules[new_module.__name__] = new_module

            # Assign new module object to parent module
            if parent_module_name:
                parent_module = __import__(parent_module_name, fromlist=['__name__'])
                setattr(parent_module, name, new_module)

            parent_names.append(name)

    def _init_plugin_files(self):
        for folder_path, folder_names, filenames in os.walk(self.folder):
            for filename in filenames:
                if filename.endswith('.py'):
                    # path/to/plugins/plugin/foo.py > plugin/foo.py > plugin.foo > shared_space.plugin.foo
                    full_plugin_path   = os.path.join(folder_path, filename)
                    base_plugin_path   = os.path.relpath(full_plugin_path, self.folder)
                    base_plugin_name   = os.path.splitext(base_plugin_path)[0].replace(os.path.sep, '.')
                    module_source_name = "{0}.file_{1}".format(shared_space.__name__, base_plugin_name)

                    loaded_module = imp.load_module(
                        module_source_name,
                        *imp.find_module(os.path.splitext(filename)[0], [folder_path])
                    )

                    self.register_plot(loaded_module.plot)

    def _init_with_statement(self):
        if not self.folder:
            raise PluginException("Plugin.folder can not be None")
        elif not self.package:
            raise PluginException("Plugin.package can not be None")
        else:
            self.register_module(self.package)

            # Find full plugins path
            plugins_path  = os.path.realpath(self.folder)

            # Find plugin directory and register plugin module in shared space by folder name
            for plugin in os.listdir(self.folder):
                plugin_path = os.path.join(plugins_path, plugin)
                if os.path.isdir(plugin_path):
                    plugin_module = types.ModuleType("{0}.plugin_{1}".format(shared_space.__name__, plugin))
                    plugin_module.__path__ = [plugin_path]

                    # Register [shared_space].[plugin] to system module
                    # set [shared_space].[plugin] property
                    # set [package].[plugin] property support (from [package] import [plugin]) syntax
                    sys.modules[plugin_module.__name__] = plugin_module
                    setattr(shared_space, plugin, plugin_module)
                    setattr(__import__(self.package, fromlist=['__name__']), plugin, plugin_module)

    def _redirect_import_name(self, module_name):
        # Redirect [package].[plugin] to [shared_space].[plugin]
        # And support (from [package].[plugin] import [method])
        if module_name.startswith(self.package + '.'):
            pieces = module_name.split('.')
            return shared_space.__name__ + '.plugin_' + '.'.join(pieces[self.package.count('.') + 1:])
        else:
            return None

    def __enter__(self):
        local_data.plugin_stacks = [self]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            local_data.plugin_stacks.pop()
        except:
            pass

def override_import(import_method):
    def wrapper(name, globals=None, locals=None, fromlist=None, level=0):
        # Try to get current plugin object
        try:
            plugin_object = local_data.plugin_stacks[-1]
        except (AttributeError, IndexError):
            plugin_object = None

        # Try to correct the package name from plugin object
        if plugin_object:
            redirected_import_name = plugin_object._redirect_import_name(name)
        else:
            redirected_import_name = None

        if redirected_import_name:
            name = redirected_import_name

        return import_method(name, globals, locals, fromlist, level)
    return wrapper

builtin.__import__ = override_import(builtin.__import__)
