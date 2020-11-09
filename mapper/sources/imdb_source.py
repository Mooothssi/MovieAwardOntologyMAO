import ast
from . import MapperDataSource
from db.models import TitleAkas, TitleBasics
from mapper.models.film import FilmModel, PersonModel, ActorModel, Gender
from sqlalchemy.orm import Session
import stringcase


class ImdbDataSource(MapperDataSource):
    def __init__(self, session: Session):
        self.session = session

    def get_film_instances(self) -> [FilmModel]:
        f_list: [FilmModel] = []
        for x in self.session.query(TitleBasics).all():
            film = FilmModel()
            for person in x.principals:
                p: PersonModel = PersonModel()
                if person.name:
                    p.name = person.name.primaryName
                p.id = person.nconst
                c = person.category.lower()
                if c in ["actor", "actress"] or person.characters is not None:
                    p: ActorModel
                    p.__class__ = ActorModel
                    p.characters = ast.literal_eval(person.characters)
                    if c == "actor":
                        p.gender = Gender.MALE
                    else:
                        p.gender = Gender.FEMALE
                    film.cast.append(p)
                else:
                    film.crew.append(p)
            film.akas = x.akas.filter(TitleAkas.region == "US").all()
            film.title = film.akas[0].title
            film.instance_name = stringcase.pascalcase(film.title.replace(" ", ""))
            f_list.append(film)
        return f_list


