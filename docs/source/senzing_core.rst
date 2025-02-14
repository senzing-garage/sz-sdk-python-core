senzing_core
============

The `senzing_core`_ Python package has 5 major modules / classes.
Senzing objects are created using an `Abstract Factory Pattern`_.

.. list-table:: Senzing classes
   :widths: 20 20 60
   :header-rows: 1

   * - Module
     - Class
     - Creation
   * - szconfig
     - SzConfigCore
     - `sz_config = sz_abstract_factory.create_config()`
   * - szconfigmanager
     - SzConfigManagerCore
     - `sz_configmanager = sz_abstract_factory.create_configmanager()`
   * - szdiagnostic
     - SzDiagnosticCore
     - `sz_diagnostic = sz_abstract_factory.create_diagnostic()`
   * - szengine
     - SzEngineCore
     - `sz_engine = sz_abstract_factory.create_engine()`
   * - szproduct
     - SzProductCore
     - `sz_product = sz_abstract_factory.create_product()`

For the full implementation of the documentation examples, visit the source code on
`GitHub`_.

szabstractfactory
-----------------

.. automodule:: senzing_core.szabstractfactory
   :members:
   :undoc-members:
   :show-inheritance:

szconfig
--------

.. automodule:: senzing_core.szconfig
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:

szconfigmanager
---------------

.. automodule:: senzing_core.szconfigmanager
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:

szdiagnostic
------------

.. automodule:: senzing_core.szdiagnostic
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:

szengine
--------

.. automodule:: senzing_core.szengine
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:

szproduct
---------

.. automodule:: senzing_core.szproduct
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:

.. _Abstract Factory Pattern: https://en.wikipedia.org/wiki/Abstract_factory_pattern
.. _GitHub: https://github.com/senzing-garage/sz-sdk-python-core/tree/main/examples
.. _senzing_core: https://github.com/senzing-garage/sz-sdk-python-core
.. _senzing-grpc: https://garage.senzing.com/sz-sdk-python-grpc