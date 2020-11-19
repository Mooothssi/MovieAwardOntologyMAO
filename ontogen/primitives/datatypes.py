from typing import Type

from owlready2.base import declare_datatype, _universal_abbrev_datatype

from ..base import Ontology, OwlEntity


class Datatype(OwlEntity):
    def __init__(self, n: str):
        super().__init__(n)
        self._data_type: Type = None

    def actualize(self, onto: Ontology) -> 'Datatype':
        declare_datatype(self.data_type, self.get_full_iri(onto), self.to_this, self.to_str)
        _universal_abbrev_datatype(type(self), self.to_this, self.to_str, self.get_full_iri(onto))
        return self

    @property
    def data_type(self):
        return self._data_type if self._data_type is not None else type(self)

    @data_type.setter
    def data_type(self, s: Type):
        self._data_type = s

    @staticmethod
    def to_this(s: str):
        return s

    @staticmethod
    def to_str(s: 'Datatype'):
        return s
