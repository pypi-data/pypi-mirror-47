#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# xarrayms documentation build configuration file, created by
# sphinx-quickstart on Fri Jun  9 13:47:02 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another
# directory, add these directories to sys.path here. If the directory is
# relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
#
import importlib
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import Mock as MagicMock


class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        obj = MagicMock()
        obj.__name__ = "name"
        obj.__doc__ = "doc"
        return obj


MOCK_MODULES = {}
_MOCK_MODULES = ['dask', 'dask.array', 'dask.sizeof', 'numpy',
                 'pyrap', 'pyrap.tables', 'xarray']

# Don't mock if we can import it.
# This allows us to build locally without
# Mocks interfering with other imports.
# e.g. np.__version__ getting tested by dask/scipy/astropy
for m in _MOCK_MODULES:
    try:
        importlib.import_module(m)
    except ImportError:
        MOCK_MODULES[m] = Mock()

sys.modules.update((k, v) for k, v in MOCK_MODULES.items())

import sphinx_rtd_theme
import xarrayms

# -- General configuration ---------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode',
              'sphinx.ext.intersphinx', 'sphinx.ext.extlinks',
              'numpydoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'xarray-ms'
copyright = u"2018, Simon Perkins"
author = u"Simon Perkins"

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = xarrayms.__version__
# The full version, including alpha/beta/rc tags.
release = xarrayms.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a
# theme further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Options for HTMLHelp output ---------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'xarraymsdoc'


# -- Options for LaTeX output ------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'xarrayms.tex',
     u'xarray-ms Documentation',
     u'Simon Perkins', 'manual'),
]


# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'xarrayms',
     u'xarray-ms Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'xarrayms',
     u'xarray-ms Documentation',
     author,
     'xarrayms',
     'One line description of project.',
     'Miscellaneous'),
]

napoleon_numpy_docstring = True
napoleon_google_docstring = False

extlinks = {
    'issue': ('https://github.com/ska-sa/xarray-ms/issues/%s', 'GH#'),
    'pr': ('https://github.com/ska-sa/xarray-ms/pull/%s', 'GH#')
}

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'dask': ('https://dask.pydata.org/en/stable', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'pyrap': ('https://casacore.github.io/python-casacore', None),
    'python': ('https://docs.python.org/3/', None),
    'xarray': ('https://xarray.pydata.org/en/stable', None),
}
