import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Console Othello'
copyright = '2023, Paarth Siloiya'
author = 'Paarth Siloiya'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'shibuya'
html_static_path = ['_static']
