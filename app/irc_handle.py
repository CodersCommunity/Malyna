# -*- coding: utf-8 -*-

"""
IRC #MZForum bot.
BOT is designed to help users chat available its functionality.
"""
import socket
import time


class IrcHandle():

    def __init__(self, config):
        self.irc_socket = socket.socket(socket.AF_INET,
                                        socket.SOCK_STREAM)
        self.irc_connect(config['server'], config['port'])
        self.irc_login(config['nickname'])
        self.irc_join(config['channel'])

    def send_data(self, command):
        self.irc_socket.send(command + '\n')

    def irc_join(self, channel):
        self.send_data("JOIN %s" % channel)

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
