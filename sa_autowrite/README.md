Sample script (put this in a file in root dir):

```python
from engine import engine
from sa_autowrite.main import insert_data, write_models

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
from sa_autowrite.main import insert_data, write_models

IMDB_FOLDER = ROOT_DIR / f'tests/data/large/imdb/'

write_models(IMDB_FOLDER, ROOT_DIR / f'autogen_db_models/imdb', max_lines=10000)


from autogen_db_models.imdb.base import Base

Base.metadata.create_all(engine)

insert_data(IMDB_FOLDER, ROOT_DIR / f'autogen_db_models/imdb')
```
