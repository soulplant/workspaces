#!/usr/bin/python

from wsprompt import WSPrompt
import sys

class Command(object):
    def name(self):
        return self._name

    def run(self, ws, args):
        pass

class OpenCommand(Command):
    def __init__(self):
        self._name = "open"

    def run(self, ws, args):
        ws.open()

class AddNoteCommand(Command):
    def __init__(self):
        self._name = "add-note"

    def run(self, ws, args):
        if len(args) > 1:
            ws.add_note(args[1])
        else:
            print "Usage: %s workspace-index note"

# First is default.
COMMANDS = [OpenCommand, AddNoteCommand]

WSPrompt(sys.argv[1:], [c() for c in COMMANDS]).run()
