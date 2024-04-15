from MuonDataLib.data.utils import (INT32, FLOAT32,
                                    stype)

import numpy as np


class HDF5(object):
    """
    A wrapper object to make it easier to write
    muon nexus v2 files
    """
    def __init__(self):
        """
        Create an empty dict of values
        """
        self._dict = {}

    def save_str(self, name, string, group):
        """
        Save a string to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param string: the string to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        dtype = stype(string)
        return group.require_dataset(name=name,
                                     shape=(1),
                                     data=np.array([string.encode()],
                                                   dtype=dtype),
                                     dtype=dtype)

    def save_float(self, name, value, group):
        """
        Save a float value to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param value: the float value to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        return group.require_dataset(name=name,
                                     shape=(1),
                                     data=[value],
                                     dtype=FLOAT32)

    def save_int(self, name, value, group):
        """
        Save an int value to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param value: the int to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        return group.require_dataset(name=name,
                                     shape=(1),
                                     data=[value],
                                     dtype=INT32)

    def save_int_array(self, name, values, group):
        """
        Save an array of ints to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param values: the int values to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        return group.require_dataset(name=name,
                                     shape=len(values),
                                     data=values,
                                     dtype=INT32)

    def save_float_array(self, name, values, group):
        """
        Save an array of float values to the relevant part of the nexus file
        :param name: the name used to reference the value in the file
        :param values: the float values to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        return group.require_dataset(name=name,
                                     shape=len(values),
                                     data=values,
                                     dtype=FLOAT32)

    def save_counts_array(self, name, N_periods, N_hist, N_x, values, group):
        """
        Save the counts array to the relevant part of the nexus file
        The counts are (period #, spec #, time values)
        :param name: the name used to reference the value in the file
        :param N_periods: the number of periods
        :param N_hist: the number of histograms
        :param N_x: the number of x (time) values
        :param values: the count values to store in the file
        :param group: the location (nexus group) to save the data to
        :return: the nexus dataset object
        """
        return group.require_dataset(name=name, shape=(N_periods, N_hist, N_x),
                                     data=values, dtype=INT32)
