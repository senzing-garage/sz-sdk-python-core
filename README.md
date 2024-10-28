# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                 |    Stmts |     Miss |   Cover |   Missing |
|----------------------------------------------------- | -------: | -------: | ------: | --------: |
| src/senzing/\_\_init\_\_.py                          |       16 |        0 |    100% |           |
| src/senzing/\_helpers.py                             |      148 |        6 |     96% |122-123, 126, 132, 152-153 |
| src/senzing/\_version.py                             |       24 |        0 |    100% |           |
| src/senzing/szabstractfactory.py                     |       99 |        6 |     94% |94, 107, 213-214, 217-218 |
| src/senzing/szconfig.py                              |       85 |        0 |    100% |           |
| src/senzing/szconfigmanager.py                       |       71 |        0 |    100% |           |
| src/senzing/szdiagnostic.py                          |       67 |        4 |     94% |261-267, 270-271 |
| src/senzing/szengine.py                              |      346 |       24 |     93% |647, 790, 807, 832, 853, 969-975, 983-987, 997-1010, 1121-1128 |
| src/senzing/szproduct.py                             |       33 |        0 |    100% |           |
| src/senzing\_abstract/\_\_init\_\_.py                |       11 |        0 |    100% |           |
| src/senzing\_abstract/constants.py                   |       12 |        0 |    100% |           |
| src/senzing\_abstract/engine\_exception\_map.py      |       19 |        0 |    100% |           |
| src/senzing\_abstract/observer\_abstract.py          |        5 |        5 |      0% |     13-33 |
| src/senzing\_abstract/szabstractfactory\_abstract.py |       27 |        1 |     96% |       200 |
| src/senzing\_abstract/szconfig\_abstract.py          |       26 |        1 |     96% |       254 |
| src/senzing\_abstract/szconfigmanager\_abstract.py   |       24 |        1 |     96% |       204 |
| src/senzing\_abstract/szdiagnostic\_abstract.py      |       20 |        1 |     95% |       137 |
| src/senzing\_abstract/szengine\_abstract.py          |       75 |        1 |     99% |      1035 |
| src/senzing\_abstract/szengineflags.py               |       92 |       16 |     83% |57-66, 72-78 |
| src/senzing\_abstract/szerror.py                     |       49 |       26 |     47% |54-55, 64-76, 85, 94-102, 114-120, 136-151 |
| src/senzing\_abstract/szhelpers.py                   |       24 |       21 |     12% |     23-44 |
| src/senzing\_abstract/szproduct\_abstract.py         |       16 |        1 |     94% |       103 |
| src/senzing\_dict/\_\_init\_\_.py                    |        6 |        6 |      0% |       1-7 |
| src/senzing\_dict/szconfig.py                        |       34 |       34 |      0% |     8-135 |
| src/senzing\_dict/szconfigmanager.py                 |       32 |       32 |      0% |     8-127 |
| src/senzing\_dict/szdiagnostic.py                    |       27 |       27 |      0% |     7-107 |
| src/senzing\_dict/szengine.py                        |       84 |       84 |      0% |     6-486 |
| src/senzing\_dict/szproduct.py                       |       23 |       23 |      0% |      7-83 |
| src/senzing\_truthset/\_\_init\_\_.py                |        5 |        0 |    100% |           |
| src/senzing\_truthset/customers.py                   |        2 |        0 |    100% |           |
| src/senzing\_truthset/datasources.py                 |        2 |        0 |    100% |           |
| src/senzing\_truthset/references.py                  |        2 |        0 |    100% |           |
| src/senzing\_truthset/watchlist.py                   |        2 |        0 |    100% |           |
|                                            **TOTAL** | **1508** |  **320** | **79%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/senzing-garage/sz-sdk-python/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/senzing-garage/sz-sdk-python/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fsenzing-garage%2Fsz-sdk-python%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.