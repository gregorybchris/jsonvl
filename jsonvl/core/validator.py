"""JSON validator."""
from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.constants.reserved import Reserved
from jsonvl.core._array.array_validation import validate_array
from jsonvl.core._boolean.boolean_validation import validate_boolean
from jsonvl.core._null.null_validation import validate_null
from jsonvl.core._number.number_validation import validate_number
from jsonvl.core._object.object_validation import validate_object
from jsonvl.core._string.string_validation import validate_string
from jsonvl.errors import ErrorMessages, JsonValidationError


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
            type = schema
            if not Primitive.has(type) and not Collection.has(type):
                raise JsonValidationError.create(ErrorMessages.UNKNOWN_TYPE, type=type)

            elif type == Primitive.BOOLEAN.value:
                validate_boolean(data, type, path)
            elif type == Primitive.NULL.value:
                validate_null(data, type, path)
            elif type == Primitive.NUMBER.value:
                validate_number(data, type, path)
            elif type == Primitive.STRING.value:
                validate_string(data, type, path)
            else:
                raise JsonValidationError.create(ErrorMessages.UNKNOWN_TYPE, type=type)
        elif isinstance(schema, list):
            types = schema
            successful_type = None
            for type in types:
                try:
                    self._validate(data, type, path)
                    successful_type = type
                    break
                except JsonValidationError:
                    pass
            if successful_type is None:
                raise JsonValidationError.create(ErrorMessages.FAILED_UNION_TYPE_PARSE, data=data, types=types)
        elif isinstance(schema, dict):
            if Reserved.TYPE not in schema:
                raise JsonValidationError.create(ErrorMessages.MISSING_TYPE_FIELD, path=path)

            type = schema[Reserved.TYPE]

            if type == Primitive.BOOLEAN.value:
                validate_boolean(data, schema, path)
            elif type == Primitive.NULL.value:
                validate_null(data, schema, path)
            elif type == Primitive.NUMBER.value:
                validate_number(data, schema, path)
            elif type == Primitive.STRING.value:
                validate_string(data, schema, path)
            elif type == Collection.ARRAY.value:
                validate_array(data, schema, self, path)
            elif type == Collection.OBJECT.value:
                validate_object(data, schema, self, path)
            else:
                raise JsonValidationError.create(ErrorMessages.UNKNOWN_TYPE, type=type)
        else:
            raise JsonValidationError.create(ErrorMessages.FAILED_TYPE_PARSE, type=schema, data=data)
