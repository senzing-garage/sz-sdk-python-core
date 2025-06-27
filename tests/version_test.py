import pytest
from senzing import SzSdkError

from senzing_core import _version

# -----------------------------------------------------------------------------
# _version testcases
# -----------------------------------------------------------------------------


def test_normalize_semantic_version() -> None:
    """Test whether semantic version strings are transformed to integer correctly."""
    tests = {
        "0.0.0": 0,
        "1.2.3": 10203,
        "11.1.13": 110113,
        "11.12.13": 111213,
        "99.99.99": 999999,
    }
    for sem_ver, number in tests.items():
        actual = _version.normalize_semantic_version(sem_ver)
        assert actual == number


def test_supports_senzingsdk_version() -> None:
    """Test whether current versions are within min/max range."""
    tests = [
        ["0.0.0", "99.99.99", "50.50.50"],
        ["10.0.0", "11.0.0", "10.1.1"],
        ["10.10.10", "10.10.12", "10.10.11"],
    ]
    for test in tests:
        actual = _version.supports_senzingsdk_version(test[0], test[1], test[2])
        assert actual


def test_supports_senzingsdk_version_exceptions() -> None:
    """Test whether exceptions are thrown when current version is outside min/max range."""
    tests = [
        ["10.10.10", "10.10.12", "10.10.9"],
        ["10.10.10", "10.10.12", "10.10.13"],
    ]

    for test in tests:
        with pytest.raises(SzSdkError):
            _version.supports_senzingsdk_version(test[0], test[1], test[2])


def test_is_supported_python_version() -> None:
    """Test whether runtime version is >= to minimum requirement."""

    actual = _version.is_supported_python_version()
    assert actual


def test_is_supported_python_version_provide_minimum() -> None:
    """Test whether runtime version is >= to minimum requirement."""
    tests = ("3.9", "3.8", "3.7", "3.6")

    for test in tests:
        actual = _version.is_supported_python_version(test)
        assert actual


def test_is_supported_python_version_exceptions() -> None:
    """Test whether runtime version is >= to minimum requirement."""
    tests = ("9.1", "9.2", "9.3", "9.4")

    for test in tests:
        with pytest.raises(SzSdkError):
            _version.is_supported_python_version(test)


def test_check_requirements() -> None:
    """Test Python and Senzing SDK binary versions are supported."""
    actual = _version.check_requirements()
    assert actual


def test_check_requirements_exceptions() -> None:
    """Test Python and Senzing SDK binary versions are supported.."""
    tests = ("9.1", "9.2", "9.3", "9.4")

    for test in tests:
        with pytest.raises(SzSdkError):
            _version.check_requirements(test)
