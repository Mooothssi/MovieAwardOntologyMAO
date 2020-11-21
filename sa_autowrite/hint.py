from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.schema import Table


class DeclaredModel(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs): ...

    @property
    @classmethod
    @abstractmethod
    def _sa_class_manager(self) -> Dict[str, InstrumentedAttribute]: ...

    @property
    @classmethod
    @abstractmethod
    def __tablename__(self) -> str: ...

    @property
    @classmethod
    @abstractmethod
    def __table__(self) -> Table: ...

    @abstractmethod
    def __call__(self, *args, **kwargs) -> 'DeclaredModel': ...
