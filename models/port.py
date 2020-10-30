from dataclasses import dataclass
from typing import ClassVar, List, Sequence

from location import Location

from .base import BaseModel
from .address import Address


@dataclass(eq=False)
class Port(BaseModel):
    _instances: ClassVar[List['Port']] = []
    fields: ClassVar[Sequence[str]] = (
        ('Port Key', None, 'int'),
        ('Address Key', None, 'int'),
        ('Port Name', None, 'nvarchar(255)'),
        ('Port Type', None, 'nvarchar(255)'),
        ('Port Size', None, 'nvarchar(255)'),
        ('Phone', None, 'nvarchar(30)'),
        ('Fax', None, 'nvarchar(30)'),
        ('800 Number', '_800_number', 'nvarchar(30)'),
        ('UN/LOCODE', 'un_locode', 'nvarchar(5)'),
        ('Email', None, 'nvarchar(255)'),
        ('Website', None, 'nvarchar(255)'),
    )

    address_key: int
    port_name: str = None
    port_type: str = None
    port_size: str = None
    phone: str = None
    fax: str = None
    _800_number: str = None
    un_locode: str = None
    email: str = None
    website: str = None

    def __post_init__(self):
        if self.un_locode is not None:
            self.un_locode = self.un_locode.strip()
            if len(self.un_locode) > 5:
                self.un_locode = None
        if self.phone is not None:
            self.phone = ''.join(c for c in self.phone if c in '0123456789+() ')
        if self.fax is not None:
            self.fax = ''.join(c for c in self.fax if c in '0123456789+() ')

    @property
    def port_key(self) -> int:
        return self.key

    @property
    def address(self) -> Address:
        return Address.get_instance_by_key(self.address_key)

    @property
    def location(self) -> Location:
        return self.address.location
