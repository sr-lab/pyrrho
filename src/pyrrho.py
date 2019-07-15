import sys
import os
import subprocess

from model.Task import Task


# Mode lookup structure.
MODE_LOOKUP = {
    0: 'elim',
    1: 'renorm',
    2: 'uni',
    3: 'heavy'
}


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


# Load task from file.
task = Task.load(sys.argv[1])

# For each file the task specifies.
for file in task.files:
    print('Now working on file:', file)
    # For each policy the task specifies.
    for policy in task.policies:
        print('Redistributing for policy:', policy.name)
        # For each mode the task specifies.
        for mode in task.modes:
            print('In mode', mode, f'({MODE_LOOKUP[mode]}) redistributing...')
            # Run policy filtration/distribution renormalization script.
            out_path = compute_out_path(task.out, file, policy.name, mode)
            subprocess.check_output(['python', 'policyfilt.py',
                '-n', str(policy.length),
                '-l', str(policy.lowers),
                '-u', str(policy.uppers),
                '-d', str(policy.digits),
                '-s', str(policy.others),
                '-a', str(policy.letters),
                '-c', str(policy.classes),
                '-w', str(policy.words),
                '-i' if policy.invert else '', # TODO: Support special requirements.
                '-m', str(mode),
                '-o', out_path,
                file])
            # Run optimal attack projection, sampling at percentiles.
            print('Running optimal attack projection (percentile sampling)...')
            subprocess.check_output(['python', 'optimalguess.py', '-c',
                '-o', compute_out_path(task.out, file, policy.name, mode, 'log'),
                out_path])
