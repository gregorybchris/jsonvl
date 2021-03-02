"""Number constraint names."""
from jsonvl._utilities.venum import Venum


class NumberConstraintNames(Venum):
    """Constraints applied to number types."""

    LT = 'lt'
    GT = 'gt'
    LTE = 'lte'
    GTE = 'gte'
    EQ = 'eq'
