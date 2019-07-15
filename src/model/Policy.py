import json


class Policy:
    """ Represents a password composition policy.
    """

    def __init__ (self, name, length=0, lowers=0, uppers=0, digits=0, others=0, letters=0, classes=0, words=0, spec=[], invert=False):
        """ Constructs a new instance of a task.

        Args:
            length (int): Specifies minimum password length.
            lowers (int): Specifies minimum number of lowercase letters.
            uppers (int): Specifies minimum number of uppercase letters.
            digits (int): Specifies minimum number of digits.
            others (int): Specifies minimum number of symbols.
            letters (int): Specifies minimum number of letters.
            classes (int): Specifies minimum number of character classes (LUDS).
            words (int): Specifies minimum number of words (letter sequences).
            spec (list of str): Specifies extra checks.
            invert (bool): Whether to invert the policy (reject all accepted, accept only rejected).
        """
        self.name = name
        self.length = length
        self.lowers = lowers
        self.uppers = uppers
        self.digits = digits
        self.others = others
        self.letters = letters
        self.classes = classes
        self.words = words
        self.spec = spec
        self.invert = invert

    @staticmethod
    def decode (obj):
        """ Decodes a password composition policy from a dictionary.

        Args:
            obj (dict): The dictionary to decode from.
        Returns:
            Policy: The decoded policy.
        """
        return Policy(obj['name'],
            obj.get('length', 0),
            obj.get('lowers', 0),
            obj.get('uppers', 0),
            obj.get('digits', 0),
            obj.get('others', 0),
            obj.get('letters', 0),
            obj.get('classes', 0),
            obj.get('words', 0),
            obj.get('spec', []),
            obj.get('invert', False))

    @staticmethod
    def load (file):
        """ Loads a password composition policy from file.

        Args:
            file (str): The filepath from which to load the password composition policy.
        Returns:
            Policy: The loaded password composition policy.
        """
        with open(file) as f:
            raw = json.load(f)
            return Policy.decode(raw)
