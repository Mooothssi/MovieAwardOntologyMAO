import typing
import uuid
from pprint import pprint

from django.db.models import Field, AutoField, ManyToOneRel
from django.db.models.fields.reverse_related import ManyToManyRel

from ontogen.utils.basics import absolutize_entity_name
import start_dj

from django.db import models

from ontogen import OwlIndividual, Ontology, OwlClass

IGNORED_FIELD_PY_TYPES = ('RelatedManager', 'ManyRelatedManager')
P_NAME = '_name'


def get_as_done(q):
    if '.None' in str(q):
        print()
        return
    return q


def field_of(model_type: typing.Type[models.Model]):
    return [f.name for f in model_type._meta.get_fields()
            if not f.auto_created]


def name_instance(inst, prefix = "mao"):
    if hasattr(inst, P_NAME):
        return getattr(inst, P_NAME)
    return f"{prefix}:{f'{inst.__class__.__name__}_{inst.id}'}"


def assign_something(onto: Ontology, subject, predicate_name: str, s_object, indiv: OwlIndividual):
    print(f'{subject} {predicate_name} {s_object}.')
    if isinstance(s_object, models.Model):
        instance_name = f'{s_object.__class__.__name__}_{s_object.id}'
        assignee = absolutize_entity_name(instance_name, onto.base_prefix)
    else:
        assignee = s_object  # str, int, built-ins
    instance_of_class: OwlClass = onto.get_entity(subject.__class__.__name__)
    indiv.be_type_of(instance_of_class)
    indiv.add_property_assertion(predicate_name, assignee)


class DjModelOntogenMixin:
    _include_ = []  # Tuple['prop_name',' owl_relation_name']
    _exclude_ = []

    @classmethod
    def model_to_entity(cls, onto: Ontology, subject: models.Model) -> OwlIndividual:
        indiv = OwlIndividual(name_instance(subject, onto.base_prefix))
        model_type: typing.Type[models.Model] = subject.__class__
        for rel in model_type._meta.get_fields():
            rel: typing.Union[ManyToOneRel, ManyToManyRel, AutoField]
            # if subject.__class__.__name__ == 'Genre':
            #     pprint([f.name for f in model_type._meta.get_fields() if not f.auto_created])
            if rel.name not in field_of(model_type):
                continue
            # if isinstance(rel, ManyToManyRel):
            #     raise AssertionError()
            # if isinstance(rel, ManyToOneRel):
            #     if rel.related_name is None:
            #         continue
            # SubGenre
            # pprint(field_of(model_type))
            if isinstance(rel, Field):
                field = rel.name
            else:
                field = rel.field.name
            if '.' in field:
                field = field.split('.')[-1]
            if rel.name in cls._exclude_ or '_ptr' in rel.name:
                continue
            if rel.name == 'id':
                continue
            relation_name = rel.name
            if not hasattr(subject, relation_name):
                continue
            s_object = getattr(subject, relation_name)
            if not s_object:
                continue
            # if rel.auto_created or object is None or object == '':
            #     continue
            if relation_name in ('label', 'comment'):
                predicate_name = absolutize_entity_name(relation_name, 'rdfs')
            else:
                predicate_name = absolutize_entity_name(relation_name, onto.base_prefix)
            if type(s_object).__name__ in ('ManyRelatedManager',):
                continue
            if type(s_object).__name__ in IGNORED_FIELD_PY_TYPES:
                # s_object = get_as_done(s_object)
                for element in list(s_object.all()):
                    assign_something(onto, subject, predicate_name, element, indiv)
            assign_something(onto, subject, predicate_name, s_object, indiv)
        for included_field, owl_field_name in cls._include_:
            s_object = getattr(subject, included_field)
            predicate_name = included_field
            assign_something(onto, subject, predicate_name, s_object, indiv)
            # if isinstance(object, models.Model):
            #     instance_name = f'{object.__class__.__name__}_{object.id}'
            #     assignee = absolutize_entity_name(instance_name, onto.base_prefix)
            # else:
            #     assignee = object  # str, int, built-ins
            # instance_of_class: OwlClass = onto.get_entity(subject.__class__.__name__)
            # indiv.be_type_of(instance_of_class)
            # indiv.add_property_assertion(predicate_name, assignee)
        assert not isinstance(indiv, str)
        return indiv



