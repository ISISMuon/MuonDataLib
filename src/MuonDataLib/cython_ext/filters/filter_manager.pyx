from MuonDataLib.cython_ext.filters.frame_filter import FrameFilter
from MuonDataLib.cython_ext.filters.min_filter import MinFilter
import json

class FilterManager(object):
    def __init__(self,
                 frames,
                 frame_times,
                 int N):

        self.frame_filter = FrameFilter(frames,
                                        frame_times,
                                        N)
        self.min_filters = {}

    def __call__(self, k):
        # need to filter frames first
        for key in self.min_filters.keys():
            # no need to carry on if any return false
            if self.min_filters[key].is_active and self.min_filters[key](k):
                return False
        return True

    def report(self):
        filters = {'frame filters': self.frame_filter.report()}
        tmp = {}
        for key in self.min_filters.keys():
            min_filter = self.min_filters[key]
            if min_filter.is_active:
                tmp[key] = min_filter.value()
        filters['min filters'] = tmp
        return filters

    def save(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.report(), f)

    def load(self, file_name):
        with open(file_name, 'r') as f:
            filters = json.load(f)
        tmp = filters['frame filters']
        for key in tmp.keys():
            self.add_frame_filter(key,
                                  tmp[key][0],
                                  tmp[key][1])

        tmp = filters['min filters']
        errors = []
        for key in tmp.keys():
            if key in self.min_filters.keys():
                self.set_min_filter(key, tmp[key])
            else:
                errors.append(key)
        if len(errors) > 0:
            msg = "The following keys were not recognised \n"
            for err in errors:
                msg += '  - ' + err + ' \n'
            raise ValueError(msg)


    """
    Min filter methods
    """
    def create_min_filter(self, str name, data):
        self.min_filters[name] = MinFilter(data)

    def _check_min_filter(self, str name):
        if name not in self.min_filters.keys():
            raise ValueError(f"{name} is not a recognised filter")

    def set_min_filter(self, str name, double min_value):
        self._check_min_filter(name)
        self.min_filters[name].set_min_filter(min_value)

    def remove_min_filter(self, str name):
        self._check_min_filter(name)
        self.min_filters[name].remove_min_filter(name)

    def get_stats(self, str name):
        return self.min_filters[name].get_stats()

    """
    frame filter methods
    """
    def add_frame_filter(self, str name, double start, double end):
        self.frame_filter.add_filter(name, start, end)

    def remove_frame_filter(self, str name):
        self.frame_filter.remove(name)

    def get_good_frames(self, data):
        import time
        start = time.time()
        result = self.frame_filter.get_frame_indicies(data)
        print('get', time.time() - start)
        return result

