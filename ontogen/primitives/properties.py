from typing import Dict, List, Type, Any

from owlready2 import ObjectProperty, Thing

from ontogen import Ontology
from ontogen.base import _get_equivalent_classes
from ontogen.base.namespaces import RDF_TYPE
from ontogen.internal import CHARACTERISTICS_MAPPING
from ontogen.primitives.base import OwlProperty


class OwlObjectProperty(OwlProperty):
    name = "ObjectProperty"
    _parent_class = ObjectProperty

    def __init__(self, name: str):
        super().__init__(name)
        self._range: Dict["OwlClass"] = []
        self._characteristics: List[str] = []
        self._realised_parent_classes.append(ObjectProperty)

    def _get_generated_class(self, onto: Ontology, **attrs) -> Type[Thing]:
        u = [CHARACTERISTICS_MAPPING.get(c, None) for c in self._characteristics]
        if self.inverse_prop is not None:
            attrs['inverse_property'] = self.get_generated_inverse(onto)
        if len(u) > 0:
            self._realised_parent_classes.extend(u)
        return super(OwlObjectProperty, self)._get_generated_class(onto, **attrs)

    def _get_generated(self, onto: Ontology, classes: list):
        return [x._get_generated_class(onto) for x in classes if x is not None]

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

    def from_dict(self, sub: Dict[str, Any]):
        super(OwlObjectProperty, self).from_dict(sub)
        self._characteristics = sub.get(RDF_TYPE, [])
