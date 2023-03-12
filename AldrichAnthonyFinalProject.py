## ----------------------------------------------
## Author: Anthony Aldrich
## Program Name: AegBot Console
## Date: 02/22/23
## Purpose: To Create a Twitch Bot GUI for Non-Tech Savy Streamers
## ----------------------------------------------


import tkinter as tk
from tkinter import ttk
import subprocess
from ttkthemes import ThemedTk
import sv_ttk
import threading
import json

# Importing required modules
# tk - GUI library
# ttk - themed GUI widgets
# subprocess - creating new processes
# ThemedTk - Tkinter widget with theme support
# sv_ttk - themed GUI widgets
# threading - allows for parallelism
# json - JavaScript Object Notation


class App:
    def __init__(self):
        ## Creating a dark themed Tkinter Window
        self.root = ThemedTk(theme="dark")
        sv_ttk.set_theme("dark")
        self.root.title("AegBot Command Center")

        ## Creating the notebook with two tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        ## Initiate the creation of tabs
        self.createBotConsole()
        self.createBotConfiguration()

    def createBotConsole(self):
        ## Create a Frame for the Console Tab
        self.ConsoleTab = tk.Frame(self.notebook)
        ## Console Box for reading output of Bot Script
        self.createInput('ConsoleBox', self.ConsoleTab, tk.Text, {'font': ('Consolas', 14), 'foreground': '#8e8cf5'}, {'side': tk.LEFT, 'fill': 'both', 'expand': True})
        ## Start Button to Initiate Script
        self.createInput("StartButton", self.ConsoleTab, ttk.Button, {'text': "Start", 'command': self.start_script, 'state': 'enable'}, {'fill': 'x', 'padx': 10, 'pady':5})
        ## Stop Button to Kill Script
        self.createInput("StopButton", self.ConsoleTab, ttk.Button, {'text': "Stop", 'command': self.stop_script, 'state': 'disable'}, {'fill': 'x', 'padx': 10, 'pady':5})
        ## Inserting images into the Frame
        self.createImage('AegBot', self.ConsoleTab, 'images/bot.png', {'fill': 'x', 'side': tk.RIGHT}, {'fill': 'both', 'expand': True})
        ## Adding everything to the Console Tab
        self.notebook.add(self.ConsoleTab, text='Bot Console')

    def createBotConfiguration(self):
        ## Creating the Panel [Tab 2]
        self.form_tab = tk.Frame(self.notebook)

        ## This is just a label for Error and Success Messages, Default is empty
        self.ErrorFrame = tk.Frame(self.form_tab)
        self.ErrorFrame.pack(fill='x', padx=10, pady=5)
        self.ErrorBox = tk.Label(self.ErrorFrame, text="", width=75)
        self.ErrorBox.pack(fill="x", padx=(0, 5))

        ## Input for Nickname of Bot
        self.createInput("Nick", self.form_tab, ttk.Entry,{'validate': 'focusout', 'validatecommand': (self.root.register(self.validateForm), '%P')},{'fill': 'x', 'padx': 10, 'pady': 5})
        ## Input for Twitch Token of Bot
        self.createInput("Token", self.form_tab, ttk.Entry,{'validate': 'focusout', 'validatecommand': (self.root.register(self.validateForm), '%P')},{'fill': 'x', 'padx': 10, 'pady': 5})
        ## Input for Room of Bot
        self.createInput("Room", self.form_tab, ttk.Entry,{'validate': 'focusout', 'validatecommand': (self.root.register(self.validateForm), '%P')},{'fill': 'x', 'padx': 10, 'pady': 5})
        ## Input for Avatar of Bot
        self.createInput("Avatar", self.form_tab, ttk.Entry,{'validate': 'focusout', 'validatecommand': (self.root.register(self.validateForm), '%P')},{'fill': 'x', 'padx': 10, 'pady': 5})
        ## Input for Command Sign of Bot
        self.createInput("Command", self.form_tab, ttk.Entry,{'validate': 'focusout', 'validatecommand': (self.root.register(self.validateForm), '%P')}, {'fill': 'x', 'padx': 10, 'pady': 5})
        ## Input for Moderation Mode of Bot
        self.createInput("Moderation", self.form_tab, ttk.Checkbutton, {}, {'fill': 'x', 'padx': 10, 'pady': 5})
        ## Input for Developer Mode of Bot
        self.createInput("DevMode", self.form_tab, ttk.Checkbutton, {}, {'fill': 'x', 'padx': 10, 'pady': 5})

        ## Submit Button
        self.createInput("EditButton", self.form_tab, ttk.Button, {'text': "Edit", 'command': self.editBotData},{'fill': 'x', 'padx': 10, 'pady': 5})
        ## Inserting AegBot Logo at Bottom
        self.createImage('AegLogo', self.form_tab, 'images/logo.png', {'fill': 'x', 'side': 'bottom'}, {'fill': 'both', 'expand': True})

        ##Calling to function to fill in the Data from JSON File
        self.fill_form()
        ## Add everything to the form Tab
        self.notebook.add(self.form_tab, text='Bot Configuration')

    def validateForm(self, input):
        ## If the input is empty return false
        if input == "":
            return False
        ## If the input is greater than 50 return false
        elif len(input) > 50:
            return False
        ## Everything else passes the Validation
        else:
            return True

    def createImage(self, name, tab, image, frameOptions={}, labelOptions={}):
        ## Creating a list of options for the label
        labelO = {**labelOptions}
        ## Creating a list of options for the frame
        frameO = {**frameOptions}
        ## Create the frame for the image
        frame = tk.Frame(tab)
        frame.pack(**frameO)
        ## making the Tkinter image from the file
        img = tk.PhotoImage(file=image)
        ## Creating the Label for the Image
        imgLabel = tk.Label(frame, image=img)
        imgLabel.pack(**labelO)
        ## Storing this inside of the Variable
        imgLabel.image = img
        ## Allowing the Image to accessed i.e. if the name is AegLogo, it can be used as this.AegLogo
        setattr(self, name, tab)

    def createInput(self, tab, name, inputType, EntryOptions={'width': 50}, FrameOptions={}):
        ## Creating a list of options for the Entry
        options = {**EntryOptions}
        ## Creating a list of options for the Frame
        frameOptions = {**FrameOptions}
        ## Creating a Frame for the Input
        frame = tk.Frame(name)
        frame.pack(**frameOptions)
        ## Only create a Label if the input is not a Button or the Bot Console
        if inputType != ttk.Button and inputType != tk.Text:
            label = tk.Label(frame, text=tab, width=12)
            label.pack(side='left', padx=(0, 5))
        ## Create the input type with the given options
        inputWidget = inputType(frame, **options)
        inputWidget.pack(side='left', fill='x', expand=True)
        ## Allowing the input to accessed i.e. if the name is Nick, it can be used as this.Nick
        setattr(self, tab, inputWidget)

    def start_script(self):
        if self.validateForm(self.Nick.get()) & self.validateForm(self.Avatar.get()) & self.validateForm(self.Command.get())& self.validateForm(self.Token.get())& self.validateForm(self.Room.get()):
            ## enables the push of the stop button
            self.StopButton.config(state='normal')
            ## disables the push of the start button
            self.StartButton.config(state='disable')
            ## clears the content of the ConsoleBox ( Script output)
            self.ConsoleBox.delete("1.0", tk.END)
            #This is the start of the script using a sub process
            self.process = subprocess.Popen(["python", "Bot/bot.py"], stdout=subprocess.PIPE,stderr=subprocess.PIPE, bufsize=0)
            ## Gets output from the script using threads
            threading.Thread(target=self.read_output, args=(self.process.stdout,)).start()
            ## Get the errors from the script using threads
            threading.Thread(target=self.read_output, args=(self.process.stderr,)).start()
        else:
            self.ConsoleBox.insert('end', "Please Enter all information before starting the bot\n \n")

    def stop_script(self):
        # Killing the script
        self.process.terminate()
        ## Notifing the user inside the Console that the script has been killed (RIP)
        self.ConsoleBox.insert('end', "script killed\n \n")
        ## Disables the push of the stop buttton
        self.StopButton.config(state='disable')
        ## enables the push of the start buttton
        self.StartButton.config(state='normal')

    def read_output(self, output):
        ## This is a for loop to iteriate through the output as it comes and inserts each line into the console box, instead of waiting till it ends and inserting it all at once.
        for line in iter(output.readline, b''):
            ## Pushes the incoming output to the bottom of the text box
            self.ConsoleBox.insert('end', line.decode(), ("big", "red"))
            self.ConsoleBox.see('end')

    def fill_form(self):
        ## with loop to go through each line of the JSON
        with open('Bot/data.json') as f:
            data = json.load(f)
            ## Insert botname to the Nick input
            self.Nick.insert(0, data['botname'])
            ## Insert avatar to the Avatar input
            self.Avatar.insert(0, data['avatar'])
            ## Insert token to the Token input
            self.Token.insert(0, data['token'])
            ## Insert token to the Token input
            self.Room.insert(0, data['room'])
            ## Insert moderation to the Moderation input
            self.Moderation.configure(variable=tk.BooleanVar(value=data['moderation']))
            ## Insert command to the Command input
            self.Command.insert(0, data['command'])

    def editBotData(self):
        ## with Loop to get every line of data.JSON
        with open('Bot/data.json', 'r+') as f:
            ## converts json into python object
            data = json.load(f)
            ## Make sure when Form is Submitted all Inputs passed Validation
            if self.validateForm(self.Nick.get()) & self.validateForm(self.Avatar.get()) & self.validateForm(self.Command.get())& self.validateForm(self.Token.get())& self.validateForm(self.Room.get()):
                ## Change the value of botname to Nick
                data['botname'] = self.Nick.get()
                ## Change the value of avatar to Avatar
                data['avatar'] = self.Avatar.get()
                ## Change the value of token to Token
                data['token'] = self.Token.get()
                ## Change the value of room to Room
                data['room'] = self.Room.get()
                ## Change the value of command to Command
                data['command'] = self.Command.get()
                ## Make errorbox show a success message
                self.ErrorBox.config(text='Bot Info has been updated!',foreground='green')
            else:
                ## Make errorbox show a error message
                self.ErrorBox.config(text='Please Fix Errors! Inputs shouldnt be empty or greater than 50', foreground='red')
            f.seek(0)
            ## changes object back to json
            json.dump(data, f, indent=4)
            f.truncate()

app = App()
app.root.mainloop()
