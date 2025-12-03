from setuptools import find_packages, setup, Extension
import numpy


version = "0.9.2b11"


PACKAGE_NAME = 'MuonDataLib'


extensions = [
              Extension(
                "MuonDataLib.cython_ext.base_sample_logs",
                sources=["src/MuonDataLib/cython_ext/base_sample_logs.pyx"],
                ),
              Extension(
                "MuonDataLib.cython_ext.event_data",
                sources=["src/MuonDataLib/cython_ext/event_data.pyx"],
                ),
              Extension(
                "MuonDataLib.cython_ext.events_cache",
                sources=["src/MuonDataLib/cython_ext/events_cache.pyx"],
                ),
              Extension(
                "MuonDataLib.cython_ext.load_events",
                sources=["src/MuonDataLib/cython_ext/load_events.pyx"],
                ),
              Extension(
                "MuonDataLib.cython_ext.stats",
                sources=["src/MuonDataLib/cython_ext/stats.pyx"]
                ),
              Extension(
                "MuonDataLib.cython_ext.filter",
                sources=["src/MuonDataLib/cython_ext/filter.pyx"]
                ),
              Extension(
                "MuonDataLib.cython_ext.utils",
                sources=["src/MuonDataLib/cython_ext/utils.pyx"]
                ),
              ]
setup(
    name=PACKAGE_NAME,
    requires=['numpy', 'cython', 'plotly'],
    setup_requires=['numpy', 'cython', 'plotly'],
    install_requires=['numpy', 'cython', 'plotly'],
    packages=find_packages(where='src'),
    ext_modules=extensions,
    version=version,
    include_dirs=[numpy.get_include()],
    package_dir={'': 'src'}
)
