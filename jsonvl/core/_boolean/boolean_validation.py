"""String validation."""
from jsonvl.constants.builtins import Primitive
from jsonvl.constants.reserved import ReservedWords
from jsonvl.errors import ErrorMessages, JsonValidationError


TYPE_NAME = Primitive.BOOLEAN.value


def validate_boolean(data, schema, defs, path, validator):
    """
    Validate a JSON boolean based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, bool):
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)

    if ReservedWords.CONSTRAINTS in schema:
        validator._validate_constraints(data, TYPE_NAME, schema[ReservedWords.CONSTRAINTS], path)


def register_boolean_constraints(validator):
    """
    Register default boolean constraints.

    :param validator: jsonvl.Validator instance on which to register the constraints.
    """
    pass
