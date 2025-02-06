from MuonDataLib.cython_ext.filter import apply_filter
from MuonDataLib.data.utils import NONE
from MuonDataLib.data.hdf5 import (HDF5,
                                   is_list,
                                   is_int,
                                   is_float)


class LogData(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.clear_filters()

    def clear_filters(self):
        self.fx = None
        self.fy = None
        self._name = None
        self._max = NONE
        self._min = NONE

    def add_filter(self, name, min_value=NONE, max_value=NONE):
        self._name = name
        self._min = min_value
        self._max = max_value

    def get_filter(self):
        return self._name, self.x, self.y, self._min, self._max

    def set_filter_values(self, fx, fy):
        self.fx = fx
        self.fy = fy

    def get_values(self):
        if self.fx is not None:
            return self.fx, self.fy
        else:
            return self.x, self.y


class SampleLogs(HDF5):
    """
    A simple class to store the sample log information
    needed for a muon nexus v2 file
    """
    def __init__(self):
        """
        Create an empty set of sample logs
        """
        self._float_dict = {}
        self._int_dict = {}
        self._bool_dict = {}
        self._look_up = {}

    def get_names(self):
        return list(self._look_up.keys())

    def apply_filter(self, name, times):
        if name not in self._look_up.keys():
            raise RuntimeError(f"The sample log {name} does not "
                               "exist in the sample logs")
        dtype = self._look_up[name]
        if dtype == 'int':
            x, y = self._int_dict[name].get_values()
        elif dtype == 'float':
            x, y = self._float_dict[name].get_values()
            self._float_dict[name].set_filter_values(*apply_filter(x,
                                                                   y,
                                                                   times))

    def add_filter(self, name, min_value, max_value):
        if name not in self._look_up.keys():
            raise RuntimeError(f"The sample log {name} does not "
                               "exist in the sample logs")
        dtype = self._look_up[name]
        if dtype == 'int':
            self._int_dict[name].add_filter(name+'_filter',
                                            min_value, max_value)
        elif dtype == 'float':
            self._float_dict[name].add_filter(name+'_filter',
                                              min_value, max_value)

    def get_filter(self, name):
        if name not in self._look_up.keys():
            raise RuntimeError(f"The sample log {name} does "
                               "not exist in the sample logs")
        dtype = self._look_up[name]
        if dtype == 'int':
            return self._int_dict[name].get_filter()
        elif dtype == 'float':
            return self._float_dict[name].get_filter()

    def add_sample_log(self, name, x_data, y_data):
        if name in self._look_up.keys():
            raise RuntimeError(f"The sample log {name} "
                               "already exists in the sample logs")
        if is_list(y_data):
            y = y_data[0]
            if is_int(y):
                self._int_dict[name] = LogData(x_data, y_data)
                self._look_up[name] = 'int'
                return
            elif is_float(y):
                self._float_dict[name] = LogData(x_data, y_data)
                self._look_up[name] = 'float'
                return
        raise RuntimeError(f"The sample log {name} is "
                           "not currently supported")

    def get_sample_log(self, name):
        if name not in self._look_up.keys():
            raise RuntimeError(f"The sample log {name} does"
                               "not exist in the sample logs")
        dtype = self._look_up[name]
        if dtype == 'int':
            return self._int_dict[name]
        elif dtype == 'float':
            return self._float_dict[name]

    def clear(self):
        self._float_dict.clear()
        self._int_dict.clear()
        self._bool_dict.clear()
        self._look_up.clear()

    def save_nxs2(self, file):
        """
        Write the user information to a
        muon nexus v2 file.
        :param file: the open file to write to

        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('user_1')
        tmp.attrs['NX_class'] = 'NXuser'
        for key in self._dict.keys():
            self.save_str(key, self._dict[key], tmp)
        """
        return
