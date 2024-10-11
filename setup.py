from setuptools import find_packages, setup, Extension
import numpy


version = "0.9.0b1"


PACKAGE_NAME = 'MuonDataLib'


extensions = [
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
