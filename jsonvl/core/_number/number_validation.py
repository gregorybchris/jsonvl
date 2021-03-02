"""String validation."""
from jsonvl.constants.builtins import Primitive
from jsonvl.constants.reserved import ReservedWords
from jsonvl.core._number import number_constraints
from jsonvl.core._number.number_constraint_names import NumberConstraintNames
from jsonvl.errors import ErrorMessages, JsonValidationError


TYPE_NAME = Primitive.NUMBER.value


def validate_number(data, schema, defs, path, validator):
    """
    Validate a JSON number based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, (int, float)):
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)

    if isinstance(schema, str):
        return

    if ReservedWords.CONSTRAINTS in schema:
        validator._validate_constraints(data, TYPE_NAME, schema[ReservedWords.CONSTRAINTS], path)


def register_number_constraints(validator):
    """
    Register default number constraints.

    :param validator: jsonvl.Validator instance on which to register the constraints.
    """
    validator.register_constraint(number_constraints.LtConstraint(),
                                  TYPE_NAME, NumberConstraintNames.LT.value)
    validator.register_constraint(number_constraints.GtConstraint(),
                                  TYPE_NAME, NumberConstraintNames.GT.value)
    validator.register_constraint(number_constraints.LteConstraint(),
                                  TYPE_NAME, NumberConstraintNames.LTE.value)
    validator.register_constraint(number_constraints.GteConstraint(),
                                  TYPE_NAME, NumberConstraintNames.GTE.value)
    validator.register_constraint(number_constraints.EqConstraint(),
                                  TYPE_NAME, NumberConstraintNames.EQ.value)
