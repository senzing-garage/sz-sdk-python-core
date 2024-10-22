import json
from typing import Any, Dict

import pytest
from pytest_schema import Regex, schema

from senzing import SzProduct

# -----------------------------------------------------------------------------
# SzProduct testcases
# -----------------------------------------------------------------------------


def test_exception(sz_product: SzProduct) -> None:
    """Test exceptions."""
    with pytest.raises(Exception):
        sz_product.check_result(-1)


def test_constructor(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    actual = SzProduct()
    actual._initialize(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    assert isinstance(actual, SzProduct)


# NOTE szproduct can be initialized without an instance name
# def test_constructor_bad_instance_name(engine_vars: Dict[Any, Any]) -> None:
#     """Test constructor."""
#     bad_instance_name = ""
#     with pytest.raises(SzError):
#         actual = SzProduct(
#             bad_instance_name,
#             engine_vars["SETTINGS"],
#         )
#         assert isinstance(actual, SzProduct)

# NOTE szproduct can be initialized without settings
# def test_constructor_bad_settings(engine_vars: Dict[Any, Any]) -> None:
#     """Test constructor."""
#     bad_settings = ""
#     with pytest.raises(SzError):
#         actual = SzProduct(
#             engine_vars["INSTANCE_NAME"],
#             bad_settings,
#         )
#         assert isinstance(actual, SzProduct)


def test_double_destroy(engine_vars: Dict[Any, Any]) -> None:
    """Test calling destroy twice."""
    actual = SzProduct()
    actual._initialize(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS_DICT"],
    )
    actual._destroy()  # pylint: disable=W0212
    actual._destroy()  # pylint: disable=W0212


def test_get_license(sz_product: SzProduct) -> None:
    """Test Senzing license."""
    actual = sz_product.get_license()
    assert isinstance(actual, str)
    actual_as_dict = json.loads(actual)
    assert schema(get_license_schema) == actual_as_dict


def test_get_version(sz_product: SzProduct) -> None:
    """Test Senzing version."""
    actual = sz_product.get_version()
    assert isinstance(actual, str)
    actual_as_dict = json.loads(actual)
    assert schema(get_version_schema) == actual_as_dict


# def test_initialize_and_destroy(sz_product: SzProduct) -> None:
#     """Test init/destroy cycle."""
#     instance_name = "Example"
#     settings: Dict[Any, Any] = {}
#     verbose_logging = SzEngineFlags.SZ_NO_LOGGING
#     sz_product.initialize(instance_name, settings, verbose_logging)
#     sz_product.destroy()


# def test_initialize_and_destroy_again(sz_product: SzProduct) -> None:
#     """Test init/destroy cycle a second time."""
#     instance_name = "Example"
#     settings = "{}"
#     verbose_logging = SzEngineFlags.SZ_NO_LOGGING
#     sz_product.initialize(instance_name, settings, verbose_logging)
#     sz_product.destroy()


# -----------------------------------------------------------------------------
# SzProduct fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_product", scope="function")
def szproduct_fixture(engine_vars: Dict[Any, Any]) -> SzProduct:
    """
    Single szproduct object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = SzProduct()
    result._initialize(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    return result


# -----------------------------------------------------------------------------
# SzProduct schemas
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
    "VERSION": Regex(
        r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$"
    ),
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
