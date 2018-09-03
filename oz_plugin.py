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

class OzFeedRegion(sublime_plugin.TextCommand):
    @with_oz
    def run(self, edit):
        global sp
        msg = ""
        for region in self.view.sel():
            if not region.empty():
                msg += self.view.substr(region)
        sp.send(msg)

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

def stop():
    global sp
    if sp:
        sp.stop()
    sp = None

class OzKillCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        stop()

class ExitListener(sublime_plugin.EventListener):
    def on_pre_close(view):
        stop()
