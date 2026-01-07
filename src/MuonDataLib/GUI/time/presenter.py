from MuonDataLib.GUI.table.presenter import TablePresenter
from MuonDataLib.GUI.time.view import TimeView
from MuonDataLib.GUI.table.column import Column, TableGroup, TableColumns


TIME_TABLE = 'time-table'


class TimePresenter(TablePresenter):
    """
    A class for the view of the time filter
    widget. This follows the MVP
    pattern.
    """
    def __init__(self):
        """
        This creates the presenter object for the
        widget.
        """
        self._previous = 'Exclude'

        # create columns
        name = Column('Name_' + TIME_TABLE, 'Name', 'text')

        start = Column('Start_' + TIME_TABLE, 'Start', 'numeric')
        end = Column('End_' + TIME_TABLE, 'End', 'numeric')

        self.cols = [self._delete_row_col,
                     name.get_column_dict,
                     {'headerName': 'Exclude filter details',
                      'children': [start.get_column_dict,
                                   end.get_column_dict]}]

        # still need to work this out
        cols = TableColumns([TableGroup([name]),
                             TableGroup([start,
                                         end],
                                        'Exclude filter details')],
                            inc_delete_row=True,
                            btn_ID=TIME_TABLE)

        cols = cols.get_column_dict

        super().__init__(TIME_TABLE,
                         self.cols,
                         name.ID)

    def _set_view(self):
        """
        Overwrite the view to give a time table view
        """
        return TimeView(self)

    def validate_row(self, change, data):
        """
        A validation check for the table.
        It has a rule that each row name
        must be unique.
        :param change: the change in the table (row)
        :param data: the data in the table
        :returns: it to update and the error message
        """
        changed = change[0]
        print('mooo', changed)
        col_name = changed['colId']
        row = changed['data']

        msg = ''
        new_value = row[col_name]
        if new_value is None:
            # keep the old one
            msg = (f'The new value {new_value} is '
                   f'outside of the data range.')
            new_value = changed['oldValue']
        elif col_name == 'Start_' + TIME_TABLE:
            end_value = row['End_' + TIME_TABLE]
            if new_value > end_value:
                # keep the old one
                msg = (f'The start value {new_value} is '
                       f'larger than the end value {end_value}')
                new_value = changed['oldValue']
        elif col_name == 'End_' + TIME_TABLE:
            start_value = row['Start_' + TIME_TABLE]
            if new_value < start_value:
                # keep the old one
                msg = (f'The end value {new_value} is '
                       f'smaller than the start value {start_value}')
                new_value = changed['oldValue']
        print(msg)
        data[changed['rowIndex']][col_name] = new_value
        return data, msg

    @property
    def default_row(self):
        """
        The code needed to create a default
        row for the time table
        :returns: dict of the values for the time table.
        """
        return {'Start_' + TIME_TABLE: 500,
                'End_' + TIME_TABLE: 1000}

    def get_range(self, data):
        """
        Gets the x range from the time table data
        :peram data' The data from the table
        :returns: the start and end values
        """
        return [data['Start_' + TIME_TABLE], data['End_' + TIME_TABLE]]

    def display_confirm(self, value, data):
        if len(data) == 0:
            self._previous = value
            self.cols[2]['headerName'] = f'{value} Filter details'
            return False, self.cols
        elif self._previous != value:
            return True, self.cols

    def confirm(self, submit, cancel, value, data):
        """
        Takes the user selection for the confirm dialog
        and does the appropriate response
        :param submit: the timestamp for the last time submit was pressed
        :param cancel: the timestamp for the last time cancel was pressed
        :param value: if to include or exclude the time table data
        :param data: the data in the time table
        :returns: the state for the time table (include/exclude),
        the data for the table, the list of column names and
        if the data has been changed
        """
        if submit > cancel:
            self._previous = value
            self.cols[2]['headerName'] = f'{value} Filter details'
            return value, [], self.cols, True
        else:
            return self._previous, data, self.cols, False

    def load(self, file):
        """
        A method to load filters from a json file
        :param file: the open file
        :returns: the data, the new state (include/exclude)
        """
        name = 'remove_filters'
        new_state = 'Exclude'
        if len(file['keep_filters']) == len(file['remove_filters']):
            raise RuntimeError("Cannot have both include and "
                               "exclude time filters")
        elif len(file['keep_filters']) > 0:
            name = 'keep_filters'
            new_state = 'Include'

        data = []
        for key in file[name].keys():
            values = file[name][key]
            data.append({'Name_' + TIME_TABLE: key,
                         'Start_' + TIME_TABLE: values[0],
                         'End_' + TIME_TABLE: values[1]})

        self._previous = new_state
        return data, new_state
