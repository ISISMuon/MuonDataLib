class Column(object):
    """
    A simple class for creating columns for
    a dash data table. This stores the extra
    information (e.g. dropdowns, validation,
    conditional formating).
    """
    def __init__(self, ID, name, dtype):
        """
        Create the details for the column.
        :param ID: the ID for the column
        :param name: the displayed name in the
        column.
        """
        if dtype in ['text', 'numeric']:
            self.ID = ID
            self.name = name
            self.dtype = dtype
            self._min = 0
            self._max = 1000
        else:
            raise ValueError(f"Unkown column dtype {dtype}."
                             "Options are 'text' and 'numeric'.")

    def set_range(self, min_value, max_value):
        if self.dtype == 'numeric':
            self._min = min_value
            self._max = max_value
        else:
            raise RuntimeError('Cannot set col range for non-numeric dtype')

    @property
    def get_column_dict(self):
        """
        Thos method generates a dict
        for the config of the column.
        :returns: the dict of the config
        """
        col = {'field': self.ID,
               'headerName': self.name,
               'width': 100}
        if self.dtype == 'text':
            col['cellEditor'] = 'agLargeTextCellEditor'
            col['cellEditorPopup'] = False
            col['cellEditorParams'] = {'maxLength': 50}

        elif self.dtype == 'numeric':
            col['cellEditor'] = 'agNumberCellEditor'
            col['cellEditorParams'] = {'min': self._min,
                                       'max': self._max,
                                       'precision': 3}

        return col
