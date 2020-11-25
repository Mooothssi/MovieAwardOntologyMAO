from typing import List, Dict, Union

from ontogen.base.assertable import OwlAssertable
from ontogen.base.namespaces import RDF_TYPE
from ontogen.base.vars import GENERATED_TYPES
from ontogen.utils.basics import absolutize_entity_name
from ontogen.primitives.base import OwlEntity, Ontology, ENTITIES, check_restrictions
from ontogen.primitives.properties import OwlObjectProperty
from ontogen.utils.basics import assign_optional_dct


class OwlClass(OwlEntity):
    """
        A class for ontology classes of instances
    """

    def __repr__(self) -> str:
        return f"OwlClass<{self.prefix}:{self.name}>"

    prefix = "owl"
    name = "Class"
    parent_name = "BaseOntologyClass"
    parent_class_names: List[str] = []

    def __init__(self, entity_name: str):
        super(OwlClass, self).__init__(entity_qualifier=entity_name)
        self.individuals: List[OwlIndividual] = []
        self.defined_properties: Dict[str, "OwlProperty" or None] = dict(ENTITIES)

    # @property
    # def is_actualized(self) -> bool:
    #     """Returns whether this Class is saved to an Ontology
    #     """
    #     return self._actualized_entity is not None
    #
    # @property
    # def actualized_entity(self):
    #     if self.is_actualized:
    #         return self._actualized_entity
    #     raise AssertionError("The entity has yet to be actualized")


class OwlIndividual(OwlEntity, OwlAssertable):
    """
    An Individual of Ontology classes
    """

    def __init__(self, name: str):
        super(OwlIndividual, self).__init__(name)
        self.onto_types: List[OwlClass] = []
        self.defined_properties: Dict[str, "OwlProperty" or None] = dict(ENTITIES)
        self._imp = None
        self.properties_values: Dict[str, ] = {}

    def be_type_of(self, cls: OwlClass):
        """
        Sets the type of this Individual to be of a given Class

        Args:
            cls: A given Class
        """
        cls.individuals.append(self)
        self.onto_types.append(cls)

    def actualize(self, onto: Ontology):
        super().actualize(onto)
        self.onto_types[0].actualize(onto)

    def _get_entity(self, onto: Ontology, relative_name: str) -> object or None:
        name = absolutize_entity_name(relative_name)
        return onto.entities.get(name, None)

    def _prepare_assertion_value(self, prop_name: str, value: Union[List, str]) -> object:
        val = value
        if isinstance(val, str) and prop_name in self.onto_types[0].defined_properties:
            prop = self.onto_types[0].defined_properties[prop_name]
            if isinstance(prop, OwlObjectProperty):
                n = value.split(":")[1]
                if n in GENERATED_TYPES:
                    return GENERATED_TYPES[n]
        return val

    def _assert_restrictions(self, types: List[str], value):
        if not check_restrictions(self.prefix, types, value):
            raise AssertionError("The added value doesn't match the range restriction!")

    def to_dict(self) -> dict:
        dct = {}
        assign_optional_dct(dct, RDF_TYPE, [cls.name for cls in self.onto_types])
        assign_optional_dct(dct, 'relations', {prop: [self.properties_values[prop]] for prop in self.properties_values})
        return dct
