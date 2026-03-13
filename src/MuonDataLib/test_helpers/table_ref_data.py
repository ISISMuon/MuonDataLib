from MuonDataLib.GUI.table.column import TableGroup, Column


VALID_DTYPES = ['text', 'numeric', 'button']


def expected_col_dict(dtype, ID='unit', name='test'):
    col = {'field': ID,
           'headerName': name,
           'width': 100,
           'hide': False}
    if dtype == 'text':
        col['cellEditor'] = 'agLargeTextCellEditor'
        col['cellEditorPopup'] = False
        col['cellEditorParams'] = {'maxLength': 50}
        col['editable'] = True

    elif dtype == 'numeric':
        col['cellEditor'] = 'agNumberCellEditor'
        col['cellEditorParams'] = {'min': -1000000,
                                   'max': 1000000,
                                   'precision': 5}
        col['editable'] = True
    elif dtype == 'button':
        col['editable'] = False
        col['cellRenderer'] = 'Button'
        col['cellRendererParams'] = {'Icon': 'bi bi-trash me-2',
                                     'className': 'btn btn-danger'}
    return col


COLS = [[Column('Unit', 'unit', dtype)] for dtype in VALID_DTYPES]
for dtype1 in VALID_DTYPES:
    for dtype2 in VALID_DTYPES:
        COLS.append([Column('Unit', 'unit', dtype1),
                     Column('Test', 'test', dtype2)])

TIME_TABLE = ''
name = Column('Name_' + TIME_TABLE, 'Name', 'text')
start = Column('Start_' + TIME_TABLE, 'Start', 'numeric')
end = Column('End_' + TIME_TABLE, 'End', 'numeric')

COL_GROUPS = [[TableGroup([Column('Unit',
                                  'unit',
                                  dtype)])] for dtype in VALID_DTYPES]

for dtype2 in VALID_DTYPES:
    c1 = Column('Unit', 'unit', dtype1)
    c2 = Column('Test', 'test', dtype2)
    c3 = Column('More', 'more', 'text')
    COL_GROUPS.append([TableGroup([c2, c3], 'group'),
                       TableGroup([c1])])
