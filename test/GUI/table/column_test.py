import unittest
from MuonDataLib.GUI.table.column import Column
from MuonDataLib.test_helpers.unit_test import TestHelper
from MuonDataLib.test_helpers.table_ref_data import VALID_DTYPES as VALID
from MuonDataLib.test_helpers.table_ref_data import expected_col_dict


class ColumnTest(TestHelper):

    def test_init(self):
        for dtype in VALID:
            with self.subTest(dtpye=dtype):
                col = Column('unit', 'test', dtype)
                self.assertEqual(col.ID, 'unit')
                self.assertEqual(col.name, 'test')
                self.assertEqual(col.dtype, dtype)
                self.assertEqual(col._min, -1e6)
                self.assertEqual(col._max, 1e6)

    def test_init_bad_dtype(self):
        try:
            _ = Column('unit', 'test', 'bool')
        except ValueError:
            pass
            return
        self.fail('A bool dtype should not be allowed')

    def test_set_icon(self):
        col = Column('unit', 'test', 'button')
        self.assertEqual(col._icon, 'bi bi-trash me-2')
        self.assertEqual(col._className, 'btn btn-danger')

        col.set_icon('tick', 'primary')
        self.assertEqual(col._icon, 'tick')
        self.assertEqual(col._className, 'primary')

        data = col.get_column_dict
        self.assertEqual(data['cellRendererParams']['Icon'],
                         'tick')
        self.assertEqual(data['cellRendererParams']['className'],
                         'primary')

    def test_set_uneditable(self):
        for dtype in VALID:
            with self.subTest(dtpye=dtype):
                col = Column('unit', 'test', dtype)
                data = col.get_column_dict
                self.assertEqual(data['editable'], dtype != 'button')

                col.set_uneditable()
                data = col.get_column_dict
                self.assertEqual(data['editable'], False)

    def test_set_range(self):
        for dtype in VALID:
            with self.subTest(dtpye=dtype):
                col = Column('unit', 'test', dtype)
                try:
                    col.set_range(1.2, 4.7)
                except RuntimeError:
                    if dtype == 'numeric':
                        self.fail('dtype nmeric should not throw an error')
                    else:
                        pass
                        return
                if dtype != 'numeric':
                    self.fail(f'dtype {dtype} should not pass')
                self.assertEqual(col._min, 1.2)
                self.assertEqual(col._max, 4.7)

    def test_is_numeric(self):
        for dtype in VALID:
            with self.subTest(dtpye=dtype):
                col = Column('unit', 'test', dtype)
                state = col.is_numeric
                if dtype == 'numeric':
                    self.assertTrue(state)
                else:
                    self.assertFalse(state)

    def test_get_column_dict(self):
        for dtype in VALID:
            with self.subTest(dtpye=dtype):
                col = Column('unit', 'test', dtype)
                col_dict = col.get_column_dict
                self.assertEqual(col_dict,
                                 expected_col_dict(dtype))


if __name__ == '__main__':
    unittest.main()
