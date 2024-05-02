# sz-sdk-python development

## Install python test tools

1. Individual tools

    ```console
    python3 -m pip install \
        bandit \
        coverage \
        black \
        flake8 \
        mypy \
        pylint \
        pytest
    ```

1. [Sphinx](https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/sphinx.md) tools

    ```console
    python3 -m pip install \
        sphinx \
        sphinx-autodoc-typehints \
        sphinx-gallery \
        sphinx-jinja2-compat \
        sphinx-prompt \
        sphinx-rtd-theme \
        sphinx-tabs \
        sphinx-toolbox \
        sphinxcontrib-applehelp \
        sphinxcontrib-devhelp \
        sphinxcontrib-htmlhelp \
        sphinxcontrib-jquery \
        sphinxcontrib-jsmath \
        sphinxcontrib-qthelp \
        sphinxcontrib-serializinghtml
    ```

## Running tests

1. [Bandit]

    ```console
    clear; make clean setup bandit
    ```

1. [Black]

    ```console
    clear; make clean setup black
    ```

1. [Flake8]

    ```console
    clear; make clean setup flake8
    ```

1. [Isort]

    ```console
    clear; make clean setup isort
    ```

1. [Mypy]

    ```console
    clear; make clean setup mypy
    ```

1. [Pylint]

    ```console
    clear; make clean setup pylint
    ```

1. [Pytest] and [Coverage]

    ```console
    clear; make clean setup pytest coverage
    ```

1. Test

    ```console
    clear; make clean setup test
    ```

1. (Optional) Run all

    ```console
    clear
    make clean setup bandit
    make clean setup black
    make clean setup flake8
    make clean setup isort
    make clean setup mypy
    make clean setup pylint
    make clean setup pytest coverage
    make clean setup test
    ```

## References

1. [Bandit]
1. [Black]
1. [Coverage]
1. [Flake8]
1. [Isort]
1. [Mypy]
1. [Pylint]
1. [Pytest]
1. [Sphinx]

[Bandit]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/bandit.md
[Black]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/black.md
[Coverage]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/coverage.md
[Flake8]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/flake8.md
[Isort]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/isort.md
[Mypy]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/mypy.md
[Pylint]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/pylint.md
[Pytest]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/pytest.md
[Sphinx]: https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/sphinx.md
