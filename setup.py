from setuptools import find_packages, setup, Extension
import numpy


version = "0.6.0b2"


PACKAGE_NAME = 'MuonDataLib'


extensions = [Extension(
                "MuonDataLib.cython_ext.add",
                sources=["src/MuonDataLib/cython_ext/add.pyx"],
                )]
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
