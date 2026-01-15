# Migrating from Version 3 to Version 4 Senzing Python SDK

This document outlines fundamental changes and differences to the version 4.0 Python SDK from the version v3.x Python SDK.
Although there are numerous changes to the version 4.0 SDK, migrating your Python applications and services is straight forward.
The changes should make development more straightforward and natural for Python developers.

If you haven't already, also check [breaking changes][breaking-changes].
This covers additional details not specifically related to Python such as hardware, software, overall SDK changes, and database schema changes.

## The G2 Naming and Prefix Retired

Artifacts such as modules, classes, exceptions and tools previously used the term "G2",
this is typically observed as a prefix to the aforementioned artifacts.
Senzing version 4.0 has, for the most part, replaced G2 with the term SZ, Sz, or sz depending on the context.
You may still notice G2 used in some of the overall product files, but the version 4.0 SDK Python artifacts now use a variant of SZ.
A few examples of such changes:

- Python SDK module naming, G2 is replaced with sz
  - G2Engine&period;py -> szengine&period;py

- Exceptions, G2 is replaced with Sz (and Error)
  - G2Exception -> SzError

- Engine flags, G2 is replaced with SZ
  - G2_ENTITY_DEFAULT_FLAGS -> SZ_ENTITY_DEFAULT_FLAGS

## Modules Structure

The version 3.x Python SDK modules are located in a single path for the product at `/opt/senzing/g2/sdk/python/senzing/` (or a project `<project_path>/sdk/python/senzing/`).
These modules contain concrete classes and methods for working with the Python SDK.

There are 2 paths for the version 4.0 modules, considering the product install path:

1. `/opt/senzing/er/sdk/python/senzing/`
   - Non-instantiable abstract base classes and constants for unifying the method signatures of concrete implementations, such as `senzing_core` below
2. `/opt/senzing/er/sdk/python/senzing_core/`
   - Instantiable concrete classes for working with the Python SDK

