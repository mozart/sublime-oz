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
from subprocess import PIPE, Popen, STDOUT
import select

#The first message from ozengine contains the port on which it opened the
#socket. The format of the message is "oz-socket XXXX XXXX"
def get_port(s):
    sp_s = str.split(s)
    return int(sp_s[1])

#Thread that runs that connects the socket and runs ozengine
class OzThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.window = sublime.active_window()

        #ozemulator
        self.process = Popen(['ozengine', 'x-oz://system/OPI.ozf'], stdout=PIPE, stderr=PIPE)
        port_output = self.process.stdout.readline().decode('utf-8')
        port = get_port(port_output)

        #socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', port))
        self.sock.settimeout(1)
        self.running = True

    def write_compiler(self, s):
        self.write_panel(s, "oz_compiler")

    def write_process(self, s):
        self.write_panel(s, "oz_output")

    def write_panel(self, s, panel_name):
        #Panel to display compilation and emulator output
        panel = self.window.find_output_panel(panel_name)
        if not panel:
            panel = self.window.create_output_panel(panel_name)
            #panel.settings().set("scope_name", "source.clojure")
            panel.settings().set("line_numbers", False)
            panel.settings().set("gutter", False)
            panel.settings().set("word_wrap", False)
            panel.set_read_only(True)

        panel.run_command("append", {
            'characters': s,
            'force': True,
            'scroll_to_end': True,
            })
        self.window.run_command('show_panel', {'panel': 'output.'+panel_name})


    def on_close(self):
        self.running = False
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except:
            pass

    def send(self, s):
        s += "\n\004\n"
        self.sock.send(s.encode('utf-8'))

    def run(self):
        inputs = [self.sock, self.process.stdout, self.process.stderr]
        while self.running:
            [readable, writable, exceptional] = select.select(inputs, [], [],
            10)
            for s in readable:
                if s is self.sock:
                    try:
                        self.write_compiler(s.recv(8012).decode('utf-8'))
                    except socket.timeout as e:
                        continue
                    except socket.error as e:
                        print(e)
                else:
                    self.write_process(s.readline().decode('utf-8'))

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.process.wait()
        panel = self.window.find_output_panel("oz_panel")
        if panel is not None:
            self.window.destroy_output_panel("oz_panel")

    def stop(self):
        exit_msg = "{Application.exit 0}\n\004\n\n"
        self.sock.send(exit_msg.encode('utf-8'))
        self.running = False
