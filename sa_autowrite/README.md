Sample script (put this in a file in root dir):

```python
from engine import engine
from sa_autowrite.create import write_models
from sa_autowrite.insert import insert_data

# Write models from data in autogen_db_models/ directory
write_models('tests/data/csv/', 'autogen_db_models/', max_lines=1000)

from autogen_db_models.base import Base
Base.metadata.create_all(engine)

insert_data('tests/data/csv/', 'autogen_db_models/')
```

Sample script for large files e.g. IMDb (put those tsv files in /tests/data/large/imdb/)

```python
from dirs import ROOT_DIR
from engine import engine
# from sa_autowrite.create import write_models
from sa_autowrite.insert import insert_xsv_data

IMDB_FOLDER = ROOT_DIR / f'tests/data/large/imdb/'

# write_models(IMDB_FOLDER, ROOT_DIR / f'autogen_db_models/imdb', max_lines=10000)


from autogen_db_models.imdb.base import Base
from autogen_db_models.imdb import TitleCrew

Base.metadata.create_all(engine)
confirmation = input("Confirm table 'TitleCrew' deletion (y/N): ")
if confirmation == 'y':
    TitleCrew.__table__.drop(engine)
    Base.metadata.create_all(engine)
elif confirmation == 'N':
    pass
else:
    raise AssertionError("invalid input")


insert_xsv_data(IMDB_FOLDER / 'title.crew.tsv', TitleCrew, chunksize=30_000, encoding='utf-8', null_values=['\\N'], ignore_cols=['_id'], skip_rows_data=30_000, read_lines_data=30_000)
```