Python doesn't have interfaces similar to other languages, using abstract base classes in this manner achieves similar functionality.
The module classes in `senzing_core` inherit from the `senzing` module classes, ensuring the required methods and signatures are implemented.
[sz-sdk-python-grpc](https://github.com/senzing-garage/sz-sdk-python-grpc) is an example of another implementation using the `senzing` abstract base classes.

## Unified Initialization and Destruction

Previously, Senzing engine objects were individually instantiated and then initialized with `init`, passing in arguments to identify the instance, engine configuration settings,
and whether to use debug tracing. G2Diagnostic, G2Engine, and G2Product example initialization code might look like:

```python
from senzing import G2Diagnostic, G2Engine, G2Exception, G2Product

try:
    g2_diagnostic = G2Diagnostic()
    g2_diagnostic.init('example', engine_config, False)
    g2_engine = G2Engine()
    g2_engine.init('example', engine_config, False)
    g2_product = G2Product()
    g2_product.init('example', engine_config, False)
except G2Exception as err:
    raise err

try:
   # Do some work with the Senzing components
   ...
except G2Exception as err:
    raise err
```

The version 4.0 SDK uses an abstract factory pattern for the creation and initialization of engine objects.
The abstract factory is instantiated with the required configuration settings.
Subsequent engine objects requested from the abstract factory use the same single set of configuration settings.
This simplifies instantiation of engines and removes the possibility of inadvertently introducing configuration errors.
The same code for version 4.0:

```python
from senzing import SzError
from senzing_core import SzAbstractFactoryCore

try:
    sz_factory = SzAbstractFactoryCore('example', engine_config, verbose_logging=False)
    sz_diagnostic = sz_factory.create_diagnostic()
    sz_engine = sz_factory.create_engine()
    sz_product = sz_factory.create_product()
except SzError as err:
    raise err

try:
   # Do some work with the Senzing components
   ...
except SZError as err:
    raise err
```

## Method Response Assignment

Gone is allocating a bytearray to return method responses to.
Prior to version 4.0, the Senzing engine returned a return code to the Python SDK method.
If the return code was non-zero the error details were requested from the engine, converted to a Python exception with the error details and raised.
As the SDK method was collecting the return code, bytearrays were used in the version 3.x SDK to assign successful responses to.

```python
try:
    response = bytearray()
    g2_engine.searchByAttributes(
        record_json_str,
        response,
        G2EngineFlags.G2_SEARCH_BY_ATTRIBUTES_MINIMAL_ALL,
    )
except G2Exception as err:
    raise err
print(response.decode())
```

This has been improved in version 4.0, allowing the SDK to access the return code separately from responses.
Responses are now returned directly as types such as `str` and `int`.

```python
try:
    response = sz_engine.search_by_attributes(record_json_str, SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_DEFAULT_FLAGS)
except SzError as err:
    raise err
print(response)
```

## "With Info" Moves From Method to Flag {#with-info}

The version 3.x SDK provides "with info" methods to request a response for methods that perform entity resolution actions, such as adding, deleting, processing, and reevaluating.
In the version 3.x SDK, for example, `addRecord` is used to add a record:

```python
g2_engine.addRecord("TEST", "78720B", record_json_str)
```

`addRecordWithInfo` is used to add a record and return a response outlining any affected entities from the operation:

```python
response = bytearray()
g2_engine.addRecordWithInfo("TEST", "78720B", record_json_str, response)
print(response)
```

The separate `WithInfo` methods have been removed in the version 4.0 SDK.
The capability is now included in the `add_record`, `delete_record`, `process_redo_record`,`reevaluate_entity`, and `reevaluate_record` methods.
Requesting the with info response is achieved with the use of the optional `flags` argument and specifying the `SZ_WITH_INFO` engine flag.
The default is not to return the with info response, in which case an empty string is returned:

```python
...
try:
   _ = sz_engine.add_record("TEST", "78720B", record_json_str)
except SzError as err:
    raise err
...
```

Return the with info response using the `flags` argument:

```python
from senzing import SzEngineFlags, SzError
...

try:
   response = sz_engine.add_record("TEST", "78720B", record_json_str, flags=SzEngineFlags.SZ_WITH_INFO)
except SzError as err:
    raise err
else:
    send_to_queue(response)
...
```

## Redo Processing

Methods for fetching and processing redo records have changed.
In the version 3.x SDK, `getRedoRecord` is used to fetch a redo record (if any are available) and `process` to request the processing of the redo record.
`process` is really an internal method, it could handle redo and other record types the Senzing engine understands.
The `process` method is no longer available in version 4.0. A simple example to process redo records, in version 3.x:

```python
redo_record = bytearray()
white True:
    g2_engine.getRedoRecord(redo_record)
    if not redo_record:
        time.sleep(30)
        continue
    g2_engine.process(redo_record.decode())
```

To achieve the same in the version 4.0 SDK the methods are now `get_redo_record` and `process_redo_record`.

```python
white True:
    redo_record = sz_engine.get_redo_record()
    if not redo_record:
        time.sleep(30)
        continue
    sz_engine.process_redo_record(redo_record)
```

## Say Goodbye to JSON-formatted Input Arguments

A number of methods take a JSON string argument in the version 3.x SDK.
These are used to describe entities, records, or data sources and JSON strings to describe these would need to be built.

A single data source code:

```python
dsrc_code = '{\"DSRC_CODE\": \"CUSTOMERS\"}'
```

Multiple data source codes:

```python
dsrc_codes = '{\"DATA_SOURCES\": [\"REFERENCE\", \"CUSTOMERS\"]}'
```

One or more entity identifiers:

```python
entities = '{\"ENTITIES\": [{\"ENTITY_ID\": 1}, {\"ENTITY_ID\": 100002}, {\"ENTITY_ID\": 3490}]}'
```

One or more record identifiers:

```python
records = '{\"RECORDS\": [{\"DATA_SOURCE\": \"CUSTOMERS\", \"RECORD_ID\": \"1001\"}, {\"DATA_SOURCE\": \"WATCHLIST\", \"RECORD_ID\": \"1007\"}]}'
```

You no longer need to construct the JSON string for such arguments in version 4.0, methods accept these arguments as normal Python types.
The JSON strings from above are represented in version 4.0 as:

A single data source code:

```python
dsrc_code = "CUSTOMERS" # A string
```

Multiple data source codes:

```python
dsrc_codes = ["REFERENCE", "CUSTOMERS"] # A list of strings
```

One or more entity identifiers:

```python
entities = [1, 100002, 3490] # A list of integers
```

One or more record identifiers:

```python
records =  [("CUSTOMERS", "1001"), ("WATCHLIST", "1007")] # A list of tuples with strings
```

For example, `findNetworkByRecordID` in version 3.x has the argument `recordList` to specify the data sources and record IDs to find paths between and networks around.

```python
response = bytearray()
g2_engine.findNetworkByRecordID(
    ('\"RECORDS\": ['
        '{\"DATA_SOURCE\": \"CUSTOMERS\", \"RECORD_ID\": \"1001\"},'
        '{\"DATA_SOURCE\": \"WATCHLIST\", \"RECORD_ID\": \"1007\"},'
        '{\"DATA_SOURCE\": \"WATCHLIST\", \"RECORD_ID\": \"1010\"},'
    ']}')
    6,
    4,
    5,
    response
)
```

The equivalent method in version 4.0 - `find_network_by_record_id` - accepts a list of tuples, each consisting of 2 strings.
The first string represents the data source, the second the record ID.

```python
response = sz_engine.find_network_by_record_id([("CUSTOMERS", "1001"), ("WATCHLIST", "1007"), ("WATCHLIST", "1010")], 6, 4, 5) # No need to JSON-encode the argument anymore
```

Similarly, a call to `findPathIncludingSourceByEntityID` with the version 3.x SDK:

```python
response = bytearray()
g2_engine.findPathIncludingSourceByEntityID(
    787,
    100180,
    4,
    "{}",
    '{\"DATA_SOURCES\": [\"REFERENCE\", \"CUSTOMERS\"]}'
    response
)
```

The same operation in version 4.0 becomes:

```python
response = sz_engine.find_path_by_entity_id(787, 100180, 4 required_data_sources=["REFERENCE", "CUSTOMERS"]) # No need to JSON-encode the argument anymore
```

These are the methods in the version 4.0 SDK with arguments no longer requiring a JSON string.

| Module   | Method                          | Argument              | Type              | Values                 |
| -------- | ------------------------------- | --------------------- | ----------------- | ---------------------- |
| szconfig | register_data_source            | data_source_code      | str               | Data Source            |
|          | unregister_data_source          | data_source_code      | str               | Data Source            |
| szengine | find_network_by_entity_id       | entity_ids            | [int, ...]        | Entity ID(s)           |
|          | find_network_by_record_id       | record_keys           | [(str, str), ...] | Data Source, Record ID |
|          | find_path_by_entity_id          | avoid_entity_ids      | [int, ...]        | Entity ID(s)           |
|          |                                 | required_data_sources | [str, ...]        | Data Source(s)         |
|          | find_path_by_record_id          | avoid_record_keys     | [(str, str), ...] | Data Source, Record ID |
|          |                                 | required_data_sources | [str, ...]        | Data Source(s)         |
|          | get_virtual_entity_by_record_id | record_keys           | [(str, str), ...] | Data Source, Record ID |

## Less is more

In addition to the `with info` methods [being removed in version 4.0](#with-info), other methods have been collapsed into fewer methods; such as for find path.
There are six methods in the version 3.x SDK for find path; three for finding paths by entity IDs and three for finding paths by record IDs.
You would choose one depending on if you were interested in excluding by entities or records in the path or, finding paths that contain specific data sources.

- `findPathByEntityID`
- `findPathByRecordID`
- `findPathExcludingByEntityID`
- `findPathExcludingByRecordID`
- `findPathIncludingSourceByEntityID`
- `findPathIncludingSourceByRecordID`

There are now 2 methods in the version 4.0 SDK, one for using entity IDs, the other using record IDs.

- `find_path_by_entity_id`
- `find_path_by_record_id`

The version 4.0 SDK methods take optional arguments for avoiding specific entities or records, and/or the path having specific data sources along it.

### findPathByEntityID -> find_path_by_entity_id

#### V3 findPathByEntityID

```python
response = bytearray()
g2_engine.findPathByEntityId(787, 201123, 3, response)
```

#### V4 find_path_by_entity_id

```python
response = sz_engine.find_path_by_entity_id(787, 201123, 3)
```

### findPathExcludingByEntityID -> find_path_by_entity_id

#### V3 findPathExcludingByEntityID

```python
response = bytearray()
g2_engine.findPathExcludingByEntityID(787, 201123, 3, '{\"ENTITIES\": [{\"ENTITY_ID\": 1}, {\"ENTITY_ID\": 100002}]}', response)
```

#### V4 find_path_by_entity_id - excluding

```python
response = sz_engine.find_path_by_entity_id(787, 201123, 3, [1, 100002])
```

### findPathIncludingSourceByEntityID -> find_path_by_entity_id

#### V3 findPathIncludingSourceByEntityID

```python
response = bytearray()
g2_engine.findPathIncludingSourceByEntityID(787, 201123, 3, '', '{\"DATA_SOURCES\": [\"REFERENCE\", \"CUSTOMERS\"]}', response)
```

#### V4 find_path_by_entity_id - including

```python
response = sz_engine.find_path_by_entity_id(787, 201123, 3, required_data_sources = ["REFERENCE", "CUSTOMERS"])
```

Note, in these examples a blank is used for `findPathIncludingSourceByEntityID` and a named argument for `find_path_by_entity_id`.
When requesting specific data sources, entity IDs to avoid can optionally be specified.

## Working with Configuration

A fairly significant change in the version 4.0 SDK compared to version 3.x pertains to working with configuration.
With version 3.x, the `G2Config` and `G2ConfigMgr` modules were independently initialized and managed.
The `G2Config` module was a functional interface used to work with in-memory configuration instances which were accessed via a numeric handle and required the closing of that handle when complete.

To create a new configuration, add a data source, and set it as the default config in the version 3.x SDK you might do the following:

```python
dsrc_code_id = bytearray()
new_config = bytearray()
new_config_id = bytearray()

try:
    # Initialize
    g2_config_mgr = G2ConfigMgr()
    g2_config_mgr.init("g2ConfigMgr", ini_params, False)
    g2_config = G2Config()
    g2_config.init("g2Config", ini_params, False)

    # Get the config handle
    config_handle = g2_config.create()

    # Add the data source to the new config and export the new config
    g2_config.addDataSource(config_handle, '{\"DSRC_CODE\": \"CUSTOMERS\"}', dsrc_code_id)
    g2_config.save(config_handle, new_config)

    # Register the new config and set it as the default
    g2_config_mgr.addConfig(new_config.decode(), "Add data source CUSTOMERS", new_config_id)
    g2_config_mgr.setDefaultConfigID(new_config_id)
except G2Exception as err:
    raise err
finally:
    # Cleanup
    config_handle.close(config_handle)
    g2_config_mgr.destroy()
    g2_config.destroy()
```

In version 4.0, the `SzConfig` module is subordinate to the `SzConfigManager` and literally represents a Senzing configuration as an object.
It removes the hassle of dealing with "config handles" that have to be closed as well:

```python
sz_factory = SzAbstractFactoryCore(MODULE_NAME, SETTINGS)

try:
    # Get the config manager from the abstract factory
    sz_configmanager = sz_factory.create_configmanager()

    # Create a new config
    sz_config = sz_configmanager.create_config_from_template()

    # Register the data source with the new config (no need to JSON encode anymore)
    sz_config.register_data_source("CUSTOMERS")

    # Register and set the default config in one shot
    new_config = sz_config.export()
    new_config_id = sz_configmanager.set_default_config(new_config), "Register data source CUSTOMERS")
except SzError as err:
    raise err
```

## Code Snippets

- [Version 4.0 Python Code Snippets](https://github.com/Senzing/code-snippets-v4/tree/main/python) provide examples of how to achieve many common tasks using the version 4.0 SDK.

## Additional Differences

These are Python specific not covered in [breaking changes][breaking-changes].
The tables don't outline every change, only those that are new or continue to exist in the version 4.0 SDK.
For a full list of changes see [breaking changes][breaking-changes]. A blank entry in the V3 column and a value in the V4 column denotes added in V4.

### Modules

| V3                      | V4                         |
| ----------------------- | -------------------------- |
| G2Config&period;py      | szconfig&period;py         |
| G2ConfigMgr&period;py   | szconfigmanager&period;py  |
| G2Diagnostic&period;py  | szdiagnostic&period;py     |
| G2Engine&period;py      | szengine&period;py         |
| G2EngineFlags&period;py | szengineflags&period;py \* |
| G2Exception&period;py   | szerror&period;py \*       |
| G2Product&period;py     | szproduct&period;py        |

\* These modules are abstract base classes located in sdk/python/senzing/

### Method Names

#### G2Config&period;py -> szconfig

| V3               | V4                       |
| ---------------- | ------------------------ |
| addDataSource    | register_data_source     |
| deleteDataSource | unregister_data_source   |
| listDataSources  | get_data_source_registry |

#### G2ConfigMgr&period;py -> szconfigmanager

| V3                     | V4                           |
| ---------------------- | ---------------------------- |
| getConfig              | create_config_from_config_id |
|                        | create_config_from_string    |
|                        | create_config_from_template  |
| getConfigList          | get_config_registry          |
| getDefaultConfigID     | get_default_config_id        |
|                        | register_config              |
| replaceDefaultConfigID | replace_default_config_id    |
|                        | set_default_config           |
| setDefaultConfigID     | set_default_config_id        |

#### G2Diagnostic&period;py -> szdiagnostic

| V3          | V4                           |
| ----------- | ---------------------------- |
| checkDBPerf | check_repository_performance |
| getDBInfo   | get_repository_info          |
|             | purge_repository             |

#### G2Engine&period;py -> szengine

| V3                                | V4                                     |
| --------------------------------- | -------------------------------------- |
| addRecord                         | add_record                             |
| closeExport                       | close_export_report                    |
| countRedoRecords                  | count_redo_records                     |
| deleteRecord                      | delete_record                          |
| exportCSVEntityReport             | export_csv_entity_report               |
| exportJSONEntityReport            | export_json_entity_report              |
| fetchNext                         | fetch_next                             |
| findInterestingEntitiesByEntityID | find_interesting_entities_by_entity_id |
| findInterestingEntitiesByRecordID | find_interesting_entities_by_record_id |
| findNetworkByEntityID             | find_network_by_entity_id              |
| findNetworkByRecordID             | find_network_by_record_id              |
| findPathByEntityID                | find_path_by_entity_id                 |
| findPathByRecordID                | find_path_by_record_id                 |
| getActiveConfigID                 | get_active_config_id                   |
| getEntityByEntityID               | get_entity_by_entity_id                |
| getEntityByRecordID               | get_entity_by_record_id                |
| getRecord                         | get_record                             |
| getRedoRecord                     | get_redo_record                        |
| getVirtualEntityByRecordID        | get_virtual_entity_by_record_id        |
| howEntityByEntityID               | how_entity_by_entity_id                |
| primeEngine                       | prime_engine                           |
|                                   | get_record_preview                     |
| processRedoRecord                 | process_redo_record                    |
| reevaluateEntity                  | reevaluate_entity                      |
| reevaluateRecord                  | reevaluate_record                      |
| searchByAttributes                | search_by_attributes                   |
| stats                             | get_stats                              |
| whyEntities                       | why_entities                           |
| whyRecords                        | why_records                            |
|                                   | why_record_in_entity                   |

#### G2Product&period;py -> szproduct

| V3      | V4          |
| ------- | ----------- |
| license | get_license |
| version | get_version |

### Exceptions

| V3                                | V4                            |
| --------------------------------- | ----------------------------- |
| G2BadInputException               | SzBadInputError               |
| G2ConfigurationException          | SzConfigurationError          |
| G2DatabaseConnectionLostException | SzDatabaseConnectionLostError |
| G2DatabaseException               | SzDatabaseError               |
|                                   | SzDatabaseTransientError      |
| G2Exception                       | SzError                       |
|                                   | SzGeneralError                |
| G2LicenseException                | SzLicenseError                |
| G2NotInitializedException         | SzNotInitializedError         |
| G2NotFoundException               | SzNotFoundError               |
|                                   | SzReplaceConflictError        |
| G2RetryableException              | SzRetryableError              |
|                                   | SzSdkError                    |
| G2RetryTimeoutExceededException   | SzRetryTimeoutExceededError   |
| G2UnhandledException              | SzUnhandledError              |
| G2UnknownDatasourceException      | SzUnknownDataSourceError      |
| G2UnrecoverableException          | SzUnrecoverableError          |

[breaking-changes]: https://www.senzing.com/docs/release/4/4_0_breaking_changes/
