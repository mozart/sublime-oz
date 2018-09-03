# Inspired from
# Copyright :
# Ramsey Nasser 2016. Provided under the MIT License
# see https://github.com/nassar/Socket
#
# Last Change :
# Andres Zarza 2018

import threading
import socket
import sublime, sublime_plugin
import re
from subprocess import PIPE, Popen
import select

#The first message from ozengine contains the port on which it opened the
#socket. The format of the message is "oz-socket XXXX XXXX"
def get_port(s):
    sp_s = str.split(s)
    return int(sp_s[1])

#Thread that runs that connects the socket and runs ozengine
class OzThread(threading.Thread):
    def __init__(self, view):
        threading.Thread.__init__(self)
        self.view = view

        #ozemulator
        self.process = Popen(['ozengine', 'x-oz://system/OPI.ozf'], stdout=PIPE, stderr=PIPE)
        print("ozengine pid : %s", self.process.pid)
        port_output = self.process.stdout.readline().decode('utf-8')
        port = get_port(port_output)
        print("Oz Socket : %s" % port)

        #socket
        self.history = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', port))
        self.sock.settimeout(1)
        self.running = True

    def go(self):
        self.setup_view()
        self.start()

    def setup_view(self):
        self.view.settings().set("scope_name", "source.clojure")
        self.view.settings().set("line_numbers", False)
        self.view.settings().set("gutter", False)
        self.view.settings().set("word_wrap", False)

    def on_close(self):
        self.running = False
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except:
            pass

    def send(self, s):
        self.sock.send(s.encode('utf-8'))


    def insert_text(self, s):
        self.view.set_read_only(False)
        self.view.run_command("append", {"characters": s})
        self.view.set_read_only(True)

    def run(self):
        inputs = [self.sock, self.process.stdout, self.process.stderr]
        while self.running:
            [readable, writable, exceptional] = select.select(inputs, [], [])
            for s in readable:
                if(s is self.sock):
                    try:
                        read = self.sock.recv(8012)
                        read = read.decode('utf-8')
                        self.insert_text(read)
                    except socket.timeout as e:
                        continue
                    except socket.error as e:
                        print(e)
                else:
                   self.insert_text(s.readline().decode('utf-8'))
