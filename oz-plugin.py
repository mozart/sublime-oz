import subprocess
from subprocess import PIPE, Popen
import sublime
import sublime_plugin

def compile_mozart(file):
    process = Popen(['ozc', '-c', file], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    process.wait()
    outs = stdout.decode('utf-8')
    errs = stderr.decode('utf-8')
    return [outs, errs]

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
        [out_comp, err_comp] = compile_mozart(file)
        [out_exec, err_exec] = execute_mozart(file+'f')
        print("Compilation Output :")
        print(out_comp)
        print(err_comp)
        print("\nExecution Output : ")
        print(out_exec)
        print(err_exec)