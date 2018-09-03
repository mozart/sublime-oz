import subprocess
from subprocess import PIPE, Popen
import sublime
import sublime_plugin
import threading
from .socket_pipe import OzThread

sp = None

def with_oz(f):
    def wrapper(*args, **kwargs):
        global sp
        if not sp:
            start_oz()
        f(*args, **kwargs)
    return wrapper

def start_oz():
    global sp
    sp = OzThread()
    sp.start()

class OzRunCommand(sublime_plugin.TextCommand):
    @with_oz
    def run(self, edit):
        pass

class OzFeedLine(sublime_plugin.TextCommand):
    @with_oz
    def run(self, edit):
        global sp
        msg = ""
        for region in self.view.sel():
            if region.empty:
                line = self.view.line(region)
                msg += self.view.substr(line) + '\n'
        sp.send(msg)

class OzFeedBufferCommand(sublime_plugin.TextCommand):
    @with_oz
    def run(self, edit):
        global sp
        msg = self.view.substr(sublime.Region(0, self.view.size()))
        sp.send(msg)

class OzKillCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global sp
        if sp:
            sp.send("{Application.exit 0}\n\004\n\n")
            #TODO
            #Close the process/socket
        sp = None
