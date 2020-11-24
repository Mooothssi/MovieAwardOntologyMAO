import re
from typing import Union, List, Any, Dict, Optional

from owlready2 import locstr

from .namespaces import ANNOTATIONS_KEY
from .vars import DATATYPE_MAP, LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME
from .vars import BUILTIN_DATA_TYPES
from ontogen.utils.basics import absolutize_entity_name, shorten_entity_name


class OwlAssertable:
    def __init__(self):
        self.properties_values: Dict[str, Any] = {}
        self.annotations: Dict[str, Any] = {}

    @property
    def properties_with_values(self) -> dict:
        new_dct = dict(self.properties_values)
        new_dct.update(self.annotations)
        return new_dct

    def actualize_assertions(self, inst):
        for set_prop in self.properties_with_values:
            v = self.properties_with_values[set_prop]
            if isinstance(v, list):
                val = [self._prepare_assertion_value(set_prop, val) for val in v]
            else:
                val = self._prepare_assertion_value(set_prop, v)
            if isinstance(val, list):
                # set_prop in BUILTIN_NAMES and
                for i, v in enumerate(val):
                    v: str
                    if "^^" in v or "@" in v:
                        split_values = re.split(r'(?:(.+)\^\^(.+)@(.+)|(.+)\^\^(.+))', v)
                        if len(split_values) > 2 and split_values[1] is not None:
                            lit, lang = (split_values[1], split_values[3])
                            val[i] = locstr(lit, lang)
                        else:
                            v, data_type = (split_values[4], split_values[5])
                            val[i] = DATATYPE_MAP[data_type](v)
            if ":" in set_prop:
                set_prop = shorten_entity_name(set_prop)
            try:
                if isinstance(val, list):
                    setattr(inst, set_prop, val)
                else:
                    setattr(inst, set_prop, [val])
            except AttributeError:
                pass

    def _prepare_assertion_value(self, set_prop: str, values: Union[List, Any]) -> object:
        return values

    def add_property_assertion(self, property_name: str, value: BUILTIN_DATA_TYPES, dct: Optional[Dict] = None):
        """Adds a property assertion to an ``OwlAssertable`` entity

        Args:
            dct: A given dictionary
            property_name: The name of a given property
            value:  A given value to be associated with a property with the given name

        Returns:
            None
        """
        if value is None:
            return
        if not (":" in property_name and len(property_name.split(":")) == 2):
            raise AssertionError("Please add prefix.")
        if dct is None:
            dct = self.properties_values
        if property_name not in dct:
            dct[property_name] = []
        dct[property_name] += [value]

    def add_annotation(self, property_name: str, value: BUILTIN_DATA_TYPES):
        """Adds an annotation to an ``OwlAssertable`` entity

        Args:
            property_name: The name of a given property
            value:  A given value to be associated with a property with the given name

        Returns:
            None
        """
        self.add_property_assertion(property_name, value, self.annotations)
        # if value is None:
        #     return
        # if not (":" in property_name and len(property_name.split(":")) == 2):
        #     raise AssertionError("Please add prefix.")
        # if property_name not in self.properties_values:
        #     self.properties_values[property_name] = []
        # self.properties_values[property_name] += [value]

    def retrieve_property(self, builtin_name: str, obj, prefix):
        val = getattr(obj, builtin_name)
        self.add_property_assertion(absolutize_entity_name(builtin_name, prefix), val)

    def add_label(self, value: BUILTIN_DATA_TYPES):
        """Add a rdfs:label AnnotationProperty with a given value of supported types

        Args:
            value: A given label. Can be a `str` or `locstr` (Literal with a language)

        Returns:
            None
        """
        self.add_property_assertion(LABEL_ENTITY_NAME, value)

    def add_comment(self, value: BUILTIN_DATA_TYPES):
        """Add a rdfs:comment AnnotationProperty with a given value of supported types

        Args:
            value: A given label. Can be a `str` or `locstr` (Literal with a language)

        Returns:
            None
        """
        self.add_property_assertion(COMMENT_ENTITY_NAME, value)

    def from_dict(self, sub: dict):
        annotations = sub.get(ANNOTATIONS_KEY, {})
        for prop_name, prop_values in annotations.items():
            for value in prop_values:
                self.add_annotation(prop_name, value)
