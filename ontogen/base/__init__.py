from abc import ABCMeta, abstractmethod
from typing import List, Type, Union

from owlready2 import Thing, ClassConstruct

from .annotable import OwlAnnotatable
from .ontology import Ontology
from .vars import BUILTIN_NAMES, DATATYPE_MAP, GENERATED_TYPES, LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME

BUILTIN_DATA_TYPES = Union[str, int]


class OntologyEntity(OwlAnnotatable, metaclass=ABCMeta):
    prefix = "owl"
    name = "any"
    _internal_dict = {}
    _parent_class = object
    parent_class_names: List[str] = []
    _parent_classes: List["OntologyEntity" or ClassConstruct] = []
    _disjoint_classes: List["OntologyEntity"] = []

    # Short for an Implementation instance
    _internal_imp_instance: Thing = None

    def __init__(self, entity_qualifier: str):
        super(OwlAnnotatable).__init__()
        self.properties_values = {}
        assert ":" in entity_qualifier, "Must include a prefix"
        pre, n = entity_qualifier.split(":")
        self.prefix = pre
        self.name = n
        self.dependencies = []
        self._parent_classes = []
        self._disjoint_classes = []
        self.equivalent_class_expressions: List[str] = []
        self.equivalent_classes: List[ClassConstruct] = []
        self._realised_parent_classes = []
        self.equivalent_class_expressions = []


    @classmethod
    def get_entity_name(cls) -> str:
        return f"{cls.prefix}:{cls.name}"

    def get_full_iri(self, onto: Ontology):
        return f"{onto.lookup_iri(self.prefix)}{self.name}"

    @abstractmethod
    def actualize(self, onto: Ontology) -> 'OntologyEntity':
        """
            Makes the entity concrete (saved) in a given Ontology
            :param onto: a given Ontology
        """
        raise NotImplementedError

    def add_superclass(self, superclass: "OntologyEntity" or "str"):
        """
        Adds a superclass of this Class.
        This Class will then be a `rdfs:subclassOf` a given superclass
        :param superclass: A given Superclass
        """
        if superclass is None:
            return
        self._parent_classes.append(superclass)

    def add_disjoint_class(self, cls: "OntologyEntity"):
        """
        Adds a disjoint class to this Class. The given class will be lazy loaded.

        Args:
            cls: an OntologyEntity
        """
        self._disjoint_classes.append(cls)

    def add_equivalent_class_expression(self, expression: str or ClassConstruct):
        """
        Adds an equivalent class to this Class

        Args:
            expression: A Class Expression in Protege Manchester Syntax
                        or an `owlready2` Class Construct

        Note:
            A Class Expression in Manchester Syntax will be lazy loaded.
        """
        if expression is None:
            return
        if isinstance(expression, ClassConstruct):
            self.equivalent_classes.append(expression)
        elif isinstance(expression, str):
            self.equivalent_class_expressions.append(expression)
            self._sync_description()
        else:
            raise TypeError("Invalid type")

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
        """Whether this Class is saved to an Ontology
        """
        return self.name in GENERATED_TYPES

    def sync(self):
        self.actualize(self.actualized_entity.namespace)

    @property
    def actualized_entity(self):
        if self.is_actualized:
            return GENERATED_TYPES[self.name]
        raise AssertionError("The entity has yet to be actualized")

    def _get_generated_class(self, onto: Ontology, **attrs) -> Type[Thing]:
        try:
            self._sync_description()
            return self.actualized_entity
        except AssertionError:
            attrs['namespace'] = onto.implementation
            default = True
            if len(self._parent_classes) > 0 or len(self._realised_parent_classes) > 0:
                self._realised_parent_classes.extend(
                    [x._get_generated_class(onto) for x in self._parent_classes
                     if x is not None and isinstance(x, OntologyEntity)])
                gen = self._realised_parent_classes
                if len(gen) > 0:
                    GENERATED_TYPES[self.name] = type(self.name, tuple(gen), attrs)
                    default = False
            if default:
                GENERATED_TYPES[self.name] = type(self.name, (self._parent_class,), attrs)
            if onto.base_prefix != self.prefix:
                p = self.get_full_iri(onto)
                self.actualized_entity.iri = p
            self._sync_description()
            return GENERATED_TYPES[self.name]

    def _sync_description(self):
        """
        Internally synchronizes with the `owlready2` representation of this Class
        """
        self.actualized_entity.equivalent_to = self.equivalent_classes

    def _sync_internal(self, onto: Ontology):
        if not self.is_individual:
            inst = self._get_generated_class(onto)
        else:
            inst = self._internal_imp_instance
        self.actualize_annotations(inst)
        # for set_prop in self.properties_values:
        #     val = self.properties_values[set_prop]
        #     if set_prop in BUILTIN_NAMES and isinstance(val, list):
        #         for i, v in enumerate(val):
        #             v: str
        #             if "^^" in v or "@" in v:
        #                 import re
        #                 split_values = re.split(r'(?:(.+)\^\^(.+)@(.+)|(.+)\^\^(.+))', v)
        #                 if len(split_values) > 2 and split_values[1] is not None:
        #                     lit, lang = (split_values[1], split_values[3])
        #                     val[i] = locstr(lit, lang)
        #                 else:
        #                     v, data_type = (split_values[4], split_values[5])
        #                     val[i] = DATATYPE_MAP[data_type](v)
        #     set_prop = set_prop.split(":")[1]
        #     try:
        #         if isinstance(val, list):
        #             setattr(inst, set_prop, val)
        #         else:
        #             setattr(inst, set_prop, [val])
        #     except AttributeError:
        #         pass
