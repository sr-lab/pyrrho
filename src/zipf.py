import sys
import os
import json

import pandas as pd
import matplotlib.pyplot as plt

from pylab import log10
from scipy import optimize

from shared.args import get_valued_arg, is_arg_passed, get_int_valued_arg


def sample (x, y, c=0, e=0):
    """ Performs logarithmic sampling on the given data.
    Args:
        x (list of float): The x-values.
        y (list of float): The y-values.
        c (int): The current offset in the data.
        e (int): The current exponent.
    Returns:
        pair: The sampled x and y values, in a pair.
    """
    if c > len(x):
        return ([], []) # Length of data exceeded, return.
    w = 2 ** e # Calculate sample interval.

    # Recursively bin data.
    nx, ny = sample(x, y, c + w, e + 1)
    return ([x[c]] + nx, [y[c]] + ny)


def print_usage (show_help_line=False):
    """ Prints the short help card for the program.
    Args:
        show_help_line (bool): If true, information on help flag `-h` will be printed.
    """
    print('Usage: python zipf.py [-hcls] [-o <outfile>] [-eq <eqfile>] [-t <title>] <infile>')
    print('Fits a powerlaw equation to a password frequency distribution.')
    if show_help_line:
        print('For extended help use \'-h\' option.')


def print_help ():
    """ Prints the full help card for the program.
    """
    print_usage()
    print('Arguments:')
    print('\tinfile: The password frequency file to fit')
    print('Options:')
    print('\t-h: Show this help screen')
    print('\t-c: Disable binning')
    print('\t-l: Disable fitting line')
    print('\t-o <str>: The file in which to place output figure')
    print('\t-eq <str>: Specify the output file in which to serialize the regression line equation')
    print('\t-t <str>: The plot title')
    print('\t-s: Suppress the plot window')
    print()
    print('Input file should be in CSV format:')
    print('\tpassword, frequency, ... <- Column headers')
    print('\t123456, 9472, ...')
    print('\thunter, 3571, ...')
    print('\tmatrix, 423, ...')


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

# Check flags.
no_binning_mode = is_arg_passed('c') # Should we avoid binning?
hide_fitting_line = is_arg_passed('l') # Should we hide the fitting line?
suppress_chart = is_arg_passed('s') # Should we suppress showing the chart?

# Get passed values.
out = get_valued_arg('o') # Get output path if one was specified.
eq_out = get_valued_arg('eq') # Get equation output path if one was specified.
title = get_valued_arg('t') # Set the title if one was specified.

# Read data frame from file.
df = pd.read_csv(file, skipinitialspace=True, skip_blank_lines=True, encoding='latin-1')

# Sort by frequency.
df.sort_values(by=['probability'], ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

# Get raw frequency values (these go on the Y axis).
ry = df['probability']

# Generate ranks (these go on the X axis) and cast to floats.
rx = range(1, len(ry) + 1)
rx = list(map(lambda j: float(j), rx))

# Bin values.
if no_binning_mode:
    x, y = rx, ry
else:
    x, y = sample(rx, ry)

# It's much better to perform a least-squares fit on the logarithms.
logx = log10(x)
logy = log10(y)

# Specify fitting and error functions.
fitting_func = lambda p, x: p[0] + p[1] * x
error_func = lambda p, x, y: y - fitting_func(p, x)

# Least squares fitting.
params_init = [1.0, -1.0]
fit = optimize.leastsq(error_func, params_init, args=(logx, logy), full_output=1)

# Get final params.
params_final = fit[0]
covar = fit[1] # TODO: What's this?

# Get alpha and amplitude.
alpha = params_final[1]
amp = 10.0 ** params_final[0]

# Dump output structure to standard output.
output = {'amp': amp, 'alpha': alpha}
print(json.dumps(output))

# Write equation file if required.
if not eq_out is None:
    eq_out_file = open(eq_out, 'w')
    print(json.dumps(output), file=eq_out_file)
    eq_out_file.close()

# Create function for regression line.
powerlaw = lambda x, amp, alpha: amp * (x ** alpha)

# Set up plot.
plt.clf()
if not hide_fitting_line:
    plt.loglog(x, powerlaw(x, amp, alpha))
plt.loglog(x, y)
if not title is None:
    plt.title(title) # Only set title if one was specified.
plt.xlabel('Rank')
plt.ylabel('Probability')

# Save file if asked to.
if out is not None:
    plt.savefig(out)

# Show plot.
if not suppress_chart:
    plt.show()
