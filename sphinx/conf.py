import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "absp"
author = "novablast"
language = "en"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

html_theme = "furo"
html_title = "absp"
