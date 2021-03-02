"""String constraints."""
import re

from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.core._string.string_formatting import (
    StringFormatPatterns, StringFormats, StringFormatters, StringFormatting)
from jsonvl.core.constraint import Constraint
from jsonvl.errors import ErrorMessages, JsonSchemaError, JsonValidationError


class InConstraint(Constraint):
    """In constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        if not isinstance(constraint_param, list):
            raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                         cons=constraint_name,
                                         param_types=[Collection.ARRAY.value],
                                         param=constraint_param)

        if data not in constraint_param:
            raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                             cons=constraint_name,
                                             param=constraint_param,
                                             data=data)


class EqConstraint(Constraint):
    """Equals constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        if not isinstance(constraint_param, str):
            raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                         cons=constraint_name,
                                         param_types=[Primitive.STRING.value],
                                         param=constraint_param)

        if data != constraint_param:
            raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                             cons=constraint_name,
                                             param=constraint_param,
                                             data=data)


class FormatConstraint(Constraint):
    """Format constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        if isinstance(constraint_param, str):
            if constraint_param == StringFormats.EMAIL.value:
                pattern = StringFormatPatterns.EMAIL
            elif constraint_param == StringFormats.PHONE.value:
                pattern = StringFormatPatterns.PHONE
            else:
                raise JsonSchemaError.create(ErrorMessages.UNKNOWN_STRING_FORMAT, format=constraint_param)

            if not re.match(pattern, data):
                raise JsonValidationError.create(ErrorMessages.INCORRECT_FORMAT, data=data, format=constraint_param)
        elif isinstance(constraint_param, dict):
            if StringFormatting.TYPE.value not in constraint_param:
                raise JsonSchemaError.create(ErrorMessages.MISSING_FORMAT_TYPE_FIELD, path=path)

            formatter = constraint_param[StringFormatting.TYPE.value]
            if formatter == StringFormatters.REGEX.value:
                if StringFormatting.PATTERN.value not in constraint_param:
                    raise JsonSchemaError.create(ErrorMessages.MISSING_FORMAT_PATTERN_FIELD, path=path)
                pattern = constraint_param[StringFormatting.PATTERN.value]
                if not re.match(pattern, data):
                    raise JsonValidationError.create(ErrorMessages.INCORRECT_FORMAT, data=data, format=pattern)
            else:
                raise JsonSchemaError.create(ErrorMessages.UNKNOWN_STRING_FORMATTER, formatter=formatter)
        else:
            valid_types = [Primitive.STRING.value, Collection.OBJECT.value]
            raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                         cons=constraint_name, param_types=valid_types, param=constraint_param)
