"""JSON validator."""
from copy import deepcopy

from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.constants.reserved import Reserved, ReservedSymbols
from jsonvl.core._array.array_validation import validate_array
from jsonvl.core._boolean.boolean_validation import validate_boolean
from jsonvl.core._null.null_validation import validate_null
from jsonvl.core._number.number_validation import validate_number
from jsonvl.core._object.object_validation import validate_object
from jsonvl.core._string.string_validation import validate_string
from jsonvl.errors import ErrorMessages, JsonSchemaError, JsonValidationError


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
        self._validate(data, schema, defs={}, path='json')

    def _validate(self, data, schema, defs, path):
        if isinstance(schema, str):
            type = schema

            if type.startswith(ReservedSymbols.REF):
                ref = type
                if ref in defs:
                    ref_schema = defs[ref]
                    self._validate(data, ref_schema, defs, path)
                    return
                else:
                    raise JsonSchemaError.create(ErrorMessages.REFERENCE_NOT_FOUND, ref=ref)

            if not Primitive.has(type) and not Collection.has(type):
                raise JsonSchemaError.create(ErrorMessages.UNKNOWN_TYPE, type=type)

            elif type == Primitive.BOOLEAN.value:
                validate_boolean(data, type, defs, path)
            elif type == Primitive.NULL.value:
                validate_null(data, type, defs, path)
            elif type == Primitive.NUMBER.value:
                validate_number(data, type, defs, path)
            elif type == Primitive.STRING.value:
                validate_string(data, type, defs, path)
            else:
                raise JsonSchemaError.create(ErrorMessages.UNKNOWN_TYPE, type=type)
        elif isinstance(schema, list):
            union_schemas = schema
            successful_schema = None
            for union_schema in union_schemas:
                try:
                    self._validate(data, union_schema, defs, path)
                    successful_schema = union_schema
                    break
                except JsonValidationError:
                    pass
            if successful_schema is None:
                raise JsonValidationError.create(ErrorMessages.FAILED_UNION_TYPE_PARSE, data=data, types=union_schemas)
        elif isinstance(schema, dict):
            if Reserved.TYPE not in schema:
                raise JsonSchemaError.create(ErrorMessages.MISSING_TYPE_FIELD, path=path)

            if Reserved.DEFS in schema:
                defs = deepcopy(defs)
                defs.update(schema[Reserved.DEFS])

            type = schema[Reserved.TYPE]

            if type == Primitive.BOOLEAN.value:
                validate_boolean(data, schema, defs, path)
            elif type == Primitive.NULL.value:
                validate_null(data, schema, defs, path)
            elif type == Primitive.NUMBER.value:
                validate_number(data, schema, defs, path)
            elif type == Primitive.STRING.value:
                validate_string(data, schema, defs, path)
            elif type == Collection.ARRAY.value:
                validate_array(data, schema, defs, path, self)
            elif type == Collection.OBJECT.value:
                validate_object(data, schema, defs, path, self)
            else:
                raise JsonSchemaError.create(ErrorMessages.UNKNOWN_TYPE, type=type)
        else:
            raise JsonSchemaError.create(ErrorMessages.FAILED_SCHEMA_TYPE_PARSE, type=schema)
