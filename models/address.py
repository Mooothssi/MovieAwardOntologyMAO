from dataclasses import dataclass


from location import Location

from .base import BaseModel


@dataclass(eq=False)
class Address(BaseModel):
    _instances = []
    fields = (
        ('Address Key', None, 'int'),
        'Address Line 1',
        'Address Line 2',
        'City',
        'Country',
        ('Alpha 2', None, 'nvarchar(2)'),
        ('ZIP Code', None, 'nvarchar(30)'),
        ('Latitude', None, 'nvarchar(30)'),
        ('Longitude', None, 'nvarchar(30)'),
    )

    address_line_1: str = None
    address_line_2: str = None
    city: str = None
    country: str = None
    alpha_2: str = None
    zip_code: str = None
    latitude: str = None
    longitude: str = None

    def __post_init__(self):
        if self.address_line_1:
            self.address_line_1 = self.address_line_1.strip()
        if self.address_line_2:
            self.address_line_2 = self.address_line_2.strip()
        if self.city:
            self.city = self.city.strip()
        self.country = self.country.strip()
        self.alpha_2 = self.alpha_2.strip()
        if self.zip_code:
            self.zip_code = self.zip_code.strip()
        if self.latitude:
            self.latitude = self.latitude.strip()
        if self.longitude:
            self.longitude = self.longitude.strip()

    @property
    def address_key(self) -> int:
        return self.key

    @property
    def location(self) -> Location:
        return Location(self.latitude, self.longitude)