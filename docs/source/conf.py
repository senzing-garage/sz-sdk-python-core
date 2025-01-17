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
copyright = "2025, Senzing"
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

# Setup for process_docstring()
PROCESS_DOCSTRING_DEBUG = os.getenv("SPHINX_PROCESS_DOCSTRING_DEBUG", "")
try:
    # Running "locally" using Make
    if not os.getenv("GITHUB_ACTIONS", ""):
        print("\nPROCESS_DOCSTRING: Not running in a GitHub action...")

        # Example response = 153-ant-1
        git_branch = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, check=True
        ).stdout.decode(encoding="utf-8")

        # Example response = git@github.com:senzing-garage/sz-sdk-python-core.git
        git_repo = subprocess.run(
            ["git", "config", "--get-all", "remote.origin.url"], capture_output=True, check=True
        ).stdout.decode(encoding="utf-8")

        # Capture only senzing-garage/sz-sdk-python-core
        if git_repo:
            git_repo_list = git_repo.split(":")
            git_repo = git_repo_list[-1]
            git_repo = git_repo.replace(".git", "")
    else:
        print("\nPROCESS_DOCSTRING: Running in a GitHub action...")
        # Example response = 153-ant-1
        git_branch = os.getenv("GITHUB_REF_NAME", "")
        # Example response = senzing-garage/sz-sdk-python-core
        git_repo = os.getenv("GITHUB_REPOSITORY", "")

    git_branch = git_branch.strip()
    git_repo = git_repo.strip()

    print(f"PROCESS_DOCSTRING: {git_branch = }")
    print(f"PROCESS_DOCSTRING: {git_repo = }\n")

    if not git_branch or not git_repo:
        raise ValueError("no value for either git_branch or git_repo")
except (subprocess.CalledProcessError, FileNotFoundError, TypeError, IndexError, ValueError) as err:
    print("ERROR: Failed processing doc strings: ")
    raise err


def process_abstract_docstring(app, what, name, obj, options, lines):
    """
    When processing doc strings from (abstract) sz-sdk-python check if any line in the doc string has a
    remote import (rli directive) for the examples and output files in a concrete package (for example,
    sz-sdk-python-core or sz-sdk-python-grpc).

    If the rli directive is found and is referencing /examples/ replace /main/ with the current branch to
    point to examples in that branch to build the docs and not the current main branch; examples in main
    may not be current if the working branch has modified them.
    """
    if PROCESS_DOCSTRING_DEBUG:
        print(f"\nPROCESS_DOCSTRING: {app = }")
        print(f"PROCESS_DOCSTRING: {what = }")
        print(f"PROCESS_DOCSTRING: {name = }")
        print(f"PROCESS_DOCSTRING: {obj = }")
        print(f"PROCESS_DOCSTRING: {options = }")
        print(f"PROCESS_DOCSTRING: {lines = }")

    for i, line in enumerate(lines):
        # .. rli:: https://raw.githubusercontent.com/senzing-garage/sz-sdk-python-core/refs/heads/main/examples/szengine/add_record.py
        if f".. rli:: https://raw.githubusercontent.com/{git_repo}/refs/heads/main/examples/" in line:
            print(f"PROCESS_DOCSTRING: Replacing /main/ with /{git_branch}/ for {what} {name}, line: {line.strip()}")
            lines[i] = line.replace("/main/", f"/{git_branch}/")
            print(f"PROCESS_DOCSTRING:\t{lines[i].strip()}\n")


def setup(app):
    """Hook to autodoc to process docs strings from (abstract) sz-sdk-python"""
    app.connect("autodoc-process-docstring", process_abstract_docstring)
