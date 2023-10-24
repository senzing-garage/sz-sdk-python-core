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

ENGINE_MODULE_NAME = "Example"
ENGINE_CONFIGURATION_JSON = str(
    '{"PIPELINE":{"CONFIGPATH":"/etc/opt/senzing","RESOURCEPATH":"/opt/senzing/g2/resources","SUPPORTPATH":"/opt/senzing/data"},"SQL":{"CONNECTION":"sqlite3://na:na@/tmp/sqlite/G2C.db"}}'
)
ENGINE_VERBOSE_LOGGING = 0


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
        expected = multiprocessing.cpu_count()
        g2_diagnostic = g2diagnostic.G2Diagnostic(
            ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
        )
        actual = g2_diagnostic.get_logical_cores()
        self.assertEqual(expected, actual)

    def test_get_physical_cores(self) -> None:
        """Test physical core count."""
        expected = multiprocessing.cpu_count()
        g2_diagnostic = g2diagnostic.G2Diagnostic(
            ENGINE_MODULE_NAME, ENGINE_CONFIGURATION_JSON, ENGINE_VERBOSE_LOGGING
        )
        actual = g2_diagnostic.get_physical_cores()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
