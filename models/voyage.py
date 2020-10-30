from datetime import date, datetime, timedelta
from typing import List, ClassVar, Sequence, Tuple, Iterable
import random
from dataclasses import dataclass, field

import numpy as np

from .base import BaseModel
from .port import Port
from .vehicle import Vehicle

from utils import km_to_mile, pairwise
from jsoncompat import Date, TimeDelta


@dataclass(eq=False)
class Leg(BaseModel):
    _instances = []
    fields = (
        ('Leg Key', None, 'int'),
        ('Origin Port Key', None, 'int'),
        ('Destination Port Key', None, 'int'),
        ('Leg Miles', None, 'decimal(19,2)'),
    )

    origin_port_key: int
    destination_port_key: int

    @property
    def leg_key(self) -> int:
        return self.key

    @property
    def origin_port(self) -> Port:
        return Port.get_instance_by_key(self.origin_port_key)

    @property
    def destination_port(self) -> Port:
        return Port.get_instance_by_key(self.destination_port_key)

    @property
    def leg_kms(self) -> float:
        d = self.origin_port.location.calculate_distance(self.destination_port.location)
        # assert d > 0
        return d

    @property
    def leg_miles(self) -> float:
        return round(km_to_mile(self.leg_kms), 2)

    def get_expected_time(self, vehicle: Vehicle) -> timedelta:
        try:
            time = timedelta(hours=self.leg_kms / vehicle.vehicle_speed_kmh)
            assert time > timedelta(0)
            return time
        except TypeError:
            return timedelta(hours=self.leg_kms / 20)

    def get_expected_fees(self, vehicle: Vehicle) -> float:
        return self.get_expected_time(vehicle).days * vehicle.vehicle_fuel_usage_per_day * 400

    @classmethod
    def get_or_create_instance_from_port_pair(cls, origin_port: Port, destination_port: Port) -> 'Leg':
        # print(cls.instances)
        for instance in cls._instances:
            if instance.origin_port_key == origin_port.port_key and instance.destination_port_key == destination_port.port_key:
                return instance
        return Leg(origin_port_key=origin_port.key, destination_port_key=destination_port.key)


def legs_to_ports(legs: Sequence[Leg]) -> List[Port]:
    ports = [legs[0].origin_port]
    for leg in legs:
        ports.append(leg.destination_port)
    return ports


def ports_to_legs(ports: Iterable[Port]) -> List[Leg]:
    return [
        Leg.get_or_create_instance_from_port_pair(origin, destination)
        for origin, destination in pairwise(ports)
    ]


@dataclass(eq=False)
class LegBridge(BaseModel):
    _instances: ClassVar[List['LegBridge']] = []
    fields = (
        ('Order', 'key', 'int'),
        'Leg Bridge Key',
        'Leg Key',
    )
    has_identity = False

    leg_bridge_key: int
    leg_key: int

    @classmethod
    def _create_new_bridge_from_legs(cls, legs: Iterable[Leg]) -> int:
        """
        Returns leg_bridge_key of the LegBridge created.
        """
        try:
            leg_bridge_key = cls._instances[-1].leg_bridge_key + 1
        except IndexError:
            # cls.instances == []
            leg_bridge_key = 1
        for leg in legs:
            cls(leg_bridge_key=leg_bridge_key, leg_key=leg.key)
        return leg_bridge_key

    @classmethod
    def get_or_create_new_bridge_from_legs(cls, legs: Iterable[Leg]) -> int:
        """
        Returns leg_bridge_key of the LegBridge created/found.
        """
        goal_leg_keys = set(leg.key for leg in legs)
        leg_keys = set()
        leg_brdige_key = None
        for instance in cls._instances:
            if leg_brdige_key is None:
                leg_brdige_key = instance.leg_bridge_key
            if instance.leg_bridge_key == leg_brdige_key:
                leg_keys.add(instance.leg_key)
            else:
                if leg_keys == goal_leg_keys:
                    return leg_brdige_key
                leg_brdige_key = None
        return cls._create_new_bridge_from_legs(legs)

    @classmethod
    def get_legs(cls, leg_bridge_key: int) -> List[Leg]:
        leg_keys = []
        for instance in cls._instances:
            if instance.leg_bridge_key == leg_bridge_key:
                leg_keys.append(instance.leg_key)
            elif leg_keys:
                break
        else:
            if not leg_keys:
                raise ValueError(f"No LegBridge with key '{leg_bridge_key} found'")
        return list(map(Leg.get_instance_by_key, leg_keys))


