from mapper.models.film import FilmModel


class MapperDataSource:
    name: str = None

    def get_film_instances(self) -> list[FilmModel]:
        pass
