# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], [markdownlint],
and this project adheres to [Semantic Versioning].

## [Unreleased]

## [1.0.3] - 2025-10-02

### Changed in 1.0.3

- Updated dependencies

## [1.0.2] - 2025-09-25

### Fixed in 1.0.2

- Destroy SzProductCore instance after use in \_\_init\_\_.py

## [1.0.1] - 2025-09-12

### Fixed in 1.0.1

- Pylint failure with updated pylint-per-file-ignores

## [1.0.0] - 2025-08-06

### Changed in 1.0.0

- Migration guide and metadata updates

## [0.4.1] - 2025-07-23

### Fixed in 0.4.1

- szconfig unregister_data_source.py example was calling register_data_source()

## [0.4.0] - 2025-07-19

### Changed in 0.4.0

- Abstract factory improvements

## [0.3.17] - 2025-07-11

### Changed in 0.3.17

- Change SzConfig.add_data_source to SzConfig.register_data_source
- Change SzConfig.delete_data_source to SzConfig.unregister_data_source
- Change SzConfig.get_data_sources to SzConfig.get_data_source_registry
- Change SzDiagnostic.check_datastore_performance to SzDiagnostic.check_repository_performance
- Change SzDiagnostic.get_datastore_info to SzDiagnostic.get_repository_info
- Change SzEngine.close_export to SzEngine.close_export_report
- Change SzEngine.preprocess_record to SzEngine.get_record_preview
- Change to new C library names

## [0.3.16] - 2025-07-02

### Added in 0.3.16

- Senzing binary and Python version checks

### Changed in 0.3.16

- Internal refactoring, clean up, and corrections

### Removed in 0.3.16

- _version.py, merged into_helpers.py

## [0.3.15] - 2025-06-18

### Changed in 0.3.15

- szconfigmanager.get_configs changed to szconfigmanager.get_config_registry

### Fixed in 0.3.15

- Example output for preprocess_record updated

## [0.3.14] - 2025-06-12

### Changed in 0.3.14

- Lowered sphinx-tabs version to 3.4.5 due to dependency issue with sphinx-toolbox currently
- Some method definitions now use new default flags instead of integer values in szengine.py
- SZ_NO_FLAGS is now defined in the abstract for szengineflags.py and no longer in constants.py

### Fixed in 0.3.14

- Change `preprocess_record` and example to use `SZ_PREPROCESS_RECORD_DEFAULT_FLAGS`

## [0.3.13] - 2025-06-10

### Changed in 0.3.13

- To be consistent with Sz engine and orjson, if json.dumps() is used (orjson not available) in _helpers.py don't add spaces after : and , separators

### Removed in 0.3.13

- `from typing_extensions import ...` in _helpers.py is removed to simplify product requirements

## [0.3.12] - 2025-05-21

### Added in 0.3.12

- New tests for szconfig

### Changed in 0.3.12

- Examples cleanup

## [0.3.11] - 2025-05-08

### Added in 0.3.11

- Improved docstring to SzAbstractFactoryCore initializer
- Added config_id argument to docstring for initialize in szengine and szdiagnostic

### Changed in 0.3.11

- Added getter property to szabstractfactory for public instance variables
- Marked internal instance variables private for szabstractfactory

### Removed in 0.3.11

- Examples for szengineflags class methods removed from abstract

## [0.3.10] - 2025-05-02

### Added in 0.3.10

- Migration guide

## [0.3.9] - 2025-04-30

### Changed in 0.3.9

- Changed default flag for why_search() to SZ_WHY_SEARCH_DEFAULT_FLAGS

## [0.3.8] - 2025-04-21

### Changed in 0.3.8

- Simplify and clean up examples

## [0.3.7] - 2025-04-18

### Changed in 0.3.7

- Case on example variables

### Removed in 0.3.7

- Empty example files for early adaptor methods that are not documented

## [0.3.6] - 2025-04-17

### Added in 0.3.6

- Expanded test coverage
- Check and raise SzSdkError for wrong types in _helpers.py build functions

### Changed in 0.3.6

- Simplified escaping JSON strings in _helpers.py
- Changed exception capturing, raising, and messages for errors occurring within the SDK
- Tests previously catching TypeError now catch SzSdkError

### Removed in 0.3.6

- SDK_EXCEPTION_MAP and functions, replaced with use of SzSdkError
- Shebang in modules

## [0.3.5] - 2025-04-16

### Added in 0.3.5

- `SzEngine.why_search`

## [0.3.4] - 2025-04-11

### Changed in 0.3.4

- Restructure `SzConfig` and `SzConfigManager`

## [0.3.3] - 2025-02-06

### Changed in 0.3.3

- On Darwin look for libSz.dylib as the Senzing lib

## [0.3.2] - 2025-01-28

### Changed in 0.3.2

- Change class names to be more specific, e.g., core vs grpc
- Simplified \_\_init\_\_.py
- Modify examples to import from senzing and senzing_core
- Modified workflows and make files to use pytest instead of unittest for examples
- Cleaned up tne examples
- With info methods return "" instead of "{}" for simpler checking

### Added in 0.3.2

- Added custom documentation processing to Sphinx
- Added documentation-requirements.txt

### Fixed in 0.3.2

- Fixed error from building Sphinx doc for html_static_path = ["_static"]

## [0.3.1] - 2024-12-04

### Added in 0.3.1

- `senzing` package dependency

### Deleted in 0.3.1

- `senzing-abstract` package dependency

## [0.3.0] - 2024-12-03

### Changed in 0.3.0

- Renamed repository from sz-sdk-python to sz-sdk-python-core

## [0.2.2] - 2024-11-28

### Changed in 0.2.2

- Aligned create engine method calls to new abstract
- Improvements to helper functions

## [0.2.1] - 2024-11-22

### Added in 0.2.1

- Improvements to helpers

## [0.2.0] - 2024-11-04

### Deleted in 0.2.0

- Deleted abstract, dict and truthset packages from core SDK

## [0.1.0] - 2024-10-27

### Added to 0.1.0

- `SzAbstractFactory`
- Updated examples

## [0.0.9] - 2024-06-13

### Added to 0.0.9

- Continued updates

## [0.0.8] - 2024-06-07

### Added to 0.0.8

- Continued updates

## [0.0.7] - 2024-05-31

### Added to 0.0.7

- Continued updates

## [0.0.6] - 2024-05-15

### Added to 0.0.6

- Continued updates to initial version

## [0.0.5] - 2024-05-07

### Added to 0.0.5

- Examples for sphinx documentation

## [0.0.4] - 2024-04-19

### Added to 0.0.4

- Updates

## [0.0.3] - 2024-04-17

### Added to 0.0.3

- Updates

## [0.0.2] - 2024-04-05

### Added to 0.0.2

- Before change from G2 to Sz

## [0.0.1] - 2024-04-01

### Added to 0.0.1

- Initial work

[Keep a Changelog]: https://keepachangelog.com/en/1.0.0/
[markdownlint]: https://dlaa.me/markdownlint/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html
