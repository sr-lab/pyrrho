import sys
import os
import subprocess

from shared.args import is_arg_passed
from model.Task import Task


# Mode lookup structure.
MODE_LOOKUP = {
    0: 'none',
    1: 'proportional',
    2: 'uniform',
    3: 'convergent',
    4: 'extraneous'
}


def print_usage (show_help_line=False):
    """ Prints the short help card for the program.
    Args:
        show_help_line (bool): If true, information on help flag `-h` will be printed.
    """
    print('Usage: python [-h] pyrrho.py <taskfile>')
    print('Interprets a task file containing instructions for password probability distribuution transformation.')
    if show_help_line:
        print('For extended help use \'-h\' option.')


def print_help ():
    """ Prints the full help card for the program.
    """
    print_usage()
    print('Arguments:')
    print('\taskfile: The task file to run (see README.md)')
    print('Options:')
    print('\t-h: Show this help screen')


def compute_out_path (dir, file, policy, mode, ext='csv'):
    """ Computes the name of a file to write renormalized data to.

    Args:
        dir (str): The base output directory path.
        file (str): The name of the original file.
        policy (str): The name of the policy used to filter the data.
        mode (int): The redistribution mode used (from policyfilt.py).
        ext (str): The file extension to use.
    """
    file_name = os.path.splitext(os.path.basename(file))[0]
    file_name += f'_{policy}_{MODE_LOOKUP[mode]}.{ext}'
    return os.path.join(dir, file_name)


# If no options specified, print usage and exit.
if len(sys.argv) == 1:
    print_usage(True)
    exit(0)

# If help flag specified, print help and exit.
if is_arg_passed('h'):
    print_help()
    exit(0)

# Load task from file.
task = Task.load(sys.argv[1])

# For each file the task specifies.
for file in task.files:
    print('Now working on file:', file)
    # For each policy the task specifies.
    for policy in task.policies:
        print('Redistributing for policy:', policy)
        # For each mode the task specifies.
        for mode in task.modes:
            print('In mode', mode, f'({MODE_LOOKUP[mode]}) redistributing...')
            # Run policy filtration/distribution renormalization script.
            out_path = compute_out_path(task.out, file, policy, mode)
            subprocess.check_output(['python3', 'authfilt.py',
                '-a', task.authority,
                '-p', policy,
                '-m', str(mode),
                '-o', out_path,
                file])
            # If redistributed probability file was produced.
            if os.path.isfile(out_path):
                # Run optimal attack projection, sampling at percentiles.
                print('Running optimal attack projection (percentile sampling)...')
                subprocess.check_output(['python3', 'optimalguess.py', '-c',
                    '-o', compute_out_path(task.out, file, policy, mode, 'log'),
                    out_path])
                # Fit equation to altered distribution.
                print('Fitting equation to altered probability distribution...')
                subprocess.check_output(['python3', 'zipf.py',
                    '-s', '-eq', compute_out_path(task.out, file, policy, mode, 'json'),
                    out_path])
            else:
                print('Redistribution was not possible for', file, 'under', policy, 'possibly because everything was filtered.')
