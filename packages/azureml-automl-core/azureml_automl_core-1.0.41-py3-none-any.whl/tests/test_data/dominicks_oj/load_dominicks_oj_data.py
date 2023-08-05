"""Utility to load the Dominick's Orange Juice data into a TimeSeriesDataFrame."""
from datetime import timedelta
import inspect
import math
import os

import pandas as pd

from automl.client.core.common.forecasting_ts_utils import last_n_periods_split
from automl.client.core.common.time_series_data_frame import TimeSeriesDataFrame

DOMINICKS_OJ_FILE_NAME = 'dominicks_oj.csv'
DOMINICKS_OJ_FEATURE_FILE_NAME = 'dominicks_oj_features.csv'
DOMINICKS_OJ_DATA_PATH = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())
))  # this directory


def load_dominicks_oj_dataset(data_path=DOMINICKS_OJ_DATA_PATH,
                              test_size=40):
    """
    Partitions the Domninick's OJ dataset into training and test dataset.

    For each grain, the last `test_size` records are used to create test
    dataset.

    .. _bayesm.package: https://www.rdocumentation.org/packages/bayesm/versions/3.0-2/topics/orangeJuice

    A larger dataset is available in R as part of the bayesm.package_.

    :param data_path: absolute path to the data directory
    :type data_path: str

    :param test_size:
        how many data points 'per grain' are set aside for
        test data.
    :type test_size: int

    :return:
        A 2-tuple of TimeSeriesDataFrame objects, first element is training
        data and second element is test data.
    :rtype: tuple
    """
    whole_data = pd.read_csv(
        os.path.join(data_path, DOMINICKS_OJ_FILE_NAME),
        low_memory=False)

    # Convert sales column to float:
    # values are logarithmic - exponentiate and round
    def expround(x):
        return math.floor(math.exp(x) + 0.5)
    whole_data['Quantity'] = whole_data['logmove'].apply(expround)

    # From SAS-exported data, it looks like
    # week 0 is that of 1989-09-07 through 1989-09-13 inclusive.
    weekZeroStart = pd.to_datetime('1989-09-07 00:00:00')
    weekZeroEnd = pd.to_datetime('1989-09-13 23:59:59')

    whole_data['WeekFirstDay'] = \
        whole_data['week'].apply(lambda n: weekZeroStart + timedelta(weeks=n))
    whole_data['WeekLastDay'] = \
        whole_data['week'].apply(lambda n: weekZeroEnd + timedelta(weeks=n))

    whole_data_ts = TimeSeriesDataFrame(whole_data,
                                        grain_colnames=['store', 'brand'],
                                        time_colname='WeekLastDay',
                                        ts_value_colname='Quantity')
    whole_data_ts.sort_index(inplace=True)

    train_data_ts, test_data_ts = last_n_periods_split(whole_data_ts, test_size)

    return train_data_ts, test_data_ts


def load_dominicks_oj_features(data_path=DOMINICKS_OJ_DATA_PATH, test_size=40):
    """
    Returns the Domninicks OJ dataset with additional features generated by
    the forecasting package transformers.

    :param data_path: absolute path to the data directory
    :type data_path: str

    :param test_size:
        how many data points 'per grain' are set aside for
        test data.
    :type test_size: int

    :return:
        A 2-tuple of TimeSeriesDataFrame objects, first element is training
        data with features and second element is test data with features.
    :rtype: tuple
    """

    feature_df = pd.read_csv(
        os.path.join(data_path, DOMINICKS_OJ_FEATURE_FILE_NAME),
        low_memory=False)

    feature_df['WeekLastDay'] = pd.to_datetime(feature_df['WeekLastDay'])

    feature_tsdf = TimeSeriesDataFrame(feature_df,
                                       grain_colnames=['store', 'brand'],
                                       time_colname='WeekLastDay',
                                       ts_value_colname='Quantity',
                                       group_colnames='store')
    feature_tsdf.sort_index(inplace=True)

    train_feature_tsdf, test_feature_tsdf = last_n_periods_split(
        feature_tsdf, test_size)

    return train_feature_tsdf, test_feature_tsdf


def load_dominicks_oj_into_pandas(data_path=DOMINICKS_OJ_DATA_PATH):
    """
    Returns the Domninicks OJ dataset with additional features generated by
    the forecasting package transformers.

    :param data_path: absolute path to the data directory
    :type data_path: str

    :return:
        pre-processed Dominicks OJ data in pandas.DataFrame
    :rtype: pandas.DataFrame
    """
    whole_df = pd.read_csv(
        os.path.join(data_path, DOMINICKS_OJ_FILE_NAME),
        low_memory=False)

    def expround(x):
        return math.floor(math.exp(x) + 0.5)

    whole_df['Quantity'] = whole_df['logmove'].apply(expround)
    week_zero_start = pd.to_datetime('1989-09-07 00:00:00')
    week_zero_end = pd.to_datetime('1989-09-13 23:59:59')
    whole_df['WeekFirstDay'] = whole_df['week'].apply(
        lambda n: week_zero_start + timedelta(weeks=n))
    whole_df['WeekLastDay'] = whole_df['week'].apply(
        lambda n: week_zero_end + timedelta(weeks=n))
    whole_df['LogQuantity'] = whole_df['logmove'].values
    whole_df['WeekNumber'] = whole_df['week'].values
    cols_to_use = ['store', 'brand', 'WeekLastDay', 'Quantity',
                   'feat', 'price', 'AGE60', 'EDUC', 'ETHNIC', 'INCOME',
                   'HHLARGE', 'WORKWOM', 'HVAL150', 'SSTRDIST', 'SSTRVOL',
                   'CPDIST5', 'CPWVOL5', 'WeekFirstDay', 'LogQuantity',
                   'WeekNumber']
    return whole_df[cols_to_use]


if __name__ == '__main__':

    train_data_ts, test_data_ts = load_dominicks_oj_dataset()
    print(train_data_ts.ts_summary())
