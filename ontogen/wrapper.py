from owlready2 import (Ontology, Thing, ThingClass)


class BaseOntologyClass(Thing):
    def __init__(self):
        pass

    @property
    def instances(self):
        return self.ontology_class.instances()

    @property
    def _ontology_class(self) -> ThingClass:
        return getattr(self.ontology, self.__class__.__name__)

    # def __setattr__(self, key, value):
    #     att = getattr(self, key)
    #     if isinstance(att, list):
    #         att += value
    #     else:
    #         new_value = [value]  # owlready2 implementation
    #         super().__setattr__(key, new_value)

