import unittest
from MuonDataLib.GUI.table.column import Column
from MuonDataLib.test_helpers.unit_test import TestHelper


class ColumnTest(TestHelper):

    def setUp(self):
        self.col = Column('test_ID', 'real_name')

    def test__init__(self):
        self.assertEqual(self.col.ID, 'test_ID')
        self.assertEqual(self.col.name, 'real_name')
        self.assertEqual(self.col.dropdown, None)
        self.assertEqual(self.col.condition, [])
        self.assertEqual(self.col.type, None)

    def check_type_template(self, data_type):
        self.col.add_type(data_type)
        self.assertEqual(data_type, self.col.type)

    def test_add_type_numeric(self):
        self.check_type_template('numeric')

    def test_add_type_text(self):
        self.check_type_template('text')

    def test_add_type_datetime(self):
        self.check_type_template('datetime')

    def test_add_type_any(self):
        self.check_type_template('any')

    def test_add_type_bad_input(self):
        with self.assertRaises(ValueError,
                               msg='Unknown data type double'):
            self.check_type_template('double')

    def test_add_dropdown(self):
        self.col.add_dropdown(['a', 'b'])
        opts = self.col.dropdown
        self.assertArrays(opts, ['a', 'b'])

    def test_add_dropdown_fail(self):
        with self.assertRaises(ValueError,
                               msg="dropdown options should be a list"):
            self.col.add_dropdown('a')

    def test_get_column_dict_basic(self):
        col = self.col.get_column_dict
        self.assertEqual(len(col), 2)
        self.assertEqual(col['name'], 'real_name')
        self.assertEqual(col['id'], 'test_ID')

    def test_get_column_dict_with_dtype(self):
        self.col.add_type('numeric')
        col = self.col.get_column_dict
        self.assertEqual(len(col), 3)
        self.assertEqual(col['type'], 'numeric')

    def test_get_column_dict_with_dropdown(self):
        self.col.add_dropdown(['test', 'unit'])
        col = self.col.get_column_dict
        self.assertEqual(len(col), 3)
        self.assertArrays(col['presentation'], 'dropdown')

    def test_get_column_dict_with_dtype_and_dropdown(self):
        self.col.add_type('numeric')
        self.col.add_dropdown(['test', 'unit'])
        col = self.col.get_column_dict
        self.assertEqual(len(col), 4)
        self.assertEqual(col['type'], 'numeric')
        self.assertArrays(col['presentation'], 'dropdown')

    def test_get_options(self):
        self.col.add_dropdown(['test', 'unit'])
        options = self.col.get_options
        self.assertEqual(options, [{'label': 'test',
                                    'value': 'test'},
                                   {'label': 'unit',
                                    'value': 'unit'}])

    def test_get_options_fails(self):
        msg = "There is no dropdown to place the options"
        with self.assertRaises(RuntimeError,
                               msg=msg):
            _ = self.col.get_options

    def test_add_condition(self):
        self.col.add_dropdown(['unit', 'test'])
        self.col.add_condition('a>2',
                               ['Start'],
                               'black',
                               'white')
        self.col.add_condition('a<2',
                               ['End'],
                               'red',
                               'blue')

        con = self.col.condition
        self.assertEqual(con, [{'bg': 'black',
                                'colour': 'white',
                                'condition': 'a>2',
                                'cols': ['Start']},
                               {'bg': 'red',
                                'colour': 'blue',
                                'condition': 'a<2',
                                'cols': ['End']}
                               ])

    def test_get_conditon(self):
        self.col.add_dropdown(['unit', 'test'])
        self.col.add_condition('a>2',
                               ['Start'],
                               'black',
                               'white')
        self.col.add_condition('a<2',
                               ['End'],
                               'red',
                               'blue')
        cons = self.col.get_conditions
        self.assertEqual(cons, [{'if': {'filter_query': 'a>2',
                                        'column_id': ['Start']},
                                 'backgroundColor': 'black',
                                 'color': 'white'},
                                {'if': {'filter_query': 'a<2',
                                        'column_id': ['End']},
                                 'backgroundColor': 'red',
                                 'color': 'blue'}])

    def test_get_no_conditon(self):
        self.col.add_dropdown(['unit', 'test'])
        cons = self.col.get_conditions
        self.assertEqual(cons, [])

    def test_get_condition_fail(self):
        msg = "There are no options for the condition to act upon"
        with self.assertRaises(RuntimeError,
                               msg=msg):
            _ = self.col.get_conditions


if __name__ == '__main__':
    unittest.main()
