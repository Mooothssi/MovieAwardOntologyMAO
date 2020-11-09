
from . import MapperDataSource
from db.models import TitleAkas, TitleBasics
from mapper.models.film import FilmModel
from sqlalchemy.orm import Session
import stringcase


class ImdbDataSource(MapperDataSource):
    def __init__(self, session: Session):
        self.session = session

    def get_film_instances(self) -> [FilmModel]:
        f_list: [FilmModel] = []
        for x in self.session.query(TitleBasics).all():
            film = FilmModel()
            film.cast = x.principals
            film.akas = x.akas.filter(TitleAkas.region == "US").all()
            film.title = film.akas[0].title
            film.instance_name = stringcase.pascalcase(film.title.replace(" ", ""))
            f_list.append(film)

        return f_list


