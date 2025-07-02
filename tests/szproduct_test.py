#! /usr/bin/env python3

import json
from typing import Any, Dict

import pytest
from pytest_schema import Regex, schema
from senzing import SzProduct

from senzing_core import SzProductCore

# -----------------------------------------------------------------------------
# Test cases
# -----------------------------------------------------------------------------


def test_get_license(sz_product: SzProduct) -> None:
    """Test SzProduct.get_license()."""
    actual = sz_product.get_license()
    assert isinstance(actual, str)
    actual_as_dict = json.loads(actual)
    assert schema(get_license_schema) == actual_as_dict


def test_get_version(sz_product: SzProduct) -> None:
    """Test SzProduct.get_version()."""
    actual = sz_product.get_version()
    assert isinstance(actual, str)
    actual_as_dict = json.loads(actual)
    assert schema(get_version_schema) == actual_as_dict


def test_help_1(sz_product: SzProduct) -> None:
    """Test SzProduct.help()."""
    sz_product.help()


def test_help_2(sz_product: SzProduct) -> None:
    """Test SzProduct.help(...)."""
    sz_product.help("get_license")


# -----------------------------------------------------------------------------
# Unique testcases
# -----------------------------------------------------------------------------


def test_constructor(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzProductCore()
    actual.initialize(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    assert isinstance(actual, SzProduct)


# NOTE szproduct can be initialized without an instance name
# def test_constructor_bad_instance_name(engine_vars: Dict[Any, Any]) -> None:
#     """Test constructor."""
#     bad_instance_name = ""
#     with pytest.raises(SzError):
#         actual = SzProductTest(
#             bad_instance_name,
#             engine_vars["SETTINGS"],
#         )
#         assert isinstance(actual, SzProductAbstract)

# NOTE szproduct can be initialized without settings
# def test_constructor_bad_settings(engine_vars: Dict[Any, Any]) -> None:
#     """Test constructor."""
#     bad_settings = ""
#     with pytest.raises(SzError):
#         actual = SzProductTest(
#             engine_vars["INSTANCE_NAME"],
#             bad_settings,
#         )
#         assert isinstance(actual, SzProductAbstract)


def test_constructor_dict(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzProductCore()
    actual.initialize(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    assert isinstance(actual, SzProduct)


def test_destroy(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzProductCore()
    actual.initialize(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    actual._destroy()  # pylint: disable=W0212


def test_exception(sz_product: SzProductCore) -> None:
    """Test exceptions."""
    with pytest.raises(Exception):
        sz_product._check_result(-1)  # pylint: disable=W0212


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_product", scope="function")
def szproduct_fixture(engine_vars: Dict[Any, Any]) -> SzProduct:
    """
    SzProduct object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = SzProductCore()
    result.initialize(  # pylint: disable=W0212
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    return result


# -----------------------------------------------------------------------------
# Schemas
# -----------------------------------------------------------------------------

get_license_schema = {
    "customer": str,
    "contract": str,
    "issueDate": Regex(r"^\d{4}-\d{2}-\d{2}$"),
    "licenseType": str,
    "licenseLevel": str,
    "billing": str,
    "expireDate": Regex(r"^\d{4}-\d{2}-\d{2}$"),
    "recordLimit": int,
}


get_version_schema = {
    "PRODUCT_NAME": str,
    "VERSION": Regex(r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$"),
    "BUILD_VERSION": str,
    "BUILD_DATE": Regex(r"^\d{4}-\d{2}-\d{2}$"),
    "BUILD_NUMBER": str,
    "COMPATIBILITY_VERSION": {
        "CONFIG_VERSION": str,
    },
    "SCHEMA_VERSION": {
        "ENGINE_SCHEMA_VERSION": str,
        "MINIMUM_REQUIRED_SCHEMA_VERSION": str,
        "MAXIMUM_REQUIRED_SCHEMA_VERSION": str,
    },
}
