from pathlib import Path
import typing
import pandas as pd

from dirs import ROOT_DIR

from ontogen import Ontology
from ontogen.converter import OntogenConverter, OwlClass, OwlIndividual
from autogen_db_models import imdb, awards
from engine import Session
import attr

_T = typing.TypeVar('_T')
FilePathOrBuffer = typing.Union[str, Path, typing.IO[typing.AnyStr]]


@attr.s
class Film:
    title_id: str = attr.ib()
    title: str = attr.ib()
    film_year: int = attr.ib()


def convert_yaml_to_owl(yaml_file: FilePathOrBuffer, owl_file: Path):
    converter = OntogenConverter.load_from_spec(yaml_file)
    # Save the results to an in-memory Ontology
    onto: Ontology = converter.export_to_ontology()
    # Save the results to an RDF/XML file Ontology. Can be 'xml' or 'ttl'
    onto.save_to_file(owl_file)


def read_attrs_list(file: FilePathOrBuffer,
                    cls: typing.Type[_T]) -> typing.List[_T]:
    """ Returns a list of attrs instances read from a CSV file. """
    df = pd.read_csv(file)
    lst = []
    for row in df.iterrows():
        lst.append(cls(**row))
    return lst


def dump_attrs_list(file: FilePathOrBuffer,
                    attrs_lst: typing.List[Film]) -> None:
    """ Dumps a list of attrs instances to a CSV file. """
    attrs_dicts = []
    for attrs in attrs_lst:
        attrs_dict = attr.asdict(attrs)
        attrs_dicts.append(attrs_dict)
    df = pd.DataFrame(attrs_dicts)
    df.to_csv(file)


def get_starting_films_from_awards() -> typing.List[Film]:
    """Returns a list of Film with attribs title_id, title, and file_year added."""
    session = Session()
    oscars = session.query(awards.Oscar).all()
    baftas = session.query(awards.Bafta).all()

    unique_oscar_films = set()
    for oscar in oscars:
        if oscar.film is None or oscar.year_film is None:
            continue
        unique_oscar_films.add((oscar.film, oscar.year_film))
    unique_bafta_films = set()
    for bafta in baftas:
        if bafta.nominee is None or bafta.year is None:
            continue
        unique_bafta_films.add((bafta.nominee, bafta.year))

    unique_award_winning_films = unique_oscar_films.union(unique_bafta_films)

    film_lst: typing.List[Film] = []
    title_akas_basics = session.query(imdb.TitleAkas.titleId, imdb.TitleAkas.title, imdb.TitleBasics.startYear).join(imdb.TitleBasics, imdb.TitleAkas.titleId == imdb.TitleBasics.tconst)

    for film in unique_award_winning_films:
        assert isinstance(film[0], str), str(film)
        assert isinstance(film[1], int), str(film)
        print(f"{film=}")
        title_akas_basic = title_akas_basics.filter(imdb.TitleAkas.title == film[0]).filter(imdb.TitleBasics.startYear == film[1]).first()
        if title_akas_basic is None:
            continue
        film_lst.append(Film(title_id=title_akas_basic[0], title=title_akas_basic[1], film_year=title_akas_basic[2]))
        print(title_akas_basic)

    return film_lst


if __name__ == '__main__':
    # convert_yaml_to_owl(ROOT_DIR / "mao.yaml", ROOT_DIR / "
    films = get_starting_films_from_awards()
    dump_attrs_list(ROOT_DIR / 'mapping/films.csv', films)
