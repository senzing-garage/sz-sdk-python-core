senzing_core
============

The `senzing-core`_ Python package has 4 major modules / classes.
Senzing objects are created using an `Abstract Factory Pattern`_.

.. list-table:: Senzing classes
   :widths: 20 20 60
   :header-rows: 1

   * - Module
     - Class
     - Creation
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

The recommendation is to use implementation classes (e.g. `senzing-core`_) to construct
Senzing objects and use classes from the `senzing`_ Abstract Base Classes (`abc`_)
to define method and function parameter types.
This allows the implementation to change without the need to change method or function signatures.
The following is an example that shows an `SzAbstractFactoryCore` being created
and used to create other Senzing objects using `senzing`_ Abstract Base Classes as interface definitions.

.. literalinclude:: ../../examples/docs/creating_senzing_objects.py
      :linenos:
      :language: python

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

.. _abc: https://docs.python.org/library/abc.html
.. _Abstract Factory Pattern: https://en.wikipedia.org/wiki/Abstract_factory_pattern
.. _docs.senzing.com: https://www.senzing.com/docs
.. _GitHub: https://github.com/senzing-garage/sz-sdk-python-core/tree/main/examples
.. _gRPC: https://grpc.io
.. _Pypi: https://pypi.org/project/senzing/
.. _senzing-core: https://github.com/senzing-garage/sz-sdk-python-core
.. _senzing-grpc: https://garage.senzing.com/sz-sdk-python-grpc
.. _senzing: https://garage.senzing.com/sz-sdk-python