import sys
import os
import time
from subprocess import *

import numpy as np
import pandas as pd

from shared.args import get_valued_arg, is_arg_passed, get_int_valued_arg


def print_usage (show_help_line=False):
    """ Prints the short help card for the program.
    Args:
        show_help_line (bool): If true, information on help flag `-h` will be printed.
    """
    print('Usage: python authfilt.py [-hi] [-a <authority>] [-p <policy>] [-m <renorm_mode>] [-o <outfile>] <infile>')
    print('Filters a CSV file of password probabilities according to an authority and redistributes filtered probabilities.')
    if show_help_line:
        print('For extended help use \'-h\' option.')


def print_help ():
    """ Prints the full help card for the program.
    """
    print_usage()
    print('Arguments:')
    print('\tinfile: The password file to filter')
    print('Options:')
    print('\t-h: Show this help screen')
    print('\t-a <str>: The file path of the authority executable to use')
    print('\t-p <str>: The name of the policy to pass to the authority')
    print('\t-m <int>: Choose a probability redistribution mode [1]')
    print('\t-i: Invert policy (filter all accepted, output only rejected)')
    print('\t-o <str>: The file in which to place output')
    print('Notes:')
    print('\t[1]: Redistribution modes include:')
    print('\t\t0: Elimination mode, eliminate outcomes only (breaks the distribution!)')
    print('\t\t1: Renormalization mode, proportionally redistributes probability of eliminated outcomes')
    print('\t\t2: Uniform mode, uniformly redistributes probability of eliminated outcomes')
    print('\t\t3: Heavy-tail mode, places probability from all eliminated outcomes into most frequent outcome')
    print()
    print('Input file should be in CSV format:')
    print('\tpassword, probability, ... <- Column headers')
    print('\t123456, 0.04362, ...')
    print('\thunter, 0.03712, ...')
    print('\tmatrix, 0.14325, ...')


# The total number of passwords the authority will ask for. Setting this too high will cause a stack overflow!
GL_BATCH_SIZE = 5000

# The authority process (global).
gl_auth_proc = None


def try_launch_auth (file, policy):
    """ Attempts to launch the global authority.

    Args:
        file (str): The binary file to execute.
        policy (str): The name of the policy to call the file with.
    """
    global gl_auth_proc # We need to assign to this global.
    gl_auth_proc = (None, file, policy)
    try:
        gl_auth_proc = (Popen([file, policy, str(GL_BATCH_SIZE)], stdin=PIPE, stdout=PIPE), file, policy)
        time.sleep(2) # Wait, it might exit immediately if parameters are incorrect.
        return gl_auth_proc[0].poll() == None
    except:
        return False


def ask_auth (pwd):
    """ Checks with the authority whether or not a password is permitted.

    Args:
        pwd (str): The password to check.
    Returns:
        bool: True if the password is permitted, otherwise False.
    """
    # Relaunch process if necessary.
    poll = gl_auth_proc[0].poll()
    if poll != None:
        try_launch_auth(gl_auth_proc[1], gl_auth_proc[2])
    # Pass password into authority (don't forget to flush).
    gl_auth_proc[0].stdin.write(f'{pwd}\n'.encode())
    gl_auth_proc[0].stdin.flush()
    # Return result, cast to boolean.
    buffer = gl_auth_proc[0].stdout.readline()
    return buffer.decode().strip().lower() == 'true'


# If no options specified, print usage and exit.
if len(sys.argv) == 1:
    print_usage(True)
    exit(0)

# If help flag specified, print help and exit.
if is_arg_passed('h'):
    print_help()
    exit(0)

# Last parameter is the filename.
file = sys.argv[-1]

# Check the target file exists.
if not os.path.isfile(file):
    print('Input file \'' + file + '\' not found.', file=sys.stderr)
    sys.exit(1)

# Try to read in policy from arguments.
authority = get_valued_arg('a')
policy = get_valued_arg('p')
invert = is_arg_passed('i')

# Check the authority file exists.
if not os.path.isfile(authority):
    print('Authority file \'' + file + '\' not found.', file=sys.stderr)

# Check we can launch it.
if not try_launch_auth(authority, policy):
    print('Could not launch authority \'' + authority + '\', check policy name and executable flag.', file=sys.stderr)
    sys.exit(1)

# Get redistribution mode.
redist_mode = 0 if not is_arg_passed('m') else get_int_valued_arg('m')

# Get output path if one was specified.
out = get_valued_arg('o')

# Read data frame from file.
df = pd.read_csv(file, skipinitialspace=True, skip_blank_lines=True, encoding='latin-1')

# Sort by probability and reset index.
df.sort_values(by=['probability'], ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

# Get total probability.
total_prob = df['probability'].sum()

# Filter passwords and reset index again.
df = df[df.apply(lambda x: invert ^ ask_auth(str(x['password'])), axis=1)]
df.reset_index(drop=True, inplace=True)

# Get rid of authority process.
gl_auth_proc[0].terminate()

# Get 'surplus' probability.
filtered_prob = df['probability'].sum()
surplus = total_prob - filtered_prob
row_count = len(df.index)

# Soft filtration, flag noncompliant passwords as unguessable.
if redist_mode == 1:
    df['probability'] /= filtered_prob
elif redist_mode == 2:
    ech = surplus / row_count
    df['probability'] += ech
elif redist_mode == 3:
    df.loc[0, 'probability'] += surplus

# Print data frame.
df.to_csv(out if not out is None else sys.stdout, index=False)
