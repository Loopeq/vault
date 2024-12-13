from enum import Enum


class StrEnum(str, Enum):
    pass


class UnitTime(StrEnum):
    DAYS = "DAYS"
    WEEKS = "WEEKS"
    MONTHS = "MONTHS"
    YEARS = "YEARS"
