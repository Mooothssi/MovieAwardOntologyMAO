from typing import List, ClassVar, Tuple, Set
from datetime import date
from dataclasses import dataclass
import random

from .address import Address
from .base import BaseModel
from .business_entity import BusinessEntity
from .commodity import Commodity
from .container import Container
from .port import Port

from jsoncompat import Date


def random_incoterm(year: int):
    if year > 2020:
        raise AssertionError('The future is not known!')
    if year == 2020:
        stats = [
            (0.1791044776, 'EXW'),
            (0.2189054726, 'FCA'),
            (0.2487562189, 'CPT'),
            (0.2885572139, 'CIP'),
            (0.3084577114, 'DPU'),
            (0.3980099502, 'DAP'),
            (0.4029850746, 'DDP'),
            (0.4328358209, 'FAS'),
            (0.5820895522, 'FOB'),
            (0.7213930348, 'CFR'),
            (1, 'CIF')
        ]
    elif year >= 2010:
        stats = [
            (0.1791044776, 'EXW'),
            (0.2189054726, 'FCA'),
            (0.2487562189, 'CPT'),
            (0.2885572139, 'CIP'),
            (0.3084577114, 'DAT'),
            (0.3980099502, 'DAP'),
            (0.4029850746, 'DDP'),
            (0.4328358209, 'FAS'),
            (0.5820895522, 'FOB'),
            (0.7213930348, 'CFR'),
            (1, 'CIF')
        ]
    elif year >= 2000:
        stats = [
            (0.1628959276, 'EXW'),
            (0.2081447964, 'FCA'),
            (0.2352941176, 'CPT'),
            (0.2805429864, 'CIP'),
            (0.3167420814, 'DDP'),
            (0.3484162896, 'FAS'),
            (0.4841628959, 'FOB'),
            (0.6244343891, 'CFR'),
            (0.8823529412, 'CIF'),
            (0.9321266968, 'DDU'),
            (0.9547511312, 'DEQ'),
            (0.9773755656, 'DES'),
            (1, 'DAF')
        ]
    else:
        raise AssertionError('Too long ago!')

    r = random.random()
    for cut_off, term in stats:
        if r <= cut_off:
            return term


def get_bol_check_digit(bol_number: str) -> str:
    # Step 1 sum all even index num multiply by 3
    sum_even_mul3 = 0
    for even_index in range(1, 16, 2):
        sum_even_mul3 += int(bol_number[even_index])
    sum_even_mul3 *= 3
    # Step 2 sum all odd index
    sum_odd = 0
    for odd_index in range(0, 15, 2):
        sum_odd += int(bol_number[odd_index])
    # Step 3 get last digit, find the number which round last digit to 0 Ex. 2 + 8 = 1 [0]
    last_dig = int(str(sum_even_mul3 + sum_odd)[-1])
    if not last_dig:
        return str(last_dig)
    return str(10 - last_dig)


