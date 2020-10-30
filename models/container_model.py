from dataclasses import dataclass

from .base import BaseModel


@dataclass(eq=False)
class ContainerModel(BaseModel):
    _instances = []
    fields = (
        ('Container Model Key', None, 'int'),
        ('ISO Size Code', None, 'nvarchar(2)'),
        ('ISO Type Code', None, 'nvarchar(2)'),
        ('Model Description', None, 'nvarchar(255)'),
        ('Owner Code', None, 'nvarchar(4)'),
        ('Serial Number Range Start', None, 'int'),
        ('Serial Number Range End', None, 'int'),
        ('Inside Length (mm)', None, 'int'),
        ('Inside Width (mm)', None, 'int'),
        ('Inside Height (mm)', None, 'int'),
        ('Inside Middle Height (mm)', None, 'int'),
        ('Inside Side Height (mm)', None, 'int'),
        ('Max stow Height', None, 'int'),
        ('Roof Opening Length (mm)', None, 'int'),
        ('Roof Opening Width (mm)', None, 'int'),
        ('Door Opening Width (mm)', None, 'int'),
        ('Door Opening Height (mm)', None, 'int'),
        ('Door Opening Width C (mm)', None, 'int'),
        ('Door Opening Width D (mm)', None, 'int'),
        ('Door Opening Width B (mm)', None, 'int'),
        ('Door Opening Height E (mm)', None, 'int'),
        ('Door Opening Height F (mm)', None, 'int'),
        ('Max Gross Weight (kg)', None, 'int'),
        ('Tare Weight (kg)', None, 'int'),
        ('Max Payload Weight (kg)', None, 'int'),
        ('Capacity (m^3)', 'capacity_cbm', 'decimal(18,3)')
    )

    iso_size_code: str
    iso_type_code: str
    owner_code: str
    model_description: str = ''
    serial_number_range_start: int = None
    serial_number_range_end: int = None
    inside_length_mm: int = None
    inside_width_mm: int = None
    inside_height_mm: int = None
    inside_middle_height_mm: int = None
    inside_side_height_mm: int = None
    max_stow_height: int = None
    roof_opening_length_mm: int = None
    roof_opening_width_mm: int = None
    door_opening_width_mm: int = None
    door_opening_height_mm: int = None
    door_opening_width_c_mm: int = None
    door_opening_width_d_mm: int = None
    door_opening_width_b_mm: int = None
    door_opening_height_e_mm: int = None
    door_opening_height_f_mm: int = None
    max_gross_weight_kg: int = None
    tare_weight_kg: int = None
    max_payload_weight_kg: int = None
    capacity_cbm: float = None

    @property
    def container_model_key(self) -> int:
        return self.key
