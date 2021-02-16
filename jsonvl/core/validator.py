"""JSON validator."""
from jsonvl.constants.reserved import Reserved
from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.core._array.array_validation import validate_array
from jsonvl.core._boolean.boolean_validation import validate_boolean
from jsonvl.core._null.null_validation import validate_null
from jsonvl.core._number.number_validation import validate_number
from jsonvl.core._object.object_validation import validate_object
from jsonvl.core._string.string_validation import validate_string
from jsonvl.errors import JsonValidationError, ErrorMessages


class Validator:
    """JSON validator."""

    def __init__(self):
        """Construct a new Validator."""
        pass

    def validate(self, data, schema):
        """
        Validate JSON data based on a schema.

        :param data: JSON data as a Python object.
        :param schema: JSON schema as a Python object.
        """
        self._validate(data, schema, path='json')

    def _validate(self, data, schema, path):
        if isinstance(schema, str):
            if not Primitive.has(schema) and not Collection.has(schema):
                raise JsonValidationError.create(ErrorMessages.UNKNOWN_TYPE, type=schema)

            if schema == Primitive.STRING.value:
                validate_string(data, schema, path)
            elif schema == Primitive.NUMBER.value:
                validate_number(data, schema, path)
        elif isinstance(schema, dict):
            if Reserved.TYPE not in schema:
                raise JsonValidationError.create(ErrorMessages.MISSING_TYPE_FIELD, path=path)

            ty = schema[Reserved.TYPE]

            if ty == Primitive.NUMBER.value:
                validate_number(data, schema, path)
            elif ty == Primitive.STRING.value:
                validate_string(data, schema, path)
            elif ty == Primitive.BOOLEAN.value:
                validate_boolean(data, schema, path)
            elif ty == Primitive.NULL.value:
                validate_null(data, schema, path)
            elif ty == Collection.ARRAY.value:
                validate_array(data, schema, self, path)
            elif ty == Collection.OBJECT.value:
                validate_object(data, schema, self, path)
            else:
                raise JsonValidationError.create(ErrorMessages.UNKNOWN_TYPE, type=ty)
        else:
            raise JsonValidationError.create(ErrorMessages.FAILED_TYPE_PARSE, type=schema, data=data)
