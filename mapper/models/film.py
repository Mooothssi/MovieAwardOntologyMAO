from .base import BaseMapperModel
from dataclasses import dataclass


@dataclass(eq=False)
class FilmModel(BaseMapperModel):
    instance_name: str = None
    title: str = ""
    cast: list = ""
    akas: list = ""
    pass
