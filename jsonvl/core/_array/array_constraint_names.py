"""Array constraint names."""
from jsonvl._utilities.venum import Venum


class ArrayConstraintNames(Venum):
    """Constraints applied to array types."""

    MAX_SIZE = 'max_size'
    MIN_SIZE = 'min_size'
    UNIQUE = 'unique'
