import urllib.request
# https://stackoverflow.com/questions/30755625/urlerror-with-sparqlwrapper-at-sparql-query-convert
# #if the arg is empty in ProxyHandler, urllib will find itself your proxy config.
# proxy_support = urllib.request.ProxyHandler({})
# opener = urllib.request.build_opener(proxy_support)
# urllib.request.install_opener(opener)
from typing import List

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

from wikidata_queries.contracts import ContentRatingContract, FilmContract
from wikidata_queries.queries import CR_QUERY_TEMPLATE, SINGLE_PROP_FILM_QUERY_TEMPLATE


class WikiDataQueryBuilder:
    def __init__(self):
        self.sparql_builder = SPARQLWrapper("https://query.wikidata.org/sparql",
                                            agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")

    def raw_query(self, fields: List[str], raw: str):
        self.sparql_builder.setQuery(raw)
        self.sparql_builder.setReturnFormat(JSON)
        results = self.sparql_builder.query().convert()
        results_df = pd.json_normalize(results['results']['bindings'])
        results_df = results_df[[f'{field}.value' for field in fields]]
        return results_df

    def query(self, fields: List[str], where: str, limit: int = None) -> pd.DataFrame:
        # From https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Cats
        fields_p = " ".join([f'?{field}' for field in fields])
        query = f"""
           SELECT {fields_p}
           WHERE
           {{
             {where}
           }}
           """
        self.sparql_builder.setQuery(query)
        if limit:
            query += f"""
            LIMIT {limit}
            """
        self.sparql_builder.setReturnFormat(JSON)
        results = self.sparql_builder.query().convert()

        results_df = pd.json_normalize(results['results']['bindings'])
        results_df[[f'{field}.value' for field in fields]].head()
        return results_df


builder = WikiDataQueryBuilder()


def get_content_ratings_for_film(wikidata_id: str) -> List[ContentRatingContract]:
    query = CR_QUERY_TEMPLATE
    df = builder.raw_query(['crpLabel', 'countryLabel', 'contentRatingLabel'], query.format(film=wikidata_id))
    ratings: List[ContentRatingContract] = []
    for index, row in df.iterrows():
        label = row['crpLabel.value']
        country = row['countryLabel.value']
        rating_category = row['contentRatingLabel.value']
        ratings.append(ContentRatingContract(label=label, appliesInCountry=country, value=rating_category))
    return ratings


def get_single_valued_prop(wikidata_id: str) -> FilmContract:
    query = SINGLE_PROP_FILM_QUERY_TEMPLATE
    df = builder.raw_query(['originatingCountryLabel', 'originalLangLabel', 'publicationDateLabel'], query.format(film=wikidata_id))
    for index, row in df.iterrows():
        country = row['originatingCountryLabel.value']
        lang = row['originalLangLabel.value']
        pub_date = row['publicationDateLabel.value']
        return FilmContract(hasCountryOfOrigin=country, hasOriginalLanguage=lang, hasPublicationDate=pub_date)


def main():
   # print(get_content_ratings_for_film('Q61448040'))
    print(get_single_valued_prop('Q61448040'))


if __name__ == '__main__':
    main()
