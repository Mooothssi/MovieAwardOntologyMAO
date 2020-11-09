from owlready2 import Ontology, Thing, ThingClass


class BaseOntologyClass(Thing):
    def __init__(self, name: str, onto: Ontology = None):
        if onto is not None:
            self.namespace = onto
            self.ontology = onto
        super().__init__(name)

    @property
    def instances(self):
        return self.ontology_class.instances()

    @property
    def _ontology_class(self) -> ThingClass:
        return getattr(self.ontology, self.__class__.__name__)


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def apply_classes_from(onto: Ontology):
    for s in all_subclasses(BaseOntologyClass):
        s.namespace = onto
        setattr(s, 'storid', onto.world._abbreviate(s.iri))
