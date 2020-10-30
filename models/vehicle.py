from dataclasses import dataclass

from location import Location
from .base import BaseModel


@dataclass(eq=False)
class Vehicle(BaseModel):
    _instances = []
    fields = (
        ('Vehicle Key', None, 'int'),
        ('Vehicle Speed (km/h)', 'vehicle_speed_kmh', 'decimal(18,3)'),
        ('Vehicle Type', None, 'nvarchar(255)'),
        ('Vehicle Name', None, 'nvarchar(255)'),
        ('Vehicle Capacity', None, 'int'),
        ('Vehicle Builder', None, 'nvarchar(255)'),
        ('Vehicle Fuel Usage per Day', None, 'decimal(18,3)'),
        ('Current Latitude', None, 'nvarchar(30)'),
        ('Current Longitude', None, 'nvarchar(30)'),
        ('IMO Number', None, 'nvarchar(7)'),
    )

    vehicle_speed_kmh: float
    vehicle_type: str = None
    vehicle_name: str = None
    vehicle_capacity: int = None
    vehicle_builder: str = None
    vehicle_fuel_usage_per_day: float = None
    current_latitude: str = None
    current_longitude: str = None
    imo_number: str = None

    def __post_init__(self):
        if self.vehicle_speed_kmh:
            self.vehicle_speed_kmh = round(self.vehicle_speed_kmh, 3)

    @property
    def current_position(self) -> Location:
        return Location(self.current_latitude, self.current_longitude)

    @property
    def vehicle_key(self) -> int:
        return self.key
