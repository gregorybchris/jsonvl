"""Value enumeration used to check for enum membership."""
from enum import Enum, unique


@unique
class Venum(Enum):
    """Value enumeration used to check for enum membership."""

    @classmethod
    def has(cls, value: str) -> bool:
        """
        Check whether the enum has a given value.

        :param value: Data value to check for enum membership.
        :return: True if the value is in the enum, otherwise False.
        """
        return value in [v.value for v in cls.__members__.values()]
