"""String constraints."""
from jsonvl.utilities.venum import Venum


class StringConstraints(Venum):
    """Constraints applied to string types."""

    EQ = 'eq'
    IN = 'in'
    FORMAT = 'format'
