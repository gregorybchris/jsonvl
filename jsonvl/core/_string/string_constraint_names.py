"""String constraints."""
from jsonvl._utilities.venum import Venum


class StringConstraintNames(Venum):
    """Constraints applied to string types."""

    EQ = 'eq'
    IN = 'in'
    FORMAT = 'format'
