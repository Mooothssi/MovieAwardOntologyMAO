from owlready2 import *
from settings import OWL_FILEPATH, OUT_PATH, OUT_FILENAME
from pathlib import Path
from db.connection import connect_database
from models.imdb.title_akas import TitleAkas
from models.imdb.title_principals import TitlePrincipal
from owl_models.base import apply_classes_from
from mapper.aggregators.film import FilmAggregator

TitleAkas.load_from_tsv("database/src/imdb-tsvs/new.tsv")
print(TitleAkas.dump_to_sql('out/any.sql'))
TitlePrincipal.load_from_tsv("database/src/imdb-tsvs/new.prin.tsv")
print(TitlePrincipal.dump_to_sql('out/any2.sql'))

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
