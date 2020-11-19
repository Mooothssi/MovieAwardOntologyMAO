from typing import List

from ontogen.primitives.base import OwlClass
from ontogen.base.vars import GENERATED_TYPES


class OwlIndividual:
    """
    Individual rep of ``owl:NamedIndividual``
    """
    def __init__(self, name: str):
        self.name = name
        self.onto_types: List[OwlClass] = []
        self._imp = None

    def be_type_of(self, t: OwlClass):
        t.indivs.append(self)
        self.onto_types.append(t)

    # GENERATED_TYPES
    # TODO: GENERATED_ENTITIES #
    def actualize(self):
        """
        ...
        """
        if self._imp:
            return
            # raise AssertionError("Already actualized")
        inst = self.onto_types[0].actualized_entity()
        inst.name = self.name.split(":")[1]
        GENERATED_TYPES[self.name] = inst
        self._imp = inst
