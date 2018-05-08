"""Add metrics."""
from datetime import timedelta

import numpy as np

from .utils import convert_frac


def add_age(df, round_to_dec=1):
    """Add column containing 'age' in years.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    round_to_dec : int, optional (default=1)
        Number of decimals to round age (in years) to.

    Returns
    -------
    df : pd.DataFrame
        Dataframe containing 'age' column.

    """
    if 'birth_datetime' not in df:
        raise ValueError('Must provide `birth_datetime` to compute age.')
    if 'measurement_datetime' not in df:
        raise ValueError('Must provide `measurement_datetime` to compute age.')

    def compute_age(row):
        """Compute age."""
        return row['measurement_datetime'] - row['birth_datetime']

    df['age'] = df.apply(lambda x: compute_age(x), axis=1)
    df['age'] = np.round((df['age']).dt.days / 365.25, decimals=round_to_dec)
    df.drop('birth_datetime', inplace=True, axis=1)

    return df


def add_rolling_avg(df, column, window):
    """Add rolling average computed over a given column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    column : str
        Name of the column to compute rolling mean over.
    window : int | float
        Time interval (in hours) to compute rolling average over.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with added column.

    """
    if column not in df:
        raise ValueError('`{}` not in dataframe.'.format(column))
    if 'measurement_datetime' not in df:
        raise ValueError('Must provide `measurement_datetime` to compute '
                         'rolling average.')

    # Convert to numerical
    df = convert_frac(df, column)

    def compute_rolling_avg(row, df, column, window):
        """Compute rolling average."""
        filter_df = df[
            (df['measurement_datetime'] >=
             (row['measurement_datetime'] - timedelta(hours=window))) &
            (df['measurement_datetime'] < row['measurement_datetime'])]
        try:
            return filter_df[column].mean()
        except ValueError:
            return float('nan')

    new_column = column + ' avg h-{}'.format(int(window))

    df[new_column] = df.apply(
        lambda x: compute_rolling_avg(x, df, column, window), axis=1)

    return df


def add_target(df, name='target'):
    """Add target (whether the patient is dead at the time of measurement).

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    name : str, optional (default='target')
        Name of the 'target' column.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with added 'target' column.

    """
    if 'death_datetime' not in df:
        raise ValueError('Must provide `birth_datetime` to compute age.')
    if 'measurement_datetime' not in df:
        raise ValueError('Must provide `measurement_datetime` to compute age.')

    def compute_target(row):
        """Compute target value."""
        if row['death_datetime'] <= row['measurement_datetime']:
            val = 1
        else:
            val = 0
        return val

    df[name] = df.apply(compute_target, axis=1)

    return df
