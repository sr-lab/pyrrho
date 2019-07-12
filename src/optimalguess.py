import sys
import os
import math
import pandas as pd

from shared.fileloading import load_lines
from shared.args import get_valued_arg, is_arg_passed, split_multi_arg


def print_usage (show_help_line=False):
    """ Prints the short help card for the program.
    """
    print('Usage: python optimalguess.py [-hc] [-o <outfile>] <targetfile>')
    print('Guesses passwords in a dataset optimally.')
    if show_help_line:
        print('For extended help use \'-h\' option.')


def print_help ():
    """ Prints the full help card for the program.
    """
    print_usage()
    print('Arguments:')
    print('\ttargetfile: The target file for the guessing attack')
    print('Options:')
    print('\t-h: Show this help screen')
    print('\t-c: Output 100 cumulative probabilities only (percentile mode)')
    print('\t-o <path>: Output to file instead of stdout')


# If no options specified, print usage and exit.
if len(sys.argv) == 1:
    print_usage(True)
    exit(0)

# If help flag specified, print help and exit.
if '-h' in sys.argv:
    print_help()
    exit(0)

# Run in percentile mode?
perc_mode = is_arg_passed('c')

# Last parameter is the target filename.
file = sys.argv[-1]

# Check the target file exists.
if not os.path.isfile(file):
    print('Target file \'' + file + '\' not found.', file=sys.stderr)
    sys.exit(1)

# Output stream is standard output by default.
output_stream = sys.stdout

# Get output file path.
output_file_path = get_valued_arg('o')
if not output_file_path is None:
    output_stream = open(output_file_path, 'w', encoding='utf-8')

# Read data frame from file.
df = pd.read_csv(file, skipinitialspace=True, skip_blank_lines=True)

# Sort by probability.
df.sort_values(by=['probability'], ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

# Print cumulative probability/frequency.
cumulative = 0
entries = len(df.index)
cycle_len = math.floor(entries / 100) if perc_mode else 1
counter = 0
for index, row in df.iterrows():
    cumulative += row['probability']
    if counter % cycle_len == 0 or counter == entries:
        print(cumulative, file=output_stream)
    counter += 1
