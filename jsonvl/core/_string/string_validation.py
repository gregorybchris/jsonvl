"""String validation."""
import re

from jsonvl.constants.reserved import Reserved
from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.core._string.string_constraints import (
    StringConstraints, StringFormatting, StringFormats, StringFormatters)
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
            elif cons_name == StringConstraints.FORMAT.value:
                _constrain_format(cons_name, data, cons_value, path)
            else:
                raise ValidationError(f"The constraint {cons_name} is not implemented for type {TYPE_NAME}")


def _check_array_type(cons_name, data, cons_param):
    if not isinstance(cons_param, list):
        raise ValidationError(f"The {cons_name} constraint value ({cons_param}) "
                              f"for the data {data} must be of {Collection.ARRAY.value} type")


def _check_string_type(cons_name, data, cons_param):
    if not isinstance(cons_param, str):
        raise ValidationError(f"The {cons_name} constraint value ({cons_param}) "
                              f"for the data {data} must be of {Primitive.STRING.value} type")


def _constrain_in(cons_name, data, cons_param, path):
    _check_array_type(cons_name, data, cons_param)
    if data not in cons_param:
        raise ValidationError(f"The value {data} (at {path}) must be one of {cons_param} to meet "
                              f"the \"{cons_name}\" constraint.")


def _constrain_eq(cons_name, data, cons_param, path):
    _check_string_type(cons_name, data, cons_param)
    if data != cons_param:
        raise ValidationError(f"The value {data} (at {path}) must equal {cons_param} to meet "
                              f"the \"{cons_name}\" constraint.")


def _constrain_format(cons_name, data, cons_param, path):
    if isinstance(cons_param, str):
        if not StringFormats.has(cons_param):
            raise ValidationError(f"Unknown format \"{cons_param}\", perhaps try a regex format instead")

        if cons_param == StringFormats.PHONE.value:
            pattern = r"^[2-9]\d{2}-\d{3}-\d{4}$"
        elif cons_param == StringFormats.EMAIL.value:
            pattern = r"^\S+@\S+\.\S+$"
        else:
            raise ValidationError(f"The format {cons_param} is not implemented")

        if not re.match(pattern, data):
            raise ValidationError(f"The data {data} did not match the {cons_param} format")
    elif isinstance(cons_param, dict):
        if StringFormatting.TYPE.value not in cons_param:
            raise ValidationError("The formatter \"type\" is required when defining a format constraint")

        formatter = cons_param[StringFormatting.TYPE.value]
        if formatter == StringFormatters.REGEX.value:
            if StringFormatting.PATTERN.value not in cons_param:
                raise ValidationError("The regex format constraint requires a \"pattern\" parameter")
            pattern = cons_param[StringFormatting.PATTERN.value]
            if not re.match(pattern, data):
                raise ValidationError(f"The data \"{data}\" did not match the provided regex pattern \"{pattern}\"")
    else:
        raise ValidationError(f"The {cons_name} constraint value ({cons_param}) "
                              f"must be of {Primitive.STRING.value} or {Collection.OBJECT.value} type")
