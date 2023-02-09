# -*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
import os
import pkgutil
import pathlib
from openexp import resources
from importlib import import_module
from libopensesame import plugins  # deprecated
from libopensesame.misc import camel_case
from libopensesame.oslogging import oslogger


class Plugin:
    """An unloaded plugin or extension. This is created for each availabe
    plugin or extension. An instance of the plugin or extension is created by
    calling Plugin.build().

    Attributes defined in the __init__.py of the plugin are available through
    this class using dict syntax Plugin['icon'] and the `in` operator.
    `Plugin.attribute()` allows you to specify a default value for the
    attribute.

    Parameters
    ----------
    mod: module
        The module that contains the plugin
    """
    
    def __init__(self, mod):
        self.name = mod.__package__.split('.')[-1]
        self._mod = mod
        self._cls = None
        self.folder = os.path.dirname(mod.__file__)
            
    def __contains__(self, attr):
        return attr in self._mod.__dict__

    def __getitem__(self, attr):
        return self._mod.__dict__[attr]
        
    def attribute(self, attr, default=None):
        return self._mod.__dict__.get(attr, default)
    
    def build(self, *args, **kwargs):
        if self._cls is None:
            resources.add_resource_folder(self.folder)
            oslogger.debug(f'finding plugin runtime for {self.name}')
            mod = import_module(
                f'{self._mod.__package__}.{self.name}')
            self._cls = self._get_cls(mod)
            if not hasattr(self._cls, 'description'):
                self._cls.description = self._get_description()
        oslogger.debug(f'building plugin gui for {self.name}')
        return self._cls(*args, **kwargs)
        
    def _get_description(self):
        return self._mod.__doc__
        
    def _get_cls(self, mod):
        
        if hasattr(mod, camel_case(self.name)):
            return getattr(mod, camel_case(self.name))
        return getattr(mod, self.name)


class OldStylePlugin:
    """An adapter that maps the new plugin API onto the old API (<= 3.3). To
    maintain backwards compatibility with old plugins. This is deprecated and
    will be removed in future versions.
    """
    
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_
        self.folder = plugins.plugin_folder(name, _type=self.type_)
        
    def __getitem__(self, attr):
        return self.attribute(attr, default=None)
        
    def attribute(self, attr, default=None):
        return plugins.plugin_property(self.name, attr, default=default, 
                                       _type=self.type_)
        
    def build(self, *args, **kwargs):
        oslogger.debug(f'building old-style plugin for {self.name}')
        if self.type_ == 'plugins':
            return plugins.load_plugin(self.name, *args, **kwargs)
        return plugins.load_extension(self.name, *args, **kwargs)


class PluginManager:
    """A manager for unloaded plugins and extensions. This scans all available
    plugins from a package (`pkg`) and provides access to these as Plugin
    objects through a dict interface. `PluginManager.filter()` can be used
    to iterate only through plugins that match on specific attributes.

    Parameters
    ----------
    pkg: module
        A plugin or extension module, typically the result of
        `import opensesame_extensions` or `import opensesame_plugins
    """
    
    # These class attributes define which classes should be instantiated for
    # the plugins
    plugin_cls = Plugin
    oldstyle_plugin_cls = OldStylePlugin
    
    def __init__(self, pkg):
        self._plugins = {}
        self._pkg = pkg
        for importer, name, ispkg in pkgutil.iter_modules(
                pkg.__path__, prefix=pkg.__name__ + '.'):
            if not ispkg:
                continue
            oslogger.debug(f'found plugin package {name} in {importer.path}')
            self._discover_subpkg(name)
        self._discover_oldstyle()
                
    def _discover_subpkg(self, name):
        pkg = import_module(name)
        for importer, plugin_name, ispkg in pkgutil.iter_modules(
                pkg.__path__, prefix=name + '.'):
            if not ispkg:
                continue
            oslogger.debug(f'found plugin {plugin_name} in {importer.path}')
            self._discover_plugin(plugin_name)
            
    def _discover_plugin(self, name):
        plugin = self.plugin_cls(import_module(name))
        if plugin.name in self._plugins:
            oslogger.warning(
                f'duplicate plugin: {plugin.name} at {plugin.folder} '
                f'already found at {self._plugins[plugin.name].folder}')
            return
        self._plugins[plugin.name] = plugin
        
    def _discover_oldstyle(self):
        type_ = 'plugins' if self._pkg.__name__ == 'opensesame_plugins' \
            else 'extensions'
        for plugin_name in plugins.list_plugins(_type=type_):
            oslogger.warning(
                f'found deprecated old-style plugin {plugin_name}')
            plugin = self.oldstyle_plugin_cls(plugin_name, type_)
            if plugin.name in self._plugins:
                oslogger.warning(
                    f'duplicate plugin: {plugin.name} at {plugin.folder} '
                    f'already found at {self._plugins[plugin.name].folder}')
                continue
            self._plugins[plugin.name] = plugin
        
    def filter(self, **kwargs):
        for plugin in self:
            for key, value in kwargs.items():
                attr = plugin.attribute(
                    key, default='default' if key == 'modes' else None)
                if isinstance(attr, (list, tuple, set, dict)):
                    if value in attr:
                        yield plugin
                elif attr == value:
                    yield plugin
        
    def __contains__(self, name):
        return name in self._plugins
    
    def __getitem__(self, name):
        return self._plugins[name]
        
    def __iter__(self):
        for plugin in self._plugins.values():
            yield plugin
