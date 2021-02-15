"""Object validation."""
from jsonvl.constants.reserved import Reserved
from jsonvl.exceptions.errors import ValidationError


def validate_object(data, schema, validator, path):
    """
    Validate a JSON object based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, dict):
        raise ValidationError(f"Expected {data} to be an object")

    if Reserved.ATTRIBUTES not in schema:
        raise ValidationError("Object types must define all attribute types with an \"attrs\" field")

    attrs_schema = schema[Reserved.ATTRIBUTES]

    missing_attrs_data = attrs_schema.keys() - data.keys()
    if len(missing_attrs_data) != 0:
        raise ValidationError(f"Data ({data}) is missing required attributes ({missing_attrs_data}) "
                              f"from the schema ({attrs_schema})")

    missing_attrs_schema = data.keys() - attrs_schema.keys()
    if len(missing_attrs_schema) != 0:
        raise ValidationError(f"Data ({data}) has extra attributes ({missing_attrs_schema}) "
                              f"not defined in the schema ({attrs_schema})")

    for attr, attr_type in attrs_schema.items():
        new_path = f'{path}.{attr}'
        validator._validate(data[attr], attr_type, new_path)
