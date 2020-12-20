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


IGNORED_FIELD_PY_TYPES = ('RelatedManager', 'ManyRelatedManager')


def model_to_entity(onto: Ontology, model: models.Model) -> OwlIndividual:
    indiv = OwlIndividual(f"mao:{f'{model.__class__.__name__}_{model.id}'}")
    prefix = 'mao'
    model_type: typing.Type[models.Model] = model.__class__
    for rel in model_type._meta.get_fields():
        rel: typing.Union[ManyToOneRel, AutoField]
        if isinstance(rel, ManyToOneRel):
            if rel.related_name is None:
                continue
        if isinstance(rel, Field):
            field = rel.name
        else:
            field = rel.field.name
        if '.' in field:
            field = field.split('.')[-1]
        if rel.name == 'id':
            continue
        p = getattr(model, rel.name)
        if type(p).__name__ in IGNORED_FIELD_PY_TYPES:
            continue
        if rel.auto_created or p is None or p == '':
            continue
        if rel.name in ('label', 'comment'):
            prop_name = absolutize_entity_name(rel.name, 'rdfs')
        else:
            prop_name = absolutize_entity_name(rel.name, onto.base_prefix)
        if isinstance(p, models.Model):
            over_id = f'{p.__class__.__name__}_{p.id}'
            val = absolutize_entity_name(over_id, onto.base_prefix)
        else:
            val = p
        indiv.be_type_of(onto.get_entity(model.__class__.__name__))
        indiv.add_property_assertion(prop_name, val)
    return indiv


if __name__ == '__main__':
    converter = OntogenConverter.load_from_spec(ROOT_DIR / "mao.yaml")
    for f in Country.objects.all():
        indiv = model_to_entity(converter.ontology, f)
        converter.ontology.add_entity(indiv)
    for f in Film.objects.all():
        indiv = model_to_entity(converter.ontology, f)
        converter.ontology.add_entity(indiv)
    onto: Ontology = converter.sync_with_ontology()
    onto.save_to_file(ROOT_DIR / "mao.owl")
