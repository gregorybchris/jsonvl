"""String validation."""
from jsonvl.constants.reserved import Reserved
from jsonvl.constants.builtins import Primitive
from jsonvl.core._number.number_constraints import NumberConstraints
from jsonvl.exceptions.errors import ValidationError


TYPE_NAME = Primitive.NUMBER.value


def validate_number(data, schema, path):
    """
    Validate a JSON number based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, (int, float)):
        raise ValidationError(f"{data} is not a valid {TYPE_NAME}")

    if isinstance(schema, str):
        return

    if Reserved.CONSTRAINTS in schema:
        type_constraints = schema[Reserved.CONSTRAINTS]
        for cons_name, cons_value in type_constraints.items():
            if not NumberConstraints.has(cons_name):
                raise ValidationError(f"The type {TYPE_NAME} has no constraint {cons_name}")

            if cons_name == NumberConstraints.LT.value:
                _constrain_lt(cons_name, data, cons_value, path)
            elif cons_name == NumberConstraints.GT.value:
                _constrain_gt(cons_name, data, cons_value, path)
            elif cons_name == NumberConstraints.LTE.value:
                _constrain_lte(cons_name, data, cons_value, path)
            elif cons_name == NumberConstraints.GTE.value:
                _constrain_gte(cons_name, data, cons_value, path)
            elif cons_name == NumberConstraints.EQ.value:
                _constrain_eq(cons_name, data, cons_value, path)


def _check_type(cons_name, data, value):
    if not isinstance(value, (int, float)):
        raise ValidationError(f"The {cons_name} constraint value ({value}) "
                              f"for the data {data} must be a {TYPE_NAME}")


def _constrain_lt(cons_name, data, value, path):
    _check_type(cons_name, data, value)
    if data >= value:
        raise ValidationError(f"Constraint \"{cons_name}\" not met with value {value} for {path}")


def _constrain_gt(cons_name, data, value, path):
    _check_type(cons_name, data, value)
    if data <= value:
        raise ValidationError(f"Constraint \"{cons_name}\" not met with value {value} for {path}")


def _constrain_lte(cons_name, data, value, path):
    _check_type(cons_name, data, value)
    if data > value:
        raise ValidationError(f"Constraint \"{cons_name}\" not met with value {value} for {path}")


def _constrain_gte(cons_name, data, value, path):
    _check_type(cons_name, data, value)
    if data < value:
        raise ValidationError(f"Constraint \"{cons_name}\" not met with value {value} for {path}")


def _constrain_eq(cons_name, data, value, path):
    _check_type(cons_name, data, value)
    if data != value:
        raise ValidationError(f"Constraint \"{cons_name}\" not met with value {value} for {path}")
