import subprocess
from subprocess import PIPE, Popen
import sublime
import sublime_plugin
import threading
from .socket_pipe import OzThread

sp = None

def kill_oz(sock):
    sock.send("{Application.exit 0}\n\004\n\n}")

def start_oz():
    global sp
    #Panel to display compilation and emulator output
    window = sublime.active_window()
    panel = window.find_output_panel('oz_panel')
    if(panel == None):
        panel = window.create_output_panel('oz_panel')
    window.run_command('show_panel', {'panel':'output.oz_panel'})
    sp = OzThread(panel)
    sp.start()

class OzRunCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        start_oz()

class OzFeedBufferCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global sp
        if(sp == None):
            start_oz()
        msg = self.view.substr(sublime.Region(0, self.view.size()))
        msg = msg + "\n\004\n"
        sp.send(msg)

class OzKillCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global sp
        kill_oz(sp)
