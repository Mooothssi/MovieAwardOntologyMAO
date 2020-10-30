from typing import List
from dataclasses import dataclass, field

from .base import BaseModel
from .address import Address


@dataclass(eq=False)
class BusinessEntity(BaseModel):
    _instances = []
    fields = (
        ('Business Entity Key', None, 'int'),
        ('Name', None, 'nvarchar(255)'),
        ('E-mail', 'email', 'nvarchar(255)'),
        ('Phone', None, 'nvarchar(30)'),
        ('Fax', None, 'nvarchar(30)'),
        ('Address Key', None, 'int'),
        ('Roles', None, None),
    )

    name: str = None
    email: str = None
    phone: str = None
    fax: str = None
    address_key: int = None
    roles: List[str] = field(default_factory=list)

    @property
    def business_entity_key(self) -> int:
        return self.key

    @property
    def address(self) -> Address:
        return Address.get_instance_by_key(self.address_key)
