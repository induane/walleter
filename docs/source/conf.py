# -*- coding: utf-8 -*-
# Documentation build config
import datetime
import sphinx_rtd_theme

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'walleter'
copyright = u'2015 - {0}, Brant Watson'.format(datetime.datetime.now().year)

version = '0.0.1'
# The full version, including alpha/beta/rc tags.
release = '0.0.1-dev.0'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []


# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here.
html_static_path = ['_static']

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'walleterdoc'

# Grouping the document tree into LaTeX files.
latex_documents = [
  ('index', 'walleter.tex', u'walleter Documentation',
   u'Brant Watson', 'manual'),
]

# Documents to append as an appendix to all manuals.
latex_appendices = ['topics/manual', ]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'walleter', u'walleter Documentation',
     [u'Brant Watson'], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'walleter', u'walleter Documentation',
   u'Brant Watson', 'walleter', 'One line description of project.',
   'Miscellaneous'),
]
