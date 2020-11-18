import unittest
from doctest import DocTestSuite

from utils import date_utils, dict_utils, str_utils


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, ignore) -> unittest.TestSuite:
    tests.addTests(map(DocTestSuite, (date_utils, dict_utils, str_utils)))
    return tests


if __name__ == '__main__':
    unittest.main()
