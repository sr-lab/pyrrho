import importlib

def load_resel_mode (name):
  """ Loads a reselection mode plugin by name.

  Args:
      name (str): The name of the mode to load (must correspond to module unde `./modes`).
  Returns:
      module: The loaded mode as a module.
  """
  mode = importlib.import_module(name)
  return mode
