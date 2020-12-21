import typing
import uuid
from pprint import pprint

from django.db.models import Field, AutoField, ManyToOneRel

from app.models import Genre
from ontogen.converter import OntogenConverter
from ontogen.mixins.base import DjModelOntogenMixin
from ontogen.primitives.properties import OwlProperty, OwlObjectProperty
from ontogen.utils.basics import absolutize_entity_name
import start_dj
from dirs import ROOT_DIR
from django.db import models

from ontogen import Ontology

from ontogen.wrapper import all_subclasses


def add_individuals(converter: OntogenConverter) -> None:
    for cls in all_subclasses(DjModelOntogenMixin):
        if cls == DjModelOntogenMixin:
            continue
        if cls == Genre:
            print()
        for inst in cls.objects.all():
            indiv = cls.model_to_entity(converter.ontology, inst)
            converter.ontology.add_entity(indiv)
    # for f in Country.objects.all():
    #     indiv = model_to_entity(converter.ontology, f)
    #     converter.ontology.add_entity(indiv)
    # for f in Film.objects.all():
    #     indiv = model_to_entity(converter.ontology, f)
    #     converter.ontology.add_entity(indiv)


if __name__ == '__main__':
    converter = OntogenConverter.load_from_spec(ROOT_DIR / "mao.yaml")

    add_individuals(converter)

    onto: Ontology = converter.sync_with_ontology()
    onto.save_to_file(ROOT_DIR / "mao.owl")
