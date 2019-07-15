import subprocess

from model.Task import Task

ss = Task.load('tasky.json')
for file in ss.files:
    print('Now working on file:', file)
    for policy in ss.policies:
        print('Redistributing for policy:', policy.name)
        for mode in ss.modes:
            print('In mode', mode, 'redistributing...')
            subprocess.check_output(['python', 'policyfilt.py', '-n', str(policy.length), '-m', str(mode), '-o', policy.name, file])

print(ss.policies)
