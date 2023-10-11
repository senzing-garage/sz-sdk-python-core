#! /usr/bin/env python3

# -----------------------------------------------------------------------------
# g2config_test.py
# -----------------------------------------------------------------------------

# Import from standard library. https://docs.python.org/3/library/

import unittest


class TestSum(unittest.TestCase):
    def test_list_int(self):
        result = 1
        self.assertEqual(result, 6)

    def test_list_int2(self):
        result = 2
        self.assertEqual(result, 6)


    def test_list_int3(self):
        result = 6
        self.assertEqual(result, 6)

    def test_list_int4(self):
        result = 6
        self.assertEqual(result, 6)


if __name__ == '__main__':
    unittest.main()
