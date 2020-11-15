import unittest
from doctest import DocTestSuite

from utils import date_utils, dict_utils, str_utils


def load_tests(loader, tests, ignore):
    tests.addTests(map(DocTestSuite, (date_utils, dict_utils, str_utils)))
    return tests


if __name__ == '__main__':
    unittest.main()
