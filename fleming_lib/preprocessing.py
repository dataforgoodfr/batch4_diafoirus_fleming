"""Preprocessing functions."""
import warnings

from datetime import timedelta

import pandas as pd
from .utils import _check_variables, get_nat_columns


def fill_last_upto(df, variables=None, h=timedelta(hours=24),
                   warning=False):
    """Fill missing value in input dataframe up to a given time.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    variables : list of str | None
        List of variables to process.
        If None, automatically select columns with missing values
    h : datetime.timedelta
        Time interval to fetch data up to.
    warning : bool
        If True, print warnings.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with added missing columns.

    """
    # Convert to list if one element
    if isinstance(variables, str):
        variables = [variables]
    # Check variables
    _check_variables(df, variables)
    _check_variables(df, 'measurement_datetime')

    # Process only columns with missing values.
    variables = get_nat_columns(df, variables)

    # Copy input dataframe
    tmp = df.copy(deep=True)

    # Time-reverse dataframe (assuming it is sorted by measurement_datetime!)
    tmp = tmp.iloc[::-1]

    def _last_valid(row, df, column, h):
        """Return last valid value up to time h prior to current datetime."""
        if pd.isnull(row[column]):  # is missing value
            # Get last (in time) valid index (but first in loc as dataframe was
            # time-reversed here)
            last_valid_index = (
                df[df['measurement_datetime'] <
                   row['measurement_datetime']][column].first_valid_index())

            # Check if posterior to -h
            if last_valid_index is None:
                if warning:
                    wrn = ('[WARNING]: could not find valid index anterior to '
                           '{} for variable {}.'.format(
                               row['measurement_datetime'], column))
                    warnings.warn(wrn)
                return pd.NaT
            else:
                if (df.loc[last_valid_index]['measurement_datetime'] -
                   row['measurement_datetime'] < h):
                    return df.loc[last_valid_index][column]
                else:
                    return pd.NaT
        else:
            return row[column]

    # Apply function to every column in `columns`
    for var in variables:
        tmp[var] = df.apply(lambda x: _last_valid(x, tmp, var, h), axis=1)

    # Time-back-reverse dataframe (assuming it is sorted by
    # measurement_datetime!)
    df = tmp.iloc[::-1]

    return df
