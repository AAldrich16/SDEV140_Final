import socket
import sys
from importlib import util
from os import path
from glob import glob
import os
from handler.twitchMessages import TwitchMessages

class Twitch(object):

    def __init__(self, IP, PORT, secret, username, channel, avatar, devMode, moderationMode):

        ## Making all the variables Accessible
        self.IP = IP
        self.PORT = PORT
        self.secret = secret
        self.username = username
        self.channel = channel
        self.avatar = avatar
        self.moderationMode = moderationMode
        self.devMode = devMode

        ## Message Class to handle all messages
        self.MessageSanitizer = TwitchMessages()

        ##Printing to the GUI
        self.outPut('Obito Twitch Bot')
        self.outPut('Made by: Anthony Aldrich')
        self.outPut('-------------------------\n')
        self.outPut('\nAttemping boot... ')

        ## Status of bot Connection
        self.status = False

        ## Attempt Boot
        self.connect()


    def outPut(self, message):
        print(f"{message}")
        sys.stdout.flush()

    ## Sending packet to Twitch
    def sendcmd(self, packet):
        self.ssl.send((f"{packet}\r\n").encode('utf-8'))

    ## Send a message on Twitch
    def privMSG(self, message):
        self.ssl.send((f":{self.username}!{self.username}@{self.username}.tmi.twitch.tv PRIVMSG #{self.channel} :{message}\r\n").encode('utf-8'))
        self.outPut(f'{self.username}: {message}')

    ## Connect to twitch IRC
    def connect(self):

        self.ssl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl.connect((self.IP, self.PORT)) ## Connect to Twitch IP:Port
        self.outPut("Connected... ")
        ## Set Boot status to true
        self.status = True
        ## Send Authenticate Packet
        self.authenticate()
        ## Start Loop
        self.loop()

    ## Basic IRC and Twitch Authentication
    def authenticate(self):
        self.sendcmd(f"PASS {self.secret}")
        self.sendcmd(f"NICK {self.username}")
        self.sendcmd(f"USER {self.username} 8 * :{self.username} ")
        self.sendcmd(f"JOIN #{self.channel}")
        self.sendcmd("CAP REQ :twitch.tv/membership")
        self.sendcmd("CAP REQ :twitch.tv/commands")
        self.sendcmd("CAP REQ :twitch.tv/tags")

    ## Handling Twitch Packets
    def handle(self, cmd):
        sanitized = self.MessageSanitizer.parse(cmd)
        if self.devMode:
            self.outPut(sanitized)

        if sanitized['command'] == "PRIVMSG":
            message = ' '.join(sanitized['parameters'])
            self.outPut(sanitized['sources']['nick'] + " said " + message)

        if self.moderationMode and sanitized['parameters'] != None:
            for words in sanitized['parameters']:
                if words in self.MessageSanitizer.censorWords:
                    self.privMSG("Please dont curse.")

    ## Bot Listen Loop
    def loop(self):
        self.outPut('Listening... \n\n')
        while self.status:
            try:
                data = self.ssl.recv(4096).decode('utf-8', errors='ignore')
                if data:
                    da = data.split(' ')
                    self.handle(da)

            except socket.timeout:
                exit()