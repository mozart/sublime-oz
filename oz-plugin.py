import subprocess
from subprocess import PIPE, Popen
import sublime
import sublime_plugin

def compile_mozart(file):
    process = Popen(['ozc', '-c', file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    process.wait()
    return_code = process.poll()
    outs = stdout.decode('utf-8')
    errs = stderr.decode('utf-8')
    return [outs, errs, return_code]

def execute_mozart(file):
    process = Popen(['ozengine', file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    process.wait()
    outs = stdout.decode('utf-8')
    errs = stderr.decode('utf-8')
    return [outs, errs]

class OzRunCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file = self.view.file_name()
        co = compile_mozart(file)
        [out_comp, err_comp, code_comp] = compile_mozart(file)
        window = sublime.active_window()
        panel = window.find_output_panel('oz_panel')
        if(panel == None):
            panel = window.create_output_panel('oz_panel')
        window.run_command('show_panel', {'panel':'output.oz_panel'})
        panel.set_read_only(False)
        panel.run_command("append", {"characters": "Compilation output :\n"})
        panel.run_command("append", {"characters": out_comp+"\n"+err_comp+"\n"})
        if(code_comp == 0):
            [out_exec, err_exec] = execute_mozart(file+'f')
            panel.run_command("append", {"characters": "Execution output:\n"})
            panel.run_command("append", {"characters": out_exec+"\n"+err_exec+"\n"})
        panel.set_read_only(True)
    def is_visible(self):
        print(self.view.window().active_panel())
        return True