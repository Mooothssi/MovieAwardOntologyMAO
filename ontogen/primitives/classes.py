from typing import List, Dict, Union
import datetime

from ontogen.base.assertable import OwlAssertable
from ontogen.base.namespaces import RDF_TYPE
from ontogen.base.vars import GENERATED_TYPES
from ontogen.primitives.base import OwlEntity, ENTITIES, check_restrictions
from ontogen.primitives.errors import OntologyConsistencyError
from ontogen.primitives.properties import OwlObjectProperty, OwlDataProperty
from ontogen.utils.basics import assign_optional_dct, shorten_entity_name


class OwlClass(OwlEntity):
    """
        A class for ontology classes of instances
    """

    def __repr__(self) -> str:
        return f"OwlClass<{self.name_with_prefix}>"

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
    """An Individual of Ontology classes
    """

    def __init__(self, name: str, classes: List[OwlClass] = None):
        """Instantiates an ``OwlIndividual``

        Args:
            name: A given name literal with a required prefix
        """
        super(OwlIndividual, self).__init__(name)
        if classes:
            self.onto_types = classes
        else:
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

    def _prepare_assertion_value(self, prop_name: str, value: Union[List, str]) -> Union[List[object], object]:
        val = value
        if isinstance(value, list):
            if prop_name in self.all_defined_properties:
                prop = self.all_defined_properties[prop_name]
                if isinstance(prop, OwlObjectProperty) and (
                        'owl:FunctionalProperty' in prop._characteristics
                        or 'owl:InverseFunctionalProperty' in prop._characteristics):
                    return self._prepare_assertion_value(prop_name, value[0])
            return [self._prepare_assertion_value(prop_name, v) for v in value]
        else:
            if isinstance(val, str) and prop_name in self.all_defined_properties:
                prop = self.all_defined_properties[prop_name]
                if not prop:
                    return value
                if isinstance(prop, OwlObjectProperty):
                    n = shorten_entity_name(value)
                    if n in GENERATED_TYPES:
                        return GENERATED_TYPES[n]
                elif isinstance(prop, OwlDataProperty):
                    r = prop.range[0]
                    if r == datetime.datetime:
                        try:
                            return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                        except ValueError:
                            raise ValueError(f'{self.name_with_prefix} has invalid value {value}')
                    return value
            raise OntologyConsistencyError(f'{prop_name} is not declared in the specs')

    @property
    def all_defined_properties(self) -> Dict[str, OwlObjectProperty]:
        dct = {}
        for t in self.onto_types:
            dct.update(t.defined_properties)
        return dct

    def _assert_restrictions(self, types: List[str], value):
        if not check_restrictions(self.prefix, types, value):
            raise AssertionError("The added value doesn't match the range restriction!")

    def to_dict(self) -> dict:
        dct = {}
        assign_optional_dct(dct, RDF_TYPE, [cls.name for cls in self.onto_types])
        assign_optional_dct(dct, 'relations', {prop: [self.properties_values[prop]] for prop in self.properties_values})
        return dct
