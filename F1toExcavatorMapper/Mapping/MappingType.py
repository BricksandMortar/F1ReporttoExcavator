from enum import Enum


class MappingType(Enum):
    # Complex attributes have a ComplexMappingType
    none = 0,
    id = 1,
    simple = 2,
    attribute = 3,
    complex = 4
