# -*- coding: utf-8 -*-

from yapsy.IPlugin import IPlugin


class Wklej(IPlugin):
    def execute(self, channel, username, command):
        if not command:
            yield channel, ("Nie bądź noobem i wklej na: "
                            "https://gist.github.com/")
