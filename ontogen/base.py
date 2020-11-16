from datetime import date
from typing import List, Type, Union

import owlready2
from owlready2 import Imp, Thing, locstr, get_ontology

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


class Ontology:
    """
    TODO: A proxy for the real implementation in `owlready2`
    """

    def __init__(self, namespace_iri: str = ""):
        self._internal_onto: owlready2.Ontology = None
        self.namespace_iri = namespace_iri

    def create(self, namespace_iri: str = ""):
        """
            Newly creates an Ontology from an existing namespace
        """
        assert self.namespace_iri == "" or namespace_iri == "", "Namespace must be set before creation"
        self._internal_onto = get_ontology(self.namespace_iri if self.namespace_iri != "" else namespace_iri)

    @classmethod
    def load_from_file(cls, filename: str) -> "Ontology":
        """
            Loads an Ontology from an existing file
            :param filename: The name of a given file
            :return: Ontology object
        """
        inst = cls()
        inst._internal_onto = get_ontology(f"file:////{filename}")
        inst._internal_onto.load()
        return inst

    def save_to_file(self, filename: str, file_format: str="rdfxml"):
        """
            Saves an Ontology with a given filename
            :param filename: A given filename
            :param file_format: The file format of given filename. Only `rdfxml` is supported by `owlready2`
        """
        self.implementation.save(file=filename, format=file_format)

    def add_rule(self, swrl_rule: str):
        """
            Adds a SWRL rule to the Ontology
            :param swrl_rule: A rule definition in SWRL
        """
        rule = Imp(namespace=self.implementation)
        rule.set_as_rule(swrl_rule.replace(f"{self.base_name}:", "").replace("^ ", ", "))

    @property
    def implementation(self) -> owlready2.Ontology:
        return self._internal_onto

    @property
    def base_name(self):
        return self.implementation.name


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
        self._realised_parent_classes = []

    @classmethod
    def get_entity_name(cls) -> str:
        return f"{cls.prefix}:{cls.name}"

    # owlready2-related implementation
    def instantiate(self, onto: Ontology, individual_name: str):
        pass

    def actualize(self, onto: Ontology):
        """
            Makes the entity concrete (saved) in a given Ontology
            :param onto: a given Ontology
        """
        pass

    def get_generated_class(self, onto: Ontology, **attrs) -> Type[Thing]:
        if self.name in GENERATED_TYPES:
            return GENERATED_TYPES[self.name]
        attrs['namespace'] = onto.implementation
        default = True
        if len(self._parent_classes) > 0 or len(self._realised_parent_classes) > 0:
            self._realised_parent_classes.extend(
                [x.get_generated_class(onto=onto) for x in self._parent_classes
                 if x is not None and isinstance(x, OntologyEntity)])
            gen = self._realised_parent_classes
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

    def _add_builtin_prop(self, builtin_name: str, value: BUILTIN_DATA_TYPES):
        if value is None:
            return
        if builtin_name not in self.properties_values:
            self.properties_values[builtin_name] = []
        self.properties_values[builtin_name] += [value]

    def add_label(self, value: BUILTIN_DATA_TYPES):
        """
            Add a rdfs:label AnnotationProperty with a given value of supported types
            :param value: A given label. Can be a `str` or `locstr` (Literal with a language)
        """
        self._add_builtin_prop(LABEL_ENTITY_NAME, value)

    def add_comment(self, value: BUILTIN_DATA_TYPES):
        """
            Add a rdfs:comment AnnotationProperty with a given value of supported types
            :param value: A given label. Can be a `str` or `locstr` (Literal with a language)
        """
        self._add_builtin_prop(COMMENT_ENTITY_NAME, value)

    def add_labels(self, values: List[BUILTIN_DATA_TYPES]):
        for v in values:
            self.add_label(v)

    def add_comments(self, values: List[BUILTIN_DATA_TYPES]):
        for v in values:
            self.add_comment(v)

    @property
    def is_individual(self) -> bool:
        return self._internal_imp_instance is not None

    @property
    def is_actualized(self) -> bool:
        return self.name in GENERATED_TYPES

    @property
    def realized_entity(self):
        if self.is_actualized:
            return GENERATED_TYPES[self.name]

    def _sync_internal(self, onto: Ontology):
        if not self.is_individual:
            inst = self.get_generated_class(onto)
        else:
            inst = self._internal_imp_instance
        for set_prop in self.properties_values:
            val = self.properties_values[set_prop]
            if set_prop in BUILTIN_NAMES and isinstance(val, list):
                for i, v in enumerate(val):
                    v: str
                    if "^^" in v or "@" in v:
                        import re
                        split_values = re.split(r'(?:(.+)\^\^(.+)@(.+)|(.+)\^\^(.+))', v)
                        if len(split_values) > 2 and split_values[1] is not None:
                            lit, lang = (split_values[1], split_values[3])
                            val[i] = locstr(lit, lang)
                        else:
                            v, data_type = (split_values[4], split_values[5])
                            val[i] = DATATYPE_MAP[data_type](v)
            set_prop = set_prop.split(":")[1]
            try:
                if isinstance(val, list):
                    setattr(inst, set_prop, val)
                else:
                    setattr(inst, set_prop, [val])
            except AttributeError:
                pass