@dataclass(eq=False)
class BillOfLading(BaseModel):
    _instances: ClassVar[List['BillOfLading']] = []
    fields = (
        ('Bill-of-Lading Key', None, 'int'),
        ('Bill-of-Lading Number', None, 'nvarchar(17)'),
        ('Issued Date', None, 'date'),
        ('Consignor Key', None, 'int'),
        ('Consignee Key', None, 'int'),
        ('Foreign Transporter Key', None, 'int'),
        ('Foreign Consolidator Key', None, 'int'),
        ('Courier Key', None, 'int'),
        ('Domestic Transporter Key', None, 'int'),
        ('Domestic Consolidator Key', None, 'int'),
        ('Ship Mode', None, 'nvarchar(50)'),
        ('Place of Receipt Key', None, 'int'),
        ('Place of Delivery Key', None, 'int'),
        ('Port of Loading Key', None, 'int'),
        ('Port of Discharge Key', None, 'int'),
        ('Commodity Key', None, 'int'),
        ('Container Key', None, 'int'),
        ('Incoterm', None, 'nvarchar(3)'),
        ('Expected Tariffs', None, 'decimal(19,2)'),
        ('Actual Tariffs', None, 'decimal(19,2)')
    )

    bol_nums: ClassVar[Set[str]] = set()

    bill_of_lading_number: str = None
    issued_date: Date = None
    consignor_key: int = None
    consignee_key: int = None
    foreign_transporter_key: int = None
    foreign_consolidator_key: int = None
    courier_key: int = None
    domestic_transporter_key: int = None
    domestic_consolidator_key: int = None
    ship_mode: str = None
    place_of_receipt_key: int = None
    place_of_delivery_key: int = None
    port_of_loading_key: int = None
    port_of_discharge_key: int = None
    commodity_key: int = None
    container_key: int = None
    incoterm: str = None
    expected_tariffs: float = None
    actual_tariffs: float = None

    def __post_init__(self):
        if self.bill_of_lading_number:
            if self.bill_of_lading_number in self.bol_nums:
                import warnings
                warnings.warn(f"duplicate Bill-of-Lading number: '{self.bill_of_lading_number}' for bol key: '{self.bill_of_lading_key}'")
            self.__class__.bol_nums.add(self.bill_of_lading_number)
        else:
            self.bill_of_lading_number = self.random_bill_of_lading_number()

    @classmethod
    def random_bill_of_lading_number(cls) -> str:
        while True:
            three, four, five = str(random.randint(1, 9)), str(random.randint(1, 9)), str(random.randint(1, 9))
            six, seven, eight = str(random.randint(1, 9)), str(random.randint(1, 9)), str(random.randint(1, 9))
            nine, ten, eleven = str(random.randint(1, 9)), str(random.randint(1, 9)), str(random.randint(1, 9))
            twelve, thirteen, fourteen = str(random.randint(1, 9)), str(random.randint(1, 9)), str(random.randint(1, 9))
            fifteen, sixteen = str(random.randint(1, 9)), str(random.randint(1, 9))
            result = "04" + three + four + five + six + seven + eight + nine + ten + eleven + twelve + thirteen + \
                     fourteen + fifteen + sixteen
            seventeen = get_bol_check_digit(result)
            ans = result + seventeen

            if ans not in cls.bol_nums:
                cls.bol_nums.add(ans)
                return ans

    @property
    def bill_of_lading_key(self) -> int:
        return self.key

    @property
    def consignor(self) -> BusinessEntity:
        return BusinessEntity.get_instance_by_key(self.consignor_key)

    @property
    def consignee(self) -> BusinessEntity:
        return BusinessEntity.get_instance_by_key(self.consignee_key)

    @property
    def foreign_transporter(self) -> BusinessEntity:
        return BusinessEntity.get_instance_by_key(self.foreign_transporter_key)

    @property
    def foreign_consolidator(self) -> BusinessEntity:
        return BusinessEntity.get_instance_by_key(self.foreign_consolidator_key)

    @property
    def courier(self) -> BusinessEntity:
        return BusinessEntity.get_instance_by_key(self.courier_key)

    @property
    def domestic_transporter(self) -> BusinessEntity:
        return BusinessEntity.get_instance_by_key(self.domestic_transporter_key)

    @property
    def domestic_consolidator(self) -> BusinessEntity:
        return BusinessEntity.get_instance_by_key(self.domestic_transporter_key)

    @property
    def place_of_receipt(self) -> Address:
        return Address.get_instance_by_key(self.place_of_receipt_key)

    @property
    def place_of_delivery(self) -> Address:
        return Address.get_instance_by_key(self.place_of_delivery_key)

    @property
    def port_of_loading(self) -> Port:
        return Port.get_instance_by_key(self.port_of_loading_key)

    @property
    def port_of_discharge(self) -> Port:
        return Port.get_instance_by_key(self.port_of_discharge_key)

    @property
    def commodity(self) -> Commodity:
        return Commodity.get_instance_by_key(self.commodity_key)

    @property
    def container(self) -> Container:
        return Container.get_instance_by_key(self.container_key)

    def get_route_str(self) -> str:
        return (
            f"{self.port_of_loading.port_name} [{self.port_of_loading_key}] "
            f"--> {self.port_of_discharge.port_name} [{self.port_of_discharge_key}]"
        )