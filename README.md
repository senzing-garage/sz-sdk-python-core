# sz-sdk-python-core

If you are beginning your journey with [Senzing],
please start with [Senzing Quick Start guides].

You are in the [Senzing Garage] where projects are "tinkered" on.
Although this GitHub repository may help you understand an approach to using Senzing,
it's not considered to be "production ready" and is not considered to be part of the Senzing product.
Heck, it may not even be appropriate for your application of Senzing!

## :warning: WARNING: sz-sdk-python-core is still in development :warning: _

At the moment, this is "work-in-progress" with Semantic Versions of `0.n.x`.
Although it can be reviewed and commented on,
the recommendation is not to use it yet.

## Synopsis

The Senzing `sz-sdk-python-core` package provides a [Python] Software Development Kit
adhering to the abstract classes of [sz-sdk-python]
that wraps the Senzing C SDK APIs.

[![Python 3.11 Badge]][Python 3.11]
[![PEP8 Badge]][PEP8]
[![PyPI version Badge]][PyPi version]
[![Downloads Badge]][Downloads]
[![License Badge]][License]
[![Coverage Badge]][Coverage]

## Overview

The Senzing `sz-sdk-python-core` packages enable Python programs to call Senzing library functions.
Under the covers, Python makes calls to the functions in the Senzing C libraries.

The `sz-sdk-python-core` package implements the following [sz-sdk-python] interfaces:

1. [SzConfig]
1. [SzConfigMgr]
1. [SzDiagnostic]
1. [SzEngine]
1. [SzProduct]

Other implementations of the [sz-sdk-python] interface include:

- [sz-sdk-python-grpc] - for calling Senzing SDK APIs over gRPC

## Use

(TODO:)

## References

1. [Development]
1. [Errors]
1. [Examples]
1. Related artifacts:
    1. [DockerHub]
1. [sz-sdk-python package reference]

[Coverage badge]: https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fsenzing-garage%2Fsz-sdk-python-core%2Fpython-coverage-comment-action-data%2Fendpoint.json
[Coverage]: https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python-core/blob/python-coverage-comment-action-data/htmlcov/index.html
[Development]: docs/development.md
[DockerHub]: https://hub.docker.com/r/senzing/sz-sdk-python-core
[Downloads Badge]: https://static.pepy.tech/badge/sz-sdk-python-core
[Downloads]: https://pepy.tech/project/sz-sdk-python-core
[Errors]: docs/errors.md
[Examples]: docs/examples.md
[License Badge]: https://img.shields.io/badge/License-Apache2-brightgreen.svg
[License]: https://github.com/senzing-garage/sz-sdk-python-core/blob/main/LICENSE
[PEP8 Badge]: https://img.shields.io/badge/code%20style-pep8-orange.svg
[PEP8]: https://www.python.org/dev/peps/pep-0008/
[PyPI version Badge]: https://badge.fury.io/py/senzing-core.svg
[PyPi version]: https://badge.fury.io/py/senzing-core
[Python 3.11 Badge]: https://img.shields.io/badge/python-3.11-blue.svg
[Python 3.11]: https://www.python.org/downloads/release/python-3110/
[Python]: https://www.python.org/
[Senzing Garage]: https://github.com/senzing-garage
[Senzing Quick Start guides]: https://docs.senzing.com/quickstart/
[Senzing]: https://senzing.com/
[sz-sdk-python package reference]: https://hub.senzing.com/sz-sdk-python/
[sz-sdk-python-grpc]: https://github.com/senzing-garage/sz-sdk-python-grpc
[sz-sdk-python]: https://github.com/senzing-garage/sz-sdk-python/tree/main/src/senzing
[SzConfig]: https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing/szconfig.py
[SzConfigMgr]: https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing/szconfigmanager.py
[SzDiagnostic]: https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing/szdiagnostic.py
[SzEngine]: https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing/szengine.py
[SzProduct]: https://github.com/senzing-garage/sz-sdk-python/blob/main/src/senzing/szproduct.py
