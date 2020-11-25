from typing import Dict, List, Any, Type

from ontogen.base import OwlEntity
from ontogen.base.namespaces import RDF_TYPE, RDFS_RANGE, RDFS_DOMAIN, OWL_INVERSE_OF
from ontogen.primitives.base import get_equivalent_datatype


class OwlProperty(OwlEntity):
    prefix = "owl"
    range = [Type[str]]

    def __init__(self, entity_qualifier: str):
        super(OwlProperty, self).__init__(entity_qualifier)
        self.range = []
        self.domain = []
        self.inverse_prop: Type or None = None

    def from_dict(self, sub: Dict[str, Any]):
        super(OwlProperty, self).from_dict(sub)
        self.range = sub.get(RDFS_RANGE, [])
        self.domain = sub.get(RDFS_DOMAIN, [])
        inv = sub.get(OWL_INVERSE_OF, [])
        if len(inv) == 1:
            self.inverse_prop = inv[0]


class OwlDataProperty(OwlProperty):
    name = "DataProperty"
    range = [str]

    def from_dict(self, sub: Dict[str, Any]):
        super().from_dict(sub)
        self.range = [get_equivalent_datatype(datatype) for datatype in sub["rdfs:range"]]


class OwlAnnotationProperty(OwlProperty):
    name = "AnnotationProperty"
    range = [str]


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
