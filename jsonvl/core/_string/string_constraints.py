
"""String constraints."""
from jsonvl.utilities.venum import Venum


class StringConstraints(Venum):
    """Constraints applied to string types."""

    EQ = 'eq'
    IN = 'in'
    FORMAT = 'format'


class StringFormats(Venum):
    """Formats for string format constraints."""

    PHONE = 'phone'
    EMAIL = 'email'


class StringFormatting(Venum):
    """Formats for string format constraints."""

    PATTERN = 'pattern'
    TYPE = 'type'


class StringFormatters(Venum):
    """Format engines for string format constraints."""

    REGEX = 'regex'
