import json

import pytest
from pytest_schema import Regex, schema

from senzing import szerror, szproduct

# -----------------------------------------------------------------------------
# G2Product fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(name="sz_product", scope="module")
def szproduct_fixture(engine_vars):
    """
    Single engine object to use for all tests.
    engine_vars is returned from conftest.py.
    """
    result = szproduct.SzProduct(
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


def test_exception(sz_product):
    """Test exceptions."""
    actual = sz_product.new_exception(0)
    assert isinstance(actual, Exception)


def test_constructor(engine_vars):
    """Test constructor."""
    actual = szproduct.SzProduct(
        engine_vars["MODULE_NAME"],
        engine_vars["INI_PARAMS"],
    )
    assert isinstance(actual, szproduct.SzProduct)


def test_constructor_bad_module_name(engine_vars):
    """Test constructor."""
    bad_module_name = ""
    with pytest.raises(szerror.SzError):
        actual = szproduct.SzProduct(
            bad_module_name,
            engine_vars["INI_PARAMS"],
        )
        assert isinstance(actual, szproduct.SzProduct)


def test_constructor_bad_ini_params(engine_vars):
    """Test constructor."""
    bad_ini_params = ""
    with pytest.raises(szerror.SzError):
        actual = szproduct.SzProduct(
            engine_vars["MODULE_NAME"],
            bad_ini_params,
        )
        assert isinstance(actual, szproduct.SzProduct)


def test_license(sz_product):
    """Test Senzing license."""
    actual = sz_product.license()
    assert isinstance(actual, str)
    actual_json = json.loads(actual)
    assert schema(license_schema) == actual_json


def test_version(sz_product):
    """Test Senzing version."""
    actual = sz_product.version()
    assert isinstance(actual, str)
    actual_json = json.loads(actual)
    assert schema(version_schema) == actual_json


def test_init_and_destroy(sz_product):
    """Test init/destroy cycle."""
    sz_product.init("Example", "{}", 0)
    sz_product.destroy()


def test_init_and_destroy_again(sz_product):
    """Test init/destroy cycle a second time."""
    sz_product.init("Example", "{}", 0)
    sz_product.destroy()
