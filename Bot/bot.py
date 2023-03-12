import json

from twitch import Twitch

class Obito:

    def __init__(self):

        ## Placeholders for variables
        self.moderationMode = None
        self.devMode = None
        self.avatar = None
        self.channel = None
        self.secret = None
        self.username = None

        ## Loading information from JSON File
        self.loadInformation()

        ## Call and Start the Bot
        Twitch('irc.chat.twitch.tv', 6667, self.secret, self.username, self.channel, self.avatar, self.devMode, self.moderationMode)

    def loadInformation(self):
        ## with loop to go through each line of the JSON
        with open("Bot/data.json", "r+") as f:
            bot_info = json.load(f)
            ## Grab Username variable
            self.username = bot_info['botname']
            ## Grab secret variable
            self.secret = bot_info['token']
            ## Grab Channel variable
            self.channel = bot_info['room']
            ## Grab avatar variable
            self.avatar = bot_info['avatar']
            ## Grab devMode variable
            self.devMode = bot_info['devmode']
            ## Grab moderationMode variable
            self.moderationMode = bot_info['moderation']
Obito()