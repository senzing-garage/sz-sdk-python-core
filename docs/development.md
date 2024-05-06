# sz-sdk-python development

## Prerequisites for development

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
    1. [git](https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/git.md)
    1. [make](https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/make.md)
    1. [docker](https://github.com/senzing-garage/knowledge-base/blob/main/WHATIS/docker.md)

## Clone repository

For more information on environment variables,
see [Environment Variables](https://github.com/senzing-garage/knowledge-base/blob/main/lists/environment-variables.md).

1. Set these environment variable values:

    ```console
    export GIT_ACCOUNT=senzing-garage
    export GIT_REPOSITORY=sz-sdk-python
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
    ```

1. Using the environment variables values just set, follow steps in [clone-repository](https://github.com/senzing-garage/knowledge-base/blob/main/HOWTO/clone-repository.md) to install the Git repository.

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

## Working with Python wheel file

1. Build the `wheel` file for distribution.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    make package
    ```

1. Verify that `senzing-grpc` is not installed.
   Example:

    ```console
    python3 -m pip freeze | grep -e senzing-grpc -e senzing_grpc
    ```

   Nothing is returned.

1. Install directly from `wheel` file.
   Example:

    ```console
    python3 -m pip install ${GIT_REPOSITORY_DIR}/dist/*.whl
    ```

1. Verify that `senzing-grpc` is installed.
   Example:

    ```console
    python3 -m pip freeze | grep -e senzing-grpc -e senzing_grpc
    ```

    Example return:
    > senzing-grpc @ file:///home/senzing/senzing-garage.git/sz-sdk-python-grpc/dist/senzing_grpc-0.0.1-py3-none-any.whl#sha256=2a4e5218d66d5be60ee31bfad5943e6611fc921f28a4326d9594ceceae7e0ac1

1. Uninstall the `senzing-grpc` python package.
   Example:

    ```console
    python3 -m pip uninstall senzing-grpc
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
