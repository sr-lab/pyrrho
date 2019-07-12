def load_file_lines(file):
    """ Loads a file as a list of lines.

    Args:
        file (str): The path of the file.
    Returns:
        list of str: A list of lines in the file.
    """
    data = []
    with open(file, mode='r') as target:
        for line in target:
            data.append(line.rstrip('\n'))
    return data


def load_float_file (file):
    """ Loads a data file of newline-delimited floating-point values.

    Args:
        file (str): The path of the file.
    Returns:
        list of float: The data from the file.
    """
    data = []
    with open(file, 'r') as target:
        for entry in target:
            data.append(float(entry))
    return data
