from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.table.view import TableView

from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import Input, Output, callback, State
from collections import Counter


class TablePresenter(PresenterTemplate):
    """
    A class for the view of the filter
    table. This follows the MVP
    pattern.
    """
    def __init__(self, ID, headers, name_col):
        """
        This creates the view object for the
        widget. The responses to the callbacks
        will be in the presenter.
        """
        self.ID = ID
        self.name_col = name_col
        
        options, conditions = self._get_dropdown_info(self.ID,
                                                      headers)
        self.options = options
        self.conditions = conditions
        self.cols = [head.get_header_dict for head in headers]
        
        self._view = TableView(self)
    
    def _get_dropdown_info(self, ID, headers):
        """
        Creates the filter widget's GUI.
        :returns: the layout of the widget's
        GUI.
        """
        options = {}
        conditions = []
        for head in headers:
            if head.dropdown is not None:
                options[head.ID] = {
                    'clearable':False,
                    'options': head.get_options
                }

                tmp = head.get_conditions
                if len(tmp) > 0:
                    for con in tmp:
                        conditions.append(con)
 
        return options, conditions

    def validate_row(self, new_row, old_row):
        return True, ''

    def validate(self, data, previous):
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
        such that the table keeps the new value
        """
        valid, msg = self.validate(data, previous)
        if valid:
            return data, ''
        return previous, msg

    def add(self, n, data):
        data.append(self.generate_default)
        return data

    @property
    def generate_default(self):
        raise NotImplemented(f"Need to set a default table for {self.ID}")
