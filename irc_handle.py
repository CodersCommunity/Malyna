# -*- coding: utf-8 -*-

"""
IRC #MZForum bot.
BOT is designed to help users chat available its functionality.
"""

import yaml
import socket
from bot_interaction import BotInteraction
import time
import string


class IrcHandle():

    def __init__(self):
        self.irc_socket = socket.socket(socket.AF_INET,
                                        socket.SOCK_STREAM)
        config = yaml.load(open("config.yaml"))
        server = config["server"]
        port = config["port"]
        self.channel = config["channel"]
        self.nickname = config["nickname"]
        self.prompt = config["prompt"]

        self.modt = False
        self.irc_connect(server, port)
        self.irc_login(self.nickname)
        self.irc_join()

    def send_data(self, command):
        self.irc_socket.send(command + '\n')

    def irc_join(self):
        self.send_data("JOIN %s" % self.channel)

    def irc_login(self, nickname, username="username",
                  password=None, realname="realname",
                  hostname="hostname", servername="servername"):
        self.send_data("USER %s %s %s %s" % (username,
                                             hostname,
                                             servername,
                                             realname))
        self.send_data("NICK " + nickname)

    def irc_connect(self, server, port):
        self.irc_socket.connect((server, port))

    def send_message(self, return_message):
        channel = ""
        message = ""

        for channel, message in return_message:
            self.irc_socket.send("PRIVMSG " + channel + " :" +
                                 message + "\r\n")
            time.sleep(0.4)

    def send_ping(self, ping):
        self.irc_socket.send(ping + "\r\n")
        print(ping)


def main():
    handle = IrcHandle()
    interaction = BotInteraction(handle.channel,
                                 handle.nickname,
                                 handle.prompt)

    read_buffer = ""
    while True:  # While Connection is Active
        read_buffer = read_buffer + handle.irc_socket.recv(1024)
        temp = string.split(read_buffer, "\n")
        read_buffer = temp.pop()

        interaction.check_timefloodtime()

        for line in temp:
            interaction.check_ping(line)
            return_message = interaction.handle_line(interaction.username,
                                                     interaction.message,
                                                     interaction.parts)
            if interaction.ping:
                handle.send_ping(interaction.ping)
            else:
                handle.send_message(return_message)

if __name__ == "__main__":
    main()