@dataclass(eq=False)
class Voyage(BaseModel):
    _instances = []
    fields = (
        ('Voyage Key', None, 'int'),
        'Leg Bridge Key',
        ('Origin Port Key', None, 'int'),
        ('Destination Port Key', None, 'int'),
    )

    leg_bridge_key: int = None

    @property
    def voyage_key(self) -> int:
        return self.key

    @property
    def legs(self) -> List[Leg]:
        return LegBridge.get_legs(self.leg_bridge_key)

    @legs.setter
    def legs(self, legs: List[Leg]):
        self.leg_bridge_key = LegBridge.get_or_create_new_bridge_from_legs(legs)

    @classmethod
    def get_or_create_instance_from_ports(cls, ports: Sequence[Port]):
        for instance in cls._instances:
            if instance.ports == ports:
                return instance
        leg_bridge_key = LegBridge.get_or_create_new_bridge_from_legs(ports_to_legs(ports))
        return cls(leg_bridge_key=leg_bridge_key)

    @property
    def ports(self) -> List[Port]:
        return legs_to_ports(self.legs)

    @ports.setter
    def ports(self, ports: List[Port]):
        self.leg_bridge_key = LegBridge.get_or_create_new_bridge_from_legs(ports_to_legs(ports))

    @property
    def origin_port_key(self) -> int:
        return self.ports[0].key

    @property
    def destination_port_key(self) -> int:
        return self.ports[-1].key

    @property
    def origin_port(self) -> Port:
        return self.ports[0]

    @property
    def destination_port(self) -> Port:
        return self.ports[-1]

    def get_expected_total_time(self, vehicle: Vehicle) -> timedelta:
        total_time = timedelta()
        for leg in self.legs:
            total_time += leg.get_expected_time(vehicle)
        return total_time


@dataclass(eq=False)
class LegSchedule(BaseModel):
    _instances = []
    fields = (
        ('Leg Schedule Key', None, 'int'),
        'Leg Key',
        'Origin Port Scheduled Departure Date',
        'Destination Port Scheduled Arrival Date',
        'Origin Port Actual Departure Date',
        'Destination Port Actual Arrival Date',
    )

    leg_key: int = None
    origin_port_scheduled_departure_date: Date = None
    destination_port_scheduled_arrival_date: Date = None
    origin_port_actual_departure_date: Date = None
    destination_port_actual_arrival_date: Date = None

    @property
    def leg_schedule_key(self) -> int:
        return self.key

    @property
    def leg(self) -> Leg:
        return Leg.get_instance_by_key(self.leg_key)

    @property
    def departure_delay(self) -> timedelta:
        return self.origin_port_actual_departure_date - self.origin_port_scheduled_departure_date

    @property
    def arrival_delay(self) -> timedelta:
        return self.destination_port_actual_arrival_date - self.destination_port_scheduled_arrival_date

    def get_actual_time(self) -> timedelta:
        return self.destination_port_actual_arrival_date - self.origin_port_actual_departure_date

    def get_fees(self, vehicle: Vehicle) -> float:
        if self.destination_port_actual_arrival_date is not None:
            if self.origin_port_actual_departure_date is not None:
                return round((
                                         self.destination_port_actual_arrival_date - self.origin_port_actual_departure_date).days * vehicle.vehicle_fuel_usage_per_day * 200,
                             2)
        return round((
                                 self.destination_port_scheduled_arrival_date - self.origin_port_scheduled_departure_date).days * vehicle.vehicle_fuel_usage_per_day * 200,
                     2)


