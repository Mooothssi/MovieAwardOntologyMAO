from pathlib import Path
import typing
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist

from dirs import ROOT_DIR

from ontogen import Ontology
from ontogen.converter import OntogenConverter, OwlClass, OwlIndividual
from autogen_db_models import imdb, awards
from engine import Session
import attr

from mao_dj.app import models
from spacy_nlp import get_not_person_name
import spacy_nlp as snlp

_T = typing.TypeVar('_T')
FilePathOrBuffer = typing.Union[str, Path, typing.IO[typing.AnyStr]]

# class PersonRole:
#     person: Person = attr.ib()
#     film: Film = attr


@attr.s(slots=True)
class Person:
    name: str = attr.ib()
    nconst: str = attr.ib()


@attr.s(slots=True)
class Film:
    title_id: str = attr.ib()
    title: str = attr.ib()
    film_year: int = attr.ib(converter=int)
    # content_rating: str = attr.ib(default=None)
    # feature_length: int = attr.ib(default=None)
    # avg_rating: float = attr.ib(default=None)
    # person_role: typing.List[typing.Tuple[Person, str]] = attr.ib(factory=list)


@attr.s(slots=True)
class Nomination:
    nominee: str = attr.ib()
    win: bool = attr.ib()
    award_agency: str = attr.ib()
    film: Film = attr.ib()


def convert_yaml_to_owl(yaml_file: FilePathOrBuffer, owl_file: Path):
    converter = OntogenConverter.load_from_spec(yaml_file)
    # Save the results to an in-memory Ontology
    onto: Ontology = converter.export_to_ontology()
    # Save the results to an RDF/XML file Ontology. Can be 'xml' or 'ttl'
    onto.save_to_file(owl_file)


def load_attrs_list(file: FilePathOrBuffer,
                    cls: typing.Type[_T]) -> typing.List[_T]:
    """ Returns a list of attrs instances read from a CSV file. """
    df = pd.read_csv(file)
    lst = []
    for i, row in df.iterrows():
        lst.append(cls(**{k: v for k, v in row.items() if k in cls.__slots__}))
    return lst


def dump_attrs_list(file: FilePathOrBuffer,
                    attrs_lst: typing.List[Film]) -> None:
    """ Dumps a list of attrs instances to a CSV file. """
    attrs_dicts = []
    for attrs in attrs_lst:
        attrs_dict = attr.asdict(attrs)
        attrs_dicts.append(attrs_dict)
    df = pd.DataFrame(attrs_dicts)
    df.to_csv(file, index=False)


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
        if bafta.workers is not None:
            film_name = get_not_person_name(bafta.nominee, bafta.workers)
            # try:
            #     film_name = get_not_person_name(bafta.nominee, bafta.workers)
            # except ValueError:
            #     film_name = None
            #     while True:
            #         res = input(f"Choose between '{bafta.nominee}' or '{bafta.workers}' as the person (1/2/q/s): ")
            #         if res == 'q':
            #             raise
            #         if res == 's':
            #             break
            #         if res == '1':
            #             film_name = bafta.workers
            #             break
            #         if res == '2':
            #             film_name = bafta.nominee
            #             break
            #     if film_name is None:
            #         continue
        else:
            film_name = bafta.nominee
        unique_bafta_films.add((film_name, bafta.year))

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


def init_awards():
    models.Award.objects.create(hasNickname='Oscars')
    models.Award.objects.create(hasNickname='BAFTA')


def add_award_info():
    films: typing.Iterable[models.Film] = models.Film.objects.all()
    session = Session()
    # oscars = session.query(awards.Oscar).all()
    # baftas = session.query(awards.Bafta).all()

    for film in films:
        oscar = session.query(awards.Oscar)\
            .filter(awards.Oscar.film == film.hasTitle)\
            .filter(awards.Oscar.year_film == film.hasInitialReleaseYear).first()

        if not oscar:
            continue

        res, name = snlp.categorize(oscar.name)
        if res == 'ORG':
            agent = models.Organization.upsert(hasName=name, label=name)
        elif res == 'PERSON':
            agent = models.Person.upsert(hasName=name)
        else:
            raise ValueError

        award = models.Award.objects.get(hasNickname='Oscars')
        award_cat = models.AwardCategory.get_instance_from_kaggle_oscar_data(oscar.category)
        award_cem = models.AwardCeremony.upsert(
                hasAward=award,
                yearHeld=oscar.year_ceremony,
                yearScreened=oscar.year_film,
                hasEditionNumber=oscar.ceremony)

        nom = models.NominationSituation.upsert(
            forFilm=film,
            hasAward=award,
            hasAwardCategory=award_cat,
            hasAwardCeremony=award_cem,
            isGivenTo=agent,
            win=oscar.winner
        )
        print(f'{film} {nom}')

        # bafta = session.query(awards.Bafta) \
        #     .filter(awards.Oscar.film == film.hasTitle) \
        #     .filter(awards.Oscar.year_film == film.hasInitialReleaseYear).first()


def add_imdb_info():
    films: typing.Iterable[models.Film] = models.Film.objects.all()
    session = Session()
    for film in films:
        tconst = film.t_const

        # add info from title_basic
        title_basic: imdb.TitleBasics = session.query(imdb.TitleBasics).filter(imdb.TitleBasics.tconst == tconst).first()
        # add genres
        for genre in title_basic.genres.split(','):
            g = models.Genre.upsert(label=genre)
            film.hasGenre.add(g)

        film.isAdult = bool(title_basic.isAdult)
        if title_basic.isAdult == 1:
            film.hasAudience = models.Audience.upsert(label='Adults')
        else:
            film.hasAudience = models.Audience.upsert(label='Children')

        film.hasFeatureLengthInMinutes = title_basic.runtimeMinutes

        # add info from title_akas
        title_akas_lst: typing.Iterable[imdb.TitleAkas] = session.query(imdb.TitleAkas, imdb.ProductionCompanies, imdb.Certificates)\
            .filter(imdb.TitleAkas.titleId == tconst)\
            .filter(imdb.TitleAkas.isOriginalTitle == 1) \
            .join(imdb.TitleBasics,
                  imdb.TitleBasics.tconst == imdb.TitleAkas.titleId)\
            .join(imdb.Certificates,
                  imdb.Certificates.title == imdb.TitleAkas.title
                  and imdb.Certificates.year == imdb.TitleBasics.startYear)\
            .join(imdb.ProductionCompanies, imdb.ProductionCompanies.title == imdb.TitleAkas.title
                  and imdb.ProductionCompanies.year == imdb.TitleBasics.startYear
                  ).all()
        for three in title_akas_lst:
            title_akas = three[0]
            prod = three[1]
            if title_akas.isOriginalTitle == 1:
                try:
                    if prod.country_code:
                        country = models.Country.objects.get(alpha_2__iexact=prod.country_code.upper())
                        film.hasCountryOfOrigin = country
                        print(f'found: {title_akas}')
                except ObjectDoesNotExist:
                    print(title_akas.region)


def read_alpha_2_to_countries(csv_file: str):
    import pandas
    df = pandas.read_csv(csv_file)
    df = df[['Country', 'Alpha-2 code', 'Alpha-3 code']]
    for i in df.iterrows():
        series = i[1]
        models.Country.objects.create(alpha_3=series['Alpha-3 code'].replace('"', '').strip(),
                                      alpha_2=series['Alpha-2 code'].replace('"', '').strip(),
                                      label=series['Country'])


if __name__ == '__main__':
    pass
