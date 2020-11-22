import unittest
from doctest import DocTestSuite

from sa_autowrite import parsers
from sa_autowrite.parsers import parse_line_re


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, ignore) -> unittest.TestSuite:
    tests.addTests(map(DocTestSuite, (parsers,)))
    return tests


class TestParsers(unittest.TestCase):

    def test_parse_line_re(self):
        test_cases = [
            (
                '"!Next?" (1994)\t\t\t\t\t\tItaly\n', {
                    'title': '!Next?',
                    'year': 1994,
                    'roman': None,
                    'type': None,
                    'episode_info': None,
                    'data': 'Italy',
                }
            ),
            (
                '"#15SecondScare" (2015)\t\t\t\t\tUSA\n', {
                    'title': '#15SecondScare',
                    'year': 2015,
                    'roman': None,
                    'type': None,
                    'episode_info': None,
                    'data': 'USA',
                }
            ),
            (
                '"#15SecondScare" (2015) {Because We Don\'t Want You to Fall Asleep (#1.3)}\tUSA\n', {
                    'title': '#15SecondScare',
                    'year': 2015,
                    'roman': None,
                    'type': None,
                    'episode_info': "Because We Don't Want You to Fall Asleep (#1.3)",
                    'data': 'USA',
                }
            ),
            (
                '"#1 Single" (2006) {Wingman (#1.6)}\t\t\tStick Figure Productions [us]\n', {
                    'title': '#1 Single',
                    'year': 2006,
                    'roman': None,
                    'type': None,
                    'episode_info': "Wingman (#1.6)",
                    'data': 'Stick Figure Productions [us]',
                },
            ),
            (
                '"#LoveMonkeyChocolateFlowers" (2014)\t\t\tUK:PG\n', {
                    'title': '#LoveMonkeyChocolateFlowers',
                    'year': 2014,
                    'roman': None,
                    'type': None,
                    'episode_info': None,
                    'data': 'UK:PG',
                },
            ),
        ]
        for string, expected in test_cases:
            with self.subTest(f"{string=},{expected=}"):
                result = parse_line_re(string)
                self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
