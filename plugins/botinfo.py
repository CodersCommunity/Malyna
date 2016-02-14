# -*- coding: utf-8 -*-

from yapsy.IPlugin import IPlugin


class BotInfo(IPlugin):
    def execute(self, channel, username, command):
        if not command:
            yield channel, ("Bot został stworzony w "
                            "celu ułatwienie pracy na IRC. Wpisz help aby "
                            "uzyskać informację o dostępnych komendach")
