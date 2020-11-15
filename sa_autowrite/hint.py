from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.schema import Table


class DeclaredModel(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def _sa_class_manager(self) -> Dict[str, InstrumentedAttribute]:
        pass

    @property
    @abstractmethod
    def __tablename__(self) -> str:
        pass

    @property
    @abstractmethod
    def __table__(self) -> Table:
        pass
