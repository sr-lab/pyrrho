import sys
import os
import numpy as np
import pandas as pd

from composition.policy import complies

from shared.args import get_valued_arg, is_arg_passed, get_int_valued_arg


def print_usage (show_help_line=False):
    """ Prints the short help card for the program.
    Args:
        show_help_line (bool): If true, information on help flag `-h` will be printed.
    """
    print('Usage: python policyfilt.py [-hi] [-nludsacw <min>] [-m <renorm_mode>] [-o <outfile>] <infile>')
    print('Filters a CSV file of password probabilities according to a policy and re.')
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
    print('\t-n <int>: Passwords shorter than <min> characters long will be removed')
    print('\t-l <int>: Passwords with fewer than <min> lowercase letters will be removed')
    print('\t-u <int>: Passwords with fewer than <min> uppercase letters will be removed')
    print('\t-d <int>: Passwords with fewer than <min> digits will be removed')
    print('\t-s <int>: Passwords with fewer than <min> symbols will be removed')
    print('\t-a <int>: Passwords with fewer than <min> letters will be removed')
    print('\t-c <int>: Passwords with fewer than <min> character classes (LUDS) will be removed')
    print('\t-w <int>: Passwords with fewer than <min> words (letter sequences) will be removed')
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
    print("Input file '" + file + "' not found.", file=sys.stderr)
    sys.exit(1)

# Try to read in policy from arguments.
length = get_int_valued_arg('n')
lowers = get_int_valued_arg('l')
uppers = get_int_valued_arg('u')
digits = get_int_valued_arg('d')
symbols = get_int_valued_arg('s')
letters = get_int_valued_arg('a')
classes = get_int_valued_arg('c')
words = get_int_valued_arg('w')
invert = is_arg_passed('i')

# Get redistribution mode.
redist_mode = 0 if not is_arg_passed('m') else get_int_valued_arg('m')

# Get output path if one was specified.
out = get_valued_arg('o')

# TODO: No support for special requirements yet.

# Default values.
if length is None:
    length = 0
if lowers is None:
    lowers = 0
if uppers is None:
    uppers = 0
if digits is None:
    digits = 0
if symbols is None:
    symbols = 0
if letters is None:
    letters = 0
if classes is None:
    classes = 0
if words is None:
    words = 0

# Read data frame from file.
df = pd.read_csv(file, skipinitialspace=True, skip_blank_lines=True, encoding='latin-1')

# Sort by probability and reset index.
df.sort_values(by=['probability'], ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

# Get total probability.
total_prob = df['probability'].sum()

# Filter passwords and reset index again.
df = df[df.apply(lambda x: complies(str(x['password']), length, lowers, uppers, digits, symbols, letters, classes, words, [], invert), axis=1)]
df.reset_index(drop=True, inplace=True)

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
