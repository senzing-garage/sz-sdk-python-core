# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/senzing-garage/sz-sdk-python/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                           |    Stmts |     Miss |   Cover |   Missing |
|------------------------------- | -------: | -------: | ------: | --------: |
| src/senzing/\_\_init\_\_.py    |        8 |        0 |    100% |           |
| src/senzing/szconfig.py        |      116 |       11 |     91% |192, 195-197, 302, 308, 313, 329, 334, 340, 349, 366 |
| src/senzing/szconfigmanager.py |      105 |       10 |     90% |178, 181-183, 230-231, 283, 292, 311, 317, 335 |
| src/senzing/szdiagnostic.py    |      103 |       18 |     83% |169, 172-174, 236, 275, 291, 299-307, 325, 334-341, 351-353 |
| src/senzing/szengine.py        |      413 |       50 |     88% |314, 317-320, 710, 715, 776, 786, 792, 907-929, 934-957, 997-1021, 1024-1049, 1079, 1092, 1143, 1151, 1199, 1210, 1222, 1229-1241, 1246, 1266, 1276, 1319, 1406-1421 |
| src/senzing/szhasher.py        |       63 |       14 |     78% |62-63, 79, 84-85, 119-120, 128, 149, 161, 179-180, 199, 206 |
| src/senzing/szproduct.py       |       61 |        7 |     89% |129, 132-134, 165-166, 210, 226 |
| src/senzing/szversion.py       |       29 |        0 |    100% |           |
|                      **TOTAL** |  **898** |  **110** | **88%** |           |


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