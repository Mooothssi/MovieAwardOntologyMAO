from owlready2 import locstr

from .vars import BUILTIN_NAMES, DATATYPE_MAP


class OwlAnnotatable:
    def __init__(self):
        self.properties_values = {}

    def actualize_annotations(self, inst):
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
            if ":" in set_prop:
                set_prop = set_prop.split(":")[1]
            try:
                if isinstance(val, list):
                    setattr(inst, set_prop, val)
                else:
                    setattr(inst, set_prop, [val])
            except AttributeError:
                pass
