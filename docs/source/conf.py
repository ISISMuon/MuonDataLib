import pathlib
import sys
from MuonDataLib.help.help_docs import _text
import os


file_name = os.path.join(os.path.dirname(__file__), 'API.MD')
with open(file_name, 'w') as file:
    file.write('''# Welcome to MuonDataLib API documentation''')

for text in _text:
    text.write_MD(file_name)

print('mpppppppppppppp', file_name)

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
              'sphinx.ext.autosummary']

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'classic'
