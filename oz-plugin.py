import subprocess
from subprocess import PIPE, Popen

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
