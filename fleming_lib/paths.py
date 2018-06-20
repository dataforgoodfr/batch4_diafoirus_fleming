"""."""
import os
import sys

import yaml


def get_userpaths(userconfig_file='userconfig.yml'):
    """Find user path from user config file."""
    file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'user',
                     userconfig_file))
    if not os.path.isfile(file):
        raise ValueError('File {} does not exist.'.format(file))
    with open(file) as f:
        userpaths = yaml.load(f)['USERPATHS']
    return userpaths 


def add_userpath(userpaths=[]):
    """Import external libraries.

    Parameters
    ----------
    userpaths : dict
        Dictionary containing userpaths.

    """
    # List of libs to append
    if not isinstance(userpaths, dict):
        raise ValueError('`userpaths` should be of type `dict`.')

    sys_path = sys.path

    for k, (name, path) in enumerate(userpaths.items()):
        if os.path.exists(path):
            print('[INFO] adding {} to sys.path'.format(path))
            sys_path.insert(k, path)
        else:
            raise OSError('Path {} coult not be resolved.'.format(path))

    # Add paths
    sys.path = sys_path


# Import userpaths
# ----------------
USERPATHS = get_userpaths()
add_userpath(USERPATHS)
