"""String validation."""
from jsonvl.constants.builtins import Primitive
from jsonvl.constants.reserved import ReservedWords
from jsonvl.core._string import string_constraints
from jsonvl.core._string.string_constraint_names import StringConstraintNames
from jsonvl.errors import ErrorMessages, JsonValidationError


TYPE_NAME = Primitive.STRING.value


def validate_string(data, schema, defs, path, validator):
    """
    Validate a JSON string based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, str):
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)

    if isinstance(schema, str):
        return

    if ReservedWords.CONSTRAINTS in schema:
        validator._validate_constraints(data, TYPE_NAME, schema[ReservedWords.CONSTRAINTS], path)


def register_string_constraints(validator):
    """
    Register default string constraints.

    :param validator: jsonvl.Validator instance on which to register the constraints.
    """
    validator.register_constraint(string_constraints.InConstraint(),
                                  TYPE_NAME, StringConstraintNames.IN.value)
    validator.register_constraint(string_constraints.EqConstraint(),
                                  TYPE_NAME, StringConstraintNames.EQ.value)
    validator.register_constraint(string_constraints.FormatConstraint(),
                                  TYPE_NAME, StringConstraintNames.FORMAT.value)