@dataclass(eq=False)
class LegScheduleBridge(BaseModel):
    _instances: ClassVar[List['LegScheduleBridge']] = []
    fields: ClassVar[Sequence['fields']] = (
        # ('Surrogate Key', 'key'),
        'Leg Schedule Bridge Key',
        'Leg Schedule Key',
    )
    has_identity = False

    leg_schedule_bridge_key: int
    leg_schedule_key: int

    @classmethod
    def _create_new_bridge_from_leg_schedules(cls, leg_schedules: Sequence[LegSchedule]) -> int:
        """
        Returns leg_schedule_bridge_key of the LegBridge created.
        """
        try:
            leg_schedule_bridge_key = cls._instances[-1].leg_schedule_bridge_key + 1
        except IndexError:
            # cls.instances == []
            leg_schedule_bridge_key = 1
        for leg_schedule in leg_schedules:
            # print('hi')
            cls(leg_schedule_bridge_key, leg_schedule.key)
        # print(cls._instances, 'ha')
        return leg_schedule_bridge_key

    @classmethod
    def get_or_create_new_bridge_from_leg_schedules(cls, leg_schedules: Sequence[LegSchedule]) -> int:
        """
        Returns leg_schedule_bridge_key of the LegBridge created/found.
        """
        # print('asd')
        goal_leg_schedule_keys = set(leg_schedule.leg_schedule_key for leg_schedule in leg_schedules)
        leg_schedule_keys = set()
        leg_schedule_bridge_key = None
        for instance in cls._instances:
            # print('ho')
            # instance: LegScheduleBridge
            if leg_schedule_bridge_key is None:
                leg_schedule_bridge_key = instance.leg_schedule_bridge_key
            if instance.leg_schedule_bridge_key == leg_schedule_bridge_key:
                leg_schedule_keys.add(instance.leg_schedule_key)
            else:
                if leg_schedule_keys == goal_leg_schedule_keys:
                    return leg_schedule_bridge_key
                leg_schedule_bridge_key = instance.leg_schedule_bridge_key
                leg_schedule_keys = set()
        return cls._create_new_bridge_from_leg_schedules(leg_schedules)

    @classmethod
    def get_leg_schedules(cls, leg_schedule_bridge_key: int) -> List[LegSchedule]:
        leg_schedule_keys = []
        for instance in cls._instances:
            if instance.leg_schedule_bridge_key == leg_schedule_bridge_key:
                leg_schedule_keys.append(instance.leg_schedule_key)
            elif leg_schedule_keys:
                break
        else:
            if not leg_schedule_keys:
                raise ValueError(f"No Leg Schedule Bridge with key {leg_schedule_bridge_key} found/")
        return list(map(LegSchedule.get_instance_by_key, leg_schedule_keys))


