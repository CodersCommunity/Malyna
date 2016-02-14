# -*- coding: utf-8 -*-

import string
from yapsy.PluginManager import PluginManager


class BotInteraction():

    def __init__(self, config):
        self.channel = config['channel']
        self.nickname = config['nickname']
        self.prompt = config['prompt']
        self.parts = ""
        self.ping = ""
        self.username = ""
        self.message = ""
        self.manager = PluginManager()
        self.manager.setPluginPlaces(["plugins"])
        self.manager.collectPlugins()

    def handle_line(self, username, message, parts):
        print(username + ": " + message)

        if self.nickname not in parts[1] and message[0:1] == self.prompt:

            message = message.replace(">", " ").split(None, 1)
            for plugin in self.manager.getAllPlugins():  # Collect all plugins
                try:
                    # Message[0] - search plugin_name
                    plugin_yapsy = self.manager.getPluginByName(message[0])
                    command = []

                    # If the message has arguments - message[1] add to command
                    if len(message) == 2:
                        command = message[1]

                    # To found plugin send arguments.
                    return plugin_yapsy.plugin_object.execute(self.channel,
                                                              username,
                                                              command)
                except:
                    continue

    def check_ping(self, line):
        if line.find("PING") != -1:  # If server pings then pong
            line = string.split(line, " ")
            self.ping = "PONG " + line[1]

        else:
            self.ping = ""
            self.parts = string.split(line, ":")

            if "QUIT" not in self.parts[1] and \
               "JOIN" not in self.parts[1] and \
               "PART" not in self.parts[1]:

                try:
                    # Sets the message variable to the actual message sent
                    self.message = self.parts[2][:len(self.parts[2]) - 1]
                except:
                    self.message = ""
                # Sets the username variable to the actual username
                usernamesplit = string.split(self.parts[1], "!")
                self.username = usernamesplit[0]
