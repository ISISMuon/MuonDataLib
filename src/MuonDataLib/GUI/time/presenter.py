from MuonDataLib.GUI.table.presenter import TablePresenter
from MuonDataLib.GUI.time.view import TimeView
from MuonDataLib.GUI.table.column import Column


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
        self.count = 0

        self._previous = 'Exclude'

        # create columns
        name = Column('Name_t', ['', 'Name'])

        start = Column('Start_t', ['Exclude data', 'Start'])
        start.add_type('numeric')

        end = Column('End_t', ['Exclude data', 'End'])
        end.add_type('numeric')

        super().__init__('time-table',
                         [name, start, end],
                         name.ID)

    def _set_view(self):
        """
        Overwrite the view to give a time table view
        """
        return TimeView(self)

    def validate_row(self, new_row, old_row):
        """
        A method to check if a new row is valie
        :param new_row: the new row
        :param old_row: The old (previous) row
        :returns: if to update and the error message
        """
        if new_row['Start_t'] > new_row['End_t']:
            msg = f'Start time {new_row["Start_t"]} is '
            msg += f'greater than end time {new_row["End_t"]}'
            return False, msg
        return True, ''

    @property
    def generate_default(self):
        """
        The code needed to create a default
        row for the time table
        :returns: dict of the values for the time table.
        """
        self.count += 1
        return {'Name': f'default_{self.count}',
                'Start': 500,
                'End': 1000}

    def get_range(self, data):
        """
        Gets the x range from the time table data
        :peram data' The data from the table
        :returns: the start and end values
        """
        return [data['Start_t'], data['End_t']]

    def display_confirm(self, value, data):
        if len(data) == 0:
            self._previous = value
            return False
        elif self._previous != value:
            return True
        return False

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

        # found a bug: dont add row, change option. The title is wrong
        if submit > cancel:
            #for k in range(len(self.cols)):
            #    header = self.cols[k]
            #    for key in header.keys():
            #        if isinstance(header[key], list):
            #            for j in range(len(header[key])):
            #                txt = self.cols[k][key][j]
            #                self.cols[k][key][j] = txt.replace(self._previous,
            #                                                   value)
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
            data.append({'Name_t': key,
                         'Start_t': values[0],
                         'End_t': values[1]})

        self._previous = new_state
        return data, new_state
