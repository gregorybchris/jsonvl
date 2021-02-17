"""String validation."""
import re

from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.constants.reserved import Reserved
from jsonvl.core._string.string_constraints import StringConstraints
from jsonvl.core._string.string_formatting import (
    StringFormatPatterns, StringFormats, StringFormatters, StringFormatting)
from jsonvl.errors import ErrorMessages, JsonSchemaError, JsonValidationError


TYPE_NAME = Primitive.STRING.value


def validate_string(data, schema, defs, path):
    """
    Validate a JSON string based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, str):
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)

    if isinstance(schema, str):
        return

    if Reserved.CONSTRAINTS in schema:
        type_constraints = schema[Reserved.CONSTRAINTS]
        for cons_name, cons_value in type_constraints.items():
            if not StringConstraints.has(cons_name):
                raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT,
                                             type=TYPE_NAME, cons=cons_name)

            if cons_name == StringConstraints.IN.value:
                _constrain_in(cons_name, data, cons_value, path)
            elif cons_name == StringConstraints.EQ.value:
                _constrain_eq(cons_name, data, cons_value, path)
            elif cons_name == StringConstraints.FORMAT.value:
                _constrain_format(cons_name, data, cons_value, path)
            else:
                raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT,
                                             type=TYPE_NAME, cons=cons_name)


def _constrain_in(cons_name, data, cons_param, path):
    if not isinstance(cons_param, list):
        raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                     cons=cons_name, param_types=[Collection.ARRAY.value], param=cons_param)

    if data not in cons_param:
        raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                         cons=cons_name, param=cons_param, data=data)


def _constrain_eq(cons_name, data, cons_param, path):
    if not isinstance(cons_param, str):
        raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                     cons=cons_name, param_types=[Primitive.STRING.value], param=cons_param)

    if data != cons_param:
        raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                         cons=cons_name, param=cons_param, data=data)


def _constrain_format(cons_name, data, cons_param, path):
    if isinstance(cons_param, str):
        if not StringFormats.has(cons_param):
            raise JsonSchemaError.create(ErrorMessages.UNKNOWN_STRING_FORMAT, format=cons_param)

        if cons_param == StringFormats.EMAIL.value:
            pattern = StringFormatPatterns.EMAIL
        elif cons_param == StringFormats.PHONE.value:
            pattern = StringFormatPatterns.PHONE
        else:
            raise JsonSchemaError.create(ErrorMessages.UNKNOWN_STRING_FORMAT, format=cons_param)

        if not re.match(pattern, data):
            raise JsonValidationError.create(ErrorMessages.INCORRECT_FORMAT, data=data, format=cons_param)
    elif isinstance(cons_param, dict):
        if StringFormatting.TYPE.value not in cons_param:
            raise JsonSchemaError.create(ErrorMessages.MISSING_FORMAT_TYPE_FIELD, path=path)

        formatter = cons_param[StringFormatting.TYPE.value]
        if formatter == StringFormatters.REGEX.value:
            if StringFormatting.PATTERN.value not in cons_param:
                raise JsonSchemaError.create(ErrorMessages.MISSING_FORMAT_PATTERN_FIELD, path=path)
            pattern = cons_param[StringFormatting.PATTERN.value]
            if not re.match(pattern, data):
                raise JsonValidationError.create(ErrorMessages.INCORRECT_FORMAT, data=data, format=pattern)
    else:
        valid_types = [Primitive.STRING.value, Collection.OBJECT.value]
        raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                     cons=cons_name, param_types=valid_types, param=cons_param)
