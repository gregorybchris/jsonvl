"""Array validation."""
from jsonvl.constants.reserved import Reserved
from jsonvl.exceptions.errors import ValidationError


def validate_array(data, schema, validator):
    """
    Validate a JSON array based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, list):
        raise ValidationError(f"Expected {data} to be an array")

    if Reserved.ELEMENT not in schema:
        raise ValidationError("Array types must define the element type with the \"elem\" field")

    elem_schema = schema[Reserved.ELEMENT]
    for elem in data:
        validator.validate(elem, elem_schema)
