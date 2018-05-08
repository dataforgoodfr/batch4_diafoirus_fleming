"""Functions to build a dataset."""
import time

import pandas as pd

from .metrics import add_age, add_rolling_avg, add_target
from .utils import to_categorical, to_onehot


def create_dataset(conn, list_patients, verbose=False):
    """Create list of dataset given a list of patients.

    Parameters
    ----------
    conn : pymonetdb.connection
        Active connection to the OMOP database.
    list_patients : list of int
        List of patients ID.
    verbose : bool
        Verbosity level.

    Returns
    -------
    frame : list of pd.DataFrame
        List of datasets, each corresponding to a patient.

    """
    t0 = time.time()
    frame = []

    if not isinstance(list_patients, list):
        list_patients = [list_patients]

    n_patients = len(list_patients)

    # Meta data
    if verbose:
        msg = 'Extracting meta data...'
        delta_t = str(int(time.time() - t0)) + ' s'
        print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

    query = """
    select
        distinct p.person_id, p.gender_source_value gender,
        p.race_source_value race, p.birth_datetime
    from
        person p
        ;"""

    meta = pd.read_sql_query(query, conn)

    # Convert categorical variable to 'categorical' type
    categorical_variables = ['gender', 'race']
    meta = to_categorical(meta, categorical_variables)
    meta = to_onehot(meta, categorical_variables)
    # One-hot column names
    meta_names = meta.columns

    for i, patient in enumerate(list_patients):
        if verbose:
            base_msg = 'Patient {} [{}/{}]'.format(patient, i+1, n_patients)
            msg = base_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        # Measures
        if verbose:
            add_msg = 'Extracting measures...'
            msg = base_msg + ' - ' + add_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        query = """
        select
            distinct m.person_id, m.measurement_datetime,
            m.measurement_concept_name, m.value_source_value,
            m.unit_source_value, d.death_datetime
        from
            measurement m
        left join
            death d on d.person_id = m.person_id
        where
            measurement_concept_id IN
            (3022318,   -- heart_rhythm
             3024171,   -- respiratory_rate
             3028354,   -- vent_settings
             3012888,   -- diastolic_bp
             3027598,   -- map_bp
             3004249,   -- systolic_bp
             3027018,   -- heart_rate
             3020891,   -- temperature
             3016502,   -- spo2
             3020716,   -- fio2
             3032652    -- glasgow coma scale
            )
        and m.person_id = {}
        order by measurement_datetime
            ;""".format(patient)

        df = pd.read_sql_query(query, conn)

        if verbose:
            add_msg = 'Formatting data...'
            msg = base_msg + ' - ' + add_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        df['death_datetime'] = pd.to_datetime(df['death_datetime'])
        df['measurement_datetime'] = pd.to_datetime(df['measurement_datetime'])

        df = add_target(df)

        df = df.pivot_table(
            index=['measurement_datetime', 'target', 'person_id'],
            columns='measurement_concept_name',
            values='value_source_value',
            aggfunc='first')
        df.reset_index(inplace=True)
        df.columns.name = None

        # Convert to numerical
        numerical_variables = [
            'BP diastolic', 'BP systolic', 'Body temperature', 'Heart rate',
            'Mean blood pressure', 'Oxygen saturation in Arterial blood',
            'Respiratory rate']
        df[numerical_variables] = df[numerical_variables].apply(
            pd.to_numeric, errors='ignore')

        # Convert to categorical and one-hot encode it
        categorical_variables = ['Heart rate rhythm']
        df = to_categorical(df, categorical_variables)
        df = to_onehot(df, categorical_variables)

        # Add meta data to measures
        if verbose:
            add_msg = 'Adding meta data...'
            msg = base_msg + ' - ' + add_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        meta_idx = (meta['person_id'] == patient)
        for meta_name in meta_names:
            df[meta_name] = meta[meta_idx][meta_name].values.squeeze()

        df = add_age(df, round_to_dec=1)

        # Add additional features
        if verbose:
            add_msg = 'Adding additional features...'
            msg = base_msg + ' - ' + add_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        df = add_rolling_avg(df, 'Respiratory rate', window=2)

        frame.append(df)

        if verbose:
            msg = 'Patient {} done.'.format(patient)
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')
            print('')

    return frame
