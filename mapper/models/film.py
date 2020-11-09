from .base import BaseMapperModel
from dataclasses import dataclass
from owl_models.film import Gender, Character


@dataclass(eq=False)
class PersonModel(BaseMapperModel):
    gender: Gender = Gender.FEMALE
    name: str = ""
    id: str = ""


@dataclass(eq=False)
class ActorModel(PersonModel):
    characters: list[str] = ""

    def generate_characters(self, film: str) -> list[Character]:
        c_list = []
        for c in self.characters:
            char = Character(f"{c}In{film}")
            char.hasName = [c]
            c_list.append(char)
        return c_list


@dataclass(eq=False)
class FilmModel(BaseMapperModel):
    cast: list[ActorModel]
    crew: list[PersonModel]
    instance_name: str = None
    title: str = ""
    akas: list = ""

    def __init__(self):
        self.cast = []
        self.crew = []



