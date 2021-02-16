"""Array constraints."""
from jsonvl.utilities.venum import Venum


class ArrayConstraints(Venum):
    """Constraints applied to array types."""

    MAX_SIZE = 'max_size'
    MIN_SIZE = 'min_size'
    UNIQUE = 'unique'
