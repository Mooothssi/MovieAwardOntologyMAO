from typing import List, ClassVar
from dataclasses import dataclass

from .base import BaseModel
from .vehicle import Vehicle
from .voyage import VoyageSchedule
from .bill_of_lading import BillOfLading


@dataclass(eq=False)
class Shipment(BaseModel):
    _instances: ClassVar[List['Shipment']] = []
    fields = (
        ('Shipment Key', None, 'int'),
        ('Voyage Schedule Key', None, 'int'),
        ('Vehicle Key', None, 'int'),
        ('Bill-of-Lading Key', None, 'int'),
        ('Voyage Fee', None, 'decimal(19,2)'),
    )

    voyage_schedule_key: int = None
    vehicle_key: int = None
    bill_of_lading_key: int = None

    @property
    def shipment_key(self) -> int:
        return self.key

    @property
    def voyage_schedule(self) -> VoyageSchedule:
        return VoyageSchedule.get_instance_by_key(self.voyage_schedule_key)

    @property
    def vehicle(self) -> Vehicle:
        return Vehicle.get_instance_by_key(self.vehicle_key)

    @vehicle.setter
    def vehicle(self, vehicle: Vehicle):
        self.vehicle_key = vehicle.vehicle_key

    @property
    def bill_of_lading(self) -> BillOfLading:
        return BillOfLading.get_instance_by_key(self.bill_of_lading_key)

    @property
    def voyage_fee(self) -> float:
        if self.vehicle_key is not None:
            return self.voyage_schedule.get_fees(self.vehicle)

    @classmethod
    def get_instances_from_voyage_schedule_key(cls, voyage_schedule_key: int) -> List['Shipment']:
        shipments = []
        for instance in cls._instances:
            instance: Shipment
            if instance.voyage_schedule_key == voyage_schedule_key:
                shipments.append(instance)
        if shipments:
            return shipments
        raise ValueError(f"No shipment with voyage schedule key = '{voyage_schedule_key}' found")
