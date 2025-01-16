# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import subprocess
import sys

project = "sz-sdk-python-core"
copyright = "2024, Senzing"
author = "senzing"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]


# -- Customization -----------------------------------------------------------

sys.path.insert(0, os.path.abspath("../../src"))

# TODO
GIT_WORKFLOW = os.getenv("GITHUB_ACTIONS", "")
if not GIT_WORKFLOW:
    print("Not running in a Github action...")
    git_branch_name = subprocess.run(
        ["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, check=True
    ).stdout.decode(encoding="utf-8")
else:
    print("Running in a Github action...")
    git_branch_name = os.getenv("GITHUB_REF_NAME", "")
git_branch_name = git_branch_name.strip()
print(f"\n{git_branch_name = }\n")

extensions = [
    "autodocsumm",  # to generate tables of functions, attributes, methods, etc.
    "sphinx_toolbox.collapse",  # support collapsable sections
    "sphinx.ext.autodoc",  # automatically generate documentation for modules
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",  # to read Google-style or Numpy-style docstrings
    "sphinxext.remoteliteralinclude",  # extends literalinclude to be able to pull files from URLs
    "sphinx.ext.viewcode",  # to allow vieing the source code in the web page
]

exclude_patterns = ["*.py"]

html_theme = "sphinx_rtd_theme"
# autodoc_inherit_docstrings = False  # don't include docstrings from the parent class
# autodoc_typehints = "description"   # Show types only in descriptions, not in signatures


# TODO
def process_docstring(app, what, name, obj, options, lines):
    print("\nDEBUG: In process_docstring()...\b")

    if "add_record" in name:
        print(f"\n{app = }")
        print(f"{what = }")
        print(f"{name = }")
        print(f"{obj = }")
        print(f"{options = }")
        print(f"{lines = }\n")
        for line in lines:
            print(f"\t{line}")

    for i, line in enumerate(lines):
        # line: str = line.strip()
        if line.startswith("                .. rli:: https://raw.githubusercontent.com/senzing-garage/"):
            print(f"Replacing in: {line}")
            lines[i] = line.replace("/main/", f"/{git_branch_name}/")


def setup(app):
    print("\nDEBUG: In setup()...\n")
    app.connect("autodoc-process-docstring", process_docstring)
