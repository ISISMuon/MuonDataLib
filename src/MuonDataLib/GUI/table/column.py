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
        if dtype in ['text', 'numeric', 'button']:
            self.ID = ID
            self.name = name
            self.dtype = dtype
            self._min = 0
            self._max = 1000
        else:
            raise ValueError(f"Unkown column dtype {dtype}."
                             "Options are 'text', 'numeric' and 'button'.")

    def set_range(self, min_value, max_value):
        if self.is_numeric:
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
        elif self.dtype == 'button':
            col['editable'] = False
            col['cellRenderer'] = 'Button'
            col['cellRendererParams'] = {'Icon': 'bi bi-trash me-2',
                                         'className': 'btn btn-danger'}
        return col

    @property
    def is_numeric(self):
        if self.dtype == 'numeric':
            return True
        return False


class TableGroup(object):
    def __init__(self, cols, name=None):
        self.name = name
        self.cols = cols
        print(name, self.cols)

    def set_range(self, min_value, max_value):
        for col in self.cols:
            if col.is_numeric:
                col.set_range(min_value,
                              max_value)

    @property
    def get_column_dict(self):
        if self.name is None:
            return [col.get_column_dict for col in self.cols]
        else:
            children = [col.get_column_dict for col in self.cols]
            return [{'headerName': self.name,
                     'children': children}]


class TableColumns(object):
    def __init__(self, col_groups, inc_delete_row, btn_ID=''):
        if inc_delete_row and btn_ID == '':
            raise RuntimeError('Need to include an ID '
                               'for the delete button')
        elif inc_delete_row:
            self.cols = [TableGroup([Column('Delete_' + btn_ID,
                                            '', 'button')])]

        for tmp in col_groups:
            self.cols.append(tmp)

    @property
    def get_column_dict(self):
        result = []
        for col in self.cols:
            result.append(*col.get_column_dict)
        return result

    def set_range(self, min_value, max_value):
        for col in self.cols:
            col.set_range(min_value,
                          max_value)
