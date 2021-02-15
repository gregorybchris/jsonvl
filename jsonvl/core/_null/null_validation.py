"""String validation."""
from jsonvl.constants.builtins import Primitive
from jsonvl.exceptions.errors import ValidationError


TYPE_NAME = Primitive.NULL.value


def validate_null(data, schema, path):
    """
    Validate a JSON null based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if data is not None:
        raise ValidationError(f"{data} is not a valid {TYPE_NAME}")
