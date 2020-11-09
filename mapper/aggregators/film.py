from .base import Aggregator
from owl_models.film import Film, Person, FilmMakingSituation, ActingSituation, Crew, Cast, Character
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
                making_of_film = FilmMakingSituation(f"{f.instance_name}Making")
                making_of_film.isSettingForFilm = [film]
                if len(f.crew) > 0:
                    crew = Crew(f"{f.instance_name}Crew")
                    crew.hasMember = []
                    making_of_film.hasCrew = [crew]
                    for member in f.crew:
                        p = Person(member.id)
                        p.hasName = [member.name]
                        crew.hasMember.append(p)
                if len(f.cast) > 0:
                    cast = Cast(f"{f.instance_name}Cast")
                    cast.hasMember = []
                    for member in f.cast:
                        act_sit = ActingSituation(f"{member.id}ActingIn{f.instance_name}")
                        p = Person(member.id)
                        if member.name != "":
                            p.hasName = [member.name]
                        p.label.en.append(member.name)
                        act_sit.hasFilm = [film]
                        act_sit.hasActor = [p]
                        act_sit.hasCharacter = member.generate_characters(f.instance_name)
                        p.assign_gender(member.gender)
                        p.actsIn = [making_of_film]
                        cast.hasMember.append(p)
                film.hasTitle = [f.title]
                print(f"Added Film#{f.instance_name} as an individual")
