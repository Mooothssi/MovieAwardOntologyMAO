
from start_dj import start_django_lite

start_django_lite()

from mao_dj.app.models import Film
from add_individuals import add_imdb_info

if __name__ == '__main__':
    for f in Film.objects.all():
        print(f)
        f.sync_from_wikidata()
    add_imdb_info()
