from owlready2 import Thing

from .base.ontology import Ontology


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]).union([cls])


def apply_classes_from(onto: Ontology):
    for s in all_subclasses(BaseOntologyClass):
        s.namespace = onto.implementation
        setattr(s, 'storid', onto.implementation.world._abbreviate(s.iri))


class BaseOntologyClass(Thing):
    def __init__(self, name: str, onto: Ontology = None):
        if onto is not None:
            self.namespace = onto.implementation
            self.ontology = onto
        super().__init__(name, namespace=self.namespace)
        apply_classes_from(self.ontology)

    @property
    def instances(self):
        return self.ontology_class.instances()

    @property
    def _ontology_class(self):
        return getattr(self.ontology, self.__class__.__name__)
