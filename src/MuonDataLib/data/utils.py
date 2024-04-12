import time
import h5py
import numpy as np
import datetime
 
INT32 = np.int32


FLOAT32 = np.float32


def convert_date_for_NXS(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S')
 

def convert_date(date):

    """

    Assume in the form f'{year} {month} {day}', time

    """

    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

 
def stype(s):
    return 'S{}'.format(len(s)+1)	