@dataclass(eq=False)
class VoyageSchedule(BaseModel):
    _instances = []
    fields = (
        ('Voyage Schedule Key', None, 'int'),
        ('Voyage Key', None, 'int'),
        'Leg Schedule Bridge Key',
    )

    leg_schedule_bridge_key: int = None

    @property
    def voyage_schedule_key(self) -> int:
        return self.key

    @property
    def voyage(self) -> Voyage:
        return Voyage.get_or_create_instance_from_ports(legs_to_ports(self.legs))

    @property
    def voyage_key(self) -> int:
        return self.voyage.key

    @property
    def legs(self) -> List[Leg]:
        return [leg_schedule.leg for leg_schedule in self.leg_schedules]

    @property
    def ports(self) -> List[Port]:
        return self.voyage.ports

    @property
    def leg_schedules(self) -> List[LegSchedule]:
        return LegScheduleBridge.get_leg_schedules(self.leg_schedule_bridge_key)

    @leg_schedules.setter
    def leg_schedules(self, leg_schedules: List[LegSchedule]):
        self.leg_schedule_bridge_key = LegScheduleBridge.get_or_create_new_bridge_from_leg_schedules(leg_schedules)

    @property
    def scheduled_departure_date(self):
        return self.leg_schedules[0].origin_port_scheduled_departure_date

    @scheduled_departure_date.setter
    def scheduled_departure_date(self, scheduled_departure_date: date):
        self.leg_schedules[0].origin_port_scheduled_departure_date = scheduled_departure_date
        # print('Please cascade scheduled date', self)

    def cascade_scheduled_date(self, vehicle: Vehicle):
        first_ls = self.leg_schedules[0]
        first_ls.destination_port_scheduled_arrival_date = first_ls.origin_port_scheduled_departure_date + first_ls.leg.get_expected_time(vehicle)
        for ls1, ls2 in pairwise(self.leg_schedules):
            expected_delay = TimeDelta(days=int(np.random.poisson(1.5, 1)))
            ls2.origin_port_scheduled_departure_date = ls1.destination_port_scheduled_arrival_date + expected_delay
            ls2.destination_port_scheduled_arrival_date = ls2.origin_port_scheduled_departure_date + ls2.leg.get_expected_time(vehicle)

            if not ls1.destination_port_scheduled_arrival_date >= ls1.origin_port_scheduled_departure_date:
                raise AssertionError(f'{ls2.destination_port_scheduled_arrival_date=} {ls1.origin_port_scheduled_departure_date=} {ls1.leg.get_expected_time(vehicle)=} {ls1.leg.leg_miles=} {ls1.leg.origin_port=} {ls1.leg.destination_port=}')
            if not ls2.destination_port_scheduled_arrival_date >= ls2.origin_port_scheduled_departure_date:
                raise AssertionError(f'{ls2.origin_port_scheduled_departure_date=} {ls2.destination_port_scheduled_arrival_date=} {expected_delay=}')

    @property
    def scheduled_arrival_date(self):
        return self.leg_schedules[-1].destination_port_scheduled_arrival_date

    @scheduled_arrival_date.setter
    def scheduled_arrival_date(self, scheduled_arrival_date: date):
        self.leg_schedules[-1].destination_port_scheduled_arrival_date = scheduled_arrival_date
        # print('Please cascade actual date', self)

    @staticmethod
    def get_delays() -> Tuple[TimeDelta, TimeDelta, TimeDelta, TimeDelta]:
        travel_delay = np.random.exponential(0.05, 1)
        travel_delay = TimeDelta(days=int(travel_delay))
        port_delay = np.random.poisson(1.5, 1)
        port_delay = TimeDelta(days=int(port_delay))

        if random.random() <= 0.05:
            accidental_delay = np.random.poisson(10, 1)
        else:
            accidental_delay = 0
        accidental_delay = TimeDelta(days=int(accidental_delay))
        if random.random() <= 0.1:
            accidental_port_delay = np.random.poisson(4, 1)
        else:
            accidental_port_delay = 0
        accidental_port_delay = TimeDelta(days=int(accidental_port_delay))
        # assert travel_delay >= timedelta(0)
        # assert port_delay >= timedelta(0)
        # assert accidental_delay >= timedelta(0)
        # assert accidental_port_delay >= timedelta(0)
        return travel_delay, port_delay, accidental_delay, accidental_port_delay

    def cascade_actual_date(self, vehicle: Vehicle):
        """
        Randomize the Actual date for both Arrival and Departure dates.
        """
        travel_delay, port_delay, accidental_delay, accidental_port_delay = self.get_delays()
        first_ls = self.leg_schedules[0]
        first_ls.origin_port_actual_departure_date = first_ls.origin_port_scheduled_departure_date + port_delay + accidental_port_delay
        first_ls.destination_port_actual_arrival_date = first_ls.origin_port_actual_departure_date + first_ls.leg.get_expected_time(vehicle) + travel_delay + accidental_delay
        for ls1, ls2 in pairwise(self.leg_schedules):
            travel_delay, port_delay, accidental_delay, accidental_port_delay = self.get_delays()
            ls2.origin_port_actual_departure_date = ls1.destination_port_actual_arrival_date + port_delay + accidental_port_delay
            ls2.destination_port_actual_arrival_date = ls2.origin_port_actual_departure_date + ls2.leg.get_expected_time(
                vehicle) + travel_delay + accidental_delay

            assert ls1.destination_port_actual_arrival_date >= ls1.origin_port_actual_departure_date
            assert ls2.destination_port_actual_arrival_date >= ls2.origin_port_actual_departure_date

    @property
    def actual_departure_date(self):
        return self.leg_schedules[0].origin_port_actual_departure_date

    @property
    def actual_arrival_date(self):
        return self.leg_schedules[-1].destination_port_actual_arrival_date

    @classmethod
    def create_voyage_schedule_from_ports(cls, ports: List[Port]) -> 'VoyageSchedule':
        # get/create leg
        legs = ports_to_legs(ports)
        # create leg schedules
        leg_schedules = [LegSchedule(leg.key) for leg in legs]
        # create leg schedule bridge
        leg_schedule_bridge = LegScheduleBridge.get_or_create_new_bridge_from_leg_schedules(leg_schedules)
        return VoyageSchedule(leg_schedule_bridge)

    def get_fees(self, vehicle: Vehicle) -> float:
        return sum(ls.get_fees(vehicle) for ls in self.leg_schedules)
