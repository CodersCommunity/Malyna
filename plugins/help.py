# -*- coding: utf-8 -*-
from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin


class Help(IPlugin):
    def execute(self, channel, username, command):
        manager = PluginManager()
        manager.setPluginPlaces(["plugins"])
        manager.collectPlugins()
        plugins = []

        if command:
            description = manager.getPluginByName(command).description
            yield channel, (description)

        else:
            for plugin in manager.getAllPlugins():
                plugins.append(plugin.name)
            yield channel, (', '.join(plugins))
