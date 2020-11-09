from .base import BaseOntologyClass


class Agent(BaseOntologyClass):
    hasName: list[str]


class Character(Agent):
    pass


class Acting(BaseOntologyClass):
    hasCharacter: list[Character]


class Person(Agent):
    actsIn: list["FilmMakingSituation"]


class MovieCrew(BaseOntologyClass):
    hasMember: list[Person]


class Film(BaseOntologyClass):
    hasTitle: list[str]


class FilmMakingSituation(BaseOntologyClass):
    hasFilm: list[Film]
    hasDirector: list[Person]
    hasPart: list[Acting]
