from abc import ABCMeta
from typing import List, Union, Dict, Any

from owlready2 import ClassConstruct, locstr

from .assertable import OwlAssertable
from .namespaces import RDFS_SUBCLASS_OF, ANNOTATIONS_KEY, OWL_DISJOINT_WITH, OWL_EQUIVALENT_CLASS, OWL_RESTRICTION
from .vars import BUILTIN_NAMES, DATATYPE_MAP, GENERATED_TYPES, LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME, \
    BUILTIN_DATA_TYPES, ANNO_ATTRS
from ..utils.basics import assign_optional_dct


def _get_equivalent_classes(sub_dict: dict) -> List:
    if OWL_EQUIVALENT_CLASS not in sub_dict:
        return []
    u = sub_dict[OWL_EQUIVALENT_CLASS]
    if isinstance(u, dict):
        return u.get(OWL_RESTRICTION, [])
    else:
        return u


class OwlEntity(OwlAssertable, metaclass=ABCMeta):
    prefix = "owl"
    _internal_dict = {}
    _parent_class = object
    parent_class_names: List[str] = []
    _parent_classes: List["OwlEntity"] = []
    _disjoint_classes: List["OwlEntity"] = []

    def __init__(self, entity_qualifier: str):
        super(OwlEntity, self).__init__()
        self.disjoint_class_names: List[str] = []
        self.properties_values = {}
        self._use_default_prefix = False
        if ":" not in entity_qualifier:
            self._use_default_prefix = True
            raise AssertionError("Must include a prefix")
        pre, n = entity_qualifier.split(":")
        self.prefix = pre
        self.name = n
        self.dependencies = []
        self._parent_classes = []
        self._disjoint_classes = []
        self.equivalent_class_expressions: List[str] = []
        self.equivalent_classes: list = []
        self._realised_parent_classes = []
        self.equivalent_class_expressions = []

    @classmethod
    def get_owl_type_entity_name(cls) -> str:
        return f"{cls.prefix}:{cls.name}"

    @property
    def name_with_prefix(self) -> str:
        return f"{self.prefix}:{self.name}"

    def get_iri(self, onto: 'Ontology'):
        return f"{onto.lookup_iri(self.prefix)}{self.name}"

    def add_superclass(self, superclass: Union["OwlEntity", "str"]):
        """Adds a superclass of this Class.
        This Class will then be an ``rdfs:subclassOf`` a given superclass

        Args:
            superclass: A given Superclass
        """
        if superclass is None:
            return
        self._parent_classes.append(superclass)

    def add_disjoint_class(self, cls: "OwlEntity"):
        """Adds a disjoint class to this Class. The given class will be lazy loaded.

        Args:
            cls: an OntologyEntity
        """
        self._disjoint_classes.append(cls)

    def add_equivalent_class_expression(self, expression: Union[str, ClassConstruct]):
        """Adds an equivalent class to this Class

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

    def add_labels(self, values: List[BUILTIN_DATA_TYPES]):
        for v in values:
            self.add_label(v)

    def add_comments(self, values: List[BUILTIN_DATA_TYPES]):
        for v in values:
            self.add_comment(v)

    @property
    def is_actualized(self) -> bool:
        """Returns whether this Class is saved to an Ontology
        """
        return self.name in GENERATED_TYPES

    def sync(self):
        self.actualize(self.actualized_entity.namespace)

    @property
    def actualized_entity(self):
        if self.is_actualized:
            return GENERATED_TYPES[self.name]
        raise AssertionError("The entity has yet to be actualized")

    def _sync_description(self):
        """Internally synchronizes with the `owlready2` representation of this Class
        """
        self.actualized_entity.equivalent_to = self.equivalent_classes

    def _sanitize(self, val: list) -> list:
        for i, ele in enumerate(val):
            if isinstance(ele, locstr):
                val[i] = f"{ele}^^xsd:string@{ele.lang}"
        return list(val)

    def to_dict(self) -> dict:
        dct = {}
        assign_optional_dct(dct, RDFS_SUBCLASS_OF, [name for name in self.parent_class_names])
        assign_optional_dct(dct, 'annotations', {v: self._sanitize(self.properties_values[v][0]) for v in self.properties_values if v in ANNO_ATTRS})
        return dct

    def from_dict(self, sub: Dict[str, Any]):
        self.disjoint_class_names = sub.get(OWL_DISJOINT_WITH, [])
        self.parent_class_names = sub.get(RDFS_SUBCLASS_OF, [])
        self.equivalent_class_expressions = _get_equivalent_classes(sub)
        super(OwlEntity, self).from_dict(sub)

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name_with_prefix}>"
