# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                           |    Stmts |     Miss |   Cover |   Missing |
|------------------------------- | -------: | -------: | ------: | --------: |
| src/senzing/\_\_init\_\_.py    |        8 |        0 |    100% |           |
| src/senzing/szconfig.py        |      119 |       11 |     91% |192, 195-197, 299, 306, 311, 326, 331, 338, 348, 365 |
| src/senzing/szconfigmanager.py |      105 |       10 |     90% |179, 182-184, 231-232, 285, 291, 306, 312, 329 |
| src/senzing/szdiagnostic.py    |      102 |       18 |     82% |165, 168-170, 232, 270, 282, 287-291, 309, 311-318, 321-323 |
| src/senzing/szengine.py        |      417 |       50 |     88% |322, 325-328, 707, 712, 761, 771, 778, 884-896, 899-913, 956-970, 973-989, 1008, 1021, 1064, 1072, 1122, 1132, 1137, 1144-1151, 1156, 1171, 1176, 1213, 1286-1295 |
| src/senzing/szproduct.py       |       61 |        7 |     89% |130, 133-135, 164-165, 208, 224 |
| src/senzing/szversion.py       |       29 |        0 |    100% |           |
|                      **TOTAL** |  **841** |   **96** | **89%** |           |


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