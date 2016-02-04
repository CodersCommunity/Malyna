# -*- coding: utf-8 -*-
import sys
import socket
import string
from datetime import datetime, timedelta
import time
from collections import defaultdict
from lmgtfy import lmgtfy
from lxml import html
import requests 

server = "chat.freenode.net"
port = 6667
nickname = "Malynka"
channel = "#kurdensens"
prompt = ">"
googler = lmgtfy.Lmgtfy()
MODT = False

#open a socket to handle the connection
irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#open a connection with the server
def irc_conn():
    irc_socket.connect((server, port))

#simple function to send data through the socket
def send_data(command):
    irc_socket.send(command + "\n")

#join the channel
def join(channel):
    send_data("JOIN %s" % channel)

#send login data (customizable)
def login(nickname, username='username', password = None, realname="realname", hostname="hostname", servername="servername"):
    send_data("USER %s %s %s %s" % (username, hostname, servername, realname))
    send_data("NICK " + nickname)

def send_message(message):
    irc_socket.send("PRIVMSG "+channel+" :" + message + "\r\n")


irc_conn()
login(nickname)
join(channel)
readbuffer = ""
end = datetime.now() + timedelta(seconds=10)
timeflood = defaultdict(lambda: 0)

while True: #While Connection is Active
    readbuffer = readbuffer + irc_socket.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()
    
    now = datetime.now()
    if now >= end:
        timeflood.clear()
        end = datetime.now() + timedelta(seconds=10)
 
    for line in temp:

        if line.find("PING") !=-1: #If server pings then pong
            line=string.split(line," ")
            irc_socket.send("PONG "+line[1]+"\r\n")
            print "PONG "+line[1]+"\r\n"
       
        else:
            parts = string.split(line, ":")
 
            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    # Sets the message variable to the actual message sent
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""
                # Sets the username variable to the actual username
                usernamesplit = string.split(parts[1], "!")
                username = usernamesplit[0]

               
                if MODT:
                    print username + ": " + message

                    if nickname in parts[1]:
                        break

                    if end > now:
                        timeflood[username] += 1

                        if timeflood[username] >= 4 and username != nickname:
                            send_message("Nie rob spamu, " + username + " bo bedzie kick!")
                            timeflood[username] = 0
                

                    #Interaction user-malyna
                    if 'haslo12345 ' in message:
                        send_message("" + message[11:])

                    if message == "ziew":
                        send_message("powiało ziewiem ;/")

                    if message == prompt + "nowosc":
                        page = requests.get('http://forum.miroslawzelent.pl/feed/activity.rss')
                        tree = html.fromstring(page.content)
                        title = tree.xpath('//item/title/text()')
                        irc_socket.send("PRIVMSG "+username+" :Najnowsze 10 tematów na forum:\r\n")
                        irc_socket.send("PRIVMSG "+username+" :==========================\r\n")
                        for wynik in title[:10]:
                            time.sleep(0.4)
                            irc_socket.send("PRIVMSG "+username+" :"+wynik.encode("utf-8")+"\r\n ")
                        irc_socket.send("PRIVMSG "+username+" :==========================\r\n")

                    if message == prompt + "botinfo":
                        irc_socket.send("PRIVMSG "+channel+" :Bot został stworzony w celu ułatwienie pracy na IRC. Wpisz help aby uzyskać informację o dostępnych komendach\r\n")

                    if message == prompt + "help":
                        send_message("gogluj [q], linki, wklej, nowosc")

                    if message == prompt + "wklej":
                        send_message("Nie badz noobem i wklej na: https://gist.github.com/")

                    if message == prompt + "linki":
                        irc_socket.send("PRIVMSG "+channel+" :\001ACTION Wysyłam zbiór linków do "+username+"\001\r\n")
                        irc_socket.send("PRIVMSG "+username+" :składnia: >linki[polecenie]\r\n")
                        irc_socket.send("PRIVMSG "+username+" :=========polecenia=========\r\n")
                        irc_socket.send("PRIVMSG "+username+" :fontello, inspiracja, spoj\r\n")
                        irc_socket.send("PRIVMSG "+username+" :===========================\r\n")

                    if message == prompt + "linki[fontello]":
                        send_message("http://forum.miroslawzelent.pl/104219/fontello-wszystko-co-powinienes-wiedziec")

                    if message == prompt + "linki[inspiracja]":
                        send_message("http://forum.miroslawzelent.pl/652/inspirujace-warte-zobaczenia-kanaly-na-youtube")

                    if message == prompt + "linki[spoj]":
                        send_message("http://forum.miroslawzelent.pl/90416/spoj-zasady-umieszczania-postow?show=90416#q90416")

                    if prompt+"gogluj " in message[:8]:
                        try:
                            address = str(googler.short_url([message[7:]]))
                            send_message(address + " Jakie to było proste, nie?")
                        except ValueError:
                            send_message("https://www.google.pl/#q="+message[8:].replace(" ", "+"))
                            #Send_message("OH, SHIT. Dżejson wysiadł")

                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True