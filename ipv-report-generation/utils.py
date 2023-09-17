# -*- coding: utf-8 -*-
"""
    pyinfluxql.utils
    ~~~~~~~~~~~~~~~~

    Utility functions
"""

from datetime import timedelta
from utility import DateTimeInterval
import os
import math


def parse_interval(interval):
    unit = interval[-1]
    scalar = int(interval[:-1])
    if unit == 's':
        key = 'seconds'
    elif unit == 'm':
        key = 'minutes'
    elif unit == 'h':
        key = 'hours'
    elif unit == 'd':
        key = 'days'
    else:
        key = 's'
    return timedelta(**{key: scalar})


def format_timedelta(td):
    """formats a timedelta into the largest unit possible
    """
    total_seconds = td.total_seconds()
    units = [(604800, 'w'), (86400, 'd'), (3600, 'h'), (60, 'm'), (1, 's')]
    for seconds, unit in units:
        if total_seconds >= seconds and total_seconds % seconds == 0:
            return "%r%s" % (int(total_seconds / seconds), unit)
    if total_seconds >= 0.001:
        if (total_seconds / 0.001) % 1 == 0:
            return "%r%s" % (int(total_seconds * 1000), 'ms')
        else:
            micro = int(total_seconds / 0.000001)
            micro += int(total_seconds % 0.000001)
            return "%r%s" % (micro, 'us')
    return "%r%s" % (int(total_seconds * 1000000), 'us')


def format_boolean(value):
    return 'true' if value else 'false'


def get_resource_dir():
    '''
    create resource directory or if exists then return the directory instead of creation
    '''
    project_dir = os.path.abspath('main.py').split('main.py')[0]
    img_dir = project_dir + 'resources'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    return img_dir

def set_yrange(max_min_data, max_col, min_col):
    '''
    calculate yaxis range and set that range for multiple chart(now only for bar chart)
    '''
    df = join_dataframes(max_min_data)
    max_list = []
    min_list = []
    for mx in max_col:
        max_list.append(df[mx].tolist()[0])
    for mn in min_col:
        min_list.append(df[mn].tolist()[0])
    DateTimeInterval.ymax = max(max_list)
    DateTimeInterval.ymin = min(min_list)


def join_dataframes(raw_data):
    first = True
    for key in raw_data.keys():
        if (first):
            dataframe = raw_data[key]
            first = False
            continue
        dataframe = dataframe.join(raw_data[key])
    dataframe = dataframe.dropna()
    return dataframe


def set_ticks(dataframe):
    dtime_interval = DateTimeInterval()
    global ticks
    ticks = dtime_interval.get_xyticks(dataframe)
    return

def get_ticks():
    return ticks

def get_formatted_time(duration_minutes):
    if(duration_minutes < 60):
        return str(duration_minutes) + 'm'
    elif(duration_minutes >= 60 and duration_minutes < (24 * 60)):
        minutes, hours = math.modf(float(duration_minutes) / float(60))
        minutes = minutes * 60
        if minutes > 1:
            return str(int(hours)) + 'h ' + str(int(minutes)) + 'm'
        else:
            return str(int(hours)) + 'h'
    else:
        hours, days = math.modf(float(duration_minutes) / float(24 * 60))
        hours = hours * 24
        if hours > 1:
            return str(int(days)) + 'd ' + str(int(hours)) + 'h'
        else:
            return str(int(days)) + 'd'