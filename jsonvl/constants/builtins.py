"""Names of data types in JSON schemas."""
from jsonvl._utilities.venum import Venum


class Primitive(Venum):
    """Enum for primitive data types."""

    BOOLEAN = 'boolean'
    NULL = 'null'
    NUMBER = 'number'
    STRING = 'string'


class Collection(Venum):
    """Enum for collection data types."""

    ARRAY = 'array'
    OBJECT = 'object'
