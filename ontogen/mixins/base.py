import typing
import uuid
from pprint import pprint

from django.db.models import Field, AutoField, ManyToOneRel

from ontogen.utils.basics import absolutize_entity_name
import start_dj

from django.db import models

from ontogen import OwlIndividual, Ontology, OwlClass

IGNORED_FIELD_PY_TYPES = ('RelatedManager', 'ManyRelatedManager')
P_NAME = '_name'


def name_instance(inst, prefix = "mao"):
    if hasattr(inst, P_NAME):
        return getattr(inst, P_NAME)
    return f"{prefix}:{f'{inst.__class__.__name__}_{inst.id}'}"


class DjModelOntogenMixin:
    _include_ = []  # Tuple['prop_name',' owl_relation_name']
    _exclude_ = []

    @classmethod
    def model_to_entity(cls, onto: Ontology, subject: models.Model) -> OwlIndividual:
        indiv = OwlIndividual(name_instance(subject, onto.base_prefix))
        model_type: typing.Type[models.Model] = subject.__class__
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
            if rel.name in cls._exclude_:
                continue
            if rel.name == 'id':
                continue
            relation_name = rel.name
            object = getattr(subject, relation_name)
            if type(object).__name__ in IGNORED_FIELD_PY_TYPES:
                continue
            if rel.auto_created or object is None or object == '':
                continue
            if relation_name in ('label', 'comment'):
                predicate_name = absolutize_entity_name(relation_name, 'rdfs')
            else:
                predicate_name = absolutize_entity_name(relation_name, onto.base_prefix)
            if isinstance(object, models.Model):
                instance_name = f'{object.__class__.__name__}_{object.id}'
                assignee = absolutize_entity_name(instance_name, onto.base_prefix)
            else:
                assignee = object # str, int, built-ins
            instance_of_class: OwlClass = onto.get_entity(subject.__class__.__name__)
            indiv.be_type_of(instance_of_class)
            indiv.add_property_assertion(predicate_name, assignee)
        for included_field, owl_field_name in cls._include_:
            object = getattr(subject, included_field)
            if isinstance(object, models.Model):
                instance_name = f'{object.__class__.__name__}_{object.id}'
                assignee = absolutize_entity_name(instance_name, onto.base_prefix)
            else:
                assignee = object  # str, int, built-ins
            instance_of_class: OwlClass = onto.get_entity(subject.__class__.__name__)
            indiv.be_type_of(instance_of_class)
            indiv.add_property_assertion(predicate_name, assignee)
        assert not isinstance(indiv, str)
        return indiv



