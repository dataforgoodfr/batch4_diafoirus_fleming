"""Utils functions."""
import pandas as pd


def to_categorical(df, variables=[]):
    """Convert variables to categorical type.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe.
    variables : list of str
        List of variables to convert to categorical.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with converted variables.

    """
    for var in variables:
        df[var] = df[var].astype('category')

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
    # Check whether input variables are categorical
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


def convert_frac(df, column):
    """Convert fractions to numerical values.

    Sometimes numbers are represented as literal in the following format
    'N/M' where N and M are integers. What follows convert these literal
    fractions to decimal floats.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    column : str
        Name of the column to convert to float.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with added column.

    """
    if column not in df:
        raise ValueError('`{}` not in dataframe.'.format(column))

    def frac_to_num(row):
        """Convert fraction to numerical."""
        try:
            if hasattr(row[column], 'str'):
                tmp = row[column].str.split('/')
            else:
                if isinstance(row[column], str):
                    tmp = row[column].split('/')
                else:
                    return row[column]
            if tmp is not None:
                if len(tmp) == 2:
                    num, denum = tmp
                    if not num:
                        tmp = None
                    elif not denum:
                        tmp = float(num)
                    else:
                        tmp = float(num) / float(denum)
                else:
                    tmp = float(tmp[0])
            return tmp
        except ValueError:
            return row[column]

    df[column] = df.apply(lambda x: frac_to_num(x), axis=1)

    # convert to numerical type
    df[column] = df[column].apply(pd.to_numeric, errors='ignore')

    return df
