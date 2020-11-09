from .base import Aggregator
from owl_models.film import Film, Person, FilmMakingSituation
from sqlalchemy.orm import Session
from ..models.film import FilmModel


class FilmAggregator(Aggregator):
    model = Film

    def __init__(self, session: Session):
        self.session = session

    def retrieve_instances_from(self, source) -> list[FilmModel]:
        return source.get_film_instances()

    def create_instances(self):
        for source in self.sources:
            s = source(self.session)
            raw_films = self.retrieve_instances_from(s)
            for f in raw_films:

                film = Film(f.instance_name)
                film.hasTitle = [f.title]
                makingOfFilm = FilmMakingSituation(f"{f.instance_name}Making")
                makingOfFilm.isSettingForFilm = [film]
                for actor in f.cast:
                    p = Person(actor.nconst)
                    p.actsIn = [makingOfFilm]

                print(f"Added Film#{f.instance_name} as an individual")
        pass
