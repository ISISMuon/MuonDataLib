import unittest
from MuonDataLib.GUI.table.column import TableGroup
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.test_helpers.table_ref_data import COLS
from MuonDataLib.test_helpers.table_ref_data import expected_col_dict


SINGLE = []
for col in COLS:
    if len(col) == 1:
        SINGLE.append(col)


class TableGroupTest(TestHelper):

    def test_init(self):
        for col_list in COLS:
            with self.subTest(col_list=col_list):
                table = TableGroup(col_list, 'grouping')
                self.assertEqual(table.name, 'grouping')
                self.assertEqual(table.cols, col_list)

    def test_bad_input(self):
        for bad_input in ['fail', [], [1, 2, 3]]:
            with self.subTest(bad_input=bad_input):
                try:
                    _ = TableGroup(bad_input, 'group')
                except ValueError:
                    pass
                    return
                self.fail(f'should not accept bad input {bad_input}')

    def test_name_check(self):
        for col_list in COLS:
            with self.subTest(col_list=col_list):
                try:
                    _ = TableGroup(col_list)
                except ValueError:
                    if len(col_list) > 1:
                        pass
                        return
                if len(col_list) > 1:

                    self.fail('should not allow no name for lists')

    def test_set_range(self):
        for col_list in COLS:
            with self.subTest(col_list=col_list):
                table = TableGroup(col_list, 'grouping')
                table.set_range(1.2, 4.7)
                for col in table.cols:
                    if col.dtype == 'numeric':
                        self.assertEqual(col._min, 1.2)
                        self.assertEqual(col._max, 4.7)
                    else:
                        # if not numeric these never update (or used)
                        self.assertEqual(col._min, -1e6)
                        self.assertEqual(col._max, 1e6)

    def test_get_column_dict(self):
        names = ['unit', 'test']
        IDs = ['Unit', 'Test']
        for col_list in COLS:
            with self.subTest(col_list=col_list):
                table = TableGroup(col_list, 'grouping')
                col_dict_list = table.get_column_dict[0]

                self.assertEqual(col_dict_list['headerName'], 'grouping')
                for k, data in enumerate(zip(table.cols,
                                             col_dict_list['children'])):
                    col = data[0]
                    col_dict = data[1]
                    self.assertEqual(col_dict,
                                     expected_col_dict(col.dtype,
                                                       IDs[k],
                                                       names[k]))

    def test_set_title(self):
        for col_list in COLS:
            with self.subTest(col_list=col_list):
                table = TableGroup(col_list, 'grouping')
                table.set_title('new')
                self.assertEqual(table.name, 'new')

    """
    These tests are for a single item in the group
    """

    def test_init_1(self):
        for col_list in SINGLE:
            with self.subTest(col_list=col_list):
                table = TableGroup(col_list)
                self.assertEqual(table.name, None)
                self.assertEqual(table.cols, col_list)

    def test_set_range_1(self):
        for col_list in SINGLE:
            with self.subTest(col_list=col_list):
                table = TableGroup(col_list)
                table.set_range(1.2, 4.7)
                for col in table.cols:
                    if col.dtype == 'numeric':
                        self.assertEqual(col._min, 1.2)
                        self.assertEqual(col._max, 4.7)
                    else:
                        # if not numeric these never update (or used)
                        self.assertEqual(col._min, 0)
                        self.assertEqual(col._max, 1000.0)

    def test_get_column_dict_1(self):
        for col_list in SINGLE:
            with self.subTest(col_list=col_list):
                table = TableGroup(col_list)
                col_dict_list = table.get_column_dict[0]
                col = table.cols[0]
                self.assertEqual(col_dict_list,
                                 expected_col_dict(col.dtype,
                                                   'Unit',
                                                   'unit'))

    def test_set_title_1(self):
        for col_list in SINGLE:
            with self.subTest(col_list=col_list):
                table = TableGroup(col_list)
                table.set_title('new')
                self.assertEqual(table.name, 'new')


if __name__ == '__main__':
    unittest.main()
