from .base import BaseOntologyClass
from enum import Enum


class Agent(BaseOntologyClass):
    hasName: list[str]


class Character(Agent):
    pass


class ActingSituation(BaseOntologyClass):
    hasCharacter: list[Character]


class Gender(BaseOntologyClass):
    UNSPECIFIED = 0
    MALE = "Male"
    FEMALE = "Female"


def GENDER_MALE():
    return Gender("Male")


def GENDER_FEMALE():
    return Gender("Female")


class Person(Agent):
    actsIn: list["FilmMakingSituation"]
    hasGender: list[str]

    def assign_gender(self, gender: Gender):
        if gender in [Gender.MALE, Gender.FEMALE]:
            if gender == Gender.MALE:
                self.hasGender = [GENDER_MALE()]
            elif gender == Gender.FEMALE:
                self.hasGender = [GENDER_FEMALE()]


class Crew(BaseOntologyClass):
    hasMember: list[Person]


class Cast(BaseOntologyClass):
    hasMember: list[Person]


class Film(BaseOntologyClass):
    hasTitle: list[str]


class FilmMakingSituation(BaseOntologyClass):
    hasFilm: list[Film]
    hasDirector: list[Person]
    hasPart: list[ActingSituation]
