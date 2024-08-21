from setuptools import find_packages, setup, Extension
import numpy


version = "0.6.0b3"


PACKAGE_NAME = 'MuonDataLib'


extensions = [
              Extension(
                "MuonDataLib.cython_ext.event_data",
                sources=["src/MuonDataLib/cython_ext/event_data.pyx"],
                language='c++',),
              Extension(
                "MuonDataLib.cython_ext.load_events",
                sources=["src/MuonDataLib/cython_ext/load_events.pyx"],
                ),
              Extension(
                "MuonDataLib.cython_ext.stats",
                sources=["src/MuonDataLib/cython_ext/stats.pyx"]
                ),
              Extension(
                "MuonDataLib.cython_ext.filters.frame_filter",
                ["src/MuonDataLib/cython_ext/filters/frame_filter.pyx"],
                language='c++',),
              Extension(
                "MuonDataLib.cython_ext.filters.min_filter",
                sources=["src/MuonDataLib/cython_ext/filters/min_filter.pyx"],
                language='c++',),

              Extension(
                'MuonDataLib.cython_ext.filters.utils',
                sources=["src/MuonDataLib/cython_ext/filters/utils.pyx",
                         "src/MuonDataLib/cython_ext/filters/_utils.cpp"],
                language="c++",
                extra_link_args=["-lz"]),

              ]
setup(
    name=PACKAGE_NAME,
    requires=['numpy', 'cython'],
    setup_requires=['numpy', 'cython'],
    install_requires=['numpy', 'cython'],
    packages=find_packages(where='src'),
    ext_modules=extensions,
    version=version,
    include_dirs=[numpy.get_include()],
    package_dir={'': 'src'}
)
