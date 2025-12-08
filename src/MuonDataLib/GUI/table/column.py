class Column(object):
    """
    A simple class for creating columns for
    a dash data table. This stores the extra
    information (e.g. dropdowns, validation,
    conditional formating).
    """
    def __init__(self, ID, name):
        """
        Create the details for the column.
        :param ID: the ID for the column
        :param name: the displayed name in the
        column.
        """
        self.ID = ID
        self.name = name
        self.dropdown = None
        self.condition = []
        self.type = None

    def add_type(self, data_type):
        """
        Sets automatic validation for the
        column.
        Allowed values are:
        - numeric
        - text
        - datetime (YYYY-MM-DD HH:MM:SS)
        - any
        :param data_type: the data type for the
        column
        """
        if data_type not in ['numeric',
                             'text',
                             'datetime',
                             'any']:
            raise ValueError(f"Unkown data type {data_type}")
        self.type = data_type

    def add_dropdown(self, options):
        """
        This will place a dropdown menu
        into the rows for the column.
        :param options: the options for the dropdown
        """
        if isinstance(options, list):
            self.dropdown = options
            return
        raise ValueError("dropdown options should be a list")

    @property
    def get_column_dict(self):
        """
        Thos method generates a dict
        for the config of the column.
        :returns: the dict of the config
        """
        header = {'id': self.ID,
                  'name': self.name}
        if self.type is not None:
            header['type'] = self.type

        if self.dropdown is not None:
            header['presentation'] = 'dropdown'

        return header

    @property
    def get_options(self):
        """
        Method to get the options for the
        dropdown menu
        :returns: the dropdown menu options
        """
        if self.dropdown is None:
            raise RuntimeError("There is no dropdown to place the options")
        return [{'label': label, 'value': label} for label in self.dropdown]

    def add_condition(self, condition, cols, bg, colour):
        """
        This method allows for a condition to be added.
        Typically this would be something like if x is
        selected in the dropdown colour cell y blue.
        Can have multiple conditions for a signle
        column.
        :params condition: the condition
        :params cols: the column ID's that are changed by the condition
        :params bg: the new background colour for the cells
        :params colour: the colour of the text in the cell
        """
        self.condition.append({'condition': condition,
                               'cols': cols,
                               'bg': bg,
                               'colour': colour})

    @property
    def get_conditions(self):
        """
        Gets the conditions on the column
        :returns: a dict of the conditions
        """
        if self.dropdown is None:
            raise RuntimeError("There are no options for "
                               "the condition to act upon")
        conditions = []
        for con in self.condition:
            conditions.append({'if': {'filter_query': con['condition'],
                                      'column_id': con['cols']},
                               'backgroundColor': con['bg'],
                               'color': con['colour']})
        return conditions
