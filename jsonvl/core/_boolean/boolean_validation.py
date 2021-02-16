"""String validation."""
from jsonvl.constants.builtins import Primitive
from jsonvl.errors import JsonValidationError, ErrorMessages


TYPE_NAME = Primitive.BOOLEAN.value


def validate_boolean(data, schema, path):
    """
    Validate a JSON boolean based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, bool):
        raise JsonValidationError.craete(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)
