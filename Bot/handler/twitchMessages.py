import re


class TwitchMessages(object):

    ## The constructor initializes the list of censor words and commands
    def __init__(self):
        self.censorWords = ["fword", "sword"]
        self.commands = ['JOIN', 'PART', 'PRIVMSG', 'PING']

    ## This method parses the Twitch message and returns a dictionary with the different parts
    def parse(self, msg):
        ## Create an empty dictionary with placeholders for the different parts of the message
        self.parsedMessage = {
            "command": None,
            "tags": None,
            "sources": None,
            "parameters": None,
            "channel": None,
            "botcommand": None,
        }
        ## Loop through each part of the message
        for messagepart in msg:
            ## If the part starts with "@" it contains tags
            if messagepart[0] == "@":
                self.parsedMessage['tags'] = self.parseTags(messagepart)
            ## If the part starts with "#" it contains the channel name
            if messagepart[0] == "#":
                self.parsedMessage['channel'] = messagepart
            ## If the part ends with ".tmi.twitch.tv" it contains the source of the message
            if messagepart.endswith('.tmi.twitch.tv'):
                self.parsedMessage['sources'] = self.parseSource(messagepart)
            ## If the part is one of the recognized commands, set it as the command
            if messagepart in self.commands:
                self.parsedMessage['command'] = self.parseCommand(messagepart)

        ## Split the message into parameters using the channel name as a delimiter
        parameters = str(msg).split(self.parsedMessage['channel'])

        ## If there is more than one parameter, parse the parameters and return the message dictionary
        if len(parameters) > 1:
            mes = parameters[1].replace("', ", ' ', 1).replace("]", '').replace(r'\r\n', '').replace("':", "'",
                                                                                                     1).replace("'",
                                                                                                                "").replace(
                " ", "").split(',')
            self.parsedMessage['parameters'] = self.parseParameter(mes)
            return self.parsedMessage
        ## Otherwise, just return the message dictionary
        else:
            return self.parsedMessage

    ## This method parses the tags and returns a dictionary of tag names and values
    def parseTags(self, tags):
        tagarray = tags.split(';')
        tagdict = {}
        for tag in tagarray:
            taginfo = tag.split('=')
            tagvalue = taginfo[1]
            tagname = taginfo[0].strip('=')

            if tagvalue == '':
                tagvalue = None

            if tagname == "badges" or tagname == "badge-info":
                badgearray = []
                badges = tagvalue.split(',')
                for badge in badges:
                    new = badge.split('/')
                    badgearray.append(new[0])

                tagdict[tagname] = badgearray
            elif tagname == "subscriber":
                tagdict[tagname] = tagvalue
            elif tagname == "emotes":
                tagdict[tagname] = tagvalue

        return tagdict

    ## This method parses the source of the message and returns a dictionary with the nick and host
    def parseSource(self, source):
        sources = {}
        if re.search(':(.*)!', source):
            nick = re.search(':(.*)!', source)
            sources['nick'] = nick.group(1)
        else:
            sources['nick'] = "TWITCH"
        sources['host'] = 'tmi.twitch.tv'
        return sources


    ## Reading Twitch Error Codes
    def parseCommand(self, command):
        if command == "002" or command == "003" or  command == "004" or  command == "353" or  command == "366" or  command == "372" or command == "375" or command == "376":
            print(f'numeric message: {command}')
        if command == "RECONNECT":
            print('The Twitch IRC server is about to terminate the connection for maintenance.')
        return command

    ## If message has Bot Command Symbol
    def parseParameter(self, parameter):
        if parameter[0][:2] == "!@":
            bot = parameter[0].split('!@')
            self.parsedMessage['botcommand'] = bot[1]
        return parameter


TM = TwitchMessages()
