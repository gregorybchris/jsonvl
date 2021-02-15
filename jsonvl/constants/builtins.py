"""Names of data types in JSON schemas."""
from jsonvl.utilities.venum import Venum


class Primitive(Venum):
    """Enum for primitive data types."""

    NUMBER = 'number'
    STRING = 'string'


class Collection(Venum):
    """Enum for collection data types."""

    ARRAY = 'array'
    OBJECT = 'object'
