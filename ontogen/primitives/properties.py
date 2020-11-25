from typing import Dict, List, Any

from ontogen.base.namespaces import RDF_TYPE
from ontogen.primitives.base import OwlProperty


class OwlObjectProperty(OwlProperty):
    name = "ObjectProperty"

    def __init__(self, name: str):
        super().__init__(name)
        self._range: Dict["OwlClass"] = []
        self._characteristics: List[str] = []

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
