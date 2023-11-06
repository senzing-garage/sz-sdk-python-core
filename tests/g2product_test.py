import json

import pytest
from pytest_schema import Regex, schema

from senzing import g2product

# -----------------------------------------------------------------------------
# G2Product fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="g2product_instance")
def g2product_instance_fixture(engine_vars):
    """
    Single engine object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = g2product.G2Product(
        engine_vars["MODULE_NAME"],
        engine_vars["INI_PARAMS"],
    )
    return result


# -----------------------------------------------------------------------------
# G2Product schemas
# -----------------------------------------------------------------------------

license_schema = {
    "customer": str,
    "contract": str,
    "issueDate": Regex(r"^\d{4}-\d{2}-\d{2}$"),
    "licenseType": str,
    "licenseLevel": str,
    "billing": str,
    "expireDate": Regex(r"^\d{4}-\d{2}-\d{2}$"),
    "recordLimit": int,
}


version_schema = {
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


# -----------------------------------------------------------------------------
# G2Product testcases
# -----------------------------------------------------------------------------


def test_exception(g2product_instance):
    """Test exceptions."""
    actual = g2product_instance.new_exception(0)
    assert isinstance(actual, Exception)


def test_init_and_destroy(g2product_instance):
    """Test Senzing license."""
    g2product_instance.init("Example", "{}", 0)
    g2product_instance.destroy()


def test_license(g2product_instance):
    """Test Senzing license."""
    actual = g2product_instance.license()
    assert isinstance(actual, str)
    actual_json = json.loads(actual)
    assert schema(license_schema) == actual_json


def test_version(g2product_instance):
    """Test Senzing version."""
    actual = g2product_instance.version()
    assert isinstance(actual, str)
    actual_json = json.loads(actual)
    assert schema(version_schema) == actual_json
