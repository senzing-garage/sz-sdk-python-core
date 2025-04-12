# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python-core/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                   |    Stmts |     Miss |   Cover |   Missing |
|--------------------------------------- | -------: | -------: | ------: | --------: |
| src/senzing\_core/\_\_init\_\_.py      |        7 |        0 |    100% |           |
| src/senzing\_core/\_helpers.py         |      135 |        3 |     98% |186, 189-190 |
| src/senzing\_core/\_version.py         |       24 |        0 |    100% |           |
| src/senzing\_core/szabstractfactory.py |       87 |       10 |     89% |92, 105, 189-190, 193-194, 196-197, 200-201 |
| src/senzing\_core/szconfig.py          |      120 |        0 |    100% |           |
| src/senzing\_core/szconfigmanager.py   |      105 |        0 |    100% |           |
| src/senzing\_core/szdiagnostic.py      |       71 |        4 |     94% |206-212, 215-216 |
| src/senzing\_core/szengine.py          |      374 |       33 |     91% |532-547, 585, 716, 733, 756, 777, 897-903, 925-936, 1042-1049 |
| src/senzing\_core/szproduct.py         |       34 |        0 |    100% |           |
|                              **TOTAL** |  **957** |   **50** | **95%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/senzing-garage/sz-sdk-python-core/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python-core/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/senzing-garage/sz-sdk-python-core/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python-core/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fsenzing-garage%2Fsz-sdk-python-core%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python-core/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.