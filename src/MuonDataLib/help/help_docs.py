HIST = 'histogram'
LOAD = 'load_events'
NXS = 'NeXus'
FILTER = 'filter'
TIME = 'time'
LOG = 'sample log'
MUONDATA = 'MuonData'
FIGURE = 'Figure (plotting)'
UTILS = 'utils'


tags = [MUONDATA, LOAD, FIGURE, UTILS,
        HIST, FILTER, TIME, LOG, NXS]


class Doc(object):
    def __init__(self, name, module, tags, description='',
                 param={}, optional_param={}, returns='',
                 example=[]):
        self.name = name
        self.module = module
        self.tags = tags
        self.description = description
        self.param = param
        self.optional_param = optional_param
        self.returns = returns
        self.example = example

    def write_text(self, file_name, text):
        with open(file_name, 'a') as file:
            file.write(text)

    def get_rst(self):
        text = f'`{self.module}`.{self.name}\n'
        for k in range(len(text)):
            text += '-'
        text += '\n'
        text += f'{self.description} \n\n'

        space = ''

        if len(self.param) > 0:
            tmp = space + '**Required Parameters:** \n'
            for info in self.param.keys():
                tmp += space + f'- `{info}`: {self.param[info]} \n'
            text += tmp

        if len(self.optional_param) > 0:
            tmp = '\n' + space + '**Optional Parameters:** \n'
            for info in self.optional_param.keys():
                msg = self.optional_param[info]
                value = f'- `{info}`: {msg[0]} *Default value:* `{msg[1]}`'
                tmp += space + value + '''.\n'''
            text += tmp

        if self.returns != '':
            text += '\n' + space + f'**Returns:** {self.returns} \n'

        if len(self.example) > 0:
            text += "\n" + space + "**Example:** \n\n"
            text += space + ".. code:: python\n \n"
            for eg in self.example:
                text += space + f'    {eg} \n'
        text += '\n\n'
        return text

    def get_MD(self):
        text = f'''# `{self.module}`.**{self.name}** \n'''
        text += f'''{self.description} \n\n'''

        space = ''

        if len(self.param) > 0:
            tmp = space + '''**Required Parameters:** \n'''
            for info in self.param.keys():
                tmp += space + f'''- `{info}`: {self.param[info]} \n'''
            text += tmp

        if len(self.optional_param) > 0:
            tmp = '''\n''' + space + '''**Optional Parameters:** \n'''
            for info in self.optional_param.keys():
                msg = self.optional_param[info]
                value = f'''- `{info}`: {msg[0]} *Default value:* `{msg[1]}`'''
                tmp += space + value + '''.\n'''
            text += tmp

        if self.returns != '':
            text += '''\n''' + space + f'''**Returns:** {self.returns} \n'''

        if len(self.example) > 0:
            text += "\n" + space + """**Example:** \n\n"""
            text += space + """``` python\n"""
            for eg in self.example:
                text += space + f'''{eg} \n'''
            text += '''```\n'''
        return text
