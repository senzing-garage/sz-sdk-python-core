#! /usr/bin/env python3

"""
TODO: g2diagnostic_grpc.py
"""

# Import from standard library. https://docs.python.org/3/library/

import os
from typing import Any, Dict, Union

from .g2diagnostic_abstract import G2DiagnosticAbstract
from .g2helpers import as_str

# Import from https://pypi.org/

# Import from Senzing.


# Metadata

__all__ = ["G2DiagnosticGrpc"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5052"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md


# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------


def find_file_in_path(filename: str) -> str:
    """Find a file in the PATH environment variable"""
    path_dirs = os.environ["PATH"].split(os.pathsep)
    for path_dir in path_dirs:
        file_path = os.path.join(path_dir, filename)
        if os.path.exists(file_path):
            return file_path
    return ""


# -----------------------------------------------------------------------------
# G2DiagnosticGrpc class
# -----------------------------------------------------------------------------


class G2DiagnosticGrpc(G2DiagnosticAbstract):
    """
    G2 config module access library
    """

    # -------------------------------------------------------------------------
    # Python dunder/magic methods
    # -------------------------------------------------------------------------

    def __init__(
        self,
        module_name: str = "",
        ini_params: Union[str, Dict[Any, Any]] = "",
        init_config_id: int = 0,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        For return value of -> None, see https://peps.python.org/pep-0484/#the-meaning-of-annotations
        """
        # pylint: disable=W0613

        self.ini_params = as_str(ini_params)
        self.init_config_id = init_config_id
        self.module_name = module_name
        self.noop = ""
        self.verbose_logging = verbose_logging

    def __del__(self) -> None:
        """Destructor"""
        self.destroy()

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2diagnostic(self, *args: Any, **kwargs: Any) -> None:
        """
        TODO: Remove once SDK methods have been implemented.

        :meta private:
        """
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # G2Diagnostic methods
    # -------------------------------------------------------------------------

    def check_db_perf(self, seconds_to_run: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2diagnostic(seconds_to_run)
        return "string"

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2diagnostic()

    def get_available_memory(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2diagnostic()
        return 0

    def get_db_info(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2diagnostic()
        return "string"

    def get_logical_cores(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2diagnostic()
        return 0

    def get_physical_cores(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2diagnostic()
        return 0

    def get_total_system_memory(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2diagnostic()
        return 0

    def init(
        self,
        module_name: str,
        ini_params: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        self.fake_g2diagnostic(module_name, ini_params, verbose_logging)

    def init_with_config_id(
        self,
        module_name: str,
        ini_params: Union[str, Dict[Any, Any]],
        init_config_id: int,
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        self.fake_g2diagnostic(module_name, ini_params, init_config_id, verbose_logging)

    def reinit(self, init_config_id: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2diagnostic(init_config_id)
