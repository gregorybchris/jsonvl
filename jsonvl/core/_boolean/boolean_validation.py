"""String validation."""
from jsonvl.constants.builtins import Primitive
from jsonvl.exceptions.errors import ValidationError


TYPE_NAME = Primitive.BOOLEAN.value


def validate_boolean(data, schema, path):
    """
    Validate a JSON boolean based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, bool):
        raise ValidationError(f"{data} is not a valid {TYPE_NAME}")

    # TODO: Handle constrained string
