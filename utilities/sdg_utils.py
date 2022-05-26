#!/usr/bin/python
#######################################################################################
#######################################################################################
#
#	Name: sdg_utils.py
#	Usage: sdg_utils
#	Description: Contains data processing methods to be used by sdg
#
#
#
#
#	Modification Log:
#	2019-03-28			Annie Castner				Initial creation
#
#######################################################################################

import math
import pandas as pd
import datetime
import numpy as np
import names
import random
from uuid import uuid4
from dateutil import parser
from faker import Faker
fake = Faker()


def name_generator(name, size, name_type='full'):
    """ Creates Names (first, last, full) for given size

    Parameters
    ----------
    name: desired field name

    size: integer number of responses to return

    name_type: first, last, full

    Returns
    -------
    Pandas DataFrame with the desired name field of desired size

    """
    # Create a dictionary to store names
    data_dict = {}

    # get first and last names
    if name_type == 'first':
        data_dict[name] = [names.get_first_name() for x in range(size)]
    elif name_type == 'last':
        data_dict[name] = [names.get_last_name() for x in range(size)]
    else:
        data_dict[name] = [names.get_full_name() for x in range(size)]

    # convert dictionary to dataframe
    df = pd.DataFrame(data_dict)

    return df


def datetime_generator(size, name, start_date, end_date, frequency="random", date_type='datetime'):
    """ Creates Dates and Times (first, last, full) for given size and frequency

    Parameters
    ----------
    size: integer number of responses to return

    name: desired name appendage

    start_date: starting date of values

    end_date: end date of values

    date_type: date or datetime

    frequency: random or a frequency from following list:
    https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases

    Returns
    -------
    Pandas DataFrame with the desired date/time columns

    """
    parsed_start = parser.parse(start_date)
    parsed_end = parser.parse(end_date)

    if frequency == 'random':
        if date_type == 'date':
            dates = [fake.date_between(start_date=parsed_start, end_date=parsed_end) for x in range(size)]
        else:
            dates = [fake.date_time_between(start_date=parsed_start, end_date=parsed_end) for x in range(size)]
    else:
        dates = pd.date_range(start=start_date, end=end_date, freq=frequency).tolist()

    df = pd.DataFrame(dates, columns=[name])
    return df


def metric_generator(size, name, met_type='float', min_val=0, max_val=100, dist='normal'):
    """ Creates Metric for given size, name, type (float or int), min, and max

    Parameters
    ----------
    size: integer number of responses to return

    name: string, desired column name

    met_type: float or int

    min_val: minimum value of metric

    max_val: maximum value of metric

    dist: uniform or normal

    Returns
    -------
    Pandas DataFrame with the desired metric in desired distribution

    """

    if dist == 'uniform':
        metric_list = [random.uniform(min_val, max_val) for x in range(size)]
    else:
        mu = min_val + ((max_val - min_val) / 2)
        sigma = (max_val - min_val)/10
        metric_list = [random.gauss(mu, sigma) for x in range(size)]

    if met_type == 'int':
        metric_list = [round(x) for x in metric_list]
    else:
        metric_list = [round(x, 2) for x in metric_list]

    df = pd.DataFrame(metric_list, columns=[name])
    return df


def categorical_generator(size, name, categories, dist):
    """ Creates Categorical column for given size, name, categories list, and distribution of values

    Parameters
    ----------
    size: integer number of responses to return

    name: string, desired column name

    categories: list of categorical values

    dist: list of distribution of categories -- elements must sum to 1

    Returns
    -------
    Pandas DataFrame with the desired categorical column

    """
    # b = random.choices(population=[1,2,3,4,5], weights=[0.5, 0.2, 0.1, 0.1, 0.1], k=50)
    cat_list = random.choices(population=categories, weights=dist, k=size)
    df = pd.DataFrame(cat_list, columns=[name])
    return df


def location_generator(size, name, loc_type):
    """ Creates Location data for given size, name, type

    Parameters
    ----------
    size: integer number of responses to return

    name: string, desired column name

    loc_type: string, address type to generate

    Returns
    -------
    Pandas DataFrame with the desired metric

    """
    # data dict to hold elements
    data_dict = {}

    # get address elements
    if loc_type == 'street address':
        data_dict[name] = [fake.street_address() for x in range(size)]
    elif loc_type == 'city':
        data_dict[name] = [fake.city() for x in range(size)]
    elif loc_type == 'state':
        data_dict[name] = [fake.state_abbr() for x in range(size)]
    elif loc_type == 'zip':
        data_dict[name] = [fake.postcode() for x in range(size)]
    elif loc_type == 'full':
        data_dict[name] = [fake.address() for x in range(size)]

    # convert to df
    df = pd.DataFrame(data_dict)

    # add full address field
    # cols = df.columns
    # df[name + ' Full Address'] = df[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

    # TODO must add lat and long to map to address
    # TODO must add ability to filter / change locations. international, certain states, etc
    # TODO country / country code

    return df


def contact_generator(size, name, contact_type):
    """ Creates Contact data for given size, name, type

    Parameters
    ----------
    size: integer number of responses to return

    name: string, desired column name

    contact_type: string, email or phone

    Returns
    -------
    Pandas DataFrame with the desired metric

    """
    # data dict to hold elements
    data_dict = {}
    # domains = ["hotmail.com", "gmail.com", "aol.com", "yahoo.com", "cox.net"]

    # get address elements
    if contact_type == 'email':
        data_dict[name] = [fake.email() for x in range(size)]
    else:
        data_dict[name] = [fake.phone_number() for x in range(size)]

    # convert to df
    df = pd.DataFrame(data_dict)

    # TODO phone area code dependent on state
    # TODO email dependent on name, maybe company
    # TODO email addresses at one company with same email format

    return df


def formatted_data_generator(size, name, format):
    """ Creates similarly formatted data for given size, name, format

    Parameters
    ----------
    size: integer number of responses to return

    name: string, desired column name

    format: string, the format to reproduce

    Returns
    -------
    Pandas DataFrame with the desired metric

    """
    # data dict to hold elements
    data_dict = {}

    # convert to df
    df = pd.DataFrame(data_dict)

    return df


def contact_generator(size, name, contact_type):
    """ Creates Contact data for given size, name, type

    Parameters
    ----------
    size: integer number of responses to return

    name: string, desired column name

    contact_type: string, email or phone

    Returns
    -------
    Pandas DataFrame with the desired metric

    """
    # data dict to hold elements
    data_dict = {}
    # domains = ["hotmail.com", "gmail.com", "aol.com", "yahoo.com", "cox.net"]

    # get address elements
    if contact_type == 'email':
        data_dict[name] = [fake.email() for x in range(size)]
    else:
        data_dict[name] = [fake.phone_number() for x in range(size)]

    # convert to df
    df = pd.DataFrame(data_dict)

    # TODO phone area code dependent on state
    # TODO email dependent on name, maybe company
    # TODO email addresses at one company with same email format

    return df


def uuid_generator(size, name):
    """ Creates a uuid for given size, name, format

    Parameters
    ----------
    size: integer number of responses to return

    name: string, desired column name

    Returns
    -------
    Pandas DataFrame with the desired uuid

    """
    # data dict to hold elements
    data_dict = {}

    data_dict[name] = [uuid4() for x in range(size)]
    # convert to df
    df = pd.DataFrame(data_dict)

    return df

