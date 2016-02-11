# -*- coding: utf-8 -*-

import string
from datetime import datetime, timedelta
from collections import defaultdict
from lmgtfy import lmgtfy
import requests
from lxml import html


class BotInteraction():

    def __init__(self, config):
        self.end = datetime.now() + timedelta(seconds=10)
        self.timeflood = defaultdict(lambda: 0)
        self.googler = lmgtfy.Lmgtfy()
        self.channel = config['channel']
        self.nickname = config['nickname']
        self.prompt = config['prompt']
        self.parts = ""
        self.ping = ""
        self.username = ""
        self.message = ""

    def handle_line(self, username, message, parts):
        print(username + ": " + message)

        if self.nickname not in parts[1]:

            if self.end > datetime.now():
                self.timeflood[username] += 1
                if (self.timeflood[username] >= 4 and username != self.nickname
                        and "freenode.net" not in username):

                    yield(self.channel, "Wyczuwam drobny spam, " + username)
                    self.timeflood[username] = 0

            # Interaction user-Malyba
            if message == "ziew":
                yield self.channel, "powiało ziewem :/"

            if message == self.prompt + "nowosc":
                page = requests.get("http://forum.miroslawzelent.pl/feed/"
                                    "activity.rss")
                tree = html.fromstring(page.content)
                title = tree.xpath('//item/title/text()')
                yield username, "Najnowsze 10 tematów na forum: "
                yield username, "============================"

                for wynik in title[:10]:
                    yield username, wynik.encode("utf-8")

                yield username, "============================"

            if message == self.prompt + "botinfo":
                yield(self.channel, "Bot został stworzony w "
                      "celu ułatwienie pracy na IRC. Wpisz help aby "
                      "uzyskać informację o dostępnych komendach")

            if message == self.prompt + "help":
                yield self.channel, "gogluj [q], linki, wklej, nowosc, botinfo"

            if message == self.prompt + "wklej":
                yield self.channel, ("Nie bądź noobem i wklej na: "
                                     "https://gist.github.com/")

            #wypisuje tylko jedna wiadomosc
            if message == self.prompt + "linki":
                yield self.channel, ("\001ACTION Wysyłam zbiór1 linków do " +
                                     username + "\001")
                yield username, "składnia: [polecenie]"
                yield username, "=========polecenia========="
                yield username, "fontello, inspiracja, spoj"
                yield username, "==========================="

            if message == self.prompt + "linki[fontello]":
                yield self.channel, ("http://forum.miroslawzelent.pl/104219/"
                                     "fontello-wszystko-co-powiniene-wiedziec")

            if message == self.prompt + "linki[inspiracja]":
                yield self.channel, ("http://forum.miroslawzelent.pl/652/"
                                     "inspirujace-warte-zobaczenia-kanaly"
                                     "-na-youtube")

            if message == self.prompt + "linki[spoj]":
                yield self.channel, ("http://forum.miroslawzelent.pl/90416"
                                     "/spoj-zasady-umieszczania-"
                                     "postow?show=90416#q90416")

            if self.prompt + "gogluj " in message[:8]:
                try:
                    address = str(self.googler.short_url([message[8:]]))

                    yield self.channel, (address + " Jakie to było proste"
                                                   ", nie?")
                except ValueError:
                    yield self.channel, ("https://www.google.pl/#q="
                                         + message[8:].replace(" ", "+"))
                    #Send_message("OH, SHIT. Dżejson wysiadł")

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

    def check_timefloodtime(self):
        if datetime.now() >= self.end:
            self.timeflood.clear()
            self.end = datetime.now() + timedelta(seconds=10)
