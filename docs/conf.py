# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

from fRAGme import __version__ as fRAGme_version

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "fRAGme"
copyright = "2024, Henning Krause"
author = "Henning Krause"

release = fRAGme_version
version = fRAGme_version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinxcontrib.spelling",
    "sphinx_sitemap",
    "matplotlib.sphinxext.plot_directive",
    "myst_parser",
    "nbsphinx",
    "nbsphinx_link",
    "jupyter_sphinx",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

autodoc_default_options = {"members": True, "inherited-members": True}


# Skip property members --> They should be defined in Attributes
def skip_property_member(app, what, name, obj, skip, options):
    if isinstance(obj, property):
        return True


def setup(app):
    app.connect("autodoc-skip-member", skip_property_member)


templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "README.md",
    "**.ipynb_checkpoints",
]

autosummary_generate = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_favicon = "_static/favicon.png"
html_theme_options = {
    "logo_only": True,
    "display_version": True,
}
html_css_files = [
    "css/custom.css",
]

latex_engine = "xelatex"
latex_elements = {
    "preamble": r"""
    \usepackage{braket}
    """,
}

suppress_warnings = ["myst.header", "config.cache"]

# base URL for sphinx_sitemap
html_baseurl = "https://krauhen.github.io/fRAGme/"
sitemap_url_scheme = "{link}"
