"""String constraints."""
from jsonvl._utilities.venum import Venum


class StringConstraintNames(Venum):
    """Constraints applied to string types."""

    MIN_LENGTH = 'min_length'
    MAX_LENGTH = 'max_length'
    EQ = 'eq'
    IN = 'in'
    FORMAT = 'format'
