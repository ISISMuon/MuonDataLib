from setuptools import find_packages, setup, Extension
import numpy
import sys


version = "0.13.0b0"


PACKAGE_NAME = 'MuonDataLib'


if sys.platform.startswith("win"):
    openmp_arg = '/openmp'
else:
    openmp_arg = '-fopenmp'

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
                sources=["src/MuonDataLib/cython_ext/stats.pyx"],
                extra_compile_args=[openmp_arg],
                extra_link_args=[openmp_arg],
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
    requires=['numpy', 'cython'],
    setup_requires=['numpy', 'cython'],
    install_requires=['numpy', 'cython'],
    packages=find_packages(where='src'),
    ext_modules=extensions,
    version=version,
    include_dirs=[numpy.get_include()],
    package_dir={'': 'src'}
)
