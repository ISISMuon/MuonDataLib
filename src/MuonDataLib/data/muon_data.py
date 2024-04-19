import h5py


class MuonData(object):
    """
    A class to store all of the information needed for muon data
    """
    def __init__(self, sample, raw_data, source, user, periods, detector1):
        """
        Creates a store for relevant muon data (defined by nxs v2)
        :param sample: the Sample data needed for nexus v2 file
        :param raw_data: the RawData data needed for nexus v2 file
        :param source: the Source data needed for nexus v2 file
        :param user: the User data needed for nexus v2 file
        :param periods: the Periods data needed for nexus v2 file
        :param detector1: the Detector1 data needed for nexus v2 file
        """
        self._dict = {}
        self._dict['raw_data'] = raw_data
        self._dict['sample'] = sample
        self._dict['source'] = source
        self._dict['user'] = user
        self._dict['periods'] = periods
        self._dict['detector_1'] = detector1

    def save_histograms(self, file_name):
        """
        Method for saving the object to a muon
        nexus v2 histogram file
        :param file_name: the name of the file to save to
        """
        file = h5py.File(file_name, 'w')
        for key in self._dict.keys():
            self._dict[key].save_nxs2(file)
        file.close()
        return
