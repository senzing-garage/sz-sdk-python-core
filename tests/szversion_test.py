import pytest

from senzing import szerror, szversion

# -----------------------------------------------------------------------------
# g2version testcases
# -----------------------------------------------------------------------------


def test_normalize_semantic_version():
    """Test whether semantic version strings are transformed to integer correctly."""
    tests = {
        "0.0.0": 0,
        "1.2.3": 10203,
        "11.1.13": 110113,
        "11.12.13": 111213,
        "99.99.99": 999999,
    }
    for sem_ver, number in tests.items():
        actual = szversion.normalize_semantic_version(sem_ver)
        assert actual == number


def test_supports_senzingapi_version():
    """Test whether current versions are within min/max range."""
    tests = [
        ["0.0.0", "99.99.99", "50.50.50"],
        ["10.0.0", "11.0.0", "10.1.1"],
        ["10.10.10", "10.10.12", "10.10.11"],
    ]
    for test in tests:
        actual = szversion.supports_senzingapi_version(test[0], test[1], test[2])
        assert actual


def test_supports_senzingapi_version_exceptions():
    """Test whether exceptions are thrown when current version is outside min/max range."""

    tests = [
        ["10.10.10", "10.10.12", "10.10.9"],
        ["10.10.10", "10.10.12", "10.10.13"],
    ]

    for test in tests:
        with pytest.raises(szerror.SzError):
            szversion.supports_senzingapi_version(test[0], test[1], test[2])
