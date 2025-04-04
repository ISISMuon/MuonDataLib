from MuonDataLib.help.muon_data import get_muon_data_docs
from MuonDataLib.help.utils import get_utils_docs
from MuonDataLib.help.figure import get_figure_docs
from MuonDataLib.help.load_events import get_load_docs

import pathlib
import sys
import os

pages = {'MuonData': get_muon_data_docs(),
         'utils': get_utils_docs(),
         'Figure': get_figure_docs(),
         'load_events': get_load_docs()}

for name in pages:
    file_name = os.path.join(os.path.dirname(__file__), 'API', name + '.rst')
    with open(file_name, 'w') as file:
        title = f'MuonDataLib API documentation: {name} \n'
        uline = ''
        for _ in title:
            uline += '='
        file.write(title)
        file.write(uline + '\n\n')

    for text in pages[name]:
        text.write_text(file_name, text.get_rst())


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

project = 'muonDataLib'
copyright = '2024, Anthony Lim'
author = 'Anthony Lim'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'nbsphinx',
              'sphinx_rtd_theme',
              'sphinx.ext.autosummary']

exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
