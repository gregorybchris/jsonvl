"""JSON validator."""
from jsonvl.constants.reserved import Reserved
from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.exceptions.errors import ValidationError
from jsonvl.core._array.array_validation import validate_array
from jsonvl.core._number.number_validation import validate_number
from jsonvl.core._object.object_validation import validate_object
from jsonvl.core._string.string_validation import validate_string


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
        if isinstance(schema, str):
            if not Primitive.has(schema) and not Collection.has(schema):
                raise ValidationError(f"Type {schema} is not a valid type")

            if schema == Primitive.STRING.value:
                validate_string(data, schema)
            elif schema == Primitive.NUMBER.value:
                validate_number(data, schema)
        elif isinstance(schema, dict):
            if Reserved.TYPE not in schema:
                raise ValidationError("No \"type\" field found in type definition")

            ty = schema[Reserved.TYPE]

            if ty == Primitive.NUMBER.value:
                validate_number(data, schema)
            elif ty == Primitive.STRING.value:
                validate_string(data, schema)
            elif ty == Collection.ARRAY.value:
                validate_array(data, schema, self)
            elif ty == Collection.OBJECT.value:
                validate_object(data, schema, self)
            else:
                raise ValidationError(f"Unknown type {ty}")
        else:
            raise ValidationError(f"Could not parse type {schema} for data {data}")
