#!/usr/bin/python
#######################################################################################
#######################################################################################
#
#	Name: data_utils.py
#	Usage: from data_utils import pull_data_from_bigquery
#	Description: Contains data processing methods to be used by all projects
#
#
#
#
#	Modification Log:
#	2018-03-13			Annie Castner				Initial creation
#   2018-08-29          Annie Castner               splitting out gcp utils
#
#######################################################################################

from pandas.io import gbq
import math
from math import radians, cos, sin, asin, sqrt
#import googlemaps
import pandas as pd
import datetime
from google.cloud import storage
#import io
import os
from tzwhere import tzwhere


def cartesian_join(df1, df2):
    """ Performs cartesian join between 2 pandas df's

    Parameters
    ----------
    df1: pandas df

    df2: pandas df

    Returns
    -------
    Pandas DataFrame with the df1 cartesian joined to df2.

    Note:
    Order of columns is df1 cols then df2.
    Assumes no columns with same name in both frames (except the key column we create)
    """
    # Create a new df cartesian join df1 and df2

    df1['key'] = 0
    df2['key'] = 0
    df = pd.merge(df1, df2, how='left', on='key').drop('key', axis=1)

    return df


def date_range_list(start_date=None, end_date=None, days=1):
    """ Returns a list of dates from start to end (inclusive of ends)

    Parameters
    ----------
    start_date:

    end_date: pandas df

    Returns
    -------
    List

    Note:
    Assumes start date is earlier in time than end date
    """
    # Create a list of dates

    if start_date is None:
        start_date = datetime.date.today()

    # default is 2 week date range. 13 delta instead of 14 (1st day is today date, plus 13 more)
    if end_date is None:
        end_date = start_date + datetime.timedelta(days)
    date_list = pd.date_range(start=start_date, end=end_date)
    #date_list = list(pd.date_range(start_date, end_date))
    #date_strings = [d.strftime('%m-%d-%Y') for d in date_list]
    return str(start_date), str(end_date), date_list #date_strings


def date_hour_start_end(duration):
    """ Returns start and end date given the duration of the job

    Parameters
    ----------
    duration:
    int number of days. default is 1 day (we make predictions for just one day usually

    Returns
    -------
    date1, hour1, date2, hour2

    Note:
    Assumes start date is earlier in time than end date
    """
    # Return days and hours to use as parameters
    start_date = datetime.datetime.now()

    end_date = start_date + datetime.timedelta(days=duration)

    hour1 = start_date.hour
    hour2 = end_date.hour

    return start_date, hour1, end_date, hour2


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956  # Radius of earth in miles. Use 6371 for km
    return c * r


def upsample(data, labels):
    """
    Using upsampling to balance the classes. Note that every data point is included at least once
    and additional data points are added by sampling with replacement.
    """
    from collections import defaultdict
    import random

    label_indices = defaultdict(lambda: list())
    for idx, label in enumerate(labels):
        label_indices[label].append(idx)

    largest_class_size = max(map(lambda l: len(l), label_indices.values()))

    upsampled_indices = []
    for label, indices in label_indices.items():
        sampled_indices = indices[:]
        while len(sampled_indices) < largest_class_size:
            sampled_indices.append(random.choice(indices))
        upsampled_indices.extend(sampled_indices)

    upsampled_labels = labels[upsampled_indices]
    upsampled_data = data[upsampled_indices, :]

    return upsampled_data, upsampled_labels


def split_by_label(data, labels, test_split_fraction):
    """
    Randomly split the data and labels into training and test sets, but do the split by label so that
    the class sizes are preserved.
    """
    from collections import defaultdict
    import random

    label_indices = defaultdict(lambda: list())
    for idx, label in enumerate(labels):
        label_indices[label].append(idx)

    test_indices = []
    train_indices = []
    for label, indices in label_indices.items():
        shuffled_indices = indices[:]
        random.shuffle(shuffled_indices)
        test_size = int(len(indices) * test_split_fraction)
        train_size = len(indices) - test_size
        test_indices.extend(shuffled_indices[:test_size])
        train_indices.extend(shuffled_indices[test_size:])

    test_labels = labels[test_indices]
    test_data = data[test_indices, :]

    train_labels = labels[train_indices]
    train_data = data[train_indices, :]

    return train_data, test_data, train_labels, test_labels


def timezone_by_coords(row):
    tzw = tzwhere.tzwhere()
    timezone_str = tzw.tzNameAt(row.lat, row.long)
    if timezone_str is None:
        timezone_str = 'America/Los_Angeles'
    return timezone_str


def csv_to_df(filename, header, delim):
    data = pd.read_csv(filename, header=header, sep=delim)
    return data
