"""Utils functions."""
import warnings

import numpy as np
import pandas as pd


def to_numeric(df, variables=[]):
    """Convert variables to numerical (int or float) type.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe.
    variables : list of str
        List of variables to convert to numerical.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with converted variables.

    """
    # convert to list if one element
    if isinstance(variables, str):
        variables = [variables]
    # check variables
    _check_variables(df, variables)
    # convert to numerical
    for var in variables:
        df[var] = df[var].apply(pd.to_numeric, errors='ignore')

    return df


def to_categorical(df, variables=[], categories=None):
    """Convert variables to categorical type.

    Missing values (NaN) are filled with 'NaN' category.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe.
    variables : list of str
        List of variables to convert to categorical.
    categories : dict of pd.core.indexes.base.Index | None
        If provided, a set of categories to apply to each categorical variable.
        The name fo the corresponding variable should be passed as the key of
        dict. If no cartegories are provided, default ones are kept.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with converted variables.

    """
    # convert to list if one element
    if isinstance(variables, str):
        variables = [variables]
    # check variables
    _check_variables(df, variables)
    # convert to categorical
    for var in variables:
        # df[var] = df[var].apply(pd.Categorical)
        df[var] = df[var].astype('category')
        # convert missing values (NaN) to category 'NaN'
        if 'Nan' not in df[var].cat.categories:
            df[var] = df[var].cat.add_categories('NaN')
        df[var].fillna('NaN', inplace=True)

    if categories:
        if not isinstance(categories, dict):
            raise ValueError('`categories` should be a dict.')
        # set categories of each categorical variable
        for var in variables:
            if var in categories:
                df[var] = df[var].cat.set_categories(categories[var])

    return df


def to_onehot(df, variables=[]):
    """One-hot encode categorical variables.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe.
    variables : list of str
        List of categorical variables to convert to one-hot.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with added one-hot encoded variables.

    """
    # check variables
    _check_variables(df, variables)
    # check whether input variables are categorical
    for var in variables:
        if df[var].dtype != 'category':
            raise ValueError(
                'Variable {} is not categorical, cannot one-hotencode.'.format(
                    var))
    if variables:
        # Get one-hots
        one_hots = pd.get_dummies(df[variables])
        # Drop original variables from dataframe
        df.drop(variables, 1, inplace=True)
        # Add one-hots to dataframe
        df = df.join(one_hots)

    return df


def convert_frac(df, variables):
    """Convert fractions to numerical values.

    Sometimes numbers are represented as literal in the following format
    'N/M' where N and M are integers. What follows convert these literal
    fractions to decimal floats.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    variables : list of str
        List of variables to convert to numerical

    Returns
    -------
    df : pd.DataFrame
        Dataframe with converted data.

    """
    # convert to list if one element
    if isinstance(variables, str):
        variables = [variables]
    # check variables
    _check_variables(df, variables)

    def frac_to_num(row):
        """Convert fraction to numerical."""
        try:
            if hasattr(row, 'str'):
                tmp = row.str.split('/')
            else:
                if isinstance(row, str):
                    tmp = row.split('/')
                else:
                    return row
            if tmp is not None:
                if len(tmp) == 2:
                    num, denum = tmp
                    if not num:
                        tmp = None
                    elif not denum:
                        tmp = float(num)
                    else:
                        if not float(denum) == 0.0:
                            tmp = float(num) / float(denum)
                        else :
                            tmp = float('NaN')
                else:
                    tmp = float(tmp[0])
            return tmp
        except ValueError:
            return row

    for var in variables:
        df[var] = df[var].apply(lambda x: frac_to_num(x))
        # convert to numerical type
        df[var] = df[var].apply(pd.to_numeric, errors='ignore')

    return df


def add_categories(categories, df, variables):
    """Convert fractions to numerical values.

    Sometimes numbers are represented as literal in the following format
    'N/M' where N and M are integers. What follows convert these literal
    fractions to decimal floats.

    Parameters
    ----------
    categories : dict of dict of pd.core.indexes.base.Index
        Dictionary containing categories corresponding to each variable (
        passed as a key).
    df : pd.DataFrame
        Input dataframe.
    variables : list of str
        List of variables to convert to numerical

    Returns
    -------
    categories : dict of dict of pd.core.indexes.base.Index
        Dictionary with added categories for the given input variables.

    """
    # convert to list if one element
    if isinstance(variables, str):
        variables = [variables]
    # check variables
    _check_variables(df, variables)

    if not categories:  # create empty dict
        categories = dict()
    if not isinstance(categories, dict):
            raise ValueError('`categories` should be a dict (even empty).')

    # copy
    tmp = df.copy(deep=True)
    # convert to categorical
    to_categorical(tmp, variables)

    for var in variables:
        # checking input type
        if tmp[var].dtype != 'category':
            raise ValueError(
                'Variable {} is not categorical, cannot one-hotencode.'.format(
                    var))
        categ_values = tmp[var]
        categ_values = categ_values.astype('category')
        # checking already-existing conflict
        if var in categories:
            wrn = '`{}` already in dict `categories`: overwriting.'.format(var)
            warnings.warn(wrn)
        categories[var] = categ_values.cat.categories

    return categories


def add_missing_columns(df, variables):
    """Add column if missing and fill it with NaN values.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    variables : list of str
        List of variables to check.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with added missing columns.

    """
    # convert to list if one element
    if isinstance(variables, str):
        variables = [variables]
    for var in variables:
        if var not in df:
            df[var] = np.nan
            wrn = ('Colmun `{}` missing: adding it and filling with '
                   'NaN.'.format(var))
            warnings.warn(wrn)

    return df


def check_length(df):
    """Check whether some patients have empty data.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.

    """
    _check_variables(df, 'person_id')
    data_lengths = df.groupby('person_id').apply(len).reset_index()
    for index, row in data_lengths.iterrows():  # iter through patients
        if row[0] == 0:  # check if empty
            warnings.warn('No data for patient {}'.format(row.person_id))


def _check_variables(df, variables):
    """Check if `variables` are contained in input dataframe."""
    if variables is not None:
        if isinstance(variables, str):
            variables = [variables]
        for var in variables:
            if var not in df:
                raise ValueError('`{}` not in dataframe.'.format(var))


def _all_nat_check(df):
    """Check if all value are NaN (returns True) or not."""
    return np.all(pd.isnull(df))


def _any_nat_check(df):
    """Check if any value is NaN (returns True) or not."""
    return np.any(pd.isnull(df))


def get_nat_columns(df, columns=None):
    """Get all columns in input dataframe with missing values.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    columns : list of str | None
        List of columns to check.
        If None, automatically select columns from `df`.

    Returns
    -------
    nat_columns : list of str
        List out columns with missing values

    """
    # convert to list if one element
    if columns is None:
        columns = df.columns
    else:
        if isinstance(columns, str):
            columns = [columns]
        _check_variables(df, columns)

    nat_columns = []

    for column in columns:
        if _any_nat_check(df[column]):
            nat_columns.append(column)

    return nat_columns
