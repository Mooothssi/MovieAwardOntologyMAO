import unittest
from io import StringIO
from doctest import DocTestSuite

from yamd import markdown, main
from dirs import ROOT_DIR


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, ignore) -> unittest.TestSuite:
    tests.addTests(map(DocTestSuite, (markdown, main)))
    return tests


class TestOwlYamlMd(unittest.TestCase):
    def test_main_test_cases(self):
        version = 'v2.0.0'
        specs = [
            ('test_case1.yaml', 'test_case1.md'),
            ('test_case2.yaml', 'test_case2.md')
        ]
        for infile, outfile in specs:
            with open(ROOT_DIR / f'tests/specs/{version}/{outfile}') as mdfile:
                expected_result = mdfile.read()
            result = StringIO()
            main.convert_owl_yaml_to_md(ROOT_DIR / f'tests/specs/{version}/{infile}', result)
            self.assertEqual(expected_result, result.getvalue())


if __name__ == '__main__':
    unittest.main()
