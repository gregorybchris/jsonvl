"""String validation."""
from jsonvl.constants.builtins import Primitive
from jsonvl.errors import ErrorMessages, JsonValidationError


TYPE_NAME = Primitive.NULL.value


def validate_null(data, schema, defs, path):
    """
    Validate a JSON null based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if data is not None:
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)
