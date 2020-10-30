from dataclasses import dataclass

from .base import BaseModel


@dataclass(eq=False)
class Commodity(BaseModel):
    _instances = []
    fields = (
        ('Commodity Key', None, 'int'),
        ('HS Code', None, 'nvarchar(6)'),
        ('Description', None, 'nvarchar(511)'),
        ('Package Size (m^3)', 'package_size', 'decimal(18,3)'),
        ('Package Weight (kg)', 'package_weight', 'decimal(18,3)'),
        # ('Densities (kg/m^3)', 'densities'),
    )

    hs_code: str
    # String/NULL
    description: str = None
    package_size: float = None
    package_weight: float = None
    densities: float = None

    @property
    def commodity_key(self) -> int:
        return self.key
