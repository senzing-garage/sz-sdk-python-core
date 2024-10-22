# sz-sdk-python development

The following instructions are useful during development.

**Note:** This has been tested on Linux and Darwin/macOS.
It has not been tested on Windows.

## Prerequisites for development

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
    1. [git]
    1. [make]
    1. [docker]
    1. [sphinx]

## Install Senzing C library

Since the Senzing library is a prerequisite, it must be installed first.

1. Verify Senzing C shared objects, configuration, and SDK header files are installed.
    1. `/opt/senzing/g2/lib`
    1. `/opt/senzing/g2/sdk/c`
    1. `/etc/opt/senzing`

1. If not installed, see [How to Install Senzing for Python Development].

## Install Git repository

1. Identify git repository.

    ```console
    export GIT_ACCOUNT=senzing-garage
    export GIT_REPOSITORY=sz-sdk-python
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"

    ```

1. Using the environment variables values just set, follow
   steps in [clone-repository] to install the Git repository.

## Dependencies

1. A one-time command to install dependencies needed for `make` targets.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    make dependencies-for-development

    ```

1. Install dependencies needed for [Python] code.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    make dependencies

    ```

## Lint

1. Run linting.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    make lint

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

1. Verify that `senzing` is not installed.
   Example:

    ```console
    python3 -m pip freeze | grep -e senzing
    ```

   Nothing is returned.

1. Install directly from `wheel` file.
   Example:

    ```console
    python3 -m pip install ${GIT_REPOSITORY_DIR}/dist/*.whl
    ```

1. Verify that `senzing` is installed.
   Example:

    ```console
    python3 -m pip freeze | grep -e senzing
    ```

    Example return:
    > senzing @ file:///home/senzing/senzing-garage.git/sz-sdk-python-/dist/senzing-0.0.1-py3-none-any.whl#sha256=2a4e5218d66d5be60ee31bfad5943e6611fc921f28a4326d9594ceceae7e0ac1

1. Uninstall the `senzing` python package.
   Example:

    ```console
    python3 -m pip uninstall senzing
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
