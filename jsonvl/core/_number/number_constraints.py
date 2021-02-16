"""Number constraints."""
from jsonvl.utilities.venum import Venum


class NumberConstraints(Venum):
    """Constraints applied to number types."""

    LT = 'lt'
    GT = 'gt'
    LTE = 'lte'
    GTE = 'gte'
    EQ = 'eq'
