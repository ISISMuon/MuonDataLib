from MuonDataLib.GUI.table.column import (TableGroup,
                                          TextColumn,
                                          NumericColumn,
                                          ButtonColumn,
                                          DropDownColumn)

VALID_DTYPES = [TextColumn, NumericColumn, ButtonColumn, DropDownColumn]


def expected_col_dict(dtype, ID='unit', name='test'):
    col = {'field': ID,
           'headerName': name,
           'width': 100,
           'hide': False}
    if dtype == TextColumn:
        col['cellEditor'] = 'agLargeTextCellEditor'
        col['cellEditorPopup'] = False
        col['cellEditorParams'] = {'maxLength': 50}
        col['editable'] = True

    elif dtype == NumericColumn:
        col['cellEditor'] = 'agNumberCellEditor'
        col['cellEditorParams'] = {'min': -1000000,
                                   'max': 1000000,
                                   'precision': 5}
        col['editable'] = True
    elif dtype == ButtonColumn:
        col['editable'] = False
        col['cellRenderer'] = 'Button'
        col['cellRendererParams'] = {'Icon': 'bi bi-trash me-2',
                                     'className': 'btn btn-danger'}
    elif dtype == DropDownColumn:
        col['cellEditor'] = "agSelectCellEditor"
        col['cellEditorParams'] = {"values": ["above", "between", "below"]}
        col['singleClickEdit'] = True
        col['editable'] = True
    return col


COLS = [[dtype('Unit', 'unit')] for dtype in VALID_DTYPES]
for dtype1 in VALID_DTYPES:
    for dtype2 in VALID_DTYPES:
        COLS.append([dtype1('Unit', 'unit'),
                     dtype2('Test', 'test')])

TIME_TABLE = ''
name = TextColumn('Name_' + TIME_TABLE, 'Name')
start = NumericColumn('Start_' + TIME_TABLE, 'Start')
end = NumericColumn('End_' + TIME_TABLE, 'End')

COL_GROUPS = [[TableGroup([dtype('Unit', 'unit')])]
              for dtype in VALID_DTYPES]

for dtype2 in VALID_DTYPES:
    c1 = dtype1('Unit', 'unit')
    c2 = dtype2('Test', 'test')
    c3 = TextColumn('More', 'more')
    COL_GROUPS.append([TableGroup([c2, c3], 'group'),
                       TableGroup([c1])])
