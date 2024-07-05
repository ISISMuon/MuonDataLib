from setuptools import find_packages, setup, Extension

VERSION = "0.5.0b3"


PACKAGE_NAME = 'MuonDataLib'


extensions = [Extension(
                "muondatalib.cython.add",
                sources=["src/muondatalib/cython/add.pyx"])]
setup(
    name=PACKAGE_NAME,
    requires=['numpy', 'cython'],
    setup_requires=['numpy', 'cython'],
    install_requires=['numpy', 'cython'],
    packages=find_packages(where='src'),
    ext_modules=extensions,
    version=VERSION,
    package_dir={'': 'src'}
)
