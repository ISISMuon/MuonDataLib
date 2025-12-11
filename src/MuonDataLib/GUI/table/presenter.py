from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.table.view import TableView

from collections import Counter


class TablePresenter(PresenterTemplate):
    """
    A class for the view of the filter
    table. This follows the MVP
    pattern.
    """
    def __init__(self, ID, columns, name_col):
        """
        This creates the view object for the
        widget. The responses to the callbacks
        will be in the presenter.
        :param ID: the ID for the table
        :param headers: a list of the columns for the
        table (see column.py)
        :param name_col: the name of the column
        """
        self.ID = ID
        self.name_col = name_col

        options, conditions = self._get_dropdown_info(columns)
        self.options = options
        self.conditions = conditions

        self._view = self._set_view()
        self.cols = self._view.col#[col.get_column_dict for col in columns]

    def _set_view(self):
        """
        A method to set the view for the widget
        :returns: the view for the widget
        """
        return TableView(self)

    def _get_dropdown_info(self, columns):
        """
        Gets the conditions and dropdown options
        for a column
        :param headers: the list of headers for the table
        :returns: the layout of the widget's
        GUI.
        """
        options = {}
        conditions = []
        for col in columns:
            if col.dropdown is not None:
                options[col.ID] = {
                    'clearable': False,
                    'options': col.get_options
                }

                tmp = col.get_conditions
                if len(tmp) > 0:
                    for con in tmp:
                        conditions.append(con)
        conditions.append({'if': {'row_index': 'odd'},
                           'backgroundColor': 'whitesmoke'})
        return options, conditions

    def validate_row(self, new_row, old_row):
        """
        Determines if a change to a row is valid
        :param new_row: the new (changed) row
        :param old_row: the old (previous) row
        :returns: if its valid and the error message
        """
        return True, ''

    def validate(self, data, previous):
        """
        A validation check for the table.
        It has a rule that each row name
        must be unique.
        :param data: the data in the table
        :param previous: the previous data in the table
        :returns it to update and the error message
        """
        if len(data) == 0:
            return True, ''

        names = [row[self.name_col] for row in data]
        repeat, num = Counter(names).most_common(1)[0]
        if num > 1:
            return False, f'Repeated name {repeat}'

        for new_row, old_row in zip(data, previous):
            if new_row != old_row:
                return self.validate_row(new_row, old_row)
        return True, ''

    def update(self, timestamp, data, previous):
        """
        This allows the user to change a value and then
        click out of the cell (without pressing enter)
        such that the table keeps the new value (if valid).
        If its not valid the table will be reverted.
        :param timestamp: the timestamp for the interaction
        :param data: the data from the table
        :param previous: the previous data from the table
        :returns: the valid data for the table, if its valid and
        the error message
        """
        valid, msg = self.validate(data, previous)
        if valid:
            return data, True, ''
        return previous, False, msg

    def add(self, n, data):
        """
        Adds a row to the table.
        :param n: the number of clicks of the add button
        :param data: the data in the table
        :returns: the data for the table and if its valid
        """
        data.append(self.generate_default)
        return data, True

    @property
    def generate_default(self):
        """
        Code to create some default values
        """
        raise NotImplementedError(f"Need to set a default table for {self.ID}")
