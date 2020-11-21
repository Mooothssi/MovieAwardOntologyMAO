from abc import ABCMeta, abstractmethod
from typing import List, Type, Union

from owlready2 import Thing, ClassConstruct
from owlready2.prop import destroy_entity

from .assertable import OwlAssertable
from .ontology import Ontology
from .vars import BUILTIN_NAMES, DATATYPE_MAP, GENERATED_TYPES, LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME, BUILTIN_DATA_TYPES


def cleanup(onto: Ontology):
    onto.implementation.graph.destroy()
    for e in GENERATED_TYPES:
        try:
            destroy_entity(GENERATED_TYPES[e])
        except:
            pass
    GENERATED_TYPES.clear()

# BUILTIN_DATA_TYPES = Union[str, int]


class OwlActualizable(metaclass=ABCMeta):
    @abstractmethod
    def actualize(self, onto: Ontology) -> 'OwlEntity':
        """
            Makes the entity concrete (saved) in a given Ontology
            :param onto: a given Ontology
        """
        raise NotImplementedError


class OwlEntity(OwlAssertable, OwlActualizable, metaclass=ABCMeta):
    prefix = "owl"
    name = "any"
    _internal_dict = {}
    _parent_class = object
    parent_class_names: List[str] = []
    _parent_classes: List["OwlEntity" or ClassConstruct] = []
    _disjoint_classes: List["OwlEntity"] = []

    # Short for an Implementation instance
    _internal_imp_instance: Thing = None

    def __init__(self, entity_qualifier: str):
        super().__init__()
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
    def actualize(self, onto: Ontology) -> 'OwlEntity':
        """
            Makes the entity concrete (saved) in a given Ontology
            :param onto: a given Ontology
        """
        raise NotImplementedError

    def add_superclass(self, superclass: Union["OwlEntity", "str"]):
        """
        Adds a superclass of this Class.
        This Class will then be a `rdfs:subclassOf` a given superclass
        :param superclass: A given Superclass
        """
        if superclass is None:
            return
        self._parent_classes.append(superclass)

    def add_disjoint_class(self, cls: "OwlEntity"):
        """
        Adds a disjoint class to this Class. The given class will be lazy loaded.

        Args:
            cls: an OntologyEntity
        """
        self._disjoint_classes.append(cls)

    def add_equivalent_class_expression(self, expression: Union[str, ClassConstruct]):
        """
        Adds an equivalent class to this Class

        Args:
            expression: A Class Expression in Protege Manchester Syntax
                        or an `owlready2` Class Construct

        Note: A Class Expression in Manchester Syntax will be lazy loaded.
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
                     if x is not None and isinstance(x, OwlEntity)])
                gen = self._realised_parent_classes
                if len(gen) > 0:
                    GENERATED_TYPES[self.name] = type(self.name, tuple(gen), attrs)
                    default = False
            if default:
                GENERATED_TYPES[self.name] = type(self.name, (self._parent_class,), attrs)
            if onto.base_prefix != self.prefix:
                p = self.get_full_iri(onto)
                self.actualized_entity.iri = p
            self.actualize_assertions(GENERATED_TYPES[self.name])
            self._sync_description()
            return GENERATED_TYPES[self.name]

    def _sync_description(self):
        """
        Internally synchronizes with the `owlready2` representation of this Class
        """
        self.actualized_entity.equivalent_to = self.equivalent_classes
