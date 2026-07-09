# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath("_ext"))

project = "inZOI ModKit"
copyright = "2026, Om1ji"
author = "Om1ji"
release = "0.1"

extensions = [
    "myst_parser",
    "sphinx.ext.autosectionlabel",
    "jsonblock",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".venv", "README.md"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

language = "ru"

autosectionlabel_prefix_document = True

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_extra_path = ["_extra"]
html_title = "inZOI ModKit"

html_theme_options = {
    "sidebar_hide_name": False,
}
