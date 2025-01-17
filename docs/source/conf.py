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
PROCESS_DOCSTRING_DEBUG = os.getenv("SPHINX_PROCESS_DOCSTRING_DEBUG", "")
# TODO
try:
    GIT_ACTIONS = os.getenv("GITHUB_ACTIONS", "")
    if not GIT_ACTIONS:
        print("PROCESS_DOCSTRING: Not running in a Github action...")

        # Example response = 153-ant-1
        git_branch = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, check=True
        ).stdout.decode(encoding="utf-8")

        # Example response = git@github.com:senzing-garage/sz-sdk-python-core.git
        git_repo = subprocess.run(
            ["git", "config", "--get-all", "remote.origin.url"], capture_output=True, check=True
        ).stdout.decode(encoding="utf-8")
        if git_repo:
            git_repo_list = git_repo.split(":")
            git_repo = git_repo_list[-1]
            git_repo = git_repo.replace(".git", "")
    else:
        print("PROCESS_DOCSTRING: Running in a Github action...")
        # Example response = 153-ant-1
        git_branch = os.getenv("GITHUB_REF_NAME", "")
        # Example response = senzing-garage/sz-sdk-python-core
        git_repo = os.getenv("GITHUB_REPOSITORY", "")

    git_branch = git_branch.strip()
    git_repo = git_repo.strip()

    # TODO Debug
    print(f"PROCESS_DOCSTRING: {git_branch = }")
    print(f"PROCESS_DOCSTRING: {git_repo = }\n")
except (subprocess.CalledProcessError, FileNotFoundError, TypeError, IndexError) as err:
    print(f"\nERROR: Failed trying to process doc strings - {err}\n")
    sys.exit(1)


# TODO
def process_docstring(app, what, name, obj, options, lines):
    # print("\nDEBUG: In process_docstring()...\b")

    if PROCESS_DOCSTRING_DEBUG:
        print(f"\n{app = }")
        print(f"{what = }")
        print(f"{name = }")
        print(f"{obj = }")
        print(f"{options = }")
        print(f"{lines = }\n")

    for i, line in enumerate(lines):
        # .. rli:: https://raw.githubusercontent.com/senzing-garage/sz-sdk-python-core/refs/heads/main/examples/szengine/add_record.py
        if f".. rli:: https://raw.githubusercontent.com/{git_repo}/refs/heads/main/examples/" in line:
            print(f"PROCESS_DOCSTRING: Replacing /main/ with /{git_branch}/ for {what} {name}, line: {line.strip()}")
            lines[i] = line.replace("/main/", f"/{git_branch}/")
            print(f"\tPROCESS_DOCSTRING: {lines[i].strip()}\n")


def setup(app):
    # print("\nDEBUG: In setup()...\n")
    app.connect("autodoc-process-docstring", process_docstring)
