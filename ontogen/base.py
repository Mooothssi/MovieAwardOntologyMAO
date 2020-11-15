from datetime import date
from typing import List, Type, Union

from owlready2 import Ontology, Thing, locstr

LABEL_ENTITY_NAME = "rdfs:label"
COMMENT_ENTITY_NAME = "rdfs:comment"

BUILTIN_DATA_TYPES = Union[str, int]
BUILTIN_NAMES = (LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME)

GENERATED_TYPES = {}
DATATYPE_MAP = {
    'xsd:boolean': bool,
    'xsd:string': str,
    'xsd:integer': int,
    'xsd:float': float,
    'xsd:decimal': float,
    'xsd:date': date
}


class OntologyEntity:
    prefix = "owl"
    name = "any"
    _internal_dict = {}
    _parent_class = object
    parent_class_names: List[str] = []
    _parent_classes: List["OntologyEntity"] = []
    _disjoint_classes: List["OntologyEntity"] = []
    # Short for an Implementation instance
    _internal_imp_instance: Thing = None

    def __init__(self, entity_qualifier: str):
        pre, n = entity_qualifier.split(":")
        self.prefix = pre
        self.name = n
        self.dependencies = []
        self._parent_classes = []
        self._disjoint_classes = []
        self.properties_values = {}

    @classmethod
    def get_entity_name(cls) -> str:
        return f"{cls.prefix}:{cls.name}"

    # owlready2-related implementation
    def instantiate(self, onto: Ontology):
        pass

    def get_generated_class(self, onto: Ontology, **attrs) -> Type[Thing]:
        if self.name in GENERATED_TYPES:
            return GENERATED_TYPES[self.name]
        attrs['namespace'] = onto
        default = True
        if len(self._parent_classes) > 0:
            gen = [x.get_generated_class(onto=onto) for x in self._parent_classes if x is not None]
            if len(gen) > 0:
                GENERATED_TYPES[self.name] = type(self.name, tuple(gen), attrs)
                default = False
        if default:
            GENERATED_TYPES[self.name] = type(self.name, (self._parent_class,), attrs)
        try:
            if len(GENERATED_TYPES[self.name].equivalent_to) > 0:
                print(GENERATED_TYPES[self.name].equivalent_to[0].__class__)
        except AttributeError:
            pass
        return GENERATED_TYPES[self.name]

    def add_superclass(self, superclass: "OntologyEntity"):
        """
        Adds a superclass of this Class.
        This Class will then be a `rdfs:subclassOf` a given superclass
        :param superclass: A given Superclass
        """
        self._parent_classes.append(superclass)

    def add_disjoint_classes(self, cls: "OntologyEntity"):
        self._disjoint_classes.append(cls)

    def add_label(self, value: BUILTIN_DATA_TYPES):
        if value is None:
            return
        self.properties_values[LABEL_ENTITY_NAME] = value

    def add_comment(self, value: BUILTIN_DATA_TYPES):
        if value is None:
            return
        self.properties_values[COMMENT_ENTITY_NAME] = value

    @property
    def is_individual(self) -> bool:
        return self._internal_imp_instance is not None

    def _sync_internal(self, onto: Ontology):
        if not self.is_individual:
            inst = self.get_generated_class(onto)
        else:
            inst = self._internal_imp_instance
        for set_prop in self.properties_values:
            val = self.properties_values[set_prop]
            if set_prop in BUILTIN_NAMES:
                val: str
                if "^^" in val or "@" in val:
                    import re
                    split_values = re.split(r'(?:(.+)\^\^(.+)@(.+)|(.+)\^\^(.+))', val)
                    if len(split_values) > 2 and split_values[1] is not None:
                        lit, lang = (split_values[1], split_values[3])
                        val = locstr(lit, lang)
                    else:
                        val, data_type = (split_values[4], split_values[5])
                        val = DATATYPE_MAP[data_type](val)
            set_prop = set_prop.split(":")[1]
            try:
                if isinstance(val, list):
                    setattr(inst, set_prop, val)
                else:
                    setattr(inst, set_prop, [val])
            except AttributeError:
                pass
