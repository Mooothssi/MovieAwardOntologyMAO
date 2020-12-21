import typing
import uuid
from pprint import pprint

from django.db.models import Field, AutoField, ManyToOneRel

from ontogen.converter import OntogenConverter
from ontogen.primitives.properties import OwlProperty, OwlObjectProperty
from ontogen.utils.basics import absolutize_entity_name
from start_dj import start_django_lite
from dirs import ROOT_DIR
from django.db import models

from ontogen import OwlClass, OwlIndividual, Ontology

start_django_lite()

from app.models import Film, Country

from ontogen.mixins import model_to_entity


def add_individuals(converter: OntogenConverter) -> None:
    for f in Country.objects.all():
        indiv = model_to_entity(converter.ontology, f)
        converter.ontology.add_entity(indiv)
    for f in Film.objects.all():
        indiv = model_to_entity(converter.ontology, f)
        converter.ontology.add_entity(indiv)


if __name__ == '__main__':
    converter = OntogenConverter.load_from_spec(ROOT_DIR / "mao.yaml")

    add_individuals(converter)

    onto: Ontology = converter.sync_with_ontology()
    onto.save_to_file(ROOT_DIR / "mao.owl")
