from typing import Type

from owlready2 import ObjectProperty, Thing

from ontogen import Ontology
from ontogen.internal import CHARACTERISTICS_MAPPING
from ontogen.primitives.base import OwlProperty
# from ontogen.primitives.classes import OwlThing


class OwlObjectProperty(OwlProperty):
    name = "ObjectProperty"
    # _range = [OwlThing()]
    _parent_class = ObjectProperty
    # _characteristics = ["owl:SymmetricProperty"]

    def __init__(self, name: str):
        super().__init__(name)
        self._range = []
        self._characteristics = []
        self._realised_parent_classes.append(ObjectProperty)
        self.inverse_prop: Type or None = None

    def _get_generated_class(self, onto: Ontology, **attrs) -> Type[Thing]:
        u = [CHARACTERISTICS_MAPPING.get(c, None) for c in self._characteristics]
        if self.inverse_prop is not None:
            attrs['inverse_property'] = self.get_generated_inverse(onto)
        if len(u) > 0:
            self._realised_parent_classes.extend(u)
        return super(OwlObjectProperty, self)._get_generated_class(onto, **attrs)

    def get_generated_range(self, onto: Ontology):
        return [x._get_generated_class(onto) for x in self.range if x is not None]

    def get_generated_inverse(self, onto: Ontology) -> Type:
        self.inverse_prop.inverse_prop = None
        return self.inverse_prop._get_generated_class(onto)

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, a):
        self._range = a
        self.dependencies.extend([b for b in a if not b == "Thing" and b != ""])
