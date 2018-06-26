"""Functions to build a dataset."""
import time

import pandas as pd

from fleming_lib.metrics import (add_age, add_rolling_avg, add_target,
                                 add_super_target)
from fleming_lib.utils import (add_categories, add_missing_columns,
                               check_length, convert_frac, to_categorical,
                               to_numeric, to_onehot)


def create_dataset(conn, list_patients, n_patients_per_batch=10,
                   verbose=False):
    """Create list of dataset given a list of patients.

    Parameters
    ----------
    conn : pymonetdb.connection
        Active connection to the OMOP database.
    list_patients : list of int
        List of patients ID.
    n_patients_per_batch : int (default=10)
        Number of patients to sequentially load data for, in order not to cause
        timeout if the query is too long to process by the server.
    verbose : bool (default=False)
        Verbosity level.

    Returns
    -------
    dataset : pd.DataFrame
        Dataset containing all data associated to each patient.

    """
    t0 = time.time()
    frame = []

    if not isinstance(list_patients, list):
        list_patients = [list_patients]

    n_patients = len(list_patients)

    # Extract meta data
    # -----------------
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

    # Dictionary containing unique categories for each categorical variable
    categories = dict()

    # Convert categorical variable to 'categorical' type
    categorical_variables = ['gender', 'race']
    # Extracting categories for each categorical variable
    categories = add_categories(categories, meta, categorical_variables)

    meta = to_categorical(meta, categorical_variables, categories)
    meta = to_onehot(meta, categorical_variables)

    # Extract unique measurements values from categorical variables
    # (here 'Heart rate rhythm')
    query = """
        select
            distinct m.measurement_concept_name, m.value_source_value
        from
            measurement m
        where
            m.measurement_concept_id in
            (3022318   -- heart_rhythm
            )
        order by
            m.measurement_concept_name, m.value_source_value
        ;"""

    unique_categ_values = pd.read_sql_query(query, conn)
    categorical_variables = ['Heart rate rhythm']
    # Adding categories of each categorical variables to dict 'categories'
    for var in categorical_variables:
        tmp = unique_categ_values.loc[
            unique_categ_values.measurement_concept_name == var]
        tmp.drop('measurement_concept_name', axis=1, inplace=True)
        tmp.rename(index=str, columns={'value_source_value': var},
                   inplace=True)
        categories = add_categories(categories, tmp, var)

    # Create sublist of patients (batch)
    sublists_patients = [list_patients[i: i+n_patients_per_batch]
                         for i in range(0, n_patients, n_patients_per_batch)]
    n_sublists = len(sublists_patients)

    # Extracting data for each patient
    for i, sublist_patients in enumerate(sublists_patients):
        if verbose:
            base_msg = 'Batch {}/{}'.format(i+1, n_sublists)
            msg = base_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        # Extract measures
        # ----------------
        if verbose:
            add_msg = 'Extracting measures...'
            msg = base_msg + ' - ' + add_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        if len(sublist_patients) == 1:
            match_person = "m.person_id = {}".format(sublist_patients[0])
        else:
            match_person = "m.person_id in {}".format(tuple(sublist_patients))

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
             3032652,   -- glasgow coma scale
             
             -- chemicals
             3019550,   -- sodium serum/plasma (en) | natremie (fr)
             3023103,   -- potassium serum/plasma (en) | kaliemie (fr)
             3024128,   -- bilirubin
             
             -- hemato
             3003282    -- Leukocytes [#/volume] in Blood by Manual count
            )
        and {}
        order by measurement_datetime
            ;""".format(match_person)

        df = pd.read_sql_query(query, conn)

        # Check if data is empty for a patient
        check_length(df)

        if verbose:
            add_msg = 'Formatting data...'
            msg = base_msg + ' - ' + add_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        df['death_datetime'] = pd.to_datetime(df['death_datetime'])
        df['measurement_datetime'] = pd.to_datetime(df['measurement_datetime'])

        # Add target: patients' death' status
        # - relative to the measurement datetime ('target')
        # - relative to the hospital stay ('super-target')
        df = df.groupby('person_id').apply(add_target)
        df = df.groupby('person_id').apply(add_super_target)

        # Convert to timeseries matrix
        df = df.pivot_table(
            index=['measurement_datetime', 'target',
                   'super_target', 'person_id'],
            columns='measurement_concept_name', values='value_source_value',
            aggfunc='first')
        df.reset_index(inplace=True)
        df.columns.name = None

        # Convert types
        # -------------
        # Convert to numerical
        numerical_variables = [
            'BP diastolic', 'BP systolic', 'Body temperature', 'Heart rate',
            'Mean blood pressure', 'Glasgow coma scale',
            'Oxygen concentration breathed',
            'Mean pressure Respiratory system airway Calculated',
            'Oxygen saturation in Arterial blood', 'Respiratory rate',
            'Leukocytes [#/volume] in Blood by Manual count',
            'Potassium serum/plasma', 'Sodium serum/plasma', 'Total Bilirubin serum/plasma'
        ]

        df = add_missing_columns(df, numerical_variables)

        df = convert_frac(df, numerical_variables)
        df = to_numeric(df, numerical_variables)

        # Convert to categorical and one-hot encode
        categorical_variables = ['Heart rate rhythm']

        df = add_missing_columns(df, categorical_variables)

        df = to_categorical(df, categorical_variables, categories)
        df = to_onehot(df, categorical_variables)

        # Add meta data to measures
        # -------------------------
        if verbose:
            add_msg = 'Adding meta data...'
            msg = base_msg + ' - ' + add_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        df = pd.merge(df, meta, how='inner', on='person_id')

        # Add additional features
        # -----------------------
        if verbose:
            add_msg = 'Adding additional features...'
            msg = base_msg + ' - ' + add_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')

        # - age
        df = df.groupby('person_id').apply(add_age, round_to_dec=1)
        # - 2h rolling average respiratory rate
        df = df.groupby('person_id').apply(
            add_rolling_avg, column='Respiratory rate', window=2)

        frame.append(df)

        if verbose:
            add_msg = 'Done'
            msg = base_msg + ' - ' + add_msg
            delta_t = str(int(time.time() - t0)) + ' s'
            print('{:100s} [{:10s}]'.format(msg, delta_t), end='\r')
            print('')

    # Concat dataframes
    dataset = pd.concat(frame)
    dataset = dataset.reindex_axis(frame[0].columns, axis=1)

    return dataset
