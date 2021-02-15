"""String validation."""
from jsonvl.constants.reserved import Reserved
from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.core._string.string_constraints import StringConstraints
from jsonvl.exceptions.errors import ValidationError


TYPE_NAME = Primitive.STRING.value


def validate_string(data, schema, path):
    """
    Validate a JSON string based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, str):
        raise ValidationError(f"{data} is not a valid {TYPE_NAME}")

    if isinstance(schema, str):
        return

    if Reserved.CONSTRAINTS in schema:
        type_constraints = schema[Reserved.CONSTRAINTS]
        for cons_name, cons_value in type_constraints.items():
            if not StringConstraints.has(cons_name):
                raise ValidationError(f"The type {TYPE_NAME} has no constraint {cons_name}")

            if cons_name == StringConstraints.IN.value:
                _constrain_in(cons_name, data, cons_value, path)
            elif cons_name == StringConstraints.EQ.value:
                _constrain_eq(cons_name, data, cons_value, path)
            else:
                raise ValidationError(f"The constraint {cons_name} is not implemented for type {TYPE_NAME}")


def _check_array_type(cons_name, data, cons_param):
    if not isinstance(cons_param, list):
        raise ValidationError(f"The {cons_name} constraint value ({cons_param}) "
                              f"for the data {data} must be of {Collection.ARRAY.value} type")


def _check_string_type(cons_name, data, cons_param):
    if not isinstance(cons_param, str):
        raise ValidationError(f"The {cons_name} constraint value ({cons_param}) "
                              f"for the data {data} must be of {Collection.STRING.value} type")


def _constrain_eq(cons_name, data, cons_param, path):
    _check_string_type(cons_name, data, cons_param)
    if data != cons_param:
        raise ValidationError(f"The value {data} (at {path}) must equal {cons_param} to meet "
                              f"the \"{cons_name}\" constraint.")


def _constrain_in(cons_name, data, cons_param, path):
    _check_array_type(cons_name, data, cons_param)
    if data not in cons_param:
        raise ValidationError(f"The value {data} (at {path}) must be one of {cons_param} to meet "
                              f"the \"{cons_name}\" constraint.")
