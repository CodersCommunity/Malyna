# -*- coding: utf-8 -*-

import requests
from lxml import html
from yapsy.IPlugin import IPlugin


class Nowosc(IPlugin):
    def execute(self, channel, username, command):
        if not command:
            page = requests.get("http://forum.miroslawzelent.pl/feed/"
                                "activity.rss")
            tree = html.fromstring(page.content)
            title = tree.xpath('//item/title/text()')
            yield username, "Najnowsze 10 tematów na forum: "
            yield username, "============================"
            for wynik in title[:10]:
                    yield username, wynik.encode("utf-8")

            yield username, "============================"
