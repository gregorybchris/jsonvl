"""Object validation."""
from jsonvl.constants.builtins import Collection
from jsonvl.constants.reserved import Reserved
from jsonvl.errors import JsonValidationError, ErrorMessages


TYPE_NAME = Collection.OBJECT.value


def validate_object(data, schema, validator, path):
    """
    Validate a JSON object based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, dict):
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)

    if Reserved.ATTRIBUTES not in schema:
        raise JsonValidationError.create(ErrorMessages.MISSING_OBJECT_ATTRS_FIELD)

    attrs_schema = schema[Reserved.ATTRIBUTES]

    missing_attrs_data = attrs_schema.keys() - data.keys()
    if len(missing_attrs_data) != 0:
        raise JsonValidationError.create(ErrorMessages.MISSING_OBJECT_ATTRS,
                                         data=data, missing_attrs=missing_attrs_data, schema=attrs_schema)

    missing_attrs_schema = data.keys() - attrs_schema.keys()
    if len(missing_attrs_schema) != 0:
        raise JsonValidationError.create(ErrorMessages.EXTRA_OBJECT_ATTRS,
                                         data=data, extra_attrs=missing_attrs_schema, schema=attrs_schema)

    for attr, attr_type in attrs_schema.items():
        new_path = f'{path}.{attr}'
        validator._validate(data[attr], attr_type, new_path)
