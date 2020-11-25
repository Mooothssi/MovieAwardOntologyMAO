from ontogen import OwlClass, Ontology
from ontogen.base import OwlEntity
from ontogen.primitives.base import OwlProperty


class OntologyBaseActualizer:
    def actualize(self, cls: OwlEntity, onto: Ontology):
        pass

    def get_actualized_entity(self, cls: OwlEntity, onto: Ontology, **attrs):
        pass


class OntologyActualizer:
    class_actualizer: OntologyBaseActualizer = None
    property_actualizer: OntologyBaseActualizer = None

    def __init__(self, onto: Ontology):
        self.onto = onto

    def actualize(self, entities: dict):
        for key, item in entities.items():
            if isinstance(item, OwlClass):
                self.class_actualizer.actualize(cls=item, onto=self.onto)
            elif isinstance(item, OwlProperty):
                self.property_actualizer.actualize(cls=item, onto=self.onto)
