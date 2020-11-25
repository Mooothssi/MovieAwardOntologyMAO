from typing import Union, Type

from owlready2 import Thing

ACTUALIZED_CLASS = Union[Thing, Type[Thing], None]
