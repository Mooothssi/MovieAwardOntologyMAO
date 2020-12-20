CR_QUERY_TEMPLATE = '''
SELECT ?crp ?crpLabel ?countryLabel ?contentRatingLabel {{
  wd:{film} wdt:P31 wd:Q11424.
  ?crp wdt:P31 wd:Q24716199;
       wdt:P17 ?country;
        wikibase:claim ?p;
         wikibase:statementProperty ?ps .
  wd:{film} ?p [?ps ?contentRating].
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
ORDER BY ?film ?cr
'''


SINGLE_PROP_FILM_QUERY_TEMPLATE = '''
SELECT ?originatingCountryLabel ?originalLangLabel ?publicationDateLabel {{
    wd:{film} wdt:P31 wd:Q11424;
    OPTIONAL {{ wd:{film}  wdt:P495 ?originatingCountry }}
    OPTIONAL {{ wd:{film}  wdt:P364 ?originalLang }}
    OPTIONAL {{ wd:{film}  wdt:P577 ?publicationDate }}
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
ORDER BY ?film ?cr ASC(?publicationDate)
LIMIT 1
'''

WIKIDATA_ID_FROM_IMDB_ID_QUERY = '''
SELECT ?film {{
    ?film wdt:P345 \"{imdb_id}\".
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
'''
