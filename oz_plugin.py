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

@with_oz
def feed_region(view):
    global sp
    msg = ""
    for region in view.sel():
        if not region.empty():
            msg += view.substr(region)
    sp.send(msg)

class OzFeedRegion(sublime_plugin.TextCommand):
    def run(self, edit):
        feed_region(self.view)

    def is_enabled(self):
        for region in self.view.sel():
            if not region.empty():
                return True
        return False

    def description(self):
        "Feed the selected text to the Oz compiler"


@with_oz
def feed_line(view):
    global sp
    msg = ""
    for region in view.sel():
        if region.empty:
            line = view.line(region)
            msg += view.substr(line) + '\n'
    sp.send(msg)

class OzFeedLine(sublime_plugin.TextCommand):
    def run(self, edit):
        feed_line(self.view)

    def is_enabled(self):
        for region in self.view.sel():
            if region.empty():
                return True
        return False

    def description(self):
        "Feed the current line to the Oz compiler"

class OzFeedBuffer(sublime_plugin.TextCommand):
    @with_oz
    def run(self, edit):
        global sp
        msg = self.view.substr(sublime.Region(0, self.view.size()))
        sp.send(msg)

    def description(self):
        "Feed the current file to the Oz compiler"

class OzFeedContext(sublime_plugin.TextCommand):
    def run(self, edit):
        global sp
        msg = ""
        for region in self.view.sel():
            if not region.empty:
                return feed_region(self.view)
        return feed_line(self.view)

    def is_enabled(self):
        for region in self.view.sel():
            return True
        return False

    def description(self):
        "Feed text to the Oz compiler"


def stop():
    global sp
    if sp:
        sp.stop()
    sp = None

class OzKillCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        stop()

    def description(self):
        "Kill the Oz compiler"

class ExitListener(sublime_plugin.EventListener):
    def on_pre_close(view):
        stop()

