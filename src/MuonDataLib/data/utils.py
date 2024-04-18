import numpy as np
import datetime


# some useful names
INT32 = np.int32
FLOAT32 = np.float32


def convert_date_for_NXS(date):
    """
    A method to change the date object into the
    format needed for the muon nexus v2 file
    :param data: the date object
    :return: a string of the date
    (<year>-<month>-<day>T<hour>:<min><sec>)
    """
    return date.strftime('%Y-%m-%dT%H:%M:%S')


def convert_date(date):

    """
    Convert the muon nexus v2 file data string into a
    date object.
    Assume in the form f'{year} {month} {day}', time
    :param date: the date string in the above format
    :return: the date object
    """

    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')


def stype(string):
    """
    A simple method for reporting
    the length of a string for saving
    to a muon nexus v2 file
    :param string: the string to be saved
    :return: a string that reports the length of the
    string
    """
    return 'S{}'.format(len(string)+1)
