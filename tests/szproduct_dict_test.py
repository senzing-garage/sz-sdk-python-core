from typing import Any, Dict

import pytest
from pytest_schema import Regex, schema
from senzing_dict import SzProduct

from senzing import SzProduct as SzProductCore

# -----------------------------------------------------------------------------
# SzProduct testcases
# -----------------------------------------------------------------------------


def test_constructor(engine_vars: Dict[Any, Any]) -> None:
    """Test constructor."""
    sz_product = SzProductCore(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )
    actual = SzProduct(sz_product)
    assert isinstance(actual, SzProduct)


def test_get_license(sz_product: SzProduct) -> None:
    """Test Senzing license."""
    actual = sz_product.get_license()
    assert schema(get_license_schema) == actual


def test_get_version(sz_product: SzProduct) -> None:
    """Test Senzing version."""
    actual = sz_product.get_version()
    assert schema(get_version_schema) == actual


def test_context_managment(engine_vars: Dict[Any, Any]) -> None:
    """Test the use of SzProduct in context."""
    with SzProductCore(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    ) as sz_product_core:
        with SzProduct(sz_product_core) as sz_product:
            actual = sz_product.get_license()
            assert schema(get_license_schema) == actual


# -----------------------------------------------------------------------------
# SzProduct fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_product", scope="module")
def szproduct_fixture(engine_vars: Dict[Any, Any]) -> SzProduct:
    """
    Single szproduct object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    sz_product = SzProductCore(
        engine_vars["INSTANCE_NAME"],
        engine_vars["SETTINGS"],
    )

    result = SzProduct(sz_product)
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
