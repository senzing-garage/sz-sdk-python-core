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


class TestG2Diagnostics(unittest.TestCase):
    """Test example"""

    def test_get_logical_cores(self):
        """Test logical core count."""
        expected = multiprocessing.cpu_count()
        g2_diagnostic = g2diagnostic.G2Diagnostic("A", "{}", 0)
        actual = g2_diagnostic.get_logical_cores()
        self.assertEqual(expected, actual)

    def test_get_physical_cores(self):
        """Test physical core count."""
        expected = multiprocessing.cpu_count()
        g2_diagnostic = g2diagnostic.G2Diagnostic("A", "{}", 0)
        actual = g2_diagnostic.get_physical_cores()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
