import unittest
import pandas as pd


TestCase = unittest.TestCase


class TestAutowrite(TestCase):

    def test_something(self):
        with open('data/autowrite/nutrient.py', 'r', encoding='utf-8') as f:
            expected_result = f.read()
        options = {
            'lines_to_consider': 100,
            'primary_key_columns': None,
        }
        self.assertEqual(expected_result, somefunction('data/csv/nutrient-100.csv', **options))

    def test_report(self):
        with open('data/autowrite/nutrient.py', 'r', encoding='utf-8') as f:
            expected_result = f.read()
        options = {
            'discard': 0,
            'max_lines': 100,
        }
        self.assertEqual(expected_result, report('data/csv/nutrient-100.csv', **options))


if __name__ == '__main__':
    unittest.main()
