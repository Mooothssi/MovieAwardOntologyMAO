import re

from owlready2 import locstr

from .vars import BUILTIN_NAMES, DATATYPE_MAP, LABEL_ENTITY_NAME, COMMENT_ENTITY_NAME
from .vars import BUILTIN_DATA_TYPES


class OwlAssertable:
    def __init__(self):
        self.properties_values = {}

    def actualize_assertions(self, inst):
        for set_prop in self.properties_values:
            val = self._prepare_assertion(set_prop)
            if set_prop in BUILTIN_NAMES and isinstance(val, list):
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
                set_prop = set_prop.split(":")[1]
            try:
                if isinstance(val, list):
                    setattr(inst, set_prop, val)
                else:
                    setattr(inst, set_prop, [val])
            except AttributeError:
                pass

    def _prepare_assertion(self, prop_name: str) -> object:
        return self.properties_values[prop_name]

    def _add_builtin_prop(self, builtin_name: str, value: BUILTIN_DATA_TYPES):
        if value is None:
            return
        if builtin_name not in self.properties_values:
            self.properties_values[builtin_name] = []
        self.properties_values[builtin_name] += [value]

    def add_label(self, value: BUILTIN_DATA_TYPES):
        """Add a rdfs:label AnnotationProperty with a given value of supported types

        Args:
            value: A given label. Can be a `str` or `locstr` (Literal with a language)

        Returns:
            None
        """
        self._add_builtin_prop(LABEL_ENTITY_NAME, value)

    def add_comment(self, value: BUILTIN_DATA_TYPES):
        """Add a rdfs:comment AnnotationProperty with a given value of supported types

        Args:
            value: A given label. Can be a `str` or `locstr` (Literal with a language)

        Returns:
            None
        """
        self._add_builtin_prop(COMMENT_ENTITY_NAME, value)
