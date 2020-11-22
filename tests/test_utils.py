import unittest
from doctest import DocTestSuite

from utils import date, dict, str


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, ignore) -> unittest.TestSuite:
    tests.addTests(map(DocTestSuite, (date, dict, str)))
    return tests


if __name__ == '__main__':
    unittest.main()
