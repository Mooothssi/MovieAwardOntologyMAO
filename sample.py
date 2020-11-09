from pathlib import Path

from owlready2 import *

from db.connection import connect_database
from mapper.aggregators.film import FilmAggregator
from models.imdb.name_basics import NameBasics
from models.imdb.title_akas import TitleAkas
from models.imdb.title_principals import TitlePrincipal
from owl_models.base import apply_classes_from
from settings import OUT_FILENAME, OUT_PATH, OWL_FILEPATH

# TitleAkas.load_from_tsv("database/src/imdb-tsvs/new.tsv")
# print(TitleAkas.dump_to_sql('out/any.sql'))
# TitlePrincipal.load_from_tsv("database/src/imdb-tsvs/new.prin.tsv")
# print(TitlePrincipal.dump_to_sql('out/any2.sql'))
NameBasics.load_from_tsv("database/src/imdb-tsvs/name.stripped.basics.tsv")
print(NameBasics.dump_to_sql('out/any3.sql'))

sess = connect_database()

onto = get_ontology(f"file:////{OWL_FILEPATH}")
onto.load()

apply_classes_from(onto)
#print(film)
#print([x.hasTitle for x in film.instances])

a = FilmAggregator(session=sess)
a.create_instances()

# print([x for x in onto.individuals()])
# print([x for x in onto.classes()])
onto.save(file=str(Path(OUT_PATH) / OUT_FILENAME), format="rdfxml")
