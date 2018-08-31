import subprocess
from subprocess import PIPE, Popen
import sublime
import sublime_plugin
import threading
from User.socket_pipe import SocketPipe

oz_proc = None
sp = None

def get_socket(s):
    sp_s = str.split(s)
    return int(sp_s[1])

class SubOz(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.process = None
        self.socket = None
        self.process = Popen(['ozengine', 'x-oz://system/OPI.ozf'], stdout=PIPE, stderr=PIPE)
        print("ozengine pid : %s", self.process.pid)
        socket_output = self.process.stdout.readline().decode('utf-8')
        self.socket = get_socket(socket_output)
        print("Oz Socket : %s" % self.socket)

    def run(self):
        while self.running:
            output = self.process.stdout.readline()
            outerr= self.process.stderr.readline()
            if output == '' and outerr == '' and self.process.poll() is not None:
                running = False
            else:
                print(output.decode('utf-8'))
                print(outerr.decode('utf-8'))

class OzRunCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global oz_proc
        oz_proc = SubOz()
        oz_proc.start()
        global sp
        sp = SocketPipe(self.view, oz_proc.socket)
        sp.start()

class OzFeedBufferCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global sp
        msg = self.view.substr(sublime.Region(0, self.view.size()))
        msg = msg + "\n\004\n"
        sp.send(msg)
