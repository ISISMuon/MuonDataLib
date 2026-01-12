class Column(object):
    """
    A simple class for creating columns for
    a dash data ag-table. This stores the extra
    information (e.g. dropdowns, validation,
    conditional formating).
    """
    def __init__(self, ID, name, dtype):
        """
        Create the details for the column.
        The min and max are only for the numeric
        data type and provide the limits
        for the values that can be entered.
        :param ID: the ID for the column
        :param name: the displayed name in the
        column.
        :param dtype: the data type for the column
        (allowed values; text, numeric, button)
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
        """
        Sets the range of allowed values for a numeric
        cell.
        :param min_value: the smallest allowed value
        :param max_value: the largest allowed value
        """
        if self.is_numeric:
            if min_value > max_value:
                raise RuntimeError("col range: Min value > Max value")
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
        """
        Checks if a cell is numeric
        :returns: a bool for if its numeric.
        """
        if self.dtype == 'numeric':
            return True
        return False


class TableGroup(object):
    def __init__(self, cols, name=None):
        """
        A class to store multiple related table
        columns. These may share a header
        (e.g. "Include data" for columns of the
        start and end values for the filters).
        :param cols: A list of columns (see above)
        :param name: The header name that is shared for
        all of the columns.
        """
        self.name = name
        self.cols = cols

    def set_range(self, min_value, max_value):
        """
        Sets the numeric ranges for all of the columns
        in the group. They will share values in time (x).
        :param min_value: the lowest allowed value
        :param max_value: the largst allowed value
        """
        for col in self.cols:
            if col.is_numeric:
                col.set_range(min_value,
                              max_value)

    @property
    def get_column_dict(self):
        """
        Creates a dict for the columns in the group.
        :returns: a dict of columns (json format)
        """
        if self.name is None:
            return [col.get_column_dict for col in self.cols]
        else:
            children = [col.get_column_dict for col in self.cols]
            return [{'headerName': self.name,
                     'children': children}]


class TableColumns(object):
    def __init__(self, col_groups, inc_delete_row, btn_ID=''):
        """
        A class for holding column groups (above).
        This creates the nice table for the GUI,
        including a delete row button
        :param col_groups: a list of the column group objects
        :param inc_delete_row" if to add a delete button to the rows
        :param btn_ID: the ID for the row button
        """
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
        """
        returns the json dict for the columns,
        which defines the table.
        :returns: the dict of the columns
        """
        result = []
        for col in self.cols:
            result.append(*col.get_column_dict)
        return result

    def set_range(self, min_value, max_value):
        """
        Loops over all columns in the table
        and sets the allowed data range to match the
        provided values
        :param min_value: the smallest allowed value
        :param max_value: the largest allowed value
        """
        for col in self.cols:
            col.set_range(min_value,
                          max_value)
