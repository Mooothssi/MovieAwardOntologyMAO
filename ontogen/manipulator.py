import stringcase
from owlready2 import Thing, Ontology, get_ontology
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import Type

from db.connection import connect_database
from tests.autowrite.nutrient import Nutrient
from tests.autowrite.base import Base
from ontogen.wrapper import BaseOntologyClass, apply_classes_from

from settings import OWL_FILEPATH


# SESSION = Session()  # connect_database()


def query_names(cls: Type[Base], onto: Ontology):
    # all_base = SESSION.query(cls).all()
    all_base = [cls()]
    for obj in all_base:
        obj.name = "example"
        thing = get_owl_thing(cls, onto)
        val = getattr(obj, "name")
        setattr(thing, get_relation_name("name"), ["example"])
        print(getattr(thing, get_relation_name("name")))
        for prop in get_model_columns(cls):
            print(prop)
    return all_base


def get_relation_name(name: str, prefix="has"):
    """
    Generates the names of relations
    :return:
    """
    return stringcase.camelcase(f"{prefix}_{name}")


def get_relation_names(cls: Type[Base], prefix="has"):
    """
    Generates the names of relations
    :return:
    """
    return [stringcase.camelcase(f"{prefix}_{str(y).replace(f'{str(cls.__name__)}.', '')}")
            for y in [getattr(cls, x) for x in cls.__dict__]
            if str(cls.__name__) in str(y)
            and isinstance(y, InstrumentedAttribute)]


def get_model_columns(cls: Type[Base]):
    """
    Generates the names of relations
    :return:
    """
    return [y.property.key
            for y in [getattr(cls, x) for x in cls.__dict__]
            if str(cls.__name__) in str(y)
            and isinstance(y, InstrumentedAttribute)]


#print(get_model_columns(Nutrient))


def get_owl_thing(cls: Type[Base], onto: Ontology):
    return BaseOntologyClass(name=cls.__name__, onto=onto)


onto = get_ontology(f"file:////{OWL_FILEPATH}")
onto.load()
apply_classes_from(onto)

# print(get_relation_names(Nutrient))
print(get_owl_thing(Nutrient, onto))
query_names(Nutrient, onto)
