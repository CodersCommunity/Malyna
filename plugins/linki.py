# -*- coding: utf-8 -*-

from yapsy.IPlugin import IPlugin


class Linki(IPlugin):
    def execute(self, channel, username, command):
        if not command:
            yield channel, ("\001ACTION Wysyłam zbiór1 linków do " +
                            username + "\001")
            yield username, "składnia: [polecenie]"
            yield username, "=========polecenia========="
            yield username, "fontello, inspiracja, spoj"
            yield username, "==========================="

        if command == "fontello":
            yield channel, ("http://forum.miroslawzelent.pl/104219/"
                            "fontello-wszystko-co-powiniene-wiedziec")

        if command == "inspiracja":
            yield channel, ("http://forum.miroslawzelent.pl/652/"
                            "inspirujace-warte-zobaczenia-kanaly"
                            "-na-youtube")

        if command == "spoj":
            yield channel, ("http://forum.miroslawzelent.pl/90416"
                            "/spoj-zasady-umieszczania-"
                            "postow?show=90416#q90416")
