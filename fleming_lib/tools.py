#!/usr/bin/env python

"""These functions were developped as tools for the Fleming project."""

__author__ = 'François-Guillaume Fernandez'
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'François-Guillaume Fernandez'
__status__ = 'Development'

import os

import numpy as np

from .paths import USERPATHS


login_path = os.path.join(USERPATHS['FLEMING'], 'user', 'full_omop_login.npy')


def progress_bar(count, total, status=''):
    """Display a progress bar.

    Parameters
    ----------
    count : int
        Number of iterations already performed.
    total : int
        Total number of iterations.
    status : str
        Status information you want to print out.

    """
    import sys
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 2)
    bar = '=' * (filled_len - 1) + '>' + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def connect_to_omop(login_dict=None):
    """Provide a PostGreSQL connection to the MIMIC db in OMOP format.

    Parameters
    ----------
    login_dict : dict
        Credentials and connection information dictionary.

    Returns
    -------
    Conn : pymonetdb.connection
        Active connection to the OMOP database.

    """
    import pymonetdb
    if login_dict is None:

        login_dict = np.load(login_path).item()

    conn = pymonetdb.connect(hostname=login_dict['hostname'],
                             database=login_dict['database'],
                             port=str(login_dict['port']),
                             username=login_dict['username'],
                             password=login_dict['password'])

    return conn
