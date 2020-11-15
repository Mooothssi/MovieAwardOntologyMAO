from owlready2 import Ontology

GENERATED_TYPES = {}


class OntologyEntity:
    prefix = "owl"
    name = "any"
    _internal_dict = {}
    _owlready_class = object

    def __init__(self, entity_qualifier: str):
        pre, n = entity_qualifier.split(":")
        self.prefix = pre
        self.name = n
        self.dependencies = []

    @classmethod
    def get_entity_qualifier(cls) -> str:
        return f"{cls.prefix}:{cls.name}"

    # owlready-related implementation
    def instantiate(self, onto: Ontology):
        pass

    def get_generated_class(self, onto: Ontology, **attrs) -> type:
        if self.name in GENERATED_TYPES:
            return GENERATED_TYPES[self.name]
        attrs['namespace'] = onto
        GENERATED_TYPES[self.name] = type(self.name, (self._owlready_class,), attrs)
        return GENERATED_TYPES[self.name]