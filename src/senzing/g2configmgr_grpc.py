#! /usr/bin/env python3

"""
TODO: g2configmgr_grpc.py
"""

# Import from standard library. https://docs.python.org/3/library/

from typing import Any, Dict, Union

# from .g2exception import translate_exception
from .g2configmgr_abstract import G2ConfigMgrAbstract
from .g2helpers import as_str

# from ctypes import *
# import functools
# import json
# import os
# import threading
# import warnings

# Import from https://pypi.org/

# Import from Senzing.


# Metadata

__all__ = ["G2ConfigMgrGrpc"]
__version__ = "0.0.1"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = "2023-10-30"
__updated__ = "2023-10-30"

SENZING_PRODUCT_ID = "5051"  # See https://github.com/Senzing/knowledge-base/blob/main/lists/senzing-component-ids.md

# -----------------------------------------------------------------------------
# G2ConfigMgrGrpc class
# -----------------------------------------------------------------------------


class G2ConfigMgrGrpc(G2ConfigMgrAbstract):
    """
    G2 config-manager module access library
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

    # -------------------------------------------------------------------------
    # Development methods - to be removed after initial development
    # -------------------------------------------------------------------------

    def fake_g2configmgr(self, *args: Any, **kwargs: Any) -> None:
        """TODO: Remove once SDK methods have been implemented."""
        if len(args) + len(kwargs) > 2000:
            print(self.noop)

    # -------------------------------------------------------------------------
    # G2ConfigMgr methods
    # -------------------------------------------------------------------------

    def add_config(
        self,
        config_str: Union[str, Dict[Any, Any]],
        config_comments: str,
        *args: Any,
        **kwargs: Any,
    ) -> int:
        self.fake_g2configmgr(config_str, config_comments)
        return 0

    def destroy(self, *args: Any, **kwargs: Any) -> None:
        self.fake_g2configmgr()

    def get_config(self, config_id: int, *args: Any, **kwargs: Any) -> str:
        self.fake_g2configmgr(config_id)
        return "string"

    def get_config_list(self, *args: Any, **kwargs: Any) -> str:
        self.fake_g2configmgr()
        return "string"

    def get_default_config_id(self, *args: Any, **kwargs: Any) -> int:
        self.fake_g2configmgr()
        return 0

    def init(
        self,
        module_name: str,
        ini_params: Union[str, Dict[Any, Any]],
        verbose_logging: int = 0,
        **kwargs: Any,
    ) -> None:
        self.fake_g2configmgr(module_name, ini_params, verbose_logging)

    def replace_default_config_id(
        self, old_config_id: int, new_config_id: int, *args: Any, **kwargs: Any
    ) -> None:
        self.fake_g2configmgr(old_config_id, new_config_id)

    def set_default_config_id(self, config_id: int, *args: Any, **kwargs: Any) -> None:
        self.fake_g2configmgr(config_id)
