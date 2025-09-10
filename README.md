# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python-core/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                   |    Stmts |     Miss |   Cover |   Missing |
|--------------------------------------- | -------: | -------: | ------: | --------: |
| src/senzing\_core/\_\_init\_\_.py      |       21 |        7 |     67% |     19-27 |
| src/senzing\_core/\_helpers.py         |      181 |       14 |     92% |43-50, 56, 141, 183, 189-190, 229-233 |
| src/senzing\_core/szabstractfactory.py |      170 |        2 |     99% |   318-319 |
| src/senzing\_core/szconfig.py          |      117 |        0 |    100% |           |
| src/senzing\_core/szconfigmanager.py   |      121 |        0 |    100% |           |
| src/senzing\_core/szdiagnostic.py      |       89 |        5 |     94% |199-205, 212, 218-219 |
| src/senzing\_core/szengine.py          |      425 |       23 |     95% |538-549, 589, 633, 748, 765, 789, 810, 947-953, 964-969 |
| src/senzing\_core/szproduct.py         |       45 |        0 |    100% |           |
|                              **TOTAL** | **1169** |   **51** | **96%** |           |


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