import json

from .Policy import Policy


class Task:
    """ Represents a data processing task.
    """

    def __init__ (self, out, files, policies, modes):
        """ Constructs a new instance of a task.

        Args:
            out (str): The directory in which to place output.
            files (list of str): A list of filepaths of probability (distribution) files to load.
            policies (list of Policy): A list of policies to filter by.
            modes (list of int): A list of redistribution modes (as taken by policyfilt.py) to use.
        """
        self.out = out
        self.files = files
        self.policies = policies
        self.modes = modes

    @staticmethod
    def load (file):
        """ Loads a task from file.

        Args:
            file (str): The filepath from which to load the task.
        Returns:
            Task: The loaded task.
        """
        with open(file) as f:
            raw = json.load(f)
            return Task(raw['out'], raw['files'], list(map(Policy.decode, raw['policies'])), raw['modes'])
