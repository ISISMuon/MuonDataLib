from MuonDataLib.data.hdf5 import HDF5


class Periods(HDF5):
    """
    A class to store the period informtaion for muon data
    """
    def __init__(self, number, labels, p_type, requested,
                 raw, output, counts, sequences):
        """
        A class to store the period data needed for a muon nexus v2 file
        :param number: the number of periods
        :param labels: a string of the period labels
        :param p_type: an int array representing the type of period
        :param requested: the number of requested frames
        :param raw: the number of raw frames
        :param output: an int array of the outputs
        :param counts: a float array of the total counts
        :param sequences: an int array of the sequences
        """
        super().__init__()
        self._dict['number'] = number
        self._dict['labels'] = labels
        self._dict['type'] = p_type
        self._dict['requested'] = requested
        self._dict['raw'] = raw
        self._dict['output'] = output
        self._dict['counts'] = counts
        self._dict['sequences'] = sequences

    def save_nxs2(self, file):
        """
        A method to save the periods information as a muon
        nexus v2 file
        :param file: the open file to write to
        """
        tmp = file.require_group('raw_data_1')
        tmp = tmp.require_group('periods')

        tmp.attrs['NX_class'] = 'NXperiod'
        self.save_int('number', self._dict['number'], tmp)
        self.save_int_array('sequences', self._dict['sequences'], tmp)
        self.save_str('labels', self._dict['labels'], tmp)
        self.save_int_array('type', self._dict['type'], tmp)
        self.save_int_array('frames_requested', self._dict['requested'], tmp)
        self.save_int_array('raw_frames', self._dict['raw'], tmp)
        self.save_int_array('output', self._dict['output'], tmp)
        self.save_float_array('total_counts', self._dict['counts'], tmp)


def read_periods_from_histogram(file):
    """
    A method for reading the period information
    a nexus v2 histogram file
    :param file: the open file to read from
    :return: the Periods object
    """
    tmp = file['raw_data_1']['periods']

    return Periods(number=tmp['number'][:][0],
                   labels=tmp['labels'][:][0].decode(),
                   p_type=tmp['type'][:],
                   requested=tmp['frames_requested'][:],
                   raw=tmp['raw_frames'][:],
                   output=tmp['output'][:],
                   counts=tmp['total_counts'][:],
                   sequences=tmp['sequences'][:])
