import unittest

from extended_csv import read_xsv_file
from dirs import ROOT_DIR

TestCase = unittest.TestCase


class MyTestCase(TestCase):

    def test_read_xsv_line_spec(self):
        test_cases = [
            ('nutrient-100.csv', None, 80, 20),
            # TODO: maybe automatically test time elapsed as well
            ('branded_food-10000.csv', 10, 10, None),
            ('sr_legacy_food-150.csv', 200, 130, 20),
            ('food_category-28.csv', 1, 1, 0),
        ]
        for file, to_read, read, skip in test_cases:
            with self.subTest(f"{file=},{to_read=},{read=},{skip=}"):
                result = read_xsv_file(ROOT_DIR / f'tests/data/csv/{file}', dialect='excel', load_at_most=to_read, discard=skip)
                self.assertEqual(read, len(result))


if __name__ == '__main__':
    unittest.main()
