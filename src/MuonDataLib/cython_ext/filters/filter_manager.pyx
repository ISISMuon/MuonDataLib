from MuonDataLib.cython_ext.filters.frame_filter import FrameFilter
from MuonDataLib.cython_ext.filters.min_filter import MinFilter


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

    """
    frame filter methods
    """
    def add_frame_filter(self, str name, double start, double end):
        self.frame_filter.add_filter(name, start, end)

    def remove_frame_filter(self, str name):
        self.frame_filter.remove(name)

    def get_good_frames(self, data):
        return self.frame_filter.get_frame_indicies(data)

