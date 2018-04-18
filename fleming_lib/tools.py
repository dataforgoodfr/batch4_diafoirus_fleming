#!/usr/bin/env python

'''
These functions were developped as tools for the Fleming project

'''

__author__ = 'François-Guillaume Fernandez'
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'François-Guillaume Fernandez'
__status__ = 'Development'


def progress_bar(count, total, status=''):
    """
    Display a progress bar

    Args:
        count (int): number of iterations already performed
        total (int): total number of iterations
        status (str): status information you want to print out
    """
    import sys
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 2)
    bar = '=' * (filled_len - 1) + '>' + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def connect_to_omop(login_dict):
    """
    Provide a PostGreSQL connection to the MIMIC db in OMOP format

    Args:
        login_dict (dict): credentials and connection information dictionary

    Returns:
        conn (pymonetdb.connection): active connection to the OMOP database
    """
    import pymonetdb
    conn = pymonetdb.connect(hostname=login_dict['hostname'], database=login_dict['database'], port=str(login_dict['port']),
                             username=login_dict['username'], password=login_dict['password'])

    return conn
