from pathlib import Path

from owlready2 import *

from db.connection import connect_database

from autogen_db_models.imdb.title_akas import TitleAkas

# TitleAkas.load_from_tsv("database/src/imdb-tsvs/new.tsv")
# print(TitleAkas.dump_to_sql('out/any.sql'))
# TitlePrincipal.load_from_tsv("database/src/imdb-tsvs/new.prin.tsv")
# print(TitlePrincipal.dump_to_sql('out/any2.sql'))
# NameBasics.load_from_tsv("database/src/imdb-tsvs/name.stripped.basics.tsv")
# print(NameBasics.dump_to_sql('out/any3.sql'))
# TitleCrew.load_from_tsv("database/src/imdb-tsvs/name.stripped.basics.tsv")
# print(TitleCrew.dump_to_sql('out/any4.sql'))

sess = connect_database()

print(sess.query(TitleAkas).limit(10).all())

