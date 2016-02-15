# -*- coding: utf-8 -*-
from lmgtfy import lmgtfy
from yapsy.IPlugin import IPlugin


class Gogluj(IPlugin):
    def execute(self, channel, username, command):
        googler = lmgtfy.Lmgtfy()

        if not command:
            yield channel, ("Syntax: >gogluj zapytanie")

        else:
            try:
                address = str(googler.short_url([command]))

                yield channel, (address + " Jakie to było proste"
                                          ", nie?")
            except ValueError:
                yield channel, ("https://www.google.pl/#q="
                                + command.replace(" ", "+"))
