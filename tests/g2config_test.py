#! /usr/bin/env python3

"""
# -----------------------------------------------------------------------------
# g2config_test.py
# -----------------------------------------------------------------------------
"""

# Import from standard library. https://docs.python.org/3/library/

import unittest


class TestSum(unittest.TestCase):
    """Test example"""

    def test_list_int(self):
        """A Simple example of 6=6"""
        result = 6
        self.assertEqual(result, 6)


if __name__ == '__main__':
    unittest.main()
