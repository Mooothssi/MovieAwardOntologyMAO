# Module: sa_autowrite

### Description

Features:
- Write SA models from data (CSV, TSV, ...)
- Show stats or data read to create models for human checking
- Insert data into database

### Getting Started

Sample script to create models

```python
from dirs import ROOT_DIR
from sa_autowrite.create import write_models

IMDB_FOLDER = ROOT_DIR / 'tests/data/large/imdb/'

write_models(IMDB_FOLDER, ROOT_DIR / f'autogen_db_models/imdb', max_lines=10000)
```

Sample script to insert data
```python
from dirs import ROOT_DIR
from engine import engine
from sa_autowrite.insert import insert_xsv_data

from autogen_db_models.imdb.base import Base
from autogen_db_models.imdb import NameBasics, TitleAkas, TitleAkas, TitleBasics, TitleBasics, TitleCrew, TitleEpisode, TitlePrincipals, TitleRatings

IMDB_FOLDER = ROOT_DIR / 'tests/data/large/imdb/'

for filename, clsname in [
    (IMDB_FOLDER / 'name.basics.tsv', NameBasics),
    # (IMDB_FOLDER / 'title.akas.tsv', TitleAkas),
    # (IMDB_FOLDER / 'title.basics.tsv', TitleBasics),
    # (IMDB_FOLDER / 'title.crew.tsv', TitleCrew),
    # (IMDB_FOLDER / 'title.episode.tsv', TitleEpisode),
    # (IMDB_FOLDER / 'title.principals.tsv', TitlePrincipals),
    # (IMDB_FOLDER / 'title.ratings.tsv', TitleRatings),
]:
    confirmation = input(f"Confirm table '{clsname.__name__}' deletion (y/N): ")
    if confirmation == 'y':
        clsname.__table__.drop(engine)
        Base.metadata.create_all(engine)
    elif confirmation == 'N':
        pass
    else:
        raise AssertionError("invalid input")

    insert_xsv_data(filename, clsname, chunksize=20_000, encoding='utf-8',
                    null_values=['\\N'], ignore_cols=['_id'],
                    skip_rows_data=0, read_lines_data=None,
                    verbose=1)
```
