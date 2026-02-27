project('muondatalib', 'c', 'cpp', 'cython')

py_mod = import('python')
py3 = py_mod.find_installation(pure: false)

cc = meson.get_compiler('c')
cy = meson.get_compiler('cython')

# Keep synced with pyproject.toml
if not cy.version().version_compare('>=3.0.6')
  error('tests requires Cython >= 3.0.6')
endif

base_cython_args = []
if cy.version().version_compare('>=3.1.0')
  base_cython_args += ['-Xfreethreading_compatible=True']
endif


incdir_numpy = run_command(py,
    ['-c', 'import numpy; print(numpy.get_include())'],
    check : true
  ).stdout().strip()

ext_modules = [{'name': 'MuonDataLib.cython_ext.base_sample_logs', 'sources': ['src/MuonDataLib/cython_ext/base_sample_logs.pyx']},
	       {'name': 'MuonDataLib.cython_ext.event_data', 'sources': ['src/MuonDataLib/cython_ext/event_data.pyx']},
               {'name': 'MuonDataLib.cython_ext.events_cache', 'sources': ['src/MuonDataLib/cython_ext/events_cache.pyx']},
               {'name': 'MuonDataLib.cython_ext.load_events', 'sources': ['src/MuonDataLib/cython_ext/load_events.pyx']},
               {'name': 'MuonDataLib.cython_ext.stats', 'sources': ['src/MuonDataLib/cython_ext/stats.pyx']},
               {'name': 'MuonDataLib.cython_ext.filter', 'sources': ['src/MuonDataLib/cython_ext/filter.pyx']},
               {'name': 'MuonDataLib.cython_ext.utils', 'sources': ['src/MuonDataLib/cython_ext/utils.pyx']}
	       ]

foreach mod : ext_modules
  py3.extension_module(
      mod['name'],
      mod['sources'],
      install: false,
      include_directories: [incdir_numpy],
      cython_args: base_cython_args,
  )
endforeach
