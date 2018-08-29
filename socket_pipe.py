# Copyright :
# Ramsey Nasser 2016. Provided under the MIT License
# see https://github.com/nassar/Socket
#
# Last Change :
# Andres Zarza 2018

import threading
import socket
import sublime, sublime_plugin

class SocketPipe(threading.Thread):
    def __init__(self, view, port):
        threading.Thread.__init__(self)
        self.runnning = True
        self.view = view
        self.writtent_characters = 0
        self.buffer = []
        self.prompt = 0
        self.history = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect('localhost', port)
        self.sock.settimeout(1)
        print("Connected SocketPipe to port : %s" % (port))

    def go(self):
        self.setup_view()
        self.update_view()
        self.start()

    def setup_view(self):
        self.view.settings().set("scope_name", "source.clojure")
        self.view.settings().set("line_numbers", False)
        self.view.settings().set("gutter", False)
        self.view.settings().set("word_wrap", False)

    def update_view(self):
         # prevent editing repl view if a selection is before the prompt
        oob = False
        self.view.settings().set("noback", False)
        for region in self.view.sel():
            # backspace is a special case, a sublime-keymap binding checks the 'noback' setting
            if region.a == self.prompt and region.b == region.a:
                self.view.settings().set("noback", True)
            if region.a < self.prompt or region.b < self.prompt:
                oob = True
        if oob:
            self.view.set_read_only(True)
        else:
            self.view.set_read_only(False)
        for b in self.buffer:
            self.view.run_command("socket_insert_text", {"content": b})
        self.buffer = []
        if self.running:
            sublime.set_timeout(self.update_view, 100)

    def on_close(self):
        self.running = False
        self.view.set_name(self.view.name() + " [CLOSED]")
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except:
            pass

    def record_history(self, s):
        rx = re.search("[\\n]*$", s)
        if rx:
            s = s[:len(rx.group()) * -1]
        hlen = len(self.history)
        if s != "" and (hlen == 0 or (hlen > 0 and s != self.history[hlen-1])):
            self.history.append(s)
            self.hist = 0

    def send(self, s):
        self.record_history(s)
        self.sock.send(s.encode('utf-8'))

    def write(self, s):
        self.buffer.append(s)

    def bump(self, s):
        self.written_characters += len(s)

    def run(self):
        while self.running:
            try:
                read = self.sock.recv(8012)
                if(len(read) == 0):
                    self.on_close()
                else:
                    self.buffer.append(read.decode('utf8'))
            except socket.timeout as e:
                continue
            except socket.error as e:
                print(e)
