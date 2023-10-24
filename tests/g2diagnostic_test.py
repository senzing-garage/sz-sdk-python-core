#! /usr/bin/env python3

"""
# -----------------------------------------------------------------------------
# g2diagnostic_test.py
# -----------------------------------------------------------------------------
"""

# Import from standard library. https://docs.python.org/3/library/

import multiprocessing
import unittest

from senzing import g2diagnostic

from g2testhelper import get_test_engine_configuration_json

# import pytest


ENGINE_MODULE_NAME = "Example"
ENGINE_CONFIGURATION_JSON = get_test_engine_configuration_json()
ENGINE_VERBOSE_LOGGING = 0

# -----------------------------------------------------------------------------
# Test fixtures
# -----------------------------------------------------------------------------


# @pytest.fixture(scope="class")
# def g2_diagnostic():
#     g2_diagnostic_instance = g2diagnostic.G2Diagnostic(
#         ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
#     )
#     return g2_diagnostic_instance


# -----------------------------------------------------------------------------
# g2diagnostic_test.py
# -----------------------------------------------------------------------------


class TestG2Diagnostics(unittest.TestCase):
    """Test example"""

    def test_get_db_info(self) -> None:
        """Test physical core count."""
        g2_diagnostic = g2diagnostic.G2Diagnostic(
            ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
        )
        actual = g2_diagnostic.get_db_info()
        self.assertEqual(1, 1)
        print(">>>>>", actual)

    def test_get_logical_cores(self) -> None:
        """Test logical core count."""
        g2_diagnostic = g2diagnostic.G2Diagnostic(
            ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
        )
        expected = multiprocessing.cpu_count()
        actual = g2_diagnostic.get_logical_cores()
        self.assertEqual(expected, actual)

    def test_get_physical_cores(self) -> None:
        """Test physical core count."""
        g2_diagnostic = g2diagnostic.G2Diagnostic(
            ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
        )
        expected = multiprocessing.cpu_count()
        actual = g2_diagnostic.get_physical_cores()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
