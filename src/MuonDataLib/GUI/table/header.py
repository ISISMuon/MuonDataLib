

class Header(object):
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.dropdown = None
        self.condition = []
        self.type = None

    def add_type(self, data_type):
        self.type = data_type

    def add_dropdown(self, options):
        self.dropdown = options

    @property
    def get_header_dict(self):
        header =  {'id': self.ID,
                  'name': self.name}
        if self.type is not None:
            header['type'] = self.type

        if self.dropdown is not None:
            header['presentation'] = 'dropdown'

        return header

    @property
    def get_options(self):
        if self.dropdown is None:
            raise RuntimeError("There is no dropdown to place the options")
        return [{'label': label, 'value': label} for label in self.dropdown]

    def add_condition(self, condition, cols, bg, colour):
        self.condition.append({'condition': condition,
                               'cols': cols,
                               'bg': bg,
                               'colour': colour})
    @property
    def get_conditions(self):
        if self.dropdown is None:
            raise RuntimeError("There are no options for the condition to act upon")
        conditions = []
        for con in self.condition:
            conditions.append({'if': {'filter_query': con['condition'],
                                      'column_id': con['cols'],
                                     },
                               'backgroundColor': con['bg'],
                               'color': con['colour']})
        return conditions
