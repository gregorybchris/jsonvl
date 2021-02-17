"""String formats."""
from jsonvl._utilities.venum import Venum


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


class StringFormatPatterns:
    """Predefined formats used to constrain string types."""

    EMAIL = r"^\S+@\S+\.\S+$"
    PHONE = r"^[2-9]\d{2}-\d{3}-\d{4}$"
