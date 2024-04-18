from MuonDataLib.data.utils import (convert_date_for_NXS,
                                    convert_date)

from MuonDataLib.data.hdf5 import HDF5


class RawData(HDF5):
    """
    A class for storing the "raw data" information for a
    muon nexus v2 file
    """
    def __init__(self, good_frames, IDF, definition, inst, title, notes,
                 run_number, duration, raw_frames, start_time, end_time, ID):
        """
        Creates the raw data object, which holds all of the information
        for the raw data section of a muon nexus v2 file
        :param good_frames: the number of good frames
        :param IDF: the version of the Instrument Definition File (IDF)
        :param definition: the definition (e.g. pulsedTD)
        :param inst: the instrument name
        :param title: the title of the experiment
        :param notes: the additional notes/comments
        :param run_number: the run number
        :param duration: the duration of the experiment
        :param raw_frames: the number of raw frames
        :param start_time: the start time of the experiment
        :param end_time: the end time of the experiment
        :param ID: a string identifier for the experiment
        """
        super().__init__()
        self._dict['good_frames'] = good_frames
        self._dict['IDF'] = IDF
        self._dict['def'] = definition
        self._dict['inst'] = inst
        self._dict['title'] = title
        self._dict['notes'] = notes
        self._dict['run_number'] = run_number
        self._dict['duration'] = duration
        self._dict['raw_frames'] = raw_frames
        self._dict['start'] = start_time
        self._dict['end'] = end_time
        self._dict['ID'] = ID

    def save_nxs2(self, file):
        """
        A method to save the information into a muon nexus v2 file
        :param file: the open file to write to.
        """
        tmp = file.require_group('raw_data_1')
        tmp.attrs['NX_class'] = 'NXentry'

        self.save_int('good_frames', self._dict['good_frames'], tmp)
        self.save_int('IDF_version', self._dict['IDF'], tmp)
        self.save_str('definition', self._dict['def'], tmp)
        self.save_str('name', self._dict['inst'], tmp)
        self.save_str('title', self._dict['title'], tmp)
        self.save_str('notes', self._dict['notes'], tmp)
        self.save_int('run_number', self._dict['run_number'], tmp)
        self.save_float('duration', self._dict['duration'], tmp)
        self.save_int('raw_frames', self._dict['raw_frames'], tmp)
        self.save_str('start_time',
                      convert_date_for_NXS(self._dict['start']),
                      tmp)
        self.save_str('end_time', convert_date_for_NXS(self._dict['end']), tmp)
        self.save_str('experiment_identifier', self._dict['ID'], tmp)

        tmp = tmp.require_group('instrument')
        self.save_str('name', self._dict['inst'], tmp)


def read_raw_data_from_histogram(file):
    """
    A function for reading the raw data information
    from a muon nexus v2 file
    :param file: the open file to read from
    :return: the RawData object
    """
    tmp = file['raw_data_1']
    return RawData(tmp['good_frames'][0],
                   tmp["IDF_version"][0],
                   tmp['definition'][0].decode(),
                   tmp['name'][0].decode(),
                   tmp['title'][0].decode(),
                   tmp['notes'][0].decode(),
                   tmp['run_number'][0],
                   tmp['duration'][0],
                   tmp['raw_frames'][0],
                   convert_date(tmp['start_time'][0].decode()),
                   convert_date(tmp['end_time'][0].decode()),
                   tmp['experiment_identifier'][0].decode())
