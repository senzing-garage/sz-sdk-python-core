.. sz-sdk-python-core documentation master file, created by
   sphinx-quickstart on Thu Oct 19 16:35:58 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`senzing_core` Python package documentation
===========================================

The `senzing-core`_ Python package is an implementation of the
`senzing`_ interface definition that communicates with the Senzing binaries.
If an implementation is needed to communicate over `gRPC`_,
use the `senzing-grpc`_ Python package.

Often, the `senzing-core`_ Python package is used in conjunction with the `senzing`_ Python package.
The `senzing`_ Python package has Abstract Base Classes (`abc`_) which define the interfaces used
by implementation classes like `senzing-core`_.
The `senzing`_ Python package also has constants and errors used by implementation classes.

The recommendation is to use implementation classes, like `senzing-core`_, to construct
Senzing objects and use classes from `senzing`_ to define method and function parameter types.
This allows the implementation to change without the need to change method or function signatures.
The following is an example that shows an `SzAbstractFactoryCore` being created and being passed to
functions using the classes from the `senzing`_ Python package.

.. literalinclude:: ../../examples/docs/using_abstract_factory_implementations.py
      :linenos:
      :language: python

Senzing has additional Software Development Kits (SDKs)
for Java, Go, and C#.
Information for these SDKs can be found at `docs.senzing.com`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   senzing_core

References
==========

#. :ref:`genindex`
#. :ref:`modindex`
#. :ref:`search`
#. `GitHub`_
#. `Pypi`_
#. `senzing-core`_
#. `senzing`_

.. _abc: https://docs.python.org/library/abc.html
.. _docs.senzing.com: https://www.senzing.com/docs
.. _GitHub: https://github.com/senzing-garage/sz-sdk-python/tree/main/examples
.. _gRPC: https://grpc.io
.. _Pypi: https://pypi.org/project/senzing/
.. _senzing-core: https://github.com/senzing-garage/sz-sdk-python-core
.. _senzing-grpc: https://garage.senzing.com/sz-sdk-python-grpc
.. _senzing: https://garage.senzing.com/sz-sdk-python