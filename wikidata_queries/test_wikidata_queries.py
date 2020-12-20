import unittest

from wikidata_queries.base import get_from_imdb_id


class TestWikidataQueries(unittest.TestCase):

    def test_queries(self):
        self.assertEqual("Q83495", get_from_imdb_id("tt0133093"))
