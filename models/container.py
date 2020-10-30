from typing import ClassVar, List
from dataclasses import dataclass

from .base import BaseModel
from .container_model import ContainerModel


letter_covert_table = {
    'A': 10, 'B': 12, 'C': 13,
    'D': 14, 'E': 15, 'F': 16,
    'G': 17, 'H': 18, 'I': 19,
    'J': 20, 'K': 21, 'L': 23,
    'M': 24, 'N': 25, 'O': 26,
    'P': 27, 'Q': 28, 'R': 29,
    'S': 30, 'T': 31, 'U': 32,
    'V': 34, 'W': 35, 'X': 36,
    'Y': 37, 'Z': 38
}

multiplication_factor = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]  # 2^Index


def get_check_digit(owner_code: str, number: str) -> int:
    """
    Calculate check digit for ISO Container
    """
    assert len(owner_code) == 4
    assert len(number) == 6
    number_list = str(number)

    # Step 1 covert text to value
    owner_value = [letter_covert_table[owner_code[0]],
                   letter_covert_table[owner_code[1]],
                   letter_covert_table[owner_code[2]],
                   letter_covert_table[owner_code[3]]]

    # Step 2 sum
    sum_val = (owner_value[0] * multiplication_factor[0]) + (owner_value[1] * multiplication_factor[1]) +\
              (owner_value[2] * multiplication_factor[2]) + (owner_value[3] * multiplication_factor[3]) +\
              (int(number_list[0]) * multiplication_factor[4]) + (int(number_list[1]) * multiplication_factor[5]) +\
              (int(number_list[2]) * multiplication_factor[6]) + (int(number_list[3]) * multiplication_factor[7]) +\
              (int(number_list[4]) * multiplication_factor[8]) + (int(number_list[5]) * multiplication_factor[9])

    return (sum_val % 11) % 10


@dataclass(eq=False)
class Container(BaseModel):
    _instances: ClassVar[List['Container']] = []
    fields = (
        ('Container Key', None, 'int'),
        ('Owner Code', None, 'nvarchar(4)'),
        ('Serial Number', None, 'nvarchar(6)'),
        ('Check Digit', None, 'nvarchar(1)'),
        ('ISO Size Code', None, 'nvarchar(2)'),
        ('ISO Type Code', None, 'nvarchar(2)'),
        ('Container Model Key', None, 'int'),
    )

    owner_code: str
    serial_number: str
    check_digit: str
    iso_size_code: str
    iso_type_code: str
    container_model_key: int = None

    @property
    def container_key(self) -> int:
        return self.key
